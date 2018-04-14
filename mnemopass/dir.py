import os
import inspect

ROOT = os.path.abspath(os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename))


def wordnet_path(filename):
    return os.path.join(ROOT, 'database', 'wordnet', filename)


def database_path(filename):
    return os.path.join(ROOT, 'database', filename)
