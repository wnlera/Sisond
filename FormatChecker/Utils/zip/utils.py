from zipfile import ZipFile


def get_inner_file(file, inner_paths: dict, inner_path=None):
    if not inner_paths:
        inner_paths = {"file": inner_path}
    with ZipFile(file, 'r') as z:
        for name, path in inner_paths.items():
            # if path is None or name is None:
            #     inner_paths[name] = None
            #     continue
            inner_paths[name] = z.read(path)
    z.close()
    return inner_paths





