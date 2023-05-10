import matplotlib.pyplot as plt
import pandas as pd

from sql_controller import SQLController

class MapPlotter():
    """ A simple clas for plotting the drones historical path and heading, as well as velocity
        This node is only hard coded to work in the bounding box lat: 63.3321, 63.3021 lon: 10.2490, 10.3255"""
    
    def __init__(self):
        self.sql_controller = SQLController()
        self.BBox = (10.26737, 10.27694, 63.31924, 63.32299)
    
        self.VELOCITY_CM = [(5, 'b'), (10, 'g'), (15, 'y'), (20, 'r'), (25, 'm')]
        
    
    def get_colour(self, int):
        for entry in self.VELOCITY_CM:
            if int < entry[0]:
                return entry[1]
            
        return 'k'
        
    def plot_history(self, flight_id: int, plot_velocity=False):
        query = f"""
        SELECT *
        FROM wgs84
        WHERE flight_key = {flight_id};
        """
        
        result: pd.DataFrame = self.sql_controller.pull(query)
        
        colours = 'b'
        if plot_velocity:
            velocities = result[6]
            colours = list(map(lambda x : self.get_colour(x), velocities))
        
        img = plt.imread("src/plotter/plotter/maps/map.png")
        fig, ax = plt.subplots(figsize = (8,7))
        ax.scatter(result[3], result[2], zorder=1, alpha= 0.2, c =colours , s=10)
        ax.set_title('Demo plot')
        ax.set_xlim(self.BBox[0],self.BBox[1])
        ax.set_ylim(self.BBox[2],self.BBox[3])
        ax.imshow(img, zorder=0, extent = self.BBox, aspect= 'equal')
        plt.show()
    
        
        
# Test

mp = MapPlotter()
mp.plot_history(350581, plot_velocity=True)
        
