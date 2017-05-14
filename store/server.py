import json

from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from store.builder import Builder
from store.portrayal import portrayCell
from store.model import Shop

with open("shop2.json") as file:
    specification = json.load(file)
    builder = Builder(specification)

    canvas_element = CanvasGrid(portrayCell, builder.dims()[0], builder.dims()[1], 500, 500)

    chart = ChartModule([{"Label": "Gini",
                          "Color": "Black"}],
                        data_collector_name='datacollector')


    server = ModularServer(Shop, [canvas_element], "Shop", specification)
    # server = ModularServer(Shop, [canvas_element,chart], "Shop", specification)



