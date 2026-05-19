# Factorial

Assembly exercise for calculating and printing the factorial of an input number.

## Files

| File | Description |
| --- | --- |
| `main.asm` | DOS Assembly source code for reading input, calculating factorial, and printing the result. |

## How It Works

The program reads decimal digits from the keyboard until Enter is pressed. It builds the input number, calculates the factorial with repeated multiplication, converts the result to ASCII digits, and prints it using DOS interrupt `21h`.

## Run

This program targets a DOS-style 8086 environment. Use a compatible assembler and emulator such as EMU8086, DOSBox with an assembler, or another DOS-compatible toolchain.

Example input:

```text
5
```

Expected output:

```text
120
```

## Notes

- The program is intended for educational use.
- Use small input values because the result is stored in CPU registers and can overflow quickly.
