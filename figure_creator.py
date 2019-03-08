import base64
import io

from matplotlib import pyplot as plt


class FigureCreator:

    def __init__(self):
        plt.grid()

    @staticmethod
    def create_figure(plots):
        """
        Create a figure for given plots.
        :param plots: list of (x_axis, y_axis)
        :return:
        """
        img = io.BytesIO()
        fig = plt.figure()
        plt.grid()
        axis = fig.add_subplot(1, 1, 1)
        for plot in plots:
            x_axis, y_axis = plot
            axis.plot(x_axis, y_axis)
        plt.savefig(img, format='png')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()
