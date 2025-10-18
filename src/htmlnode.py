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
