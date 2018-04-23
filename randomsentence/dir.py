"""
Defines ROOT as project_name/project_name/. Useful when installing using pip/setup.py.
"""

import os
import inspect

ROOT = os.path.abspath(os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename))


def database_path(database):
    return os.path.join(ROOT, 'database', database)
