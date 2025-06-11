#include <vmlinux.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>
#include <bpf/bpf_core_read.h>

#define MAX_ENTRIES 10240
#define MAX_COMM_LEN 16
#define MAX_FILENAME_LEN 256

enum event_type {
    EVENT_PROCESS_START,
    EVENT_PROCESS_END,
    EVENT_SYSCALL_ENTER,
    EVENT_SYSCALL_EXIT,
    EVENT_MEMORY_ALLOC,
    EVENT_MEMORY_FREE,
    EVENT_PAGE_FAULT,
    EVENT_MMAP,
    EVENT_MUNMAP
};

struct event_data {
    __u64 timestamp;
    __u32 pid;
    __u32 tid;
    __u32 event_type;
    __u64 addr;
    __u64 size;
    __s64 retval;
    __u32 syscall_nr;
    __u64 args[6];
    char comm[MAX_COMM_LEN];
    char filename[MAX_FILENAME_LEN];
};

struct memory_alloc {
    __u64 addr;
    __u64 size;
    __u64 timestamp;
    __u32 pid;
};

struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 256 * 1024);
} events SEC(".maps");

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, MAX_ENTRIES);
    __type(key, __u32);
    __type(value, __u8);
} target_pids SEC(".maps");

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, MAX_ENTRIES);
    __type(key, __u64);
    __type(value, struct memory_alloc);
} memory_map SEC(".maps");

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, MAX_ENTRIES);
    __type(key, __u32);
    __type(value, __u64);
} syscall_enter_time SEC(".maps");

static __always_inline bool is_target_pid(__u32 pid) {
    return bpf_map_lookup_elem(&target_pids, &pid) != NULL;
}

SEC("tp/sched/sched_process_exec")
int trace_process_exec(void *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = bpf_ktime_get_ns();
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_PROCESS_START;
    bpf_get_current_comm(event->comm, sizeof(event->comm));

    __builtin_memcpy(event->filename, event->comm, MAX_COMM_LEN);

    bpf_ringbuf_submit(event, 0);
    return 0;
}

SEC("kprobe/bprm_execve")
int trace_process_exec_binprm(struct pt_regs *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = bpf_ktime_get_ns();
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_PROCESS_START;
    bpf_get_current_comm(event->comm, sizeof(event->comm));
    __builtin_memcpy(event->filename, event->comm, MAX_COMM_LEN);

    bpf_ringbuf_submit(event, 0);
    return 0;
}

SEC("tp/sched/sched_process_exit")
int trace_process_exit(struct trace_event_raw_sched_process_template *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = bpf_ktime_get_ns();
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_PROCESS_END;
    bpf_get_current_comm(event->comm, sizeof(event->comm));

    bpf_ringbuf_submit(event, 0);
    return 0;
}

SEC("tp/raw_syscalls/sys_enter")
int trace_sys_enter(struct trace_event_raw_sys_enter *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    __u64 timestamp = bpf_ktime_get_ns();
    bpf_map_update_elem(&syscall_enter_time, &pid, &timestamp, BPF_ANY);

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = timestamp;
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_SYSCALL_ENTER;
    event->syscall_nr = ctx->id;

    event->args[0] = ctx->args[0];
    event->args[1] = ctx->args[1];
    event->args[2] = ctx->args[2];
    event->args[3] = ctx->args[3];
    event->args[4] = ctx->args[4];
    event->args[5] = ctx->args[5];

    bpf_get_current_comm(event->comm, sizeof(event->comm));

    bpf_ringbuf_submit(event, 0);
    return 0;
}

SEC("tp/raw_syscalls/sys_exit")
int trace_sys_exit(struct trace_event_raw_sys_exit *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = bpf_ktime_get_ns();
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_SYSCALL_EXIT;
    event->retval = ctx->ret;
    bpf_get_current_comm(event->comm, sizeof(event->comm));

    bpf_ringbuf_submit(event, 0);
    return 0;
}

SEC("uprobe")
int trace_malloc(struct pt_regs *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    __u64 size = PT_REGS_PARM1(ctx);

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = bpf_ktime_get_ns();
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_MEMORY_ALLOC;
    event->size = size;
    bpf_get_current_comm(event->comm, sizeof(event->comm));

    bpf_ringbuf_submit(event, 0);
    return 0;
}

SEC("uretprobe")
int trace_malloc_ret(struct pt_regs *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    __u64 addr = PT_REGS_RC(ctx);
    if (addr == 0)
        return 0;

    struct memory_alloc alloc = {
        .addr = addr,
        .timestamp = bpf_ktime_get_ns(),
        .pid = pid,
        .size = 0,
    };

    bpf_map_update_elem(&memory_map, &addr, &alloc, BPF_ANY);
    return 0;
}

SEC("uprobe")
int trace_free(struct pt_regs *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    __u64 addr = PT_REGS_PARM1(ctx);
    if (addr == 0)
        return 0;

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = bpf_ktime_get_ns();
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_MEMORY_FREE;
    event->addr = addr;
    bpf_get_current_comm(event->comm, sizeof(event->comm));

    bpf_map_delete_elem(&memory_map, &addr);
    bpf_ringbuf_submit(event, 0);
    return 0;
}

SEC("tp/syscalls/sys_enter_mmap")
int trace_mmap_syscall(struct trace_event_raw_sys_enter *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = bpf_ktime_get_ns();
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_PAGE_FAULT; // Use page fault event type
    event->addr = 0;
    event->size = ctx->args[1]; // length parameter
    bpf_get_current_comm(event->comm, sizeof(event->comm));

    bpf_ringbuf_submit(event, 0);
    return 0;
}

SEC("tp/kmem/kmalloc")
int trace_kmalloc(void *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = bpf_ktime_get_ns();
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_PAGE_FAULT; // Reuse existing event type
    event->addr = 0;
    bpf_get_current_comm(event->comm, sizeof(event->comm));

    bpf_ringbuf_submit(event, 0);
    return 0;
}

SEC("tp/kmem/kfree")
int trace_kfree(void *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = bpf_ktime_get_ns();
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_PAGE_FAULT; // Reuse existing event type
    event->addr = 0;
    bpf_get_current_comm(event->comm, sizeof(event->comm));

    bpf_ringbuf_submit(event, 0);
    return 0;
}

SEC("tp/vmscan/mm_vmscan_direct_reclaim_begin")
int trace_reclaim_begin(void *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = bpf_ktime_get_ns();
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_PAGE_FAULT;
    event->addr = 0;
    bpf_get_current_comm(event->comm, sizeof(event->comm));

    bpf_ringbuf_submit(event, 0);
    return 0;
}

SEC("tp/syscalls/sys_enter_brk")
int trace_brk_enter(struct trace_event_raw_sys_enter *ctx) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;

    if (!is_target_pid(pid))
        return 0;

    struct event_data *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return 0;

    event->timestamp = bpf_ktime_get_ns();
    event->pid = pid;
    event->tid = bpf_get_current_pid_tgid() & 0xffffffff;
    event->event_type = EVENT_PAGE_FAULT;
    event->addr = ctx->args[0]; // brk address
    bpf_get_current_comm(event->comm, sizeof(event->comm));

    bpf_ringbuf_submit(event, 0);
    return 0;
}

char LICENSE[] SEC("license") = "GPL";
