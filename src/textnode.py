from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url= None):
        if not isinstance(text_type, TextType):
            raise ValueError("text_type must be an instance of TextType enum")
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, node):
        return self.text == node.text and self.text_type == node.text_type and self.url == node.url
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case (TextType.TEXT):
            return LeafNode(None, text_node.text)
            
        case (TextType.BOLD):
            return LeafNode("b", text_node.text)
            
        case (TextType.ITALIC):
            return LeafNode("i", text_node.text)
            
        case (TextType.CODE):
            return LeafNode("code", text_node.text)
            
        case (TextType.LINK):
            return LeafNode("a", text_node.text, {"href": text_node.url})
            
        case (TextType.IMAGE):
            return LeafNode("img", "", {"src":text_node.url, "alt": text_node.text})

        case _:
                raise Exception("Text node is of unknown type")    
    