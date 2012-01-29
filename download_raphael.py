#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
from download_and_zip import *

# Download raphael js
os.chdir("js")
f = download_file(url_raphael)
os.chdir("..")

