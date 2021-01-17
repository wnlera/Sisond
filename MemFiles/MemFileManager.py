from typing import Dict

from .MemFile import MemFile


class MemFileManager:
    def __init__(self):
        self.__files: Dict[str, MemFile] = {}

    def add_file(self, uuid, file: MemFile):
        self.remove_timeout_files()
        if uuid not in self.__files:
            self.__files[uuid] = file
        else:
            raise ValueError("uuid collision!")

    def get_file(self, uuid):
        self.remove_timeout_files()
        if uuid not in self.__files:
            print(f"{uuid} not found in {self.__files.keys()}")
            return None
        file = self.__files[uuid]
        return file

    def remove_timeout_files(self):
        to_remove = set()
        for uuid, file in self.__files.items():
            if file.expired:
                file.wipe()
                to_remove.add(uuid)
        if len(to_remove):
            print(f"Removed {len(to_remove)} files")
        for elem in to_remove:
            self.__files.pop(elem)
