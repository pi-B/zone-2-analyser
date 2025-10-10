from pandas import DataFrame
import seaborn as sns
from matplotlib.axes import Axes 
from matplotlib import pyplot, ticker
import logging
from time import sleep
logger = logging.getLogger(__name__)

"""
Data is constituted of 4 columns : "Allure moyenne","Durée","Fréquence cardiaque moyenne","Date"
We want to plot the data using "Date" on the x axis and "Allure moyenne" on the y axis, and color the dots from "Fréquence cardiaque moyenne"
"""

class GraphManager:

    data : DataFrame
    organised_data : Axes

    def __init__(self, data: DataFrame):
        self.data = data

    def create_graph(self):
        palette = sns.color_palette("Spectral_r", as_cmap=True)
        # palette.reversed()
        res = sns.scatterplot(data=self.data,x="Date",y=self.data["Allure moyenne"].dt.total_seconds(),hue="Fréquence cardiaque moyenne",palette=palette)
        self.organised_data = res


    def display_graph(self):
        if self.organised_data is None:
            logger.critical("Trying to display a graph without the data prepared, exiting")
            exit(0)

        pyplot.gca().yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda s, _: f"{int(s//60):02d}:{int(s%60):02d}")
        )
        pyplot.ylabel("Allure moyenne (MM:SS)")
        pyplot.show()

        pyplot.show()

12364567744

        