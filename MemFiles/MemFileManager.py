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
            return None
        file = self.__files[uuid]
        file.file.seek(0)
        return file

    def remove_timeout_files(self):
        to_remove = set()
        for uuid, file in self.__files.items():
            if file.expired:
                file.wipe()
                to_remove.add(uuid)
        for elem in to_remove:
            self.__files.pop(elem)
