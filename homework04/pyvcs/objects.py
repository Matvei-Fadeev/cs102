import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    encoded_data = (fmt + " " + str(len(data))).encode()
    sha = hashlib.sha1(encoded_data + b"\0" + data).hexdigest()
    if write:
        path = repo_find()
        if not (path / "objects" / sha[:2]).exists():
            (path / "objects" / sha[:2]).mkdir()
        with open(path / "objects" / sha[:2] / sha[2:], "wb") as file:
            file.write(zlib.compress((fmt + " " + str(len(data))).encode() + b"\0" + data))
    return sha


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    list = []
    if len(obj_name) < 5 or len(obj_name) > 39:
        raise Exception(f"Not a valid object name {obj_name}")
    first_dir = (gitdir / "objects").glob("*")
    for i in first_dir:
        second_dir = i.glob("*")
        for j in second_dir:
            full_name = j.parent.name + j.name
            if obj_name == full_name[:len(obj_name)]:
                list.append(full_name)
    if not list:
        raise Exception(f"Not a valid object name {obj_name}")
    return list


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    return resolve_object(obj_name, gitdir)[0]


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    with open(gitdir / "objects" / sha[:2] / sha[2:], "rb") as f:
        undecompressed_data = zlib.decompress(f.read())
    result_list = []
    tmp = undecompressed_data.find(b" ")
    result_list.append(undecompressed_data[:tmp].decode("ascii"))
    tmp = undecompressed_data.find(b"\x00")
    result_list.append(undecompressed_data[tmp + 1:])
    return result_list


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    tree = []

    while data:
        sha_index = data.index(b"\00")
        mode, name = map(lambda x: x.decode(), data[:sha_index].split(b" "))
        sha = data[sha_index + 1: sha_index + 21]
        tree.append((int(mode), name, sha.hex()))
        data = data[sha_index + 21:]
    return tree


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    info = read_object(obj_name, gitdir)
    if info[0] == "commit" or info[0] == "blob":
        print(info[1].decode())
    else:
        for tree in read_tree(info[1]):
            if tree[0] == 40000:
                print(f"{tree[0]:06}", "tree", tree[2] + "\t" + tree[1])
            else:
                print(f"{tree[0]:06}", "blob", tree[2] + "\t" + tree[1])


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    fmt, data = read_object(tree_sha, gitdir)
    tree = read_tree(data)
    result_files = []
    for index in tree:
        if index[0] != 100644:
            l1 = find_tree_files(index[2], gitdir)
            for k in l1:
                result_files.append((index[1] + '/' + k[0], k[1]))
        else:
            result_files.append((index[1], index[2]))
    return result_files


def commit_parse(raw: bytes, start: int = 0, dct=None):
    result = tp.Dict[str, tp.Any]
    for i in map(lambda x: x.decode(), raw.split(b"\n")):
        if "tree" in i or "parent" in i or "author" in i or "committer" in i:
            name, value = i.split(" ", maxsplit=1)
            result[name] = value
        else:
            result["message"].append(i)
    return result
