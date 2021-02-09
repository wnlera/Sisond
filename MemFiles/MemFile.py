from datetime import datetime, timedelta
from io import BytesIO
import os

class MemFile:
    """
    Класс для хранения файлов в памяти
    """
    def __init__(self, file: BytesIO, url, name):
        self._file: BytesIO = file
        self._file.seek(0)
        # self.file = file
        self.url = url  # todo: избыточно, это хранится в менеджере
        self.name = name
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(minutes=5)
        self.__replicate_to_fs()
        # self.expires_at = self.created_at + timedelta(minutes=1)

    def wipe(self):
        del self._file
        del self.url
        del self.name
        del self.created_at

    def __replicate_to_fs(self):
        f = self.file
        folder_static = "static"
        folder_upload = "upload"
        path = os.path.join(folder_static, folder_upload)

        if not os.path.exists(folder_static):
            os.mkdir(folder_static)
        if not os.path.exists(path):
            os.mkdir(path)

        dot_pos = self.name.rfind(".")
        filename, ext = self.name[:dot_pos], self.name[dot_pos:]
        fullpath = os.path.join(path, self.name)
        if os.path.exists(fullpath):
            candidates = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            biggest_num = 0
            for candidate in candidates:
                print(candidate)
                if filename not in candidate:
                    continue
                print(candidate)
                number_pos_left = candidate.rfind("(") + 1
                number_pos_right = candidate.rfind(")")
                number = candidate[number_pos_left:number_pos_right]
                try:
                    number = int(number)
                except:
                    print(number)
                    number = 0
                if number > biggest_num:
                    biggest_num = number

            biggest_num += 1
            fullpath = os.path.join(path, filename + f"({biggest_num})" + ext)

        with open(fullpath, "wb") as fw:
            fw.write(f.getbuffer())

    @property
    def file(self) -> BytesIO:
        copyfile = BytesIO()
        self.copy_filelike_to_filelike(copyfile)
        copyfile.seek(0)

        assert not copyfile.closed, "IO is closed, which is not expected"

        return copyfile

    def copy_filelike_to_filelike(self, dst, bufsize=16384):
        while True:
            buf = self._file.read(bufsize)
            if not buf:
                break
            dst.write(buf)
        self._file.seek(0)

    @property
    def expired(self) -> bool:
        return datetime.now() >= self.expires_at




