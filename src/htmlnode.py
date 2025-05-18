
class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("function to_html is not implemented for class HTMLNode")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for key in self.props:
            props_html += f' {key}="{self.props[key]}"'
        return props_html
    
    def __repr__(self):
        to_print = [f"This is current tag: {self.tag}",
                    f"This is current value: {self.value}",
                    f"This is current children: {self.children}",
                    f"This is current props: {self.props}"]
        return("\n".join(to_print))
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props= props)

        
    def to_html(self):
        if self.value is None:
            raise ValueError ("value is not specified")
        
        if not self.tag:
            return self.value
        
        if self.tag == "img":
            return f"<{self.tag}{super().props_to_html()}>"
        
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag = tag, children = children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError ("tag has not been specified")
        if not self.children:
            raise ValueError ("children have not been specified")
        
        string_agreg = ""
        for child in self.children:
            string_agreg += child.to_html()
            
        return f"<{self.tag}{super().props_to_html()}>{string_agreg}</{self.tag}>"