# Compiler Design

Compiler design coursework for Professor Jalil Ghavidel.

## Projects

| Directory | Description |
| --- | --- |
| `dolme/` | Dolme programming language and compiler project. |

`dolme/` is linked as a separate Git repository through a Git submodule. See `dolme/README.md` for build, usage, testing, and project-layout details.

## Submodule Notes

When cloning this repository, initialize submodules with:

```bash
git submodule update --init --recursive
```

To update the Dolme project to a newer commit, update it inside `dolme/`, then commit the submodule pointer from the parent repository.
