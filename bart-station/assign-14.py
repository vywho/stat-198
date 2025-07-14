""" Visualization of average weekday BART ridership data from January 2024. 

Assignment 14 submission for Stat 198: Interactive Data Science course at UC Berkeley. 

Author: Vy Ho
License: BSD-3-Clause
"""

from sketchingpy import Sketch2D
import pandas as pd

STATION_DATA = 'stations.csv'
BAYAREA = 'bayarea.geojson'
WEEKDAY1 = 'weekday-data/weekday1.csv'
LAND_COLOR  = '#c0c8ca'
STATION_COLOR = '#88e6fd'
BACKGROUND_COLOR = '#F0F0FF'

RIDER_COLORS = ['#ffffcc',
                '#a1dab4',
                '#41b6c4',
                '#2c7fb8',
                '#253494']

# Page dimensions
WIDTH = 1000 
LENGTH = 1000
CENTER_X = WIDTH // 2
CENTER_Y = LENGTH // 2
MAP_SCALE = 85

# Center of map, San Mateo + a litle further north
CENTER_LAT = 37.6500
CENTER_LONG = -122.2047
STATION_WIDTH = 10

LEGEND_HEIGHT = 200
LEGEND_WIDTH = 180
LEGEND_LEFT = 10
LEGEND_BOTTOM = 300
BOX_WIDTH = 20
BOX_HEIGHT = 10

FONT = 'fonts/PublicSans-Regular.otf'
DARK_TEXT_COLOR = '#000000'

class Stations: 
    """Combines ridership data across stations for January 2024"""
    def __init__(self): 
        """Formats ridership data and creates the corresponding bins and a dictionary mapping stations to its corresponding data. """
        self.df = pd.read_csv(STATION_DATA) 

        # Formatting Ridership data
        data = pd.read_csv(WEEKDAY1)
        data = data.drop(index=0)
        data = data[[data.columns[0], data.columns[-1]]]
        data = data.rename(columns = {
            data.columns[0]: 'code', 
            data.columns[1]: 'Total Avg Weekday'
        })
        print(data)
        data['Total Avg Weekday'] = data['Total Avg Weekday'].str.replace(',', '').astype(int)
        
        # Merging dfs together
        self.df = pd.merge(self.df, data, on='code', how='inner')

        # Bins for legend, bins are equal countwise 
        bins = pd.qcut(data['Total Avg Weekday'], q=5)
        bins = list(bins.unique())
        self.bins = sorted([int(x.right) for x in bins])

        # Dict mapping station coordinate range to station name, avg ridership data
        self.station_loc = {}
        for index, row in self.df.iterrows(): 
            name = row['name']
            avg = row['Total Avg Weekday']
            lat = row['latitude']
            long = row['longitude']
            self.station_loc[(long, lat)] = [name, avg]

class Graphic: 
    """Main class that draws all components for the BART graphic."""
    
    def __init__(self, stations):
        self._sketch = Sketch2D(WIDTH, LENGTH)
        self.stations = stations
 
    def draw(self):
        """Draws the map, converts the station data, and draws the interactive graphic."""
        self.draw_map()
        self.station_to_pixels()
        self._sketch.on_step(lambda x: self.draw_allparts())

        self._sketch.show()

    def draw_allparts(self): 
        """Draws each component of the graphic."""
        self.draw_map()
        self.draw_stations()
        self.draw_legend()
        self.draw_title()
        self.interactive_station()

    def draw_map(self):
        """Draws the background map."""
        # Set center coordinates of on map
        self._sketch.set_map_pan(CENTER_LONG, CENTER_LAT) 
        self._sketch.set_map_zoom(MAP_SCALE)  
        self._sketch.set_map_placement(CENTER_X, CENTER_Y)  

        self._sketch.clear(BACKGROUND_COLOR)
        
        # Load Bay Area map and draws outline
        data_layer = self._sketch.get_data_layer()
        geojson = data_layer.get_json(BAYAREA)
        geo_polgyons = self._sketch.parse_geojson(geojson)
        
        geo_polgyon = geo_polgyons[0]
        shape = geo_polgyon.to_shape()
        
        self._sketch.set_fill(LAND_COLOR)
        self._sketch.clear_stroke()
        self._sketch.draw_shape(shape)

    def draw_stations(self): 
        """Draws each station on the map and colors it according to its data."""
        self._sketch.push_map()
        self._sketch.push_style()
        self._sketch.push_transform()

        self._sketch.clear_stroke()
        self._sketch.set_ellipse_mode('center')

        dt = self.stations.df
        for _, row in dt.iterrows(): 
            rider = row['Total Avg Weekday']
            for i in range(len(RIDER_COLORS)): 
                if rider <= self.stations.bins[i]: 
                    self._sketch.set_fill(RIDER_COLORS[i])
                    break    

            long, lat = row['longitude'], row['latitude']
            x, y = self._sketch.convert_geo_to_pixel(long, lat)
            self._sketch.draw_ellipse(x, y, STATION_WIDTH, STATION_WIDTH)

        self._sketch.pop_map()
        self._sketch.pop_style()
        self._sketch.pop_transform()
    
    def draw_legend(self): 
        """Draws the graphic legend."""
        self._sketch.push_map()
        self._sketch.push_style()
        self._sketch.push_transform()

        bins = [[self.stations.bins[i] + 1, self.stations.bins[i + 1]]for i in range(0, len(self.stations.bins) - 1)]
        bins = [[0, self.stations.bins[0]]] + bins

        # Draw legend box
        x, y = LEGEND_LEFT, LENGTH - LEGEND_BOTTOM
        self._sketch.clear_fill()
        self._sketch.set_stroke(DARK_TEXT_COLOR)
        self._sketch.set_rect_mode('corner')
        self._sketch.draw_rect(x, y, LEGEND_WIDTH, LEGEND_HEIGHT)
        
        # Draw legend title
        self._sketch.clear_stroke()
        self._sketch.set_fill(DARK_TEXT_COLOR)
        self._sketch.set_text_align('center')
        self._sketch.set_text_font(FONT, 15)
        self._sketch.draw_text((LEGEND_LEFT + LEGEND_WIDTH)/2 + 5, y + 0.75*(LEGEND_HEIGHT/6), 'Avg Weekday Ridership')

        # Draw bins and corresponding color rectangle
        self._sketch.clear_stroke()
        text_x_offset = 55
        box_x_offset = 15
        y_offset = 20

        for i in range(len(bins)): 
            self._sketch.set_fill(DARK_TEXT_COLOR)
            self._sketch.set_text_align('left')
            self._sketch.set_text_font(FONT, 15)
            self._sketch.draw_text(x + text_x_offset, y + (i + 1)*(LEGEND_HEIGHT/6) + y_offset, f'({bins[i][0]}, {bins[i][1]}]')

            self._sketch.set_fill(RIDER_COLORS[i])
            self._sketch.set_rect_mode('corner')
            self._sketch.draw_rect(x + box_x_offset, y + (i + 1)*(LEGEND_HEIGHT/6) + y_offset/2, BOX_WIDTH, BOX_HEIGHT)

        self._sketch.pop_map()
        self._sketch.pop_style()
        self._sketch.pop_transform()

    def draw_title(self): 
        """Draws the title of the graphic."""
        self._sketch.push_map()
        self._sketch.push_style()
        self._sketch.push_transform()

        self._sketch.set_fill(DARK_TEXT_COLOR)
        self._sketch.set_text_align('center')
        self._sketch.set_text_font(FONT, 30)
        self._sketch.draw_text(WIDTH//2, 45, 'January 2024 BART Average Weekday Ridership')

        self._sketch.pop_map()
        self._sketch.pop_style()
        self._sketch.pop_transform()

    def interactive_station(self): 
        """Displays the station data if the user's mouse is hovering over a station."""
        self._sketch.push_map()
        self._sketch.push_style()
        self._sketch.push_transform()
 
        mouse = self._sketch.get_mouse()
        x_coord, y_coord = mouse.get_pointer_x(), mouse.get_pointer_y()

        station_stats = self.station_stats(x_coord, y_coord)
        if station_stats: 
            name, data = station_stats[0], station_stats[1]
            print(name, data)
            self._sketch.set_fill(DARK_TEXT_COLOR)
            self._sketch.set_text_font(FONT, 20)
            self._sketch.draw_text(LEGEND_LEFT, LENGTH - LEGEND_BOTTOM - 35, f'{name} Station')
            self._sketch.draw_text(LEGEND_LEFT, LENGTH - LEGEND_BOTTOM - 5, f'Avg Weekday Riders: {data}')

        self._sketch.pop_map()
        self._sketch.pop_style()
        self._sketch.pop_transform()

    def station_to_pixels(self): 
        """Convert station geographical coordinates to pixel coordinates. Also stores the bounds of the station point."""
        station_coords = self.stations.station_loc

        # dictionary mapping pixels to the station name, weekday data
        self.station_pixels = {}
        for coords in station_coords: 
            long, lat = coords[0], coords[1]
            x, y = self._sketch.convert_geo_to_pixel(long, lat)
            x_range = (x - STATION_WIDTH/2, x + STATION_WIDTH/2)
            y_range = (y - STATION_WIDTH/2, y + STATION_WIDTH/2)
            self.station_pixels[(x_range, y_range)] = station_coords[coords]
    
    def station_stats(self, x, y):
        """Given pixel coordinates, check if the coordinates fall within a station and return the station data if so."""
        # checks if mouse is hovering over a station
        for coords in self.station_pixels: 
            if coords[0][0] <= x <= coords[0][1] and coords[1][0] <= y <= coords[1][1]: 
                return self.station_pixels[coords]
            
stations = Stations()
graphic = Graphic(stations)
graphic.draw()