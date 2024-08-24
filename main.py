#
#   author:qiuyuan
#
#
import io
import os
import re
import shutil
import sys
from pathlib import Path
from yaml import load, Loader

from inotifyrecursive import INotify, flags


class Rule:
    name: str
    base: list
    rm_dir_if_empty: bool
    recursion: bool
    move_to: str
    suffixes: list
    regulars: list
    rename: list

    def __init__(self, rule, base):
        self.move_to = os.path.expandvars(rule.get('move_to'))
        self.suffixes = rule.get('suffixes')
        self.name = rule.get('name')
        self.rm_dir_if_empty = rule.get('rm_dir_if_empty')
        self.rm_ignore = rule.get('rm_ignore')
        self.recursion = rule.get('recursion')
        self.base = base.copy()
        self.base.append('/')  # 防止死循环
        self.overwrite = rule.get('overwrite')
        self.regulars = rule.get('regulars')
        self.rename = rule.get('rename')

    def handle(self, path):
        if self.__match(path):
            print("matched")
            self.__move(path, self.__rename(path.name))

    def __rm_ignore_match(self, name):
        if len(self.rm_ignore) > 0:
            for r in self.rm_ignore:
                if r in name:
                    return True

    def __rm_dir(self, path):
        if self.rm_dir_if_empty:
            dir_path = path.parent
            if str(dir_path) not in self.base:
                scandir = os.scandir(dir_path)
                for f in scandir:
                    if not self.__rm_ignore_match(f.name):
                        print(f"当前文件夹不为空，存在文件{f.name}，不做删除")
                        return
                dir_path.rmdir()
                print(f"delete dir : {dir_path}")

    def __move(self, path, new_name):
        if self.move_to is None:
            print("未定义目标目录")
            return
        new_path = os.path.join(self.move_to, new_name)
        if not self.overwrite:
            suffix = path.suffix
            i = 0
            while os.path.exists(new_path):
                i += 1
                print(f" 路径 {new_path} 已存在，生成新路径")
                new_path = os.path.join(self.move_to, f"{new_name.split(suffix)[0]}-({i}){suffix}")
        print(f"{path}  move to {new_path}")
        shutil.move(path, new_path)
        self.__rm_dir(path)

    def __match_suffixes(self, path):
        if self.suffixes is None:
            return True
        for ext in self.suffixes:
            if path.is_file():
                if path.suffix == ext:
                    return True
        return False

    def __match_regulars(self, path):
        if self.regulars is None:
            return True
        for regular in self.regulars:
            if re.search(regular, path.name):
                return True
        return False

    def __rename(self, name):
        if self.rename is None:
            return name
        new_name = name
        for rule in self.rename:
            new_name = new_name.replace(rule['ori'], rule['new'])
        return new_name

    def __match(self, path):
        return self.__match_suffixes(path) and self.__match_regulars(path)


class Watcher:
    name: str
    dirs: list = []
    rules: list
    startup: bool

    def __init__(self):
        stream = io.open(yaml_path, "r")
        config = load(stream, Loader)
        self.name = config.get("name", "no name")
        self.startup = config.get("startup", False)
        dirs = config.get("dirs")
        if len(dirs) == 0:
            raise Exception("未配置目录")
        for d in dirs:
            d = os.path.expandvars(d)
            if not os.path.exists(d):
                raise Exception(f"目录:{d} 不存在")
            self.dirs.append(d)
        rules = config.get("rules")
        self.rules = [Rule(rule, self.dirs) for rule in rules]

    def __handle_rule(self, path):
        for rule in self.rules:
            rule.handle(path)

    def __scan_dir(self, directory):
        scandir = os.scandir(directory)
        for f in scandir:
            path = Path(f)
            if path.is_dir():
                self.__scan_dir(path)
            else:
                self.__handle_rule(path)

    def start(self):
        if self.startup:
            print("配置了startup，立即开始扫描目录")
            for d in self.dirs:
                print(f"正在扫描目录 {d}")
                self.__scan_dir(Path(d))
        print("立即处理逻辑结束，开始监听目录")
        with INotify() as inotify:
            for path in self.dirs:
                inotify.add_watch_recursive(path, flags.CREATE)
                print(f"watching {path}")
            while True:
                for event in inotify.read():
                    path = Path(Path(inotify.get_path(event.wd)) / Path(event.name))
                    try:
                        self.__handle_rule(path)
                    except BaseException as e:
                        print(e)
                        continue


if __name__ == '__main__':
    if len(sys.argv) == 1:
        yaml_path = "config.yaml"
    else:
        yaml_path = sys.argv[1]
    Watcher().start()
