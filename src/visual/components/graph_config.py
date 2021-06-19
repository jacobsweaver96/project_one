

class GraphConfig:
    __color_ls = [
        'red',
        'green',
        'orange',
        'purple',
        'pink',
        'indigo',
        'blue',
    ]

    def __init__(self):
        self.colors = self.__color_ls
        self.is_symmetric = False
        self.is_circle = False
        self.is_layered = False

    def with_colors(self, colors: []):
        if len(colors) == 0:
            return self
        self.colors = colors
        return self

    def with_symmetry(self, val=True):
        self.is_symmetric = val
        return self

    def as_circle(self, val=True):
        self.is_circle = val
        return self

    def as_multi_layer(self, val=True):
        if val:
            self.is_circle = False
        self.is_layered = val
        return self

    def get_color(self, index: int):
        color_len = len(self.colors)
        c_index = index % (color_len - 1)
        return self.colors[c_index]

    def get_inverse_color(self, index: int):
        color_len = len(self.colors)
        c_index = index % (color_len - 1)
        return self.colors[color_len - c_index - 1]
