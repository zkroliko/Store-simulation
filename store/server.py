from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from store.portrayal import portrayCell
from store.model import Shop

canvas_element = CanvasGrid(portrayCell, 30, 30, 500, 500)

chart = ChartModule([{"Label": "Gini",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

server = ModularServer(Shop, [canvas_element,chart], "Shop",
                       30, 30)
