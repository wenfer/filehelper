import io
import os
import shutil
from pathlib import Path
from yaml import load, Loader

from inotifyrecursive import INotify, flags


class Rule:
    name: str
    dir: str
    move_to: str
    extensions: list

    def __init__(self, rule):
        self.move_to = os.path.expandvars(rule.get('move_to'))
        self.extensions = rule.get('extensions')
        self.name = rule.get('name')

    def match(self, path):
        for ext in self.extensions:
            if path.is_file():
                if path.suffix == ext:
                    return True
        return False


class Watcher:
    name: str
    dirs: list
    rules: list

    def __init__(self):
        stream = io.open("config.yaml", "r")
        config = load(stream, Loader)
        self.name = config.get("name")
        self.dirs = config.get("dirs")
        rules = config.get("rules")
        self.rules = [Rule(rule) for rule in rules]

    def start(self):
        with INotify() as inotify:
            for d in self.dirs:
                path = os.path.expandvars(d)
                inotify.add_watch_recursive(path, flags.CREATE)
                print(f"watching {d}")
            while True:
                for event in inotify.read():
                    for rule in self.rules:
                        try:
                            path = Path(Path(inotify.get_path(event.wd)) / Path(event.name))
                            if rule.match(path):
                                print(f'{rule.name} matched :{path} , file moved to {rule.move_to}')
                                shutil.move(path, rule.move_to)
                        except BaseException as e:
                            print(e)
                            continue


if __name__ == '__main__':
    Watcher().start()
