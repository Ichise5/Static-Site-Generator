from gencontent import *

import sys
import os


dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]



    delete_public(dir_path_public)
    copy_static(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content,template_path, dir_path_public, basepath)

main()
