from download_and_zip import *

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)

file_name_scour = url_scour.split('/')[-1]
download_file(url_scour, file_name_scour)
extract(file_name_scour, ".")

