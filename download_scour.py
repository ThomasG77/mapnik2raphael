from download_and_zip import *
url_scour = "http://www.codedread.com/scour/scour-0.26.zip"
file_name_scour = url_scour.split('/')[-1]
download_file(url_scour, file_name_scour)
extract(file_name_scour, ".")

