import os
import shutil
from markdown_blocks import markdown_to_html_node


def delete_public(path: str) -> None:
    if not os.path.exists(path):
        return
    for item in os.scandir(path):
        if item.is_dir():
            delete_public(item.path)
            #print("removing directory "+item.name)
            os.rmdir(item.path)
        else:
            #print("removing file "+item.name)
            os.remove(item.path)

def copy_static(static:str, public: str) -> None:
    #print(static)
    for item in os.scandir(static):
        if item.is_dir():
            #print("Making directory of path \n" + item.name + "\n in public")
            os.mkdir(item.path.replace(static,public))
            copy_static(item.path, item.path.replace(static,public))
        else:
            #print("Copying fil of path \n" + item.name + "\n to public")
            shutil.copy(item.path, item.path.replace(static, public))

def extract_title(markdown:str)->str:
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("there is no header in the first line")

def generate_page(from_path:str, template_path:str, dest_path:str, basepath:str):
    print(f"Generating pages from {from_path} to {dest_path} using {template_path}")
    with open(from_path,'r') as f:
        markdown = f.read()
    with open(template_path,'r') as f:
        template = f.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace(r'href="/', f'href="{basepath}')
    template = template.replace(r'src="/', f'src="{basepath}')

    with open(dest_path,'w') as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files = os.scandir(dir_path_content)

    for file in files:
        if file.is_dir():
            os.mkdir(os.path.join(dest_dir_path, file.name))
            generate_pages_recursive(os.path.join(dir_path_content, file.name),
                                     template_path,
                                     os.path.join(dest_dir_path, file.name),
                                     basepath)
        else:
            generate_page(os.path.join(dir_path_content, file.name),
                                        template_path,
                                        os.path.join(dest_dir_path, file.name.replace('.md', '.html')),
                                        basepath)