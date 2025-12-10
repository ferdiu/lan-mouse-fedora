# lan-mouse RPM Spec

Build RPM package for lan-mouse on Fedora.

## Source download

```bash
spectool -g -R lan-mouse.spec
```

## Builddep

```bash
# Need root privileges
dnf builddep lan-mouse.spec
```

## Build

```bash
rpmbuild -ba lan-mouse.spec
```
