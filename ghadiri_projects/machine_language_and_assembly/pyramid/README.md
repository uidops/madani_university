# Pyramid

Programming exercise for printing a centered star pyramid from a user-provided height.

## Files

| File | Description |
| --- | --- |
| `pyramid.c` | C implementation of the pyramid program. |
| `pyramid.asm` | DOS Assembly implementation of the same exercise. |
| `pyramid.pdf` | Assignment report or exported document. |
| `pyramid_0351.pdf` | Additional exported report/document file. |
| `pyramid.docx` | Editable report/document file. |

## Run The C Version

From this directory:

```bash
gcc pyramid.c -o pyramid
./pyramid
```

Enter the pyramid height when prompted by the program.

Example input:

```text
5
```

Example output:

```text
    *
   ***
  *****
 *******
*********
```

## Run The Assembly Version

The Assembly implementation targets a DOS-style 8086 runtime and uses interrupt `21h` for input and output. Assemble and run it with EMU8086, DOSBox with a compatible assembler, or another DOS-compatible toolchain.

## Notes

- `pyramid.c` is the easiest version to compile and test on a modern system.
- The Assembly version is kept for the course's low-level programming requirements.
- Generated binaries should not be committed.
