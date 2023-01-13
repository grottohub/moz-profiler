import json
import os
import sys

from pathlib import Path


class Storage:
    def __init__(self):
        home = Path.home()
        self.path = os.path.abspath(f"{home}/.moz-profiler-config.json")
        if not os.path.exists(self.path):
            Path(self.path).touch()
            print(self.path)
            with open(self.path, "w") as store:
                store.write("{}")

    def load(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path) as raw_data:
                stored_data = json.load(raw_data)
                return stored_data

        return {}

    def store(self, data: dict):
        stored_data = self.load()

        for key in data.keys():
            stored_data[key] = data[key]

        with open(self.path, "w") as raw_data:
            json.dump(stored_data, fp=raw_data)

    def get(self, key: str):
        data = self.load()
        return data.get(key)


storage = Storage()

if __name__ == "__main__":
    if sys.argv[1] == "get":
        print(storage.get(sys.argv[2]))
