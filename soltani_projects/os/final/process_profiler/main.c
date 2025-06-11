#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <errno.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <time.h>
#include <bpf/libbpf.h>
#include <bpf/bpf.h>
#include "process_profiler.skel.h"
#include <fcntl.h>

#define MAX_ENTRIES 10240
#define MAX_COMM_LEN 16
#define MAX_FILENAME_LEN 256

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

static volatile bool exiting = false;
static struct process_profiler_bpf *skel;
static pid_t target_pid = 0;
static char target_program[256];
static char **target_args;

static struct {
    uint64_t syscalls;
    uint64_t memory_allocs;
    uint64_t memory_frees;
    uint64_t page_faults;
    uint64_t mmaps;
    uint64_t munmaps;
    uint64_t total_allocated;
    uint64_t total_freed;
    uint64_t peak_memory;
    uint64_t current_memory;

    uint64_t minor_faults;
    uint64_t major_faults;
    uint64_t vsz;       // Virtual memory size
    uint64_t rss;       // Resident set size
    uint64_t rss_peak;
    uint64_t swap_used;
} stats = {0};

static void sig_handler(int sig __attribute__((unused))) {
    exiting = true;
}

struct syscall_map {
    int num;
    const char *name;
};

#if defined(__x86_64__) || defined(__i386__)
#define IS_X86_ARCH 1
static struct syscall_map x86_syscalls[] = {
    {0, "read"},
    {1, "write"},
    {2, "open"},
    {3, "close"},
    {4, "stat"},
    {5, "fstat"},
    {6, "lstat"},
    {7, "poll"},
    {8, "lseek"},
    {9, "mmap"},
    {10, "mprotect"},
    {11, "munmap"},
    {12, "brk"},
    {13, "rt_sigaction"},
    {14, "rt_sigprocmask"},
    {15, "rt_sigreturn"},
    {16, "ioctl"},
    {17, "pread64"},
    {18, "pwrite64"},
    {19, "readv"},
    {20, "writev"},
    {21, "access"},
    {22, "pipe"},
    {23, "select"},
    {24, "sched_yield"},
    {25, "mremap"},
    {26, "msync"},
    {27, "mincore"},
    {28, "madvise"},
    {29, "shmget"},
    {30, "shmat"},
    {31, "shmctl"},
    {32, "dup"},
    {33, "dup2"},
    {34, "pause"},
    {35, "nanosleep"},
    {36, "getitimer"},
    {37, "alarm"},
    {38, "setitimer"},
    {39, "getpid"},
    {40, "sendfile"},
    {41, "socket"},
    {42, "connect"},
    {43, "accept"},
    {44, "sendto"},
    {45, "recvfrom"},
    {46, "sendmsg"},
    {47, "recvmsg"},
    {48, "shutdown"},
    {49, "bind"},
    {50, "listen"},
    {51, "getsockname"},
    {52, "getpeername"},
    {53, "socketpair"},
    {54, "setsockopt"},
    {55, "getsockopt"},
    {56, "clone"},
    {57, "fork"},
    {58, "vfork"},
    {59, "execve"},
    {60, "exit"},
    {61, "wait4"},
    {62, "kill"},
    {63, "uname"},
    {64, "semget"},
    {65, "semop"},
    {66, "semctl"},
    {67, "shmdt"},
    {68, "msgget"},
    {69, "msgsnd"},
    {70, "msgrcv"},
    {71, "msgctl"},
    {72, "fcntl"},
    {73, "flock"},
    {74, "fsync"},
    {75, "fdatasync"},
    {76, "truncate"},
    {77, "ftruncate"},
    {78, "getdents"},
    {79, "getcwd"},
    {80, "chdir"},
    {81, "fchdir"},
    {82, "rename"},
    {83, "mkdir"},
    {84, "rmdir"},
    {85, "creat"},
    {86, "link"},
    {87, "unlink"},
    {88, "symlink"},
    {89, "readlink"},
    {90, "chmod"},
    {91, "fchmod"},
    {92, "chown"},
    {93, "fchown"},
    {94, "lchown"},
    {95, "umask"},
    {96, "gettimeofday"},
    {97, "getrlimit"},
    {98, "getrusage"},
    {99, "sysinfo"},
    {100, "times"},
    {101, "ptrace"},
    {102, "getuid"},
    {103, "syslog"},
    {104, "getgid"},
    {105, "setuid"},
    {106, "setgid"},
    {107, "geteuid"},
    {108, "getegid"},
    {109, "setpgid"},
    {110, "getppid"},
    {111, "getpgrp"},
    {112, "setsid"},
    {113, "setreuid"},
    {114, "setregid"},
    {115, "getgroups"},
    {116, "setgroups"},
    {117, "setresuid"},
    {118, "getresuid"},
    {119, "setresgid"},
    {120, "getresgid"},
    {121, "getpgid"},
    {122, "setfsuid"},
    {123, "setfsgid"},
    {124, "getsid"},
    {125, "capget"},
    {126, "capset"},
    {127, "rt_sigpending"},
    {128, "rt_sigtimedwait"},
    {129, "rt_sigqueueinfo"},
    {130, "rt_sigsuspend"},
    {131, "sigaltstack"},
    {132, "utime"},
    {133, "mknod"},
    {134, "uselib"},
    {135, "personality"},
    {136, "ustat"},
    {137, "statfs"},
    {138, "fstatfs"},
    {139, "sysfs"},
    {140, "getpriority"},
    {141, "setpriority"},
    {142, "sched_setparam"},
    {143, "sched_getparam"},
    {144, "sched_setscheduler"},
    {145, "sched_getscheduler"},
    {146, "sched_get_priority_max"},
    {147, "sched_get_priority_min"},
    {148, "sched_rr_get_interval"},
    {149, "mlock"},
    {150, "munlock"},
    {151, "mlockall"},
    {152, "munlockall"},
    {153, "vhangup"},
    {154, "modify_ldt"},
    {155, "pivot_root"},
    {156, "_sysctl"},
    {157, "prctl"},
    {158, "arch_prctl"},
    {159, "adjtimex"},
    {160, "setrlimit"},
    {161, "chroot"},
    {162, "sync"},
    {163, "acct"},
    {164, "settimeofday"},
    {165, "mount"},
    {166, "umount2"},
    {167, "swapon"},
    {168, "swapoff"},
    {169, "reboot"},
    {170, "sethostname"},
    {171, "setdomainname"},
    {172, "iopl"},
    {173, "ioperm"},
    {174, "create_module"},
    {175, "init_module"},
    {176, "delete_module"},
    {177, "get_kernel_syms"},
    {178, "query_module"},
    {179, "quotactl"},
    {180, "nfsservctl"},
    {181, "getpmsg"},
    {182, "putpmsg"},
    {183, "afs_syscall"},
    {184, "tuxcall"},
    {185, "security"},
    {186, "gettid"},
    {187, "readahead"},
    {188, "setxattr"},
    {189, "lsetxattr"},
    {190, "fsetxattr"},
    {191, "getxattr"},
    {192, "lgetxattr"},
    {193, "fgetxattr"},
    {194, "listxattr"},
    {195, "llistxattr"},
    {196, "flistxattr"},
    {197, "removexattr"},
    {198, "lremovexattr"},
    {199, "fremovexattr"},
    {200, "tkill"},
    {201, "time"},
    {202, "futex"},
    {203, "sched_setaffinity"},
    {204, "sched_getaffinity"},
    {205, "set_thread_area"},
    {206, "io_setup"},
    {207, "io_destroy"},
    {208, "io_getevents"},
    {209, "io_submit"},
    {210, "io_cancel"},
    {211, "get_thread_area"},
    {212, "lookup_dcookie"},
    {213, "epoll_create"},
    {214, "epoll_ctl_old"},
    {215, "epoll_wait_old"},
    {216, "remap_file_pages"},
    {217, "getdents64"},
    {218, "set_tid_address"},
    {219, "restart_syscall"},
    {220, "semtimedop"},
    {221, "fadvise64"},
    {222, "timer_create"},
    {223, "timer_settime"},
    {224, "timer_gettime"},
    {225, "timer_getoverrun"},
    {226, "timer_delete"},
    {227, "clock_settime"},
    {228, "clock_gettime"},
    {229, "clock_getres"},
    {230, "clock_nanosleep"},
    {231, "exit_group"},
    {232, "epoll_wait"},
    {233, "epoll_ctl"},
    {234, "tgkill"},
    {235, "utimes"},
    {236, "vserver"},
    {237, "mbind"},
    {238, "set_mempolicy"},
    {239, "get_mempolicy"},
    {240, "mq_open"},
    {241, "mq_unlink"},
    {242, "mq_timedsend"},
    {243, "mq_timedreceive"},
    {244, "mq_notify"},
    {245, "mq_getsetattr"},
    {246, "kexec_load"},
    {247, "waitid"},
    {248, "add_key"},
    {249, "request_key"},
    {250, "keyctl"},
    {251, "ioprio_set"},
    {252, "ioprio_get"},
    {253, "inotify_init"},
    {254, "inotify_add_watch"},
    {255, "inotify_rm_watch"},
    {256, "migrate_pages"},
    {257, "openat"},
    {258, "mkdirat"},
    {259, "mknodat"},
    {260, "fchownat"},
    {261, "futimesat"},
    {262, "newfstatat"},
    {263, "unlinkat"},
    {264, "renameat"},
    {265, "linkat"},
    {266, "symlinkat"},
    {267, "readlinkat"},
    {268, "fchmodat"},
    {269, "faccessat"},
    {270, "pselect6"},
    {271, "ppoll"},
    {272, "unshare"},
    {273, "set_robust_list"},
    {274, "get_robust_list"},
    {275, "splice"},
    {276, "tee"},
    {277, "sync_file_range"},
    {278, "vmsplice"},
    {279, "move_pages"},
    {280, "utimensat"},
    {281, "epoll_pwait"},
    {282, "signalfd"},
    {283, "timerfd_create"},
    {284, "eventfd"},
    {285, "fallocate"},
    {286, "timerfd_settime"},
    {287, "timerfd_gettime"},
    {288, "accept4"},
    {289, "signalfd4"},
    {290, "eventfd2"},
    {291, "epoll_create1"},
    {292, "dup3"},
    {293, "pipe2"},
    {294, "inotify_init1"},
    {295, "preadv"},
    {296, "pwritev"},
    {297, "rt_tgsigqueueinfo"},
    {298, "perf_event_open"},
    {299, "recvmmsg"},
    {300, "fanotify_init"},
    {301, "fanotify_mark"},
    {302, "prlimit64"},
    {303, "name_to_handle_at"},
    {304, "open_by_handle_at"},
    {305, "clock_adjtime"},
    {306, "syncfs"},
    {307, "sendmmsg"},
    {308, "setns"},
    {309, "getcpu"},
    {310, "process_vm_readv"},
    {311, "process_vm_writev"},
    {312, "kcmp"},
    {313, "finit_module"},
    {-1, NULL}  // Sentinel to mark the end
};

#define IS_AARCH64_ARCH 0
#else
#define IS_X86_ARCH 0
#define IS_AARCH64_ARCH 1
#endif

#if defined(__aarch64__) || !defined(IS_X86_ARCH)
static struct syscall_map aarch64_syscalls[] = {
    {0, "io_setup"},
    {1, "io_destroy"},
    {2, "io_submit"},
    {3, "io_cancel"},
    {4, "io_getevents"},
    {5, "setxattr"},
    {6, "lsetxattr"},
    {7, "fsetxattr"},
    {8, "getxattr"},
    {9, "lgetxattr"},
    {10, "fgetxattr"},
    {11, "listxattr"},
    {12, "llistxattr"},
    {13, "flistxattr"},
    {14, "removexattr"},
    {15, "lremovexattr"},
    {16, "fremovexattr"},
    {17, "getcwd"},
    {18, "lookup_dcookie"},
    {19, "eventfd2"},
    {20, "epoll_create1"},
    {21, "epoll_ctl"},
    {22, "epoll_pwait"},
    {23, "dup"},
    {24, "dup3"},
    {25, "fcntl"},
    {26, "inotify_init1"},
    {27, "inotify_add_watch"},
    {28, "inotify_rm_watch"},
    {29, "ioctl"},
    {30, "ioprio_set"},
    {31, "ioprio_get"},
    {32, "flock"},
    {33, "mknodat"},
    {34, "mkdirat"},
    {35, "unlinkat"},
    {36, "symlinkat"},
    {37, "linkat"},
    {38, "renameat"},
    {39, "umount2"},
    {40, "mount"},
    {41, "pivot_root"},
    {42, "nfsservctl"},
    {43, "statfs"},
    {44, "fstatfs"},
    {45, "truncate"},
    {46, "ftruncate"},
    {47, "fallocate"},
    {48, "faccessat"},
    {49, "chdir"},
    {50, "fchdir"},
    {51, "chroot"},
    {52, "fchmod"},
    {53, "fchmodat"},
    {54, "fchownat"},
    {55, "fchown"},
    {56, "openat"},
    {57, "close"},
    {58, "vhangup"},
    {59, "pipe2"},
    {60, "quotactl"},
    {61, "getdents64"},
    {62, "lseek"},
    {63, "read"},
    {64, "write"},
    {65, "readv"},
    {66, "writev"},
    {67, "pread64"},
    {68, "pwrite64"},
    {69, "preadv"},
    {70, "pwritev"},
    {71, "sendfile"},
    {72, "pselect6"},
    {73, "ppoll"},
    {74, "signalfd4"},
    {75, "vmsplice"},
    {76, "splice"},
    {77, "tee"},
    {78, "readlinkat"},
    {79, "newfstatat"},
    {80, "fstat"},
    {81, "sync"},
    {82, "fsync"},
    {83, "fdatasync"},
    {84, "sync_file_range"},
    {85, "timerfd_create"},
    {86, "timerfd_settime"},
    {87, "timerfd_gettime"},
    {88, "utimensat"},
    {89, "acct"},
    {90, "capget"},
    {91, "capset"},
    {92, "personality"},
    {93, "exit"},
    {94, "exit_group"},
    {95, "waitid"},
    {96, "set_tid_address"},
    {97, "unshare"},
    {98, "futex"},
    {99, "set_robust_list"},
    {100, "get_robust_list"},
    {101, "nanosleep"},
    {102, "getitimer"},
    {103, "setitimer"},
    {104, "kexec_load"},
    {105, "init_module"},
    {106, "delete_module"},
    {107, "timer_create"},
    {108, "timer_gettime"},
    {109, "timer_getoverrun"},
    {110, "timer_settime"},
    {111, "timer_delete"},
    {112, "clock_settime"},
    {113, "clock_gettime"},
    {114, "clock_getres"},
    {115, "clock_nanosleep"},
    {116, "syslog"},
    {117, "ptrace"},
    {118, "sched_setparam"},
    {119, "sched_setscheduler"},
    {120, "sched_getscheduler"},
    {121, "sched_getparam"},
    {122, "sched_setaffinity"},
    {123, "sched_getaffinity"},
    {124, "sched_yield"},
    {125, "sched_get_priority_max"},
    {126, "sched_get_priority_min"},
    {127, "sched_rr_get_interval"},
    {128, "restart_syscall"},
    {129, "kill"},
    {130, "tkill"},
    {131, "tgkill"},
    {132, "sigaltstack"},
    {133, "rt_sigsuspend"},
    {134, "rt_sigaction"},
    {135, "rt_sigprocmask"},
    {136, "rt_sigpending"},
    {137, "rt_sigtimedwait"},
    {138, "rt_sigqueueinfo"},
    {139, "rt_sigreturn"},
    {140, "setpriority"},
    {141, "getpriority"},
    {142, "reboot"},
    {143, "setregid"},
    {144, "setgid"},
    {145, "setreuid"},
    {146, "setuid"},
    {147, "setresuid"},
    {148, "getresuid"},
    {149, "setresgid"},
    {150, "getresgid"},
    {151, "setfsuid"},
    {152, "setfsgid"},
    {153, "times"},
    {154, "setpgid"},
    {155, "getpgid"},
    {156, "getsid"},
    {157, "setsid"},
    {158, "getgroups"},
    {159, "setgroups"},
    {160, "uname"},
    {161, "sethostname"},
    {162, "setdomainname"},
    {163, "getrlimit"},
    {164, "setrlimit"},
    {165, "getrusage"},
    {166, "umask"},
    {167, "prctl"},
    {168, "getcpu"},
    {169, "gettimeofday"},
    {170, "settimeofday"},
    {171, "adjtimex"},
    {172, "getpid"},
    {173, "getppid"},
    {174, "getuid"},
    {175, "geteuid"},
    {176, "getgid"},
    {177, "getegid"},
    {178, "gettid"},
    {179, "sysinfo"},
    {180, "mq_open"},
    {181, "mq_unlink"},
    {182, "mq_timedsend"},
    {183, "mq_timedreceive"},
    {184, "mq_notify"},
    {185, "mq_getsetattr"},
    {186, "msgget"},
    {187, "msgctl"},
    {188, "msgrcv"},
    {189, "msgsnd"},
    {190, "semget"},
    {191, "semctl"},
    {192, "semtimedop"},
    {193, "semop"},
    {194, "shmget"},
    {195, "shmctl"},
    {196, "shmat"},
    {197, "shmdt"},
    {198, "socket"},
    {199, "socketpair"},
    {200, "bind"},
    {201, "listen"},
    {202, "accept"},
    {203, "connect"},
    {204, "getsockname"},
    {205, "getpeername"},
    {206, "sendto"},
    {207, "recvfrom"},
    {208, "setsockopt"},
    {209, "getsockopt"},
    {210, "shutdown"},
    {211, "sendmsg"},
    {212, "recvmsg"},
    {213, "readahead"},
    {214, "brk"},
    {215, "munmap"},
    {216, "mremap"},
    {217, "add_key"},
    {218, "request_key"},
    {219, "keyctl"},
    {220, "clone"},
    {221, "execve"},
    {222, "mmap"},
    {223, "fadvise64"},
    {224, "swapon"},
    {225, "swapoff"},
    {226, "mprotect"},
    {227, "msync"},
    {228, "mlock"},
    {229, "munlock"},
    {230, "mlockall"},
    {231, "munlockall"},
    {232, "mincore"},
    {233, "madvise"},
    {234, "remap_file_pages"},
    {235, "mbind"},
    {236, "get_mempolicy"},
    {237, "set_mempolicy"},
    {238, "migrate_pages"},
    {239, "move_pages"},
    {240, "rt_tgsigqueueinfo"},
    {241, "perf_event_open"},
    {242, "accept4"},
    {243, "recvmmsg"},
    {244, "wait4"},
    {260, "process_vm_readv"},
    {261, "process_vm_writev"},
    {262, "preadv2"},
    {263, "pwritev2"},
    {-1, NULL}
};
#endif

static const char *get_syscall_name(int syscall_nr) {
#if IS_X86_ARCH
    for (int i = 0; x86_syscalls[i].name != NULL; i++) {
        if (x86_syscalls[i].num == syscall_nr) {
            return x86_syscalls[i].name;
        }
    }
#endif

#if IS_AARCH64_ARCH
        for (int i = 0; aarch64_syscalls[i].name != NULL; i++) {
            if (aarch64_syscalls[i].num == syscall_nr) {
                return aarch64_syscalls[i].name;
            }
        }
#endif

    return "unknown_syscall";
}

static int syscall_verbose = 1;

typedef enum {
    ARG_INT,       // Integer
    ARG_UINT,      // Unsigned integer
    ARG_HEX,       // Hexadecimal value
    ARG_STR,       // String pointer
    ARG_PTR,       // Pointer
    ARG_FD,        // File descriptor
    ARG_NONE       // Unused argument
} arg_type_t;

struct syscall_arg_desc {
    const char *name;
    arg_type_t type;
};

struct syscall_info {
    const char *name;
    int num_args;
    struct syscall_arg_desc args[6];
};

static struct syscall_info syscall_descriptions[] = {
    {
        .name = "read",
        .num_args = 3,
        .args = {
            {"fd", ARG_FD},
            {"buf", ARG_PTR},
            {"count", ARG_UINT},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE}
        }
    },
    {
        .name = "write",
        .num_args = 3,
        .args = {
            {"fd", ARG_FD},
            {"buf", ARG_PTR},
            {"count", ARG_UINT},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE}
        }
    },
    {
        .name = "open",
        .num_args = 3,
        .args = {
            {"filename", ARG_STR},
            {"flags", ARG_HEX},
            {"mode", ARG_HEX},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE}
        }
    },
    {
        .name = "close",
        .num_args = 1,
        .args = {
            {"fd", ARG_FD},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE}
        }
    },
    {
        .name = "brk",
        .num_args = 1,
        .args = {
            {"addr", ARG_PTR},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE}
        }
    },
    {
        .name = "mmap",
        .num_args = 6,
        .args = {
            {"addr", ARG_PTR},
            {"length", ARG_UINT},
            {"prot", ARG_HEX},
            {"flags", ARG_HEX},
            {"fd", ARG_FD},
            {"offset", ARG_UINT}
        }
    },
    {
        .name = "munmap",
        .num_args = 2,
        .args = {
            {"addr", ARG_PTR},
            {"length", ARG_UINT},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE}
        }
    },
    {
        .name = "exit",
        .num_args = 1,
        .args = {
            {"status", ARG_INT},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE},
            {"", ARG_NONE}
        }
    },
    {NULL, 0, {{NULL, ARG_NONE}}}
};

static const struct syscall_info *get_syscall_info(const char *name) {
    for (int i = 0; syscall_descriptions[i].name != NULL; i++) {
        if (strcmp(syscall_descriptions[i].name, name) == 0) {
            return &syscall_descriptions[i];
        }
    }
    return NULL;
}

static void format_syscall_args(const char *syscall_name, __u64 args[6], char *buffer, size_t buffer_size) {
    const struct syscall_info *info = get_syscall_info(syscall_name);

    if (!info || !syscall_verbose) {
        snprintf(buffer, buffer_size, "args=[0x%llx, 0x%llx, 0x%llx, 0x%llx, 0x%llx, 0x%llx]",
                 args[0], args[1], args[2], args[3], args[4], args[5]);
        return;
    }

    int pos = 0;
    pos += snprintf(buffer + pos, buffer_size - pos, "args=[");

    for (int i = 0; i < info->num_args && i < 6; i++) {
        if (i > 0) {
            pos += snprintf(buffer + pos, buffer_size - pos, ", ");
        }

        switch (info->args[i].type) {
            case ARG_INT:
                pos += snprintf(buffer + pos, buffer_size - pos, "%s=%lld",
                               info->args[i].name, (long long)args[i]);
                break;
            case ARG_UINT:
                pos += snprintf(buffer + pos, buffer_size - pos, "%s=%llu",
                               info->args[i].name, (unsigned long long)args[i]);
                break;
            case ARG_HEX:
                pos += snprintf(buffer + pos, buffer_size - pos, "%s=0x%llx",
                               info->args[i].name, (unsigned long long)args[i]);
                break;
            case ARG_STR:
                pos += snprintf(buffer + pos, buffer_size - pos, "%s=<%p>",
                               info->args[i].name, (void*)args[i]);
                break;
            case ARG_PTR:
                pos += snprintf(buffer + pos, buffer_size - pos, "%s=%p",
                               info->args[i].name, (void*)args[i]);
                break;
            case ARG_FD:
                pos += snprintf(buffer + pos, buffer_size - pos, "%s=%d",
                               info->args[i].name, (int)args[i]);
                break;
            default:
                pos += snprintf(buffer + pos, buffer_size - pos, "%s=0x%llx",
                               info->args[i].name, (unsigned long long)args[i]);
                break;
        }
    }

    snprintf(buffer + pos, buffer_size - pos, "]");
}

static int handle_event(void *ctx __attribute__((unused)), void *data, size_t data_sz __attribute__((unused))) {
    const struct event_data *e = data;

    printf("[%llu.%09llu] PID: %u TID: %u COMM: %s EVENT: ",
           e->timestamp / 1000000000ULL, e->timestamp % 1000000000ULL,
           e->pid, e->tid, e->comm);

    switch (e->event_type) {
        case 0: // EVENT_PROCESS_START
            printf("PROCESS_START FILENAME: %s\n", e->filename);
            break;
        case 1: // EVENT_PROCESS_END
            printf("PROCESS_END\n");
            break;
        case 2: // EVENT_SYSCALL_ENTER
            {
                const char *syscall_name = get_syscall_name(e->syscall_nr);
                char args_buffer[256];
                format_syscall_args(syscall_name, e->args, args_buffer, sizeof(args_buffer));
                printf("SYSCALL_ENTER SYSCALL: %s (%u) %s\n",
                       syscall_name, e->syscall_nr, args_buffer);
                stats.syscalls++;
            }
            break;
        case 3: // EVENT_SYSCALL_EXIT
            printf("SYSCALL_EXIT RETVAL: %lld\n", e->retval);
            break;
        case 4: // EVENT_MEMORY_ALLOC
            printf("MEMORY_ALLOC SIZE: %llu\n", e->size);
            stats.memory_allocs++;
            stats.total_allocated += e->size;
            stats.current_memory += e->size;
            if (stats.current_memory > stats.peak_memory)
                stats.peak_memory = stats.current_memory;
            break;
        case 5: // EVENT_MEMORY_FREE
            printf("MEMORY_FREE ADDR: 0x%llx\n", e->addr);
            stats.memory_frees++;
            break;
        case 6: // EVENT_PAGE_FAULT
            printf("PAGE_FAULT ADDR: 0x%llx\n", e->addr);
            stats.page_faults++;

            // If we have additional info about the fault type from BPF, we could
            // increment minor_faults or major_faults here
            break;
        case 7: // EVENT_MMAP
            printf("MMAP SIZE: %llu\n", e->size);
            stats.mmaps++;
            break;
        case 8: // EVENT_MUNMAP
            printf("MUNMAP ADDR: 0x%llx SIZE: %llu\n", e->addr, e->size);
            stats.munmaps++;
            break;
        default:
            printf("UNKNOWN\n");
            break;
    }

    return 0;
}

static int add_target_pid(int map_fd, pid_t pid) {
    uint8_t val = 1;
    int ret = bpf_map_update_elem(map_fd, &pid, &val, BPF_ANY);

    if (ret == 0) {
        printf("Added PID %d to target map\n", pid);
    } else {
        fprintf(stderr, "Failed to add PID %d to target map: %s\n", pid, strerror(errno));
    }

    return ret;
}

static void print_memory_leaks(int map_fd) {
    uint64_t key = 0, next_key = 0;
    struct {
        uint64_t addr;
        uint64_t size;
        uint64_t timestamp;
        uint32_t pid;
    } value;
    int found_leaks = 0;

    printf("\n=== MEMORY LEAK ANALYSIS ===\n");

    if (bpf_map_get_next_key(map_fd, NULL, &key) == 0) {
        do {
            if (bpf_map_lookup_elem(map_fd, &key, &value) == 0) {
                if (!found_leaks) {
                    printf("Potential memory leaks detected:\n");
                    found_leaks = 1;
                }
                printf("  LEAK: addr=0x%lx size=%lu pid=%u timestamp=%lu\n",
                       value.addr, value.size, value.pid, value.timestamp);
            }
        } while (bpf_map_get_next_key(map_fd, &key, &next_key) == 0 && (key = next_key));
    }

    if (!found_leaks) {
        printf("No memory leaks detected!\n");
    }
}

static void print_statistics() {
    printf("\n=== PROFILING STATISTICS ===\n");
    printf("System calls: %lu\n", stats.syscalls);
    printf("Memory allocations: %lu\n", stats.memory_allocs);
    printf("Memory frees: %lu\n", stats.memory_frees);
    printf("Page faults: %lu\n", stats.page_faults);
    printf("Memory mappings (mmap): %lu\n", stats.mmaps);
    printf("Memory unmappings (munmap): %lu\n", stats.munmaps);
    printf("Total allocated: %lu bytes\n", stats.total_allocated);
    printf("Total freed: %lu bytes\n", stats.total_freed);
    printf("Peak memory usage: %lu bytes\n", stats.peak_memory);
    printf("Current memory usage: %lu bytes\n", stats.current_memory);

    if (stats.memory_allocs > stats.memory_frees) {
        printf("Potential memory leaks: %lu allocations not freed\n",
               stats.memory_allocs - stats.memory_frees);
    }
}

static void collect_proc_stats(pid_t pid) {
    char path[64];
    FILE *fp;

    snprintf(path, sizeof(path), "/proc/%d/stat", pid);
    fp = fopen(path, "r");
    if (fp) {
        // Format: pid (comm) state ppid ... minflt cmajflt ...
        long long int min_flt = 0, maj_flt = 0;
        if (fscanf(fp, "%*d %*s %*c %*d %*d %*d %*d %*d %*u %lld %lld", &min_flt, &maj_flt) == 2) {
            stats.minor_faults = min_flt;
            stats.major_faults = maj_flt;
        }
        fclose(fp);
    }

    snprintf(path, sizeof(path), "/proc/%d/status", pid);
    fp = fopen(path, "r");
    if (fp) {
        char line[256];
        while (fgets(line, sizeof(line), fp)) {
            unsigned long val;

            if (sscanf(line, "VmSize: %lu kB", &val) == 1) {
                stats.vsz = val * 1024; // Convert to bytes
            }
            else if (sscanf(line, "VmRSS: %lu kB", &val) == 1) {
                stats.rss = val * 1024; // Convert to bytes
            }
            else if (sscanf(line, "VmHWM: %lu kB", &val) == 1) {
                stats.rss_peak = val * 1024; // Convert to bytes
            }
            else if (sscanf(line, "VmSwap: %lu kB", &val) == 1) {
                stats.swap_used = val * 1024; // Convert to bytes
            }
        }
        fclose(fp);
    }

    if (stats.rss == 0) {
        stats.rss = stats.current_memory;
        stats.rss_peak = stats.peak_memory;
    }
}

static void print_paging_stats() {
    printf("\n=== MEMORY PAGING STATISTICS ===\n");
    printf("Minor page faults: %llu\n", (unsigned long long)stats.minor_faults);
    printf("Major page faults: %llu\n", (unsigned long long)stats.major_faults);
    printf("Virtual memory size: %llu bytes (%.2f MB)\n",
           (unsigned long long)stats.vsz, (double)stats.vsz / (1024 * 1024));
    printf("Resident set size: %llu bytes (%.2f MB)\n",
           (unsigned long long)stats.rss, (double)stats.rss / (1024 * 1024));
    printf("Peak resident set size: %llu bytes (%.2f MB)\n",
           (unsigned long long)stats.rss_peak, (double)stats.rss_peak / (1024 * 1024));

    if (stats.swap_used > 0) {
        printf("Swap usage: %llu bytes (%.2f MB)\n",
               (unsigned long long)stats.swap_used, (double)stats.swap_used / (1024 * 1024));
    }

    double exec_time = 0;
    if (stats.syscalls > 0 || stats.page_faults > 0 || stats.memory_allocs > 0) {
        exec_time = stats.page_faults > 0 ?
                    (double)stats.page_faults / (stats.minor_faults + stats.major_faults) : 0;
        printf("Page fault rate: %.2f faults/sec\n", exec_time);
    }

    printf("Memory efficiency:\n");
    if (stats.vsz > 0) {
        printf("  - RSS/VSZ ratio: %.2f%%\n",
               stats.vsz > 0 ? ((double)stats.rss / stats.vsz) * 100.0 : 0);
    }

    if (stats.total_allocated > 0) {
        printf("  - Allocation efficiency: %.2f%%\n",
               ((double)(stats.total_allocated - stats.total_freed) / stats.total_allocated) * 100.0);
    }
}

static int attach_uprobe_malloc_free(struct process_profiler_bpf *skel, pid_t pid __attribute__((unused))) {
    const char *libc_path = "/lib/aarch64-linux-gnu/libc.so.6";

    if (access(libc_path, F_OK) != 0) {
        FILE *fp;
        char path[256];
        char cmd[] = "ldconfig -p | grep libc.so.6 | awk '{print $NF}' | head -n1";

        fp = popen(cmd, "r");
        if (fp == NULL) {
            fprintf(stderr, "Failed to run ldconfig to find libc\n");
            return -1;
        }

        if (fgets(path, sizeof(path), fp) != NULL) {
            // Remove newline
            path[strcspn(path, "\n")] = 0;
            libc_path = strdup(path);
            printf("Found libc at: %s\n", libc_path);
        }
        pclose(fp);

        if (access(libc_path, F_OK) != 0) {
            fprintf(stderr, "Could not find libc.so.6 on the system\n");
            return -1;
        }
    }

    unsigned long malloc_offset = 0;
    FILE *fp;
    char cmd[512];
    char line[256];

    snprintf(cmd, sizeof(cmd), "objdump -T %s | grep ' malloc$' | awk '{print $1}'", libc_path);
    fp = popen(cmd, "r");
    if (fp != NULL) {
        if (fgets(line, sizeof(line), fp) != NULL) {
            malloc_offset = strtoul(line, NULL, 16);
            printf("Found malloc at offset: 0x%lx\n", malloc_offset);
        }
        pclose(fp);
    }

    unsigned long free_offset = 0;
    snprintf(cmd, sizeof(cmd), "objdump -T %s | grep ' free$' | awk '{print $1}'", libc_path);
    fp = popen(cmd, "r");
    if (fp != NULL) {
        if (fgets(line, sizeof(line), fp) != NULL) {
            // Convert hex string to long
            free_offset = strtoul(line, NULL, 16);
            printf("Found free at offset: 0x%lx\n", free_offset);
        }
        pclose(fp);
    }

    // Attach malloc uprobe using the correct libbpf API
    if (malloc_offset > 0) {
        // Use -1 for PID to attach to all processes
        skel->links.trace_malloc = bpf_program__attach_uprobe(skel->progs.trace_malloc,
                                                         false, -1, libc_path,
                                                         malloc_offset);
        if (!skel->links.trace_malloc) {
            fprintf(stderr, "Warning: Failed to attach malloc uprobe\n");
        } else {
            printf("Successfully attached malloc uprobe\n");

            // Attach malloc uretprobe if the uprobe succeeded
            skel->links.trace_malloc_ret = bpf_program__attach_uprobe(skel->progs.trace_malloc_ret,
                                                                 true, -1, libc_path,
                                                                 malloc_offset);
            if (!skel->links.trace_malloc_ret) {
                fprintf(stderr, "Warning: Failed to attach malloc uretprobe\n");
            } else {
                printf("Successfully attached malloc uretprobe\n");
            }
        }
    } else {
        fprintf(stderr, "Could not find malloc in libc\n");
    }

    // Attach free uprobe
    if (free_offset > 0) {
        skel->links.trace_free = bpf_program__attach_uprobe(skel->progs.trace_free,
                                                       false, -1, libc_path,
                                                       free_offset);
        if (!skel->links.trace_free) {
            fprintf(stderr, "Warning: Failed to attach free uprobe\n");
        } else {
            printf("Successfully attached free uprobe\n");
        }
    } else {
        fprintf(stderr, "Could not find free in libc\n");
    }

    return 0;
}

static int wait_for_process(pid_t pid) {
    int status;
    int ret;

    printf("Waiting for process %d to complete...\n", pid);

    while ((ret = waitpid(pid, &status, WNOHANG)) == 0) {
        if (kill(pid, 0) == -1 && errno == ESRCH) {
            printf("Process %d has exited\n", pid);
            break;
        }
        usleep(100000);
    }

    if (ret > 0) {
        if (WIFEXITED(status)) {
            printf("Target process exited with status: %d\n", WEXITSTATUS(status));
        } else if (WIFSIGNALED(status)) {
            printf("Target process killed by signal: %d\n", WTERMSIG(status));
        }
    }

    return status;
}

static pid_t spawn_target_program() {
    // Set up a pipe for synchronization
    int sync_pipe[2];
    if (pipe(sync_pipe) == -1) {
        perror("pipe");
        return -1;
    }

    pid_t pid = fork();

    if (pid == 0) {
        close(sync_pipe[1]);

        char buf;
        if (read(sync_pipe[0], &buf, 1) != 1) {
            perror("Child read from pipe failed");
            exit(1);
        }
        close(sync_pipe[0]);

        execvp(target_program, target_args);
        perror("execvp");
        exit(1);
    } else if (pid > 0) {
        close(sync_pipe[0]);

        printf("Spawned target process with PID: %d\n", pid);

        printf("Attaching BPF programs before starting process...\n");
        sleep(1);

        if (write(sync_pipe[1], "x", 1) != 1) {
            perror("Parent write to pipe failed");
            return -1;
        }
        close(sync_pipe[1]);

        return pid;
    } else {
        perror("fork");
        return -1;
    }
}

int main(int argc, char **argv) {
    struct ring_buffer *rb = NULL;
    int err;

    if (argc < 2) {
        printf("Usage: %s <program> [args...]\n", argv[0]);
        printf("       %s -p <pid>\n", argv[0]);
        return 1;
    }

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-q") == 0 || strcmp(argv[i], "--quiet") == 0) {
            syscall_verbose = 0;
            continue;
        }

        if (strcmp(argv[i], "-p") == 0) {
            if (i + 1 < argc) {
                target_pid = atoi(argv[i+1]);
                if (target_pid <= 0) {
                    fprintf(stderr, "Error: Invalid PID\n");
                    return 1;
                }
                i++; // Skip the next argument
            } else {
                fprintf(stderr, "Error: PID required after -p\n");
                return 1;
            }
        } else if (i == 1) {
            // First non-option argument is the program
            strcpy(target_program, argv[i]);
            target_args = &argv[i];
            break;
        }
    }

    if (target_pid == 0 && target_program[0] == '\0') {
        printf("Usage: %s [-q|--quiet] <program> [args...]\n", argv[0]);
        printf("       %s [-q|--quiet] -p <pid>\n", argv[0]);
        return 1;
    }

    signal(SIGINT, sig_handler);
    signal(SIGTERM, sig_handler);

    struct rlimit rlim_new = {
        .rlim_cur = RLIM_INFINITY,
        .rlim_max = RLIM_INFINITY,
    };
    if (setrlimit(RLIMIT_MEMLOCK, &rlim_new)) {
        fprintf(stderr, "Failed to increase RLIMIT_MEMLOCK limit!\n");
        return 1;
    }

    skel = process_profiler_bpf__open();
    if (!skel) {
        fprintf(stderr, "Failed to open BPF skeleton\n");
        return 1;
    }

    err = process_profiler_bpf__load(skel);
    if (err) {
        fprintf(stderr, "Failed to load and verify BPF skeleton\n");
        goto cleanup;
    }

    err = process_profiler_bpf__attach(skel);
    if (err) {
        fprintf(stderr, "Failed to attach BPF skeleton\n");
        goto cleanup;
    }

    if (attach_uprobe_malloc_free(skel, -1) < 0) {
        fprintf(stderr, "Warning: Failed to attach malloc/free uprobes, memory leak detection will be limited\n");
        // Continue anyway, other tracing will still work
    }

    if (target_pid == 0) {
        target_pid = spawn_target_program();
        if (target_pid < 0) {
            goto cleanup;
        }
    }

    err = add_target_pid(bpf_map__fd(skel->maps.target_pids), target_pid);
    if (err) {
        fprintf(stderr, "Failed to add target PID to map\n");
        goto cleanup;
    }

    rb = ring_buffer__new(bpf_map__fd(skel->maps.events), handle_event, NULL, NULL);
    if (!rb) {
        err = -1;
        fprintf(stderr, "Failed to create ring buffer\n");
        goto cleanup;
    }

    printf("Successfully started profiling PID %d\n", target_pid);

    while (!exiting) {
        err = ring_buffer__poll(rb, 100);
        if (err == -EINTR) {
            err = 0;
            break;
        }
        if (err < 0) {
            printf("Error polling ring buffer: %d\n", err);
            break;
        }

        if (kill(target_pid, 0) == -1 && errno == ESRCH) {
            printf("Target process has exited\n");
            break;
        }

        static int counter = 0;
        if (++counter % 10 == 0 && target_pid > 0 && kill(target_pid, 0) == 0) {
            collect_proc_stats(target_pid);
            counter = 0;
        }
    }

    if (target_args) {
        wait_for_process(target_pid);
    }

    collect_proc_stats(target_pid);

    print_statistics();
    print_memory_leaks(bpf_map__fd(skel->maps.memory_map));
    print_paging_stats();

cleanup:
    ring_buffer__free(rb);
    process_profiler_bpf__destroy(skel);
    return err < 0 ? -err : 0;
}
