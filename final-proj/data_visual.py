"""Visualization of Github commit message data from January 2020. 

Final Project submission for Stat 198: Interactive Data Science course at UC Berkeley.

Author: Vy Ho
License: BSD-3-Clause
"""
import pandas as pd
from sketchingpy import Sketch2D
from data_processing import DataModel

data_model = DataModel()

# TEXT SIZES
HEADER_SIZE = 38
TEXT_SIZE = 28
LEGEND_TEXT_SIZE = 15
USER_TEXT_SIZE = 17
TITLE_SIZE = 70
TERMINAL_SIZE = 18
HOVER_SIZE = 20
INFO_SIZE = 25

TITLE_OFFSET_X = 20
TITLE_OFFSET_Y = 10 

WIDTH  = 1400
HEIGHT = 950
PADDING  = 50

BOTTOM_RECT_HEIGHT = 200
BOTTOM_RECT_WIDTH = WIDTH - PADDING*2

QUAD_WIDTH = (WIDTH - PADDING*2)/2
QUAD_HEIGHT = (HEIGHT - PADDING*2 - BOTTOM_RECT_HEIGHT)/2

# TITLE QUADRANT
TITLE_X = PADDING
TITLE_Y = PADDING

# INFO PAGES
INFO_RADIUS = 10
BEZIER_R = 70

# TOP 5 WORDS QUADRANT
WORDS_X = PADDING + QUAD_WIDTH
WORDS_Y = PADDING
WORD_MAX = 1500
WORD_MAX_WIDTH = QUAD_WIDTH*2/3 - 20
WORDBAR_WIDTH = 25
WORDS_STEP = 300
WORD_RANGE = (0, WORD_MAX + 1, WORDS_STEP)

# TOP 5 USERS QUADRANT
USERS_X = PADDING + QUAD_WIDTH
USERS_Y = PADDING + QUAD_HEIGHT
USERBAR_WIDTH = 70
USER_MAX = 250
USER_MAX_LENGTH = QUAD_HEIGHT - PADDING*3/2 - HEADER_SIZE
USER_STEP = 50
USER_RANGE = (0, USER_MAX + 1, USER_STEP)

# COMMIT MESSAGE QUADRANT 
COMMIT_X = PADDING 
COMMIT_Y = PADDING + QUAD_HEIGHT
MAX_LINE_LENGTH = 55
LINE_LENGTH = MAX_LINE_LENGTH - 3
FIRST_LINE_LENGTH = MAX_LINE_LENGTH - len('$ git commit --')

# GRAPH RECT 
LINEGRAPH_X = PADDING 
LINEGRAPH_Y = PADDING + QUAD_HEIGHT*2
MESSAGE_MAX = 5
MESSAGE_MAX_LENGTH = BOTTOM_RECT_HEIGHT - HEADER_SIZE - PADDING*5/4
RADIUS = 5
DAYS = 31
DAYS_MAX_WIDTH = BOTTOM_RECT_WIDTH - PADDING*1/3 - PADDING*3/2
BLOCK = 10

# COLORS
BACKGROUND_COLOR = '#161b22'
HEADER_COLOR = '#f0f6fc'
WORD_COLOR = '#6e7681'
USER_COLOR = '#58a6ff'
COMMIT_COLOR = '#3fb950'
BORDER_COLOR = '#0c2d6b'
TERMINAL_YELLOW = '#C39C00'
GRID_COLOR = '#30363d'
TERMINAL_PURPLE = '#800080'
POINT_COLORS = ['#E4EBE6','#BFFFD1', '#5FED83', '#08872B', '#104C35']

PLATFORM = 'MINGW64'

# FONTS
HEADER_FONT = 'fonts/MonaSans-SemiBold.otf'
TEXT_FONT = 'fonts/MonaSans-Medium.otf'
TERMINAL_FONT = 'fonts/CascadiaCode-Regular.otf'

GRAPHIC_TYPES = {'title': (TITLE_X, TITLE_Y), 
                 'words': (WORDS_X, WORDS_Y), 
                 'users': (USERS_X, USERS_Y), 
                 'commit': (COMMIT_X, COMMIT_Y), 
                 'timeline': (LINEGRAPH_X, LINEGRAPH_Y)}

GRAPHIC_TITLES = {'title': '', 
                 'words': 'top 5 most used words', 
                 'users': 'top 5 active users', 
                 'commit': 'view a commit message', 
                 'timeline': 'word usage over time: '}

GRAPHIC_INFO = {'title': ['the following graphic is a snapshot summary of', 
                          'commit messages that occurred in january 2020.', 
                          'hover over each information icon for more', 
                          'information about the visualization.', 
                          '', 
                          '',
                          'enjoy! - vy ho'], 
                 'words': ["here lie the most frequent words seen in commit",
                           "messages. common filler words and articles, such as",
                           "'to' and 'the', were filtered out to highlight more", 
                           "interesting words. hover over each bar for exact", 
                           'counts.'], 
                 'users': ["here lie the most active users in regards to commit", 
                           "messages. usernames containing '[bot]' were filtered", 
                           "filtered out to remove bots. hover over each bar for", 
                           "exact counts."], 
                 'commit': ["view the statistics of a specific word as well as a",
                            "random commit message that used the entered word.",  
                            "press any key to get started. view the entered word's",
                            "usage timeline below. to search for a new word", 
                            "press any key."], 
                 'timeline': ["view a timeline of a word's frequency. the graph depicts the # of commit messages containing the", 
                              "specified word over the course of january. hover over each point for details. this graphic was inspired",
                              "by github's own commit message frequency visualization. the color key expresses each day's frequency", 
                              "relative to the total count in increasing units of 20th percentile.", 
                            ]
                }

# create scale for bar graphs
class NumericScale: 
    """
    given a max_value and a length, scales a numeric range across the specified length to create an axis
    """
    def __init__(self, max_value, length): 
        """
        max_value: an interger, the maximum numeric value
        length: an integer, the maximum length of the axis 
        """
        self.max_value = max_value
        self.length = length

    def get_position(self, value): 
        """
        value: an integer

        given an integer, returns the length to which corresponds to the value on the axis
        """
        percent = value / self.max_value 
        return percent * self.length
    
    def draw_horizontal_axis(self, sketch, range_info, x, y, buff, max_y, grid): 
        """
        range_info: tuple of length 3
        scale: function
        x: integer
        y: integer
        buff: integer
        max_value: integer

        given the scale and starting coordinates (x, y) of the axis, draws a horizontal
        axis according to the provided scale
        """
        # draw the axis 
        sketch.set_stroke_weight(2)
        sketch.set_stroke(HEADER_COLOR)
        sketch.draw_line(x, y, x + self.get_position(self.max_value), y)

        up_tick = y - 5
        bottom_tick = y + 5
        y_num = y + buff
        
        # draw each step value and mark 
        for i in range(range_info[0], range_info[1], range_info[2]): 
            sketch.set_stroke_weight(2)
            # draw the gridline
            if grid: 
                sketch.set_stroke(GRID_COLOR)
                sketch.draw_line(x + self.get_position(i), y, x + self.get_position(i), max_y)

            # draw the tick mark
            sketch.set_stroke(HEADER_COLOR)
            sketch.draw_line(x + self.get_position(i), up_tick, x + self.get_position(i), bottom_tick)
            # draw the value
            sketch.clear_stroke()
            sketch.draw_text(x + self.get_position(i), y_num, str(i))

    def draw_vertical_axis(self, sketch, range_info, x, y, buff, max_x): 
        """"
        range_info: tuple of length 3
        scale: function
        x: integer
        y: integer
        buff: integer
        max_value: integer

        given the scale and starting coordinates (x, y) of the axis, draws a vertical
        axis according to the provided scale
        """
        # draw the axis
        sketch.set_stroke_weight(2)
        sketch.set_stroke(HEADER_COLOR)
        sketch.draw_line(x, y, x, y - self.get_position(self.max_value))

        left_tick = x - 5
        right_tick = x + 5
        x_num = x - buff

        #draw each step value and mark
        for i in range(range_info[0], range_info[1], range_info[2]): 
            # draw grid line
            sketch.set_stroke(GRID_COLOR)
            sketch.draw_line(x, y - self.get_position(i), max_x ,y - self.get_position(i))

            # draw the tick mark
            sketch.set_stroke_weight(2)
            sketch.set_stroke(HEADER_COLOR)
            sketch.draw_line(left_tick, y - self.get_position(i), right_tick, y - self.get_position(i))

            # draw the value
            sketch.clear_stroke()
            sketch.draw_text(x_num, y - self.get_position(i), str(i))

# main class to draw each component of the graph
class Graphic: 
    input_text = []
    word_bars = []
    user_bars = []
    timeline_points = []
    commit_message = None

    def __init__(self, data_model):
        """
        data_model: DataModel instance
        word_scale: NumericScale instance
        user_scale: NumericScale instance
        message_scale: NumericScale instance
        """
        self._sketch = Sketch2D(WIDTH, HEIGHT) 
        self.data_model = data_model

        self.words_graphic = TopWords(self._sketch, data_model)
        self.user_graphic = TopUsers(self._sketch, data_model)
        self.view_commit_graphic = Commit(self._sketch, data_model)

        self._sketch.create_buffer('static', WIDTH, HEIGHT, BACKGROUND_COLOR)

    def draw(self): 
        """
        draws the entire graphic
        """
        self.draw_static()
        self._sketch.on_step(lambda x: self.draw_interactive())
        self._sketch.show()

    def draw_interactive(self): 
        """
        draws each componenet of the graphic and the functions needed for user interaction
        """
        self._sketch.clear(BACKGROUND_COLOR)
        self._sketch.get_keyboard().on_key_press(self.view_commit_graphic.on_key_press)
        self._sketch.draw_buffer(0, 0, 'static')
        self.view_commit_graphic.draw()
        self.interactive_bar()
        self.info_interactive()

    def draw_static(self): 
        """
        draws the static components in a buffer
        """
        self._sketch.enter_buffer('static')

        # self.guidelines()
        self.draw_title()
        self.words_graphic.draw()
        self.user_graphic.draw()
        self.draw_info_bubbles()

        self._sketch.exit_buffer()

    def guidelines(self): 
        """
        draws guidelines outlining each section of the graphic. 
        not used in the final graphic
        """
        self._sketch.push_style()
        self._sketch.push_transform()

        self._sketch.set_stroke(COMMIT_COLOR)
        self._sketch.set_stroke_weight(1)
        self._sketch.draw_line(PADDING, 0, PADDING, HEIGHT)
        self._sketch.draw_line(PADDING + QUAD_WIDTH, 0, PADDING + QUAD_WIDTH, HEIGHT- BOTTOM_RECT_HEIGHT - PADDING)
        self._sketch.draw_line(PADDING + QUAD_WIDTH*2, 0, PADDING + QUAD_WIDTH*2, HEIGHT)
        self._sketch.draw_line(0, PADDING, WIDTH, PADDING)
        self._sketch.draw_line(0, PADDING + QUAD_HEIGHT, WIDTH, PADDING + QUAD_HEIGHT)
        self._sketch.draw_line(0, PADDING + QUAD_HEIGHT*2, WIDTH, PADDING + QUAD_HEIGHT*2)
        self._sketch.draw_line(0, HEIGHT - PADDING, WIDTH, HEIGHT - PADDING)

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def draw_info_bubbles(self): 
        """
        draws info bubble for each of the graphic sections
        """
        for i in GRAPHIC_TYPES.keys(): 
            self.draw_info_bubble(i)
    
    def draw_info_bubble(self, graphic): 
        """
        graphic: string

        draw info buttons according to the given graphic type
        """
        self._sketch.push_style()
        self._sketch.push_transform()

        X,Y = GRAPHIC_TYPES[graphic][0], GRAPHIC_TYPES[graphic][1]
        self._sketch.translate(X, Y)

        y = INFO_RADIUS*3
       
        if graphic == 'timeline': 
            x = BOTTOM_RECT_WIDTH - INFO_RADIUS*3
        else: 
            x = QUAD_WIDTH - INFO_RADIUS*3

        self._sketch.set_stroke(HEADER_COLOR)
        self._sketch.set_stroke_weight(2)
        self._sketch.clear_fill()
        self._sketch.set_ellipse_mode('center')
        self._sketch.draw_ellipse(x, y, INFO_RADIUS*2, INFO_RADIUS*2)

        self._sketch.clear_stroke()
        self._sketch.set_text_align('center', 'center')
        self._sketch.set_text_font(TEXT_FONT, USER_TEXT_SIZE)
        self._sketch.set_fill(HEADER_COLOR)
        self._sketch.draw_text(x, y, 'i')

        self._sketch.pop_style()
        self._sketch.pop_transform()
    
    def touching_info(self, graphic, x_coord, y_coord):
        """
        graphic: string
        x_coord: integer
        y_coord: integer

        given a graphic, determine if the user is hovering on an info icon. 
        returns a boolean
        """
        x = y = 0

        x, y = GRAPHIC_TYPES[graphic][0], GRAPHIC_TYPES[graphic][1]
        if graphic == 'timeline': 
            x += BOTTOM_RECT_WIDTH
        else: 
            x += QUAD_WIDTH
                
        x1, y1 = x - INFO_RADIUS*4, y + INFO_RADIUS*2
        x2, y2 = x - INFO_RADIUS*2, y + INFO_RADIUS*4

        if x1 <= x_coord <= x2 and y1 <= y_coord <= y2: 
            return True
        return False
    
    def info_interactive(self): 
        """
        check if user is hovering over any information icons and display its info if so
        """
        self._sketch.push_style()
        self._sketch.push_transform()

        for key, value in GRAPHIC_TYPES.items(): 
            X, Y = value[0], value[1]
            self._sketch.translate(X, Y)

            mouse = self._sketch.get_mouse()
            x_coord, y_coord = mouse.get_pointer_x(), mouse.get_pointer_y()

            if key == 'timeline': 
                x = BOTTOM_RECT_WIDTH - INFO_RADIUS*3
            else: 
                x = QUAD_WIDTH - INFO_RADIUS*3
           
            y = INFO_RADIUS*3

            if self.touching_info(key, x_coord, y_coord): 
                # show info message
                self.draw_display_info(key)

                # invert info circle color
                self._sketch.set_stroke(BACKGROUND_COLOR)
                self._sketch.set_stroke_weight(2)
                self._sketch.set_fill(HEADER_COLOR)
                self._sketch.set_ellipse_mode('center')
                self._sketch.draw_ellipse(x, y, INFO_RADIUS*2, INFO_RADIUS*2)

                self._sketch.clear_stroke()
                self._sketch.set_text_align('center', 'center')
                self._sketch.set_text_font(TEXT_FONT, USER_TEXT_SIZE)
                self._sketch.set_fill(BACKGROUND_COLOR)
                self._sketch.draw_text(x, y, 'i')
            
            self._sketch.translate(-X, -Y) # reset translation 

        self._sketch.pop_style()
        self._sketch.pop_transform()
    
    def draw_display_info(self, graphic): 
        """
        graphic: a string

        draws information box for the given graphic
        """

        self._sketch.push_style()
        self._sketch.push_transform()

        x, y = GRAPHIC_TYPES[graphic]
        height = width = 0

        if graphic == 'timeline': 
            height = BOTTOM_RECT_HEIGHT
            width = BOTTOM_RECT_WIDTH
        else: 
            height = QUAD_HEIGHT
            width = QUAD_WIDTH

        # draw rounded rectangle 
        shape = self.draw_info_page(0, 0, width, height, BEZIER_R)
        self._sketch.draw_shape(shape)

        # draw title of graphic (only for the non title quadrants)
        if graphic != 'title': 
            self._sketch.clear_stroke()
            self._sketch.set_text_font(HEADER_FONT, HEADER_SIZE)
            self._sketch.set_text_align('left', 'baseline')
            self._sketch.set_fill(BACKGROUND_COLOR)
            self._sketch.draw_text(TITLE_OFFSET_X, HEADER_SIZE + TITLE_OFFSET_Y, GRAPHIC_TITLES[graphic])

        info_text = GRAPHIC_INFO[graphic] # retrieve corresponding text

        self._sketch.set_text_font(TEXT_FONT, INFO_SIZE)
        self._sketch.set_text_align('left', 'baseline')
        self._sketch.set_fill(WORD_COLOR)

        buff = TITLE_OFFSET_Y*3
        
        # draw each line 
        x, y = TITLE_OFFSET_X, HEADER_SIZE + TITLE_OFFSET_Y*4
        for i in range(len(info_text)):
            line = info_text[i]
            self._sketch.draw_text(x, y, line)

            y += buff
        
        self._sketch.pop_style()
        self._sketch.pop_transform()

    def draw_info_page(self, x, y, w, h, r): 
        """
        x: integer
        y: integer
        w: integer
        h: integer
        r: integer

        given the top left coordinates x, y draw a rounded rectangle with width w
        and height h. roundedness dependent on r, higher values with a greater curve.
        draws the info page via a bezier curve
        """
        self._sketch.set_stroke_weight(2)
        self._sketch.set_stroke(HEADER_COLOR)
        self._sketch.set_fill(HEADER_COLOR)
        
        shape = self._sketch.start_shape(x + r, y)
        shape.add_line_to(x + w - r, y)
        shape.add_bezier_to(x + w, y, 
                            x + w, y + r, 
                            x + w, y + r)
        shape.add_line_to(x + w, y + h - r)
        shape.add_bezier_to(x + w, y + h, 
                            x + w - r, y + h, 
                            x + w - r, y + h)
        shape.add_line_to(x + r, y + h)
        shape.add_bezier_to(x, y + h,
                            x, y + h - r,
                            x, y + h - r)
        shape.add_line_to(x, y + r)
        shape.add_bezier_to(x, y,
                            x + r, y,
                            x + r, y)
        shape.close()
        return shape

    def draw_title(self):
        """
        draws the main title
        """
        self._sketch.push_style()
        self._sketch.push_transform()

        self._sketch.translate(TITLE_X, TITLE_Y)

        buffer = TITLE_SIZE # spacing between each line
        self._sketch.clear_stroke()
        self._sketch.set_text_font(HEADER_FONT, TITLE_SIZE)
        self._sketch.set_fill(HEADER_COLOR)
        self._sketch.set_text_align('left', 'top')
        lines = ['github', 'commit', 'messages from', 'january 2020']

        for i in range(len(lines)): 
            self._sketch.draw_text(TITLE_OFFSET_X, buffer*i, lines[i])

        self._sketch.pop_style()
        self._sketch.pop_transform()
   
    def draw_bars(self, x, y, width, height, color, vert): 
        """
        x: integer
        y: integer
        width: integer
        height: integer
        color: string
        vert: boolean

        draws a bar according to the given upper leftmost coordinate, width, height, color, and orientation
        additionally records the boundaries of the bar
        """
        self._sketch.set_rect_mode('corner')
        self._sketch.set_fill(color)
        self._sketch.draw_rect(x, y, width, height)

        if vert:
            x1, y1, x2, y2 = USERS_X + x, USERS_Y + HEADER_SIZE + y, USERS_X + x + width, USERS_Y + HEADER_SIZE + y + height
            self.user_bars.append([x1, y1, x2, y2])
        else: 
            x1, y1, x2, y2 = WORDS_X + x, WORDS_Y + HEADER_SIZE + y, WORDS_X + x + width, WORDS_Y + HEADER_SIZE + y + height
            self.word_bars.append([x1, y1, x2, y2])

    def interactive_bar(self): 
        """
        draws interactive components of bar graphs if a user is hovering over a bar graph
        """
        self._sketch.push_style()
        self._sketch.push_transform()

        self._sketch.set_text_font(TEXT_FONT, HOVER_SIZE)
        self._sketch.clear_stroke()
        buff = 5

        # user coordinates
        mouse = self._sketch.get_mouse()
        x_coord, y_coord = mouse.get_pointer_x(), mouse.get_pointer_y()

        user_bar = self.bar_hover(x_coord, y_coord, True)
        word_bar = self.bar_hover(x_coord, y_coord, False)

        # if user is hovering over a bar
        if user_bar: 
            self._sketch.set_text_align('center', 'bottom')
            user = user_bar[0]
            count = user_bar[1]
            bar = user_bar[2]

            x1, y1, x2, y2 = self.user_bars[bar][0], self.user_bars[bar][1], self.user_bars[bar][2], self.user_bars[bar][3]
           
           # draw value and highlight the bar
            self._sketch.draw_text(x1 + USERBAR_WIDTH/2, y1 - buff, str(count))
            self.draw_bar_highlight(x1, y1, x2, y2)
        elif word_bar: 
            self._sketch.set_text_align('left', 'top')
            word = word_bar[0]
            count = word_bar[1]
            bar = word_bar[2]
            
            x1, y1, x2, y2 = self.word_bars[bar][0], self.word_bars[bar][1], self.word_bars[bar][2], self.word_bars[bar][3]

            # draw value and highlight the bar
            self._sketch.draw_text(x1 + buff, y1 + buff, str(count) + ' appearances')
            self.draw_bar_highlight(x1, y1, x2, y2)

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def bar_hover(self, x, y, user): 
        """
        x: integer
        y: integer
        user: boolean

        given x, y coordinates and the type of bar graph, return the bar's information 
        if the user's mouse is found within the bar's bounds. otherwise reutrns None
        """
        # get the df of the top values
        if user: 
            coords = self.user_bars
            col = 'user'
            series = self.data_model.get_top5_users()
        else: 
            coords = self.word_bars
            col = 'word'
            series = self.data_model.get_top5_words()

        # iterate through each values and determine if user is hovering within the bounds
        for i in range(len(coords)): 
            if coords[i][0] <= x <= coords[i][2] and coords[i][1] <= y <= coords[i][3]:
                row = series.iloc[i]
                col = row[col]
                count = row['count']
                return col, count, i
            
    def draw_bar_highlight(self, x1, y1, x2, y2): 
        """
        x1 = integer
        y1 = integer
        x2 = integer
        y2 = integer
        
        given the top left and the lower right coordinates, draw a rectangle
        """
        self._sketch.clear_fill()
        self._sketch.set_stroke_weight(3)
        self._sketch.set_stroke(HEADER_COLOR)
        self._sketch.set_rect_mode('corners')
        self._sketch.draw_rect(x1, y1, x2, y2)

    def draw_round_rect(self, x, y, w, h, r): 
        """
        x: integer
        y: integer
        w: integer
        h: integer
        r: integer

        given the top left coordinates x, y draw a rounded rectangle with width w
        and height h. roundedness dependent on r, higher values with a greater curve. 
        does not work well for small rectangles
        """
        self._sketch.set_stroke_weight(2)
        self._sketch.set_stroke(HEADER_COLOR)
        self._sketch.clear_fill()
        # sides
        self._sketch.draw_line(x + r, y, x + w - r, y)
        self._sketch.draw_line(x, y + r, x, y + h - r)
        self._sketch.draw_line(x + w, y + r, x + w, y + h - r)
        self._sketch.draw_line(x + r, y + h, x + w - r, y + h)
        
        # rounded corners
        self._sketch.set_arc_mode('radius')
        self._sketch.set_angle_mode('degrees')

        self._sketch.draw_arc(x + r, y + r, r, r, 270, 0)
        self._sketch.draw_arc(x + r, y + h - r, r, r, 180, 270)
        self._sketch.draw_arc(x + w - r, y + r, r, r, 0, 90)
        self._sketch.draw_arc(x + w - r, y + h - r, r, r, 90, 180)

class TopWords(Graphic): 

    def __init__(self, sketch, data_model): 
        self._sketch = sketch
        self.data_model = data_model
        self.scale = NumericScale(WORD_MAX, WORD_MAX_WIDTH)
 
    def draw(self): 
        self.draw_word_legend()
        self.draw_top_words()

    def draw_top_words(self): 
        """
        draws the top words quadrant
        """
        self._sketch.push_style()
        self._sketch.push_transform()
        
        self._sketch.translate(WORDS_X, WORDS_Y + HEADER_SIZE)

        top5 = self.data_model.get_top5_words()
        
        self._sketch.clear_stroke()
        self._sketch.set_text_font(TEXT_FONT, TEXT_SIZE)
        self._sketch.set_text_align('left', 'top')
        self._sketch.set_rect_mode('corner')

        buffer = TEXT_SIZE + TITLE_OFFSET_Y # spacing in between bars
        x_word = PADDING # x coord for words 
        y = buffer # starting y coord 
        x_bar = QUAD_WIDTH*1/3 # x coordinate for the bar graph
        
        # iterate through the df rows and draw the word and the corresponding bar graph
        i = 1
        for index, row in top5.iterrows():
            word = row['word'] 
            count = row['count']

            self.draw_bars(x_bar, y, self.scale.get_position(count), WORDBAR_WIDTH, WORD_COLOR, False)
            self._sketch.draw_text(x_word - PADDING/2, y, f'{i}.')
            self._sketch.set_fill(HEADER_COLOR)
            self._sketch.draw_text(x_word, y, word)

            y += buffer
            i += 1
        
        self._sketch.pop_style()
        self._sketch.pop_transform()

    def draw_word_legend(self):
        """
        draw the title and the axis associated with the top 5 words graphic
        """
        self._sketch.push_style()
        self._sketch.push_transform()
        
        self._sketch.translate(WORDS_X, WORDS_Y)

        self._sketch.clear_stroke()
        self._sketch.set_text_font(TEXT_FONT, HEADER_SIZE)
        self._sketch.set_text_align('left', 'baseline')
        self._sketch.set_fill(HEADER_COLOR)

        # title
        self._sketch.draw_text(TITLE_OFFSET_X, HEADER_SIZE + TITLE_OFFSET_Y, GRAPHIC_TITLES['words'])
        
        # x-axis 
        buffer = TEXT_SIZE + 10
        x = QUAD_WIDTH*1/3
        y = HEADER_SIZE + buffer*6
        
        # axis labels 
        self._sketch.set_text_font(TEXT_FONT, LEGEND_TEXT_SIZE)
        self._sketch.set_text_align('center', 'baseline')

        self.scale.draw_horizontal_axis(self._sketch, WORD_RANGE, x, y, PADDING/2, TEXT_SIZE + TITLE_OFFSET_Y + HEADER_SIZE, True)

        self._sketch.draw_text(x + self.scale.get_position(self.scale.max_value/2), y + buffer, '# of appearances')

        self._sketch.pop_style()
        self._sketch.pop_transform()

class TopUsers(Graphic):

    def __init__(self, sketch, data_model): 
        self._sketch = sketch
        self.data_model = data_model
        self.scale = NumericScale(USER_MAX, USER_MAX_LENGTH)
 
    def draw(self): 
        self.draw_user_legend()
        self.draw_top_users()

    def draw_top_users(self): 
        """
        draw the top 5 users graphic
        """        
        self._sketch.push_style()
        self._sketch.push_transform()
        
        self._sketch.translate(USERS_X, USERS_Y + HEADER_SIZE)

        top5 = self.data_model.get_top5_users()

        x, y = PADDING*3/2, QUAD_HEIGHT - PADDING*3/2
        x_end = QUAD_WIDTH - PADDING*1/3
        buffer = USERBAR_WIDTH + ((x_end - x) - USERBAR_WIDTH*5)/6
        x += buffer - USERBAR_WIDTH
        # iterate through each row and draw its corresponding bar graph and value
        for index, row in top5.iterrows(): 
            user = row['user']
            count = row['count']
            
            y_bar = y - self.scale.get_position(count)
            self.draw_bars(x, y_bar, USERBAR_WIDTH, self.scale.get_position(count), USER_COLOR, True)

            self._sketch.set_fill(HEADER_COLOR)
            self._sketch.clear_stroke()
            self._sketch.set_text_font(TEXT_FONT, USER_TEXT_SIZE)
            self._sketch.set_text_align('center', 'top')
            self._sketch.draw_text(x + USERBAR_WIDTH/2, y + 3, user)

            x += buffer

        self._sketch.pop_style()
        self._sketch.pop_transform()
        
        # self.draw_info('users')
        
    def draw_user_legend(self): 
        """
        draw the title and axis labels for the user graphic
        """
        self._sketch.push_style()
        self._sketch.push_transform()

        self._sketch.translate(USERS_X, USERS_Y)

        self._sketch.clear_stroke()
        self._sketch.set_text_font(TEXT_FONT, HEADER_SIZE)
        self._sketch.set_text_align('left', 'baseline')
        self._sketch.set_fill(HEADER_COLOR)

        # title
        self._sketch.draw_text(TITLE_OFFSET_X, HEADER_SIZE + TITLE_OFFSET_Y, GRAPHIC_TITLES['users'])

        # y-axis
        self._sketch.translate(0, HEADER_SIZE)
        x = PADDING*3/2
        y = QUAD_HEIGHT - (PADDING*3/2)
        self._sketch.set_text_font(TEXT_FONT, LEGEND_TEXT_SIZE)
        self._sketch.set_text_align('right', 'center')

        self.scale.draw_vertical_axis(self._sketch, USER_RANGE, x, y, 12,  QUAD_WIDTH - PADDING*1/3)

        # y-axis title
        self._sketch.set_text_font(TEXT_FONT, LEGEND_TEXT_SIZE)
        self._sketch.set_angle_mode('degrees')
        self._sketch.rotate(-90)
        self._sketch.set_text_align('center', 'baseline')
        self._sketch.draw_text(-(QUAD_HEIGHT - HEADER_SIZE)/2, PADDING*3/5, '# of commit messages')
        self._sketch.rotate(90)
    
        self._sketch.pop_style()
        self._sketch.pop_transform()

class Commit(Graphic): 
    def __init__(self, sketch, data_model): 
        self._sketch = sketch
        self.data_model = data_model
        self.timeline_scale = NumericScale(DAYS, DAYS_MAX_WIDTH)
        self.message_scale = NumericScale(MESSAGE_MAX, MESSAGE_MAX_LENGTH)
        self.default_message_scale = self.message_scale
    
    def draw(self): 
        self.draw_typing()
        self.draw_timeline()
        self.interactive_timeline()

    def draw_typing(self):
        """
        draw the interactive user typing graphic
        """
        self._sketch.push_style()
        self._sketch.push_transform()

        self._sketch.translate(COMMIT_X, COMMIT_Y)
        
        self._sketch.clear_stroke()

        # title 
        self._sketch.set_text_font(TEXT_FONT, HEADER_SIZE)
        self._sketch.set_text_align('left', 'baseline')
        self._sketch.set_fill(HEADER_COLOR)
        self._sketch.draw_text(TITLE_OFFSET_X, HEADER_SIZE + TITLE_OFFSET_Y, GRAPHIC_TITLES['commit'])

        shape = self.draw_round_rect(PADDING//2, PADDING*3/2, QUAD_WIDTH - PADDING, 50, 10)
        # user input so far
        typed = ''.join(self.input_text)

        self._sketch.pop_style()
        self._sketch.pop_transform()

        if self.commit_message is not None: 
            self.draw_commit()
        else:
            self.draw_user_type(typed)
        
        # self.draw_info('commit')

    def draw_commit(self): 
        """
        draw a commit messsage
        """
        self._sketch.push_style()
        self._sketch.push_transform()

        self._sketch.translate(COMMIT_X, COMMIT_Y)

        self._sketch.set_text_font(TERMINAL_FONT, TEXT_SIZE)
        self._sketch.set_text_align('left', 'baseline')
        # draw user input
        terminal_y = QUAD_HEIGHT - PADDING*2

        x = PADDING/2 + 10
        y = PADDING*3/2 + HEADER_SIZE
        self._sketch.draw_text(x, y, self.commit_message[0])
        second = third = None
        
        if self.commit_message[1] == 'no commit message found': 
            word_count = user_count = 0
            commit_message = self.commit_message[1]  
        else: 
            self._sketch.set_text_font(TERMINAL_FONT, TERMINAL_SIZE)
            repo = self.commit_message[1]
            user = self.commit_message[2]
            message = self.commit_message[3]
            word_count = self.data_model.get_word_count(self.commit_message[0])
            user_count = self.data_model.get_user_count(self.commit_message[0])
            
            # text overspill, split message into at most three lines
            if len(message) > FIRST_LINE_LENGTH: 
                first = message[:FIRST_LINE_LENGTH]
                second = message[FIRST_LINE_LENGTH:FIRST_LINE_LENGTH + MAX_LINE_LENGTH]
                third = message[FIRST_LINE_LENGTH + MAX_LINE_LENGTH: FIRST_LINE_LENGTH + MAX_LINE_LENGTH*2 - 3] 
                if len(message) > FIRST_LINE_LENGTH + MAX_LINE_LENGTH*2 - 3: 
                    third = third + '...'
                message = first

            # draw terminal directory + color code each segment
            self._sketch.clear_stroke()
            self._sketch.set_fill(COMMIT_COLOR)
            self._sketch.draw_text(x,  terminal_y, f'{user}')
            self._sketch.set_fill(TERMINAL_PURPLE)
            self._sketch.draw_text(x, terminal_y, f"{len(user)*' '} {PLATFORM}")

            self._sketch.set_fill(TERMINAL_YELLOW)
            terminal_message = f"{(len(user) + len(PLATFORM))*' '}  ~/{repo}"
            # user + repo overspill, slice line short to fit 
            if len(terminal_message) > LINE_LENGTH: 
                terminal_message = terminal_message[:LINE_LENGTH] + '...'

            self._sketch.draw_text(x,  terminal_y, terminal_message)
            commit_message = f'$ git commit --{message}'
        
        self._sketch.set_text_align('left', 'top')
        self._sketch.set_text_font(TERMINAL_FONT, TERMINAL_SIZE)
        self._sketch.set_fill(HEADER_COLOR)
        
        # draw commit message
        self._sketch.draw_text(x, terminal_y + PADDING/2, commit_message)
        # draw additional lines if there are any
        if second: 
            self._sketch.draw_text(x, terminal_y + PADDING, second)
        if third: 
            self._sketch.draw_text(x, terminal_y + PADDING*3/2, third)
        
        # draw word statistics 
        self._sketch.draw_text(x, y + PADDING, f"appears in {len(str(word_count))*' '} commit messages")
        self._sketch.draw_text(x, y + PADDING*3/2, f"used by {len(str(user_count))*' '} different users")
        self._sketch.set_fill(COMMIT_COLOR)
        self._sketch.draw_text(x, y + PADDING, f"{len('appears in ')*' '}{word_count}")
        self._sketch.set_fill(USER_COLOR)
        self._sketch.draw_text(x, y + PADDING*3/2, f"{len('used by ')*' '}{user_count}")
        self._sketch.set_fill(WORD_COLOR)
        self._sketch.draw_text(x, y + PADDING/2, 'press any key to try a new word')

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def draw_user_type(self, typed): 
        """
        draw user input as they're typing
        """
        self._sketch.push_style()
        self._sketch.push_transform()

        self._sketch.translate(COMMIT_X, COMMIT_Y)

        self._sketch.clear_stroke()
        self._sketch.set_text_font(TERMINAL_FONT, TEXT_SIZE)
        self._sketch.set_text_align('left', 'baseline')

        cursor_x = PADDING/2
        text_x = cursor_x + 10
        text_y = PADDING*3/2 + HEADER_SIZE

        instruct_x = text_x
        instruct_y = text_y + PADDING

        # blinking cursor
        time = self._sketch.get_millis_shown() // 500
        if time % 2 == 0: 
            white_cursor = True
        else: 
            white_cursor = False
        
        # if the user has not typed anything
        if not typed: 
            self.draw_cursor(cursor_x, text_y, white_cursor)
            self._sketch.set_fill(WORD_COLOR)
            self._sketch.draw_text(text_x, text_y, 'type a word and press enter')
        else: 
            self._sketch.set_fill(HEADER_COLOR)
            self._sketch.draw_text(text_x, text_y, typed)
            self.draw_cursor(text_x + len(typed)*15, text_y, white_cursor)

            self._sketch.set_fill(WORD_COLOR)
            self._sketch.draw_text(instruct_x, instruct_y, 'press enter to search')

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def draw_cursor(self, x, y, white):
        """
        x: integer
        y: integer
        white: boolean

        draws a cursor, color dependent on white value
        """
        if white: 
            self._sketch.set_fill(HEADER_COLOR)
        else: 
            self._sketch.set_fill(WORD_COLOR)
        
        self._sketch.draw_text(x, y, '|') 

    def on_key_press(self, key): 
        """
        key: button object

        records the keys pressed
        """
        button = key.get_name()
        print(button)

        # reset commit_message after it is displayed
        if self.commit_message is not None: 
            self.commit_message = None
       
        if button == 'backspace': 
            if self.input_text: 
                self.input_text.pop()
        elif button == 'return': # user has finished typing
            if self.input_text:
                self.commit_message = self.data_model.get_commit(''.join(self.input_text))
                self.input_text = []
        elif len(button) == 1: # only record letters
            self.input_text.append(button)

    def draw_timeline(self): 
        """
        draw the timeline graphic
        """
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.translate(LINEGRAPH_X, LINEGRAPH_Y)

        self._sketch.clear_stroke()
        self._sketch.set_text_align('left', 'baseline')
        self._sketch.set_text_font(TEXT_FONT, HEADER_SIZE)
        self._sketch.set_fill(COMMIT_COLOR)
        
        df = None

        # if there is a commit_message to display
        if self.commit_message: 
            word = self.commit_message[0] # word to be displayed
            
            if self.commit_message[1] != 'no commit message found':
                # if there is a commit message, scale the vertical axis based on the maximum count value
                df = self.data_model.get_word_timeline(word) 
                max_messages = max(max(df['count']), MESSAGE_MAX) # compare against minimum vertical axis value
                self.message_scale = NumericScale(max_messages, MESSAGE_MAX_LENGTH)

            text = f"{len('word usage over time: ')*2*' '} {word}" 
            self._sketch.clear_stroke()
            self._sketch.draw_text(TITLE_OFFSET_X, HEADER_SIZE + TITLE_OFFSET_Y, text)

        else: # reset interactive points and vetical axis
            self.message_scale = self.default_message_scale
            self.timeline_points = []

        self._sketch.pop_transform()
        self._sketch.pop_style()

        self.draw_timeline_legend()
        self.draw_timeline_line(df)

    def draw_timeline_line(self, df): 
        """
        df: dataframe

        draw the line graph based on the given data in df
        """
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.translate(LINEGRAPH_X, LINEGRAPH_Y + 10)
        
        self._sketch.set_stroke_weight(3)

        if df is not None: 
            self.draw_all_lines(df)
            self.draw_all_points(df)

        self._sketch.pop_transform()
        self._sketch.pop_style()

    def get_point_color(self, value, max_value):
        """
        value: integer
        max_value: integer

        given a value and the max_value, return the color corresponding to the percentile bin of the value. 
        """
        unit = max_value / 5
        for i in range(1, 5): 
            if (i - 1)*unit <= value < i*unit: 
                return POINT_COLORS[i - 1]
        return POINT_COLORS[4]        
    
    def draw_all_points(self, df): 
        """
        df: dataframe

        given a dataframe, draws all the points in the dataframe in the timeline graphic
        """
        x, y = PADDING*3/2, BOTTOM_RECT_HEIGHT - PADDING
        max_value = max(df['count'])
        self._sketch.set_ellipse_mode('center')
        
        # iterate through df and graph points
        for index, row in df.iterrows(): 
            day = row['day'] 
            count = row['count'] 
            curr_x, curr_y = x + self.timeline_scale.get_position(day), y - self.message_scale.get_position(count)
            
            point_color = self.get_point_color(count, max_value)
            self._sketch.set_stroke(point_color)
            self._sketch.set_fill(point_color)

            self._sketch.draw_ellipse(curr_x, curr_y, RADIUS*2, RADIUS*2)

            x1, y1, x2, y2, = LINEGRAPH_X + curr_x - RADIUS, LINEGRAPH_Y + TITLE_OFFSET_Y+ curr_y - RADIUS, LINEGRAPH_X + curr_x + RADIUS, LINEGRAPH_Y + TITLE_OFFSET_Y + curr_y + RADIUS
            
            # record points for interactivity 
            self.timeline_points.append([x1, y1, x2, y2, day, count])
            
    def draw_all_lines(self, df): 
        """
        df: dataframe

        given a dataframe, draw all the lines in the dataframe in the timeline graphic
        """
        x, y = PADDING*3/2, BOTTOM_RECT_HEIGHT - PADDING
        prev_x, prev_y = x, y
        
        self._sketch.set_stroke(WORD_COLOR)
        # iterate through df and draw points and lines
        for index, row in df.iterrows(): 
            day = row['day'] 
            count = row['count'] 
            curr_x, curr_y = x + self.timeline_scale.get_position(day), y - self.message_scale.get_position(count)
            
            self._sketch.draw_line(prev_x, prev_y, curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

    def draw_timeline_legend(self): 
        """
        draw legend for timeline graphic
        """
        self._sketch.push_style()
        self._sketch.push_transform()

        self._sketch.translate(LINEGRAPH_X, LINEGRAPH_Y)
        
        # title
        self._sketch.clear_stroke()
        self._sketch.set_text_font(TEXT_FONT, HEADER_SIZE)
        self._sketch.set_fill(HEADER_COLOR)
        self._sketch.set_text_align('left', 'baseline')

        self._sketch.draw_text(TITLE_OFFSET_X, HEADER_SIZE + TITLE_OFFSET_Y, GRAPHIC_TITLES['timeline'])

        # y-axis title
        self._sketch.set_text_font(TEXT_FONT, LEGEND_TEXT_SIZE)
        self._sketch.set_angle_mode('degrees')
        self._sketch.rotate(-90)
        self._sketch.set_text_align('center', 'baseline')
        self._sketch.draw_text(-BOTTOM_RECT_HEIGHT/2, PADDING*1/3 + 15, '# of commit')
        self._sketch.draw_text(-BOTTOM_RECT_HEIGHT/2, PADDING*1/3 + 30, 'messages')
        self._sketch.rotate(90)

        # y-axis
        x, y = PADDING*3/2, BOTTOM_RECT_HEIGHT - PADDING + TITLE_OFFSET_Y
        x_end = x + DAYS_MAX_WIDTH
   
        self._sketch.set_text_font(TEXT_FONT, LEGEND_TEXT_SIZE)
        self._sketch.set_text_align('right', 'center')

        range_info = (0, self.message_scale.max_value + 1, self.message_scale.max_value // 5)
        self.message_scale.draw_vertical_axis(self._sketch, range_info, x, y, 10, x_end)

       # x-axis
        day_dist = (x_end - x)/31
        self._sketch.set_text_align('center', 'baseline')

        range_info = (1, DAYS + 1, 1)
        self.timeline_scale.draw_horizontal_axis(self._sketch, range_info, x, y, 18, None, False)

        # x-axis label
        self._sketch.set_text_font(TEXT_FONT, LEGEND_TEXT_SIZE)
        self._sketch.set_text_align('center', 'top')
        self._sketch.draw_text((x_end - x)/2, BOTTOM_RECT_HEIGHT - PADDING/3, 'day of the month' )

        # colored squares
        self._sketch.set_rect_mode('center')
        buff = 20
        x_start = BOTTOM_RECT_WIDTH - (BLOCK*5 + buff*5) - PADDING
        y = INFO_RADIUS*3

        x = x_start
        for i in range(len(POINT_COLORS)): 
            color = POINT_COLORS[i]
            self._sketch.set_fill(color)
            self._sketch.draw_rect(x, y, BLOCK, BLOCK)
            x += buff
        
        self._sketch.set_fill(HEADER_COLOR)
        self._sketch.set_text_font(TEXT_FONT, LEGEND_TEXT_SIZE)
        self._sketch.set_text_align('right', 'center')
        self._sketch.draw_text(x_start - BLOCK, y, 'less')
        self._sketch.set_text_align('left', 'center')
        self._sketch.draw_text(x_start + buff*5, y, 'more')

        self._sketch.pop_transform()
        self._sketch.pop_style()

    def interactive_timeline(self): 
        """
        checks if user is hovering over a point on the timeline and draws its info
        """
        self._sketch.push_transform()
        self._sketch.push_style()

        mouse = self._sketch.get_mouse()
        x_coord, y_coord = mouse.get_pointer_x(), mouse.get_pointer_y()

        touching = self.touching_point(x_coord, y_coord)
        if touching: 
            x, y = touching[0] + RADIUS, touching[1] + RADIUS
            day = touching[2]
            count = touching[3]
            
            self.draw_point_highlight(x, y)
            self.draw_count_box(x, y, count, day)

        self._sketch.pop_transform()
        self._sketch.pop_style()
    
    def draw_point_highlight(self, x, y):
        """
        x: integer
        y: integer

        draw a white circle highlight centered at x, y
        """ 
        self._sketch.set_ellipse_mode('center')
        self._sketch.set_stroke_weight(3)
        self._sketch.set_fill(HEADER_COLOR)
        self._sketch.set_stroke(HEADER_COLOR)
        self._sketch.draw_ellipse(x, y, RADIUS*2, RADIUS*2)

    def draw_count_box(self, x, y, count, day): 
        """
        x: integer
        y: integer
        count: integer 
        day: integer

        draw info box with upper left coordinates x, y
        """
        self._sketch.set_rect_mode('corner')
        self._sketch.set_fill(HEADER_COLOR)
        self._sketch.draw_rect(x, y, 85, 40)

        self._sketch.clear_stroke()
        self._sketch.set_fill(BACKGROUND_COLOR)
        self._sketch.set_text_align('left', 'top')
        self._sketch.set_text_font(TEXT_FONT, LEGEND_TEXT_SIZE)

        self._sketch.draw_text(x + TITLE_OFFSET_X/2, y + 5, f'day: {day}')
        self._sketch.draw_text(x + TITLE_OFFSET_X/2, y + 25, f'count: {count}')

    def touching_point(self, x_coord, y_coord): 
        """
        x_coord: integer
        y_coord: integer
        
        return center coordinates, count, day info if x_coord and y_coord are within bounds of a point 
        """
        for i in range(len(self.timeline_points)): 
            if self.timeline_points[i][0] <= x_coord <= self.timeline_points[i][2] and self.timeline_points[i][1] <= y_coord <= self.timeline_points[i][3]: 
                return self.timeline_points[i][0], self.timeline_points[i][1], self.timeline_points[i][4], self.timeline_points[i][5]

graphic = Graphic(data_model)
graphic.draw()


