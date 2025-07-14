"""Interactive visualization of average weekday BART ridership data from 2024. 

Assignment 15 submission for Stat 198: Interactive Data Science course at UC Berkeley. 

Author: Vy Ho
License: BSD-3-Clause
"""
from sketchingpy import Sketch2D
import pandas as pd

STATION_DATA = 'stations.csv'
BAYAREA = 'bayarea.geojson'
LAND_COLOR  = '#c0c8ca'
STATION_COLOR = '#88e6fd'
BACKGROUND_COLOR = '#F0F0FF'
MONTHS = 12

RIDER_COLORS = ['#ffffcc',
                '#a1dab4',
                '#41b6c4',
                '#2c7fb8',
                '#253494']

NUM_TO_MONTH = {1: 'Jan', 
                2: 'Feb', 
                3: 'Mar', 
                4: 'Apr', 
                5: 'May', 
                6: 'June', 
                7: 'July', 
                8: 'Aug', 
                9: 'Sep', 
                10: 'Oct',
                11: 'Nov', 
                12: 'Dec'}

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
BORDER_WEIGHT = 2

LEGEND_HEIGHT = 200
LEGEND_WIDTH = 180
LEGEND_LEFT = 10
LEGEND_BOTTOM = 300
BOX_WIDTH = 20
BOX_HEIGHT = 10

TITLE_Y = 45
BUTTON_HEIGHT = 33
BUTTON_X = LEGEND_LEFT*2 + LEGEND_WIDTH
BUTTON_Y = 915
INSTR_X = WIDTH - 425
INSTR_Y = 275


FONT = 'fonts/PublicSans-Regular.otf'
DARK_TEXT_COLOR = '#000000'

class Stations: 
    """Combines and compiles ridership data across stations for 2024"""
    def __init__(self): 
        """
        Create dataframes for the stations and the monthly weekday information.
        """

        self.df = pd.read_csv(STATION_DATA) 

        # Removing duplicate row 
        i = self.df[(self.df.code == 'CL')].index
        self.df.drop(i._data[0], inplace=True)

        self.df.set_index('code', inplace=True)
        min_avg = float('inf')
        max_avg = float('-inf')
        for i in range(1, MONTHS + 1): 
            data = pd.read_csv(f'weekday-data/weekday{i}.csv')
            data = data.drop(index=0) # Drop first row titled Avg Weekday
            data = data[[data.columns[0], data.columns[-1]]] # Grab station title and total avg weekday
            
            # Rename columns
            data = data.rename(columns ={
                data.columns[0]: 'code', 
                data.columns[1]: f'{i} Avg Weekday'
            })
            # Remove commas and change data type 
            print(data)
            data[f'{i} Avg Weekday'] = data[f'{i} Avg Weekday'].str.replace(',', '').astype(int)

            min_avg = min(min_avg, data[f'{i} Avg Weekday'].min())
            max_avg = max(max_avg, data[f'{i} Avg Weekday'].max())
            print(min_avg, max_avg)

            # Merge to main df
            self.df = pd.merge(self.df, data, on='code', how='inner')        
        
        # Bins for legend, bins are equal width based on overall min and max of avgs
        bins_width = int((max_avg - min_avg) / 5)
        self.bins = [min_avg + i*bins_width for i in range(5)] + [max_avg]        

class Graphic: 
    """Main class that draws all components for the BART graphic."""    
    def __init__(self, stations):
        self._sketch = Sketch2D(WIDTH, LENGTH)
        self.stations = stations
        self.month = 1 # default month
        self.month_buttons = {} # maps month button coords to month num
        self.buttons = False
 
    def draw(self):
        """
        Draws the background map and draws each graphic on each step for interactivity.
        """
        self.draw_map() # draw map to set up zoom and coordinates
        self.station_to_pixels()
        self._sketch.on_step(lambda x: self.draw_allparts())

        self._sketch.show()

    def draw_allparts(self):
        """
        Draws each component of the graphic.
        """ 
        mouse = self._sketch.get_mouse()
        mouse.on_button_press(lambda x: self.interactive_month())
        self.draw_map()
        self.draw_stations()
        self.draw_legend()
        self.draw_title()
        self.draw_button()
        self.interactive_station()

    def draw_map(self):
        """
        Draws the background map.
        """
        # set center coordinates of on map
        self._sketch.set_map_pan(CENTER_LONG, CENTER_LAT) 
        self._sketch.set_map_zoom(MAP_SCALE)  
        self._sketch.set_map_placement(CENTER_X, CENTER_Y)  

        self._sketch.clear(BACKGROUND_COLOR)
        
        # load bay area map + draw  bay area outline
        data_layer = self._sketch.get_data_layer()
        geojson = data_layer.get_json(BAYAREA)
        geo_polgyons = self._sketch.parse_geojson(geojson)
        
        geo_polgyon = geo_polgyons[0]
        shape = geo_polgyon.to_shape()
        
        self._sketch.set_fill(LAND_COLOR)
        self._sketch.clear_stroke()
        self._sketch.draw_shape(shape)

    def draw_stations(self): 
        """
        Draws eacch bart station and colors each bart station according to ridership data.
        """
        self._sketch.push_map()
        self._sketch.push_style()
        self._sketch.push_transform()

        self._sketch.clear_stroke()
        self._sketch.clear_fill()
        self._sketch.set_ellipse_mode('center')

        dt = self.stations.df
        for _, row in dt.iterrows(): 
            rider = row[f'{self.month} Avg Weekday']
            for i in range(len(RIDER_COLORS)): 
                if rider <= self.stations.bins[i + 1]: 
                    self._sketch.set_fill(RIDER_COLORS[i])
                    break    
            
            long, lat = row['longitude'], row['latitude']
            x, y = self._sketch.convert_geo_to_pixel(long, lat)
            self._sketch.draw_ellipse(x, y, STATION_WIDTH, STATION_WIDTH)

            self._sketch.set_stroke(BACKGROUND_COLOR)
            self._sketch.set_stroke_weight(BORDER_WEIGHT)
            self._sketch.clear_fill()
            self._sketch.draw_ellipse(x, y, STATION_WIDTH, STATION_WIDTH)

        self._sketch.pop_map()
        self._sketch.pop_style()
        self._sketch.pop_transform()
    
    def draw_legend(self): 
        """
        Draws ridership legend.
        """
        self._sketch.push_map()
        self._sketch.push_style()
        self._sketch.push_transform()

        bins = [[self.stations.bins[i] + 1, self.stations.bins[i + 1]] for i in range(1, len(self.stations.bins) - 1)]
        bins = [[0, self.stations.bins[1]]] + bins

        # draw legend box
        x, y = LEGEND_LEFT, LENGTH - LEGEND_BOTTOM
        self._sketch.clear_fill()
        self._sketch.set_stroke_weight(BORDER_WEIGHT)
        self._sketch.set_stroke(DARK_TEXT_COLOR)
        self._sketch.set_rect_mode('corner')
        self._sketch.draw_rect(x, y, LEGEND_WIDTH, LEGEND_HEIGHT)
        
        # draw legend title
        self._sketch.clear_stroke()
        self._sketch.set_fill(DARK_TEXT_COLOR)
        self._sketch.set_text_align('center')
        self._sketch.set_text_font(FONT, 15)
        self._sketch.draw_text((LEGEND_LEFT + LEGEND_WIDTH)/2 + 5, y + 0.75*(LEGEND_HEIGHT/6), 'Avg Weekday Ridership')

        # draw bins + corresponding color rect
        self._sketch.clear_stroke()
        text_x_offset = 55
        box_x_offset = 15
        y_offset = 20

        for i in range(len(bins)): 
            self._sketch.set_fill(DARK_TEXT_COLOR)
            self._sketch.set_text_align('left')
            self._sketch.set_text_font(FONT, 16)
            self._sketch.draw_text(x + text_x_offset, y + (i + 1)*(LEGEND_HEIGHT/6) + y_offset, f'({bins[i][0]}, {bins[i][1]}]')

            self._sketch.set_fill(RIDER_COLORS[i])
            self._sketch.set_rect_mode('corner')
            self._sketch.draw_rect(x + box_x_offset, y + (i + 1)*(LEGEND_HEIGHT/6) + y_offset/2, BOX_WIDTH, BOX_HEIGHT)

        self._sketch.pop_map()
        self._sketch.pop_style()
        self._sketch.pop_transform()

    def draw_title(self): 
        """
        Draws the title.
        """
        self._sketch.push_map()
        self._sketch.push_style()
        self._sketch.push_transform()

        # upper title
        self._sketch.set_fill(DARK_TEXT_COLOR)
        self._sketch.set_text_align('left')
        self._sketch.set_text_font(FONT, 30)
        self._sketch.draw_text(WIDTH//5, TITLE_Y, f'{NUM_TO_MONTH[self.month]} 2024 BART Average Weekday Ridership')

        # data viz on screen instructions
        self._sketch.set_text_font(FONT, 20)
        self._sketch.draw_text(INSTR_X, INSTR_Y, '1. Click on a button below to select a month')
        self._sketch.draw_text(INSTR_X, INSTR_Y + 20, '2. Hover over a station to get more info')

        self._sketch.pop_map()
        self._sketch.pop_style()
        self._sketch.pop_transform()

    def draw_button(self): 
        """
        Draws monthly buttons. 
        """
        self._sketch.push_map()
        self._sketch.push_style()
        self._sketch.push_transform()
                
        self._sketch.set_stroke_weight(BORDER_WEIGHT)
        self._sketch.set_rect_mode('corner')

        self._sketch.set_text_align('left')
        self._sketch.set_text_font(FONT, 20)

        start_x, start_y = BUTTON_X, BUTTON_Y
        offset = 5
        for i in range(1, len(NUM_TO_MONTH) + 1): 
            # draw button box
            button_width = len(NUM_TO_MONTH[i]) * 16
            self._sketch.clear_fill()
            # if the month is the current month data being viewed, invert button colors
            if i == self.month: 
                self._sketch.set_stroke(BACKGROUND_COLOR)
                self._sketch.set_fill(DARK_TEXT_COLOR)
            else: 
                self._sketch.set_stroke(DARK_TEXT_COLOR)
            self._sketch.set_stroke_weight(BORDER_WEIGHT)
            self._sketch.draw_rect(start_x, start_y, button_width, BUTTON_HEIGHT)
            # draw 
            if i == self.month: 
                self._sketch.set_fill(BACKGROUND_COLOR)
            else: 
                self._sketch.set_fill(DARK_TEXT_COLOR)
            self._sketch.clear_stroke()
            self._sketch.draw_text(start_x + offset, start_y + offset*5, f'{NUM_TO_MONTH[i]}')
    
            # dict to hold button ranges
            # boolean so the dictionary is not rewritten each time the buttons are drawn (;-; couldnt think of a good way to do this in a separate function)
            if not self.buttons:
                x_range = (start_x, start_x + button_width)
                y_range = (start_y, start_y + button_width)
                self.month_buttons[(x_range, y_range)] = i
            start_x = start_x + button_width
        self.buttons = True 

        self._sketch.pop_map()
        self._sketch.pop_style()
        self._sketch.pop_transform()

    def interactive_month(self): 
        """
        Change data based on which month button has been clicked.
        """
        # function is only called when button is clicked
        # set month to the corresponding one the user is clicking on
        mouse = self._sketch.get_mouse()
        x, y = mouse.get_pointer_x(), mouse.get_pointer_y()

        for coords in self.month_buttons: 
            if coords[0][0] <= x <= coords[0][1] and coords[1][0] <= y <= coords[1][1]: 
                month = self.month_buttons[coords]
                self.month = month
    
    def interactive_station(self): 
        """
        Displays station data if user is hovering over a station point. 
        """
        # if mouse is hovering over station, show station stats in left side of graphic, otherwise dont
        self._sketch.push_map()
        self._sketch.push_style()
        self._sketch.push_transform()
        
        mouse = self._sketch.get_mouse()
        x_coord, y_coord = mouse.get_pointer_x(), mouse.get_pointer_y()

        station_stats = self.station_stats(x_coord, y_coord, self.month)
        if station_stats: 
            name, data, long, lat = station_stats[0], station_stats[1], station_stats[2], station_stats[3]
            self._sketch.clear_stroke()
            self._sketch.set_fill(DARK_TEXT_COLOR)
            self._sketch.set_text_font(FONT, 20)
            self._sketch.draw_text(LEGEND_LEFT, LENGTH - LEGEND_BOTTOM - 35, f'{name} Station')
            self._sketch.draw_text(LEGEND_LEFT, LENGTH - LEGEND_BOTTOM - 5, f'Avg Weekday Riders: {data}')

            # draw circle around station
            self._sketch.set_stroke(DARK_TEXT_COLOR)
            self._sketch.set_stroke_weight(BORDER_WEIGHT)
            self._sketch.clear_fill()
            self._sketch.set_ellipse_mode('center')
            x, y = self._sketch.convert_geo_to_pixel(long, lat)
            self._sketch.draw_ellipse(x, y, STATION_WIDTH, STATION_WIDTH)

        self._sketch.pop_map()
        self._sketch.pop_style()
        self._sketch.pop_transform()

    def station_to_pixels(self): 
        """
        For each station, record the coordinates of the perimeter of the station point.
        """
        station_coords = self.stations.df
        # dictionary mapping pixels to the station name
        
        self.station_pixels = {}
        for index, row in station_coords.iterrows(): 
            name = row['name']
            code = index
            # avg = row['Total Avg Weekday']
            lat = row['latitude']
            long = row['longitude']
            x, y = self._sketch.convert_geo_to_pixel(long, lat)
            x_range = (x - STATION_WIDTH/2, x + STATION_WIDTH/2)
            y_range = (y - STATION_WIDTH/2, y + STATION_WIDTH/2)
            self.station_pixels[(x_range, y_range)] = [name, code]
            print(name, code, long, lat)
    
    def station_stats(self, x, y, month):
        """
        x: float
        y: float
        month: string

        Given a coordinate and a month, returns corresponding station data if user is hovering over a station
        """
        # checks if mouse is hovering over a station
        for coords in self.station_pixels: 
            if coords[0][0] <= x <= coords[0][1] and coords[1][0] <= y <= coords[1][1]: 
                station_name, station_code = self.station_pixels[coords][0], self.station_pixels[coords][1]
                station_data = self.stations.df.loc[station_code, f'{month} Avg Weekday']
                long = self.stations.df.loc[station_code, 'longitude']
                lat = self.stations.df.loc[station_code, 'latitude']
                return station_name, station_data, long, lat
            
stations = Stations()
graphic = Graphic(stations)
graphic.draw()