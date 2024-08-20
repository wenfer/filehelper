import io
import os
from pathlib import Path
from yaml import load, dump, Loader
from asyncinotify import Inotify, Mask
import asyncio


class Rule:
    name: str
    dir: str
    move_to: str
    extensions: list

    def __init__(self, rule):
        self.dir = rule.get('dir')
        self.move_to = rule.get('move_to')
        self.extensions = rule.get('extensions')
        self.name = rule.get('name')


class Watcher:
    name: str
    rules: list

    def __init__(self):
        # {'name': 'test', 'rules': [{'name': 'movie', 'dir': '${HOME}/Downloads', 'move_to': '${HOME}/Movie', 'extensions': ['.mp4', '.mkv']}]}
        stream = io.open("config.yaml", "r")
        config = load(stream, Loader)
        self.name = config.get("name")
        rules = config.get("rules")
        self.rules = [Rule(rule) for rule in rules]

    async def start(self):
        with Inotify() as inotify:
            for rule in self.rules:
                path = os.path.expandvars(rule.dir)
                inotify.add_watch(path, Mask.MODIFY | Mask.CREATE)
                print(f"watching {path}")
            # Iterate events forever, yielding them one at a time
            async for event in inotify:
                # Events have a helpful __repr__.  They also have a reference to
                # their Watch instance.
                print(event)

                # the contained path may or may not be valid UTF-8.  See the note
                # below
                print(repr(event.path.suffix))


if __name__ == '__main__':
    asyncio.run(Watcher().start())
