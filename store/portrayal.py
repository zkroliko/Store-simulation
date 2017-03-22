def portrayCell(cell):
    '''
    This function is registered with the visualization server to be called
    each tick to indicate how to draw the cell in its current state.
    :param cell:  the cell in the simulation
    :return: the portrayal dictionary.
    '''
    assert cell is not None
    return {
        "Shape": "rect",
        "text": "c",
        "w": 1,
        "h": 1,
        "Filled": "false",
        "Layer": 0,
        "x": cell.x,
        "y": cell.y,
        "Color": "white",
        "text_color": "red"
    }
