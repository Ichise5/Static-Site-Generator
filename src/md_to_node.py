from textnode import *
import re

def text_to_nodes(text:str) -> list[TextNode]:
    list_of_nodes = [TextNode(text, TextType.TEXT)]
    list_of_nodes = split_nodes_delimiter(list_of_nodes, "**", TextType.BOLD)
    list_of_nodes = split_nodes_delimiter(list_of_nodes, "_", TextType.ITALIC)
    list_of_nodes = split_nodes_delimiter(list_of_nodes, "`", TextType.CODE)
    list_of_nodes = split_nodes_image(list_of_nodes)
    list_of_nodes = split_nodes_link(list_of_nodes)
    return list_of_nodes


def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type: TextType) ->list[TextNode]:

    list_of_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            list_of_nodes.append(node)
            continue

        delim_strings = node.text.split(delimiter)
        if len(delim_strings)%2 == 0:
            raise Exception("this is not valid md syntax, formatting section is not closed")
        
        for idx, string in enumerate(delim_strings):
            if string == "":
                continue
            if idx%2 == 0:
                list_of_nodes.append(TextNode(string,TextType.TEXT))
            else:
                list_of_nodes.append(TextNode(string,text_type))

    return list_of_nodes

def extract_markdown_images(text:str)-> list[tuple]:
    regex_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex_pattern,text)
    return matches

def extract_markdown_links(text:str)->list[tuple]:
    regex_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex_pattern,text)
    return matches

def split_nodes_image(old_nodes: list[TextNode])->list[TextNode]:
    list_of_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            list_of_nodes.append(old_node)
            continue

        curr_text = old_node.text
        images = extract_markdown_images(curr_text)
        
        if not images:
            list_of_nodes.append(old_node)
            continue

        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            
            parts = curr_text.split(image_markdown, 1)

            if parts[0]:
                list_of_nodes.append(TextNode(parts[0], TextType.TEXT))

            list_of_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            if len(parts) > 1:
                curr_text = parts[1]
            else:
                curr_text = ""
        
        if curr_text:
            list_of_nodes.append(TextNode(curr_text, TextType.TEXT))

    return list_of_nodes

def split_nodes_link(old_nodes: list[TextNode])->list[TextNode]:
    list_of_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            list_of_nodes.append(old_node)
            continue

        curr_text = old_node.text
        links = extract_markdown_links(curr_text)
        
        if not links:
            list_of_nodes.append(old_node)
            continue

        for link_alt, link_url in links:
            link_markdown = f"[{link_alt}]({link_url})"
            
            parts = curr_text.split(link_markdown, 1)

            if parts[0]:
                list_of_nodes.append(TextNode(parts[0], TextType.TEXT))

            list_of_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            
            if len(parts) > 1:
                curr_text = parts[1]
            else:
                curr_text = ""
        
        if curr_text:
            list_of_nodes.append(TextNode(curr_text, TextType.TEXT))

    return list_of_nodes



