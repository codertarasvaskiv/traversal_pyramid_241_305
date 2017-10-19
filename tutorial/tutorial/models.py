from persistent import Persistent
from persistent.mapping import PersistentMapping


class Wiki(PersistentMapping):
    __name__ = None
    __parent__ = None


class Page(Persistent):
    def __init__(self, data):
        self.data = data
        self.tree = dict()

    def __getitem__(self, key):
        if key in self.tree:
            return self.tree[key]
        raise KeyError


class Sentence(Persistent):
    def __init__(self, data):
        self.data = data
        self.tree = dict()

    def __getitem__(self, key):
        if key in self.tree:
            return self.tree[key]
        raise KeyError


def appmaker(zodb_root):

    if 'app_root' not in zodb_root:
        app_root = Wiki()
        frontpage = Page('This is the front page')
        frontpage.tree = dict()
        app_root['FrontPage'] = frontpage
        frontpage.__name__ = 'FrontPage'
        frontpage.__parent__ = app_root
        zodb_root['app_root'] = app_root
    return zodb_root['app_root']