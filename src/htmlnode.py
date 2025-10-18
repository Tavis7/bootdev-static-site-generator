class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag      = tag
        self.value    = value
        self.children = children
        self.props    = props

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        return ("".join(map(lambda key: f' {key}="{self.props[key]}"', self.props))
                if self.props != None else "")

    def __repr__(self):
        return ", ".join([f'HTMLNode(tag="{self.tag}"',
                          f'value="{self.value}"',
                          f'children="{self.children}"',
                          f'props={self.props})'])

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf node with no value")

        otag,ctag = "",""
        if self.tag != None:
            otag,ctag = f"<{self.tag}{self.props_to_html()}>",f"</{self.tag}>"

        return f'{otag}{self.value}{ctag}'
