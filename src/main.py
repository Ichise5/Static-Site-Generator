from gencontent import *

import sys
import os


def main():
    args = sys.argv[0]
    basepath = args[0]
    if basepath not in locals() or basepath == "":
        basepath = "/"

    #print(args)
    dir_path_static = basepath+"static"
    dir_path_public = basepath+"docs"
    dir_path_content = basepath+"content"
    template_path = basepath+"template.html"

    delete_public(dir_path_public)
    copy_static(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content,template_path, dir_path_public, basepath)

main()
