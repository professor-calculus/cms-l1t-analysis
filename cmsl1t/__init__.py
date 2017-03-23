from __future__ import absolute_import
import os
import sys
import logging

__version__ = '0.0.1'


if 'PROJECT_ROOT' not in os.environ:
    print("Could not find environmental variable 'PROJECT_ROOT'")
    print("You need to run 'source bin/env.sh' first!")
    sys.exit(-1)
PROJECT_ROOT = os.environ['PROJECT_ROOT']

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# add loggers
ch = logging.StreamHandler()
if not os.environ.get("DEBUG", False):
    ch.setLevel(logging.ERROR)
else:
    ch.setLevel(logging.DEBUG)
# log format
formatter = logging.Formatter(
    '%(asctime)s [%(name)s]  %(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
