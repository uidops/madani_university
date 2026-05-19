# Madani University Projects

This repository collects my personal course projects, exercises, and final assignments for Madani University courses. The projects cover algorithms, artificial intelligence, simulation, operating systems, numerical methods, web design, databases, and low-level programming.

Most work is organized by professor or course name. Each top-level `*_projects` directory contains the assignments, experiments, and related source files for that course area.

## Repository Structure

| Directory | Contents |
| --- | --- |
| `ghadiri_projects/` | Assembly and C exercises such as factorial and pyramid programs. |
| `ghavidel_projects/` | Professor Jalil Ghavidel course projects, including AI and compiler design work. |
| `heydarian_projects/` | Professor Mohsen Heydarian simulation projects, including random-walk and genetic-algorithm Rust exercises. |
| `imanzadeh_projects/` | Professor Sodabeh Imanzadeh projects, including web-designing exercises and database setup. |
| `mehanfar_projects/` | Professor Mehanfar assignments, including algorithm analysis and C data-structure exercises. |
| `norian_projects/` | Professor Farshid Norian algorithm projects, including Kruskal, Dijkstra, N-Queen, TSP, OBST, and scheduling. |
| `oskouei_projects/` | Professor Amin Golzari Oskouei assignments, including Python exercises, K-means, ciphers, and final project work. |
| `pourmahmood_projects/` | Professor Jafar PourMahmood numerical methods projects for root finding and equation solving. |
| `soltani_projects/` | Professor Akram Soltani operating-system projects, including dining philosophers and process profiling. |
| `tarhib_projects/` | Professor Sanaz Tarhib assignments, including Python/NumPy exercises and a PyQt RSS reader final project. |

## Languages And Tools

The repository contains projects written in several languages:

- Python for algorithms, AI, numerical methods, and application scripts.
- Rust for simulation exercises.
- C for systems programming and low-level assignments.
- Assembly for basic architecture exercises.
- HTML, CSS, and JavaScript for web-design assignments.
- Prolog for logic-programming exercises.

## Running Projects

Because each assignment is independent, run commands from the specific project directory rather than the repository root.

### Python

```bash
python3 main.py
```

Some Python projects may require extra packages. If a project includes its own dependency notes, follow those first.

### Rust

```bash
cargo run
```

Rust projects are standard Cargo packages. Build artifacts are ignored through each package's `.gitignore`.

### C

```bash
gcc main.c -o main
./main
```

Some operating-system projects may require Linux-specific headers, libraries, or elevated privileges depending on the assignment.

### Web Projects

Open the relevant `index.html` file in a browser, or serve the directory with a local static server.

```bash
python3 -m http.server
```

## Organization Notes

- Keep each assignment inside the appropriate professor or course directory.
- Add a small local README inside complex project folders when setup or execution is not obvious.
- Do not commit generated build folders such as Rust `target/`, compiled binaries, cache files, or OS metadata files.
- Prefer clear file names and simple run instructions so future readers can test projects quickly.

## Purpose

This repository is intended as a personal archive of university coursework. It should make it easy to browse past projects, run individual assignments, and preserve useful examples for later reference.
