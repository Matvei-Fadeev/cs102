import hashlib
import operator
import os
import pathlib
import struct
import typing as tp
from operator import attrgetter

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        values = (
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode()
        )
        for_s_length = str(len(self.name))
        for_x_length = str(8 - (62 + len(self.name)) % 8)
        format = "!LLLLLLLLLL20sH" + for_s_length + "s" + for_x_length + "x"
        result = struct.pack(format, *values)
        return result

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        for_s_length = str(len(data) - 62)
        format = "!LLLLLLLLLL20sH" + for_s_length + "s"
        unpacked_data = struct.unpack(format, data)
        result = GitIndexEntry(*unpacked_data[:-1], unpacked_data[-1].rstrip(b'\00').decode())
        return result


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    list = []
    if not (gitdir / "index").exists():
        return []
    with open(gitdir / "index", "rb") as f:
        head = f.read(12)
        index = f.read()
    unpacked_data = struct.unpack('!L', head[8:])
    for _ in range(unpacked_data[0]):
        end = len(index) - 1
        for j in range(63, len(index), 8):
            if index[j] == 0:
                end = j
                break
        list.append(GitIndexEntry.unpack(index[:end + 1]))
        if len(index) != end - 1:
            index = index[end + 1:]

    return list


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    head = struct.pack("!4sLL", b"DIRC", 2, len(entries))
    data = b""
    for i in entries:
        data = data + GitIndexEntry.pack(i)
    sha = hashlib.sha1(head + data).digest()
    with open(gitdir / "index", "wb") as f:
        f.write(head + data + sha)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    if not details:
        list = read_index(gitdir)
        for i in list:
            print(i.name)
    else:
        list = read_index(gitdir)
        for i in list:
            data = oct(i.mode)[2:]
            print(f"{data} {i.sha1.hex()} 0\t{i.name}")


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    result = []
    for i in paths:
        list = os.stat(i)
        with open(i, "rb") as f:
            data = f.read()
        sha = hash_object(data, "blob", True)
        result.append(

            GitIndexEntry(
                int(list.st_ctime),
                (int(str(list.st_ctime_ns)[-1])),
                int(list.st_mtime),
                int(str(list.st_mtime_ns)[-1]),
                list.st_dev,
                list.st_ino,
                list.st_mode,
                list.st_uid,
                list.st_gid,
                list.st_size,
                bytes.fromhex(sha),
                7,
                str(i).replace('\\', '/'),
            )

        )
    if write:
        result.sort(key=lambda x: x[-1])
        write_index(gitdir, result)
