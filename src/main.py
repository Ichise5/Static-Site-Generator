from gencontent import *

import os





def main():
    dir_path_static = "./static"
    dir_path_public = "./public"
    dir_path_content = "./content"
    template_path = "./template.html"

    delete_public(dir_path_public)
    copy_static(dir_path_static)
    generate_pages_recursive(dir_path_content,template_path, dir_path_public)

main()
