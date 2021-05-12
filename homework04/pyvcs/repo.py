import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    if "GIT_DIR" in os.environ:
        env = os.environ["GIT_DIR"]
    else:
        env = ".pyvcs"
    path = pathlib.Path(workdir)
    path = path.absolute()
    tmp_count = 0
    for dir_path, dir_names, filenames in os.walk(path):
        for i in dir_names:
            a = os.path.join(dir_path, i)
            if i == env:
                return pathlib.Path(a)
    list = os.path.dirname(path)
    while len(str(list)) > 1:
        dirs = os.listdir(list)
        if env in dirs:
            a = os.path.join(list, env)
            return pathlib.Path(a)
        list = os.path.dirname(list)
    if tmp_count == 0:
        raise AssertionError("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    list = os.environ["GIT_DIR"] if "GIT_DIR" in os.environ else ".pyvcs"
    path = pathlib.Path(workdir)

    if path.is_file():
        raise Exception(f"{path} is not a directory")
    os.mkdir(list)
    with open(path / list / "HEAD", "w") as file:
        file.write("ref: refs/heads/master\n")
    with open(path / list / "config", "w") as file:
        file.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
    with open(path / list / "description", "w") as file:
        file.write("Unnamed pyvcs repository.\n")
    (path / list / "objects").mkdir()
    (path / list / "refs").mkdir()
    (path / list / "refs" / "tags").mkdir()
    (path / list / "refs" / "heads").mkdir()
    return path / list
