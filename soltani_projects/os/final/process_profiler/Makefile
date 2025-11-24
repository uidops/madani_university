CC = clang
CLANG = clang
BPFTOOL = bpftool

CFLAGS = -O2 -Wall -Wextra
INCLUDES = -I/usr/include/bpf -I./include
LIBS = -lbpf -lelf -lz

TARGET = process_profiler
BPF_OBJ = process_profiler.bpf.o
SKEL_H = process_profiler.skel.h

.PHONY: all clean

all: $(TARGET)

vmlinux.h:
	$(BPFTOOL) btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h

$(BPF_OBJ): process_profiler.bpf.c vmlinux.h
	$(CLANG) -g -O2 -target bpf -D__TARGET_ARCH_arm64 -I. -c $< -o $@

$(TARGET)-original: process_profiler.bpf.c vmlinux.h main.c
	$(CLANG) -g -O2 -target bpf -D__TARGET_ARCH_arm64 -I. -c process_profiler.bpf.c -o process_profiler.bpf.o
	$(BPFTOOL) gen skeleton process_profiler.bpf.o > process_profiler.skel.h
	$(CC) $(CFLAGS) $(INCLUDES) main.c $(LIBS) -o $@

$(SKEL_H): $(BPF_OBJ)
	$(BPFTOOL) gen skeleton $< > $@

$(TARGET): main.c $(SKEL_H)
	$(CC) $(CFLAGS) $(INCLUDES) $< $(LIBS) -o $@

clean:
	rm -f $(TARGET) $(BPF_OBJ) $(SKEL_H) vmlinux.h

install-deps:
	sudo apt update
	sudo apt install -y libbpf-dev clang llvm linux-tools-common linux-headers-$(shell uname -r)

help:
	@echo "Available targets:"
	@echo "  all          - Build the profiler"
	@echo "  clean        - Clean build artifacts"
	@echo "  install-deps - Install required dependencies"
	@echo "  help         - Show this help"
	@echo ""
	@echo "Usage examples:"
	@echo "  ./process_profiler /bin/ls -la"
	@echo "  ./process_profiler -p 1234"
