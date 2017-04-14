import os
from ..config import root_dir


def replace_all(text, dic):
    """
    Search and replace
    """
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


def gen_start_urls(url, keywords, replace_whitespice=None):
    """
    Builds start_urls for spider according to keywords
    """
    start_urls = []
    for keyword in keywords:
        if replace_whitespice:
            keyword = replace_all(keyword, {' ': replace_whitespice})
        start_urls.append(url % keyword)
    return start_urls


def read_motivation(user):
    """
    Read Motivation.txt and return text format
    """
    motiv_file = user + ' Motivation.txt'
    file_path = os.path.join(root_dir, 'data', motiv_file)

    with open(file_path, 'r') as content_file:
        Motivation = content_file.read()

    Motivation = Motivation.decode("utf-8")
    return Motivation


def set_clipboard(text):
    """
    Set the Clipboard to the specified string

    """
    from Tkinter import Tk
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.destroy()
