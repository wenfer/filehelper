"""
文件监控助手
new Env('filehelper');
cron: 1 * * * * ?

"""
import io
import os
import re
import shutil
import sys
from pathlib import Path
from yaml import load, Loader


class Rule:
    name: str
    base: list
    move_to: str
    suffixes: list
    regulars: list
    rename: list

    def __init__(self, rule, base):
        self.move_to = os.path.expandvars(rule.get('move_to'))
        self.suffixes = rule.get('suffixes')
        self.name = rule.get('name')
        self.base = base.copy()
        self.base.append('/')  # 防止死循环
        self.overwrite = rule.get('overwrite')
        self.regulars = rule.get('regulars')
        self.rename = rule.get('rename')

    def handle(self, path):
        if self.__match(path):
            print("matched")
            self.__move(path, self.__rename(path.name))

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
            print(regular)
            if re.search(regular, path.name):
                return True
        return False

    def __rename(self, name):
        if self.rename is None:
            return name
        new_name = name
        for rule in self.rename:
            new_name = re.sub(rule['ori'], rule['new'], name)
        return new_name

    def __match(self, path):
        return self.__match_suffixes(path) and self.__match_regulars(path)


class FileHelper:
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
        print("开始扫描目录")
        for d in self.dirs:
            print(f"正在扫描目录 {d}")
            self.__scan_dir(Path(d))
        print("立即处理逻辑结束，开始监听目录")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        yaml_path = "config.yml"
    else:
        yaml_path = sys.argv[1]
    FileHelper().start()
