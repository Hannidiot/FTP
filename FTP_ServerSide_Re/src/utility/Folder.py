"""
    In this file, some utilities of folder is encapsulated
"""
import os
import time

__all__ = ["listdir_by_order", "get_folder_info"]


def listdir_by_order(path, show_hide=True):
    """
        The function is to sort all elements in folder

    :param path: the folder path
    :param show_hide: whether hidden file or package is shown
    :return: list of folder first ordered by alphabetical order
    """
    if not os.path.isdir(path):
        raise NotADirectoryError

    info = [x for x in os.listdir(path) if not x.startswith('.')] if show_hide else os.listdir(path)
    file_list = []
    folder_list = []
    for i in info:
        if os.path.isfile(i):
            file_list.append(i)
        else:
            folder_list.append(i)
    folder_list = sorted(folder_list)
    file_list = sorted(file_list)
    return folder_list + file_list


def get_folder_info(path):
    """
        The function will return a list of tuple including
            name,
            type,
            size(if isfile),
            modified time(if isfile)

    :param path: the folder path
    :return: one list of file info tuple
    """
    if not os.path.isdir(path):
        raise NotADirectoryError

    info = listdir_by_order(path)
    result = []
    for i in info:
        if os.path.isfile(i):
            result.append((
                i,
                'file',
                os.path.getsize(i),
                time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(i)))
            ))
        else:
            result.append((i, 'folder'))
    return result

if __name__ == "__main__":
    print(get_folder_info("."))
