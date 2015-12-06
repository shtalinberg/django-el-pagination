#!/usr/bin/env python

from __future__ import unicode_literals
import os
import sys

from django.core.management import execute_from_command_line


if __name__ == '__main__':
    root = os.path.join(os.path.dirname(__file__), '..')
    sys.path.append(os.path.abspath(root))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    execute_from_command_line(sys.argv)
