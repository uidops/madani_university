#ifndef PROCESS_PROFILER_H
#define PROCESS_PROFILER_H

#include <stdint.h>

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
    uint64_t timestamp;
    uint32_t pid;
    uint32_t tid;
    uint32_t event_type;
    uint64_t addr;
    uint64_t size;
    int64_t retval;
    uint32_t syscall_nr;
    char comm[MAX_COMM_LEN];
    char filename[MAX_FILENAME_LEN];
};

struct memory_alloc {
    uint64_t addr;
    uint64_t size;
    uint64_t timestamp;
    uint32_t pid;
};

#endif
