import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    with open(gitdir / ref, "w") as file:
        file.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    with open(gitdir / name, "w") as file:
        file.write(ref)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD" and not is_detached(gitdir):
        return resolve_head(gitdir)
    if (gitdir / refname).exists():
        with open(gitdir / refname) as file:
            return file.read()


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    if is_detached(gitdir):
        with open(gitdir / "HEAD", "r") as file:
            return file.read()
    else:
        return ref_resolve(gitdir, get_ref(gitdir))


def is_detached(gitdir: pathlib.Path) -> bool:
    with open(gitdir / "HEAD", "r") as file:
        return len(file.read()) == 40


def get_ref(gitdir: pathlib.Path) -> str:
    with open(gitdir / "HEAD") as file:
        result = file.read()
    if result[:5] == "ref: ":
        result = result[5:-1]
    return result
