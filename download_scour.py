from download_and_zip import *

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)

f = download_file(url_scour)
extract(f, ".")

