#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)

def removeFilesCaseSensitive(patterns_list):
    files_list = []
    for f in [name for pattern in patterns_list for name in glob.glob(pattern)]:
        print f
        os.remove(f)
        files_list.append(f)
    if len(files_list) == 0:
        s = "No file to suppress"
    elif len(files_list) == 1:
        s = "Suppressed file is " + files_list[0]
    else:
        s = "Suppressed files are :\n" + "\n".join(files_list)
    print s

def regexListMatchCaseInsensitive(filename, regex_list):
    for regex in regex_list:
        compiled_regex = re.compile(fnmatch.translate(regex), re.IGNORECASE)
        if compiled_regex.match(filename):
            val = True
            break
        else:
            val = False
    return val

def listFilesCaseInsensitive(path, regex_list = ""):
    lists = []
    for dir_name, sub_dirs, files in os.walk(path):
        #exclude git and svn files
        if ".git" not in dir_name and ".svn" not in dir_name:
            for file in files:
                absolute_path = os.path.join(dir_name, file)
                # if no regex return list of files
                if regex_list == "":
                    lists.append(absolute_path)
                else:
                #Match regex
                    if regexListMatchCaseInsensitive(file, regex_list):
                        lists.append(absolute_path)
    return lists

files_to_delete = listFilesCaseInsensitive(os.getcwd(), patterns_list)

print files_to_delete

for file in files_to_delete: os.remove(file)

# delete dirs
import shutil

for dir in dirs_to_delete:
    if os.path.isdir(dir):
        shutil.rmtree(dir)

