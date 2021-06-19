import matplotlib.pyplot as plt


class PlotBuilder3d:
    def __init__(self):
        self.x_data = []
        self.x_label = None

        self.y_data = []
        self.y_label = None

        self.z_data = []
        self.z_label = None

        self.c_data = []
        self.c_map = 'hsv'

    def add_x_axis(self, data, label):
        self.x_data = data
        self.x_label = label

    def add_y_axis(self, data, label):
        self.y_data = data
        self.y_label = label

    def add_z_axis(self, data, label):
        self.z_data = data
        self.z_label = label

    def add_c_axis(self, data, c_map='hsv'):
        self.c_data = data
        self.c_map = c_map

    def build(self):
        ax = plt.axes(projection='3d')
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        ax.set_zlabel(self.z_label)
        ax.scatter3D(self.x_data, self.y_data, self.z_data, c=self.c_data, cmap=self.c_map)
