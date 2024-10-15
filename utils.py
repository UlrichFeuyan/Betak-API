import os


def img_path(instance, filename):
    path = f"backend/{type(instance).__name__}/"
    ext = filename.split('.')[-1]
    return os.path.join(path, filename)