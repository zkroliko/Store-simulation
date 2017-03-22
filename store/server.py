from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from store.portrayal import portrayCell
from store.model import Shop

canvas_element = CanvasGrid(portrayCell, 30, 30, 500, 500)

server = ModularServer(Shop, [canvas_element], "Shop",
                       30, 30)
