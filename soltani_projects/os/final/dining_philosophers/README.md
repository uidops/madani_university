# Dining Philosophers

C implementation of the dining philosophers synchronization problem.

## Files

| File | Description |
| --- | --- |
| `main.c` | POSIX threads, semaphores, and ncurses-based visualization. |
| `CMakeLists.txt` | CMake project configuration. |
| `Makefile` | Generated or helper makefile. |
| `dining.pdf` | Project report or exported document. |

## Build

Using CMake from this directory:

```bash
cmake .
make
```

Or compile manually if dependencies are available:

```bash
cc main.c -o dining_philosophers -lpthread -lncurses
```

## Run

```bash
./dining_philosophers
```

## Notes

- The program uses POSIX threads, named semaphores, and ncurses.
- Press `q` during execution to quit.
- Generated binaries and CMake cache/build files should not be committed.
