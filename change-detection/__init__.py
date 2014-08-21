# -*- coding: utf-8 -*-

# __init__.py
# Visual Cognitive Neuroscience Lab
# Brock University
#
# Created by Thomas Nelson on 2013-10-24
#
# This library was developed for use by the Visual Cognitive
# Neuroscience Lab at Brock University.

"""A set of color change detection tasks.

"""

# Version info for program
__version__='1.0.0'
__license__='MIT'
__author__='Thomas Nelson'
__author_email__='tn90ca@gmail.com'
__url__='http://www.tnelson.ca/change-detection'
__downloadUrl__='https://github.com/Chippers255/change-detection'

# Import all files and functions into the module
__all__ = ['trial', 'standard_trial', 'subject']

# Deprecated to keep older scripts who import this from breaking
from trial import *
from standard_trial import *
from subject import *change-detection