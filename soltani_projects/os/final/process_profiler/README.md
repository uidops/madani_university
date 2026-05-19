# Process Profiler

Linux eBPF process profiler written in C.

## Files

| File | Description |
| --- | --- |
| `main.c` | User-space profiler program that loads and reads eBPF events. |
| `process_profiler.bpf.c` | eBPF program for process, syscall, memory, and page-fault events. |
| `include/process_profiler.h` | Shared header definitions. |
| `Makefile` | Build commands for the profiler. |
| `process_profiler.pdf` | Project report or exported document. |

## Build

From this directory:

```bash
make
```

## Run

The profiler depends on Linux eBPF support and usually requires elevated privileges.

```bash
sudo ./process_profiler <program> [args...]
```

## Requirements

- Linux with eBPF support
- Clang/LLVM
- libbpf development files
- bpftool or generated BPF skeleton support
- Root privileges or suitable BPF permissions

## Notes

- This project is Linux-specific and is not expected to run on macOS without a Linux VM or container with BPF support.
- Generated binaries, skeleton files, and build outputs should not be committed.
