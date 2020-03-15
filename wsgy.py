#!/usr/bin/python
import sys
import os

project_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,project_directory)
sys.path.insert(0,os.path.join(project_directory, 'src'))
from application import app as application