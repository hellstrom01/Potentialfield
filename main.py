from potential import Potential, Visualize
import pygame



if __name__ == "__main__":
    fields = Potential()
    fields.create_map()
    visualizer = Visualize(fields)
    visualizer.draw_map()