"""Visualization of employment data from the US census. 

Assignment 9 submission for Stat 198: Interactive Data Science course at UC Berkeley.

Author: Vy Ho
License: BSD-3-Clause
"""
from sketchingpy import Sketch2D
import data_model

WIDTH = 1000
HEIGHT = 1200
BACKGROUND_COLOR = '#FFFFFF'

DATA  = 'C:/Users/vyh04/sp25/stat198/job-satisfaction/income-gaps.csv'
OCCUP_COLORS = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']
WAGE_COLOR = '#2da1e2'
FONT = 'PublicSans-Regular.otf'

DARK_TEXT_COLOR = '#333333'
LIGHT_TEXT_COLOR = '#666666'

OVERLAY_COLOR = '#1d1d35'
OCCUPATION_AXIS_COLOR = '#E0E0E0'
GAP_COLOR = '#505050'

LEFT_PAD = 20
RIGHT_PAD = 20
TOP_PAD = 60
BOTTOM_PAD = 40
GUTTER_PAD = 10

TOP_AXIS_HEIGHT = 14
BOTTOM_AXIS_HEIGHT = 40

START_X_COLLEGE = LEFT_PAD
END_X_COLLEGE = START_X_COLLEGE + 400

START_Y_COLLEGE = TOP_PAD 
END_Y_COLLEGE = HEIGHT - BOTTOM_PAD

START_X_WAGE = END_X_COLLEGE + 20
START_Y_WAGE = TOP_PAD
END_X_WAGE = START_X_WAGE + 500
END_Y_WAGE = HEIGHT - BOTTOM_PAD

TOTAL_WAGEDIFF = 20

class WageScale: 
# Code adapted from Sam Pottinger
# Source: https://github.com/sampottinger/census-example-sketchingpy/blob/main/assignment_9.py
# Original license: BSD-3-Clause
    def __init__(self, dataset):
        """Create a new horizontal scale for occupation groups (docc03).

        Args:
            dataset: data_model.Dataset to use in constructing this scale.
        """
        self._occupations = sorted(dataset.get_docc03_vals())
        self._max_wage= TOTAL_WAGEDIFF
        self._width = END_X_WAGE - START_X_WAGE
    
    
    def get_position(self, wage):
        """Get the horizontal position for an unemployment level.

        Args:
            unemployment: A unemp value (0 - 100) from data_model to convert.

        Returns:
            float: Horizontal pixel position within START_X_UNEMPLOYMENT and
                END_X_UNEMPLOYMENT.
        """
        percent = wage / self._max_wage
        return percent * self._width

class OccupationScale:
# Code adapted from Sam Pottinger
# Source: https://github.com/sampottinger/census-example-sketchingpy/blob/main/assignment_9.py
# Original license: BSD-3-Clause
# Modifications: WageScale adapted to for occupations. 

    def __init__(self, dataset):
        """Create a new vertical scale for occupation groups (docc03).

        Args:
            dataset: data_model.Dataset to use in constructing this scale.
        """
        self._occupations = sorted(dataset.get_docc03_vals())
        self._height = END_Y_COLLEGE - START_Y_COLLEGE

    def get_position(self, occupation):
        """Get the vertical position for an occupation.

        Args:
            occupation: String occuation name matching docc03.

        Returns:
            float: Vertical position which is expected to be within
                START_Y_COLLEGE and END_Y_COLLEGE.
        """
        index = self._occupations.index(occupation)
        index_offset = index + 0.5
        percent = index_offset / len(self._occupations)
        return self._height * percent

class Graphic: 
    """Draws the entire graphic."""
    def __init__(self, sketch, occup, wage):
        self._sketch = sketch
        self.occup = occup
        self.wage = wage
        self._width  = WIDTH
    
    def draw(self): 
        """Draws each component"""
        self._sketch.clear(BACKGROUND_COLOR)

        self.occup.draw()
        self.wage.draw()
        
        self.draw_title()
        self._sketch.show()
        
    def draw_title(self):
        """Draws the title."""
        self._sketch.clear_stroke()
        self._sketch.set_fill(DARK_TEXT_COLOR)
        self._sketch.set_text_align('center')
        self._sketch.set_text_font(FONT, 20)
        self._sketch.draw_text(self._width/2, 30, 'Education and Gender Wage Differences across Occupation')

class MedianWageByGender:
    """Draws the Median Wage component of the graphic."""
    
    def __init__(self, sketch, data, vert, horz):
        self._sketch = sketch
        self._data = data
        self.vert_scale = vert
        self.horiz_scale = horz
        self._width = END_X_WAGE - START_X_WAGE
        self._total = TOTAL_WAGEDIFF
    
    def draw(self): 
        self._sketch.push_transform()
        self._sketch.push_style()
        
        self.draw_axis()
        self.draw_bars()
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
    
    def draw_axis(self): 
        """Draws the axis."""
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.translate(START_X_WAGE, END_Y_WAGE + 10)

        self._sketch.clear_stroke()
        self._sketch.set_fill(DARK_TEXT_COLOR)
        self._sketch.set_text_align('center', 'bottom')
        self._sketch.set_text_font(FONT, 12)

        wage_width = self._total
        wage_bins = range(0, wage_width + 1, 5)
        for wage in wage_bins:
            x = self.horiz_scale.get_position(wage)
            self._sketch.draw_text(x, 0, f'${wage}')

        self._sketch.draw_text(self.horiz_scale.get_position(10), 20, 'Dollar Median Wage Difference $(Male - Female)')

        self._sketch.pop_style()
        self._sketch.pop_transform()
    
    def draw_bars(self):
        """Draws each horizontal bar representing wage difference between men and women for all occupations."""
        self._sketch.push_transform()
        self._sketch.push_style()
        # for each occupation, draw occupation
        self._sketch.translate(START_X_WAGE, START_Y_WAGE)

        for occupation in self._data.get_docc03_vals():
            self.draw_occupation(occupation)
        
        self._sketch.pop_style()
        self._sketch.pop_transform()

    def draw_occupation(self, occupation):
        """Given an occupation, draws the corresponding horizontal bar representing wage difference/"""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        y = self.vert_scale.get_position(occupation)
        self._sketch.translate(0, y)
        
        query = data_model.Query()
        query.set_docc03(occupation)
        
        query.set_female(False)
        male_wage = self._data.get_wageotc(query)
        
        query.set_female(True)
        female_wage = self._data.get_wageotc(query)
        
        wage_dif = male_wage - female_wage
        width = (wage_dif/self._total)*self._width - 1
        
        self._sketch.clear_stroke()
        self._sketch.set_rect_mode('corner')
        self._sketch.set_fill(WAGE_COLOR)
        
        if width < 0: 
            self._sketch.translate(width, 0)
            self._sketch.draw_rect(0, 0, abs(width), 20)
            self._sketch.translate(-width, 0)
        else:
            self._sketch.draw_rect(0, 0, width, 20)
        
        self._sketch.set_text_font(FONT, 12)
        self._sketch.set_fill(OVERLAY_COLOR)

        self._sketch.set_text_align('left', 'center')
        wage_diff_label =f'${round(wage_dif, 2)}'
        self._sketch.draw_text(1, 6, wage_diff_label)
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
        
class CollegeEducByOccupation: 
    """Draws college education portion of the graphic."""
    def __init__(self, sketch, data, vert): 
        self._sketch = sketch
        self._data = data
        self._width = END_X_COLLEGE - START_X_COLLEGE
        self.vert_scale = vert
        self.colors = OCCUP_COLORS

    def draw(self):
        self._sketch.push_transform()
        self._sketch.push_style()
        
        self.draw_axis()
        self.draw_bars()
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
        
    def draw_axis(self): 
        """Draws the axis."""
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.translate(START_X_COLLEGE, START_Y_COLLEGE)
        
        educ_cat = sorted(self._data.get_educ_vals())
        offset =  (1 / len(educ_cat)) * self._width
        
        self._sketch.clear_stroke()
        self._sketch.set_text_font(FONT, 9)
        self._sketch.set_rect_mode('corner')
        
        x = 0 + offset / 2
        for educ, color in zip(educ_cat, self.colors):
            
            self._sketch.set_fill(color)
            self._sketch.draw_rect(x, 0, 10, 10)
            
            self._sketch.set_fill(DARK_TEXT_COLOR)
            self._sketch.set_text_align('center')
            self._sketch.draw_text(x, -10, f'{educ}')
            x = x + offset
        
        self._sketch.clear_stroke()
        self._sketch.set_text_font(FONT, 12)
        self._sketch.set_fill(DARK_TEXT_COLOR)
        self._sketch.set_text_align('center')
        self._sketch.draw_text(self._width/2, self.vert_scale._height + 30, f'Education Level Distribution')
        
        self._sketch.pop_style()
        self._sketch.pop_transform() 
    
    def draw_bars(self):
        """Draws the horizonal bar for each occupation representing education history."""
        # for each occupation, draw occupation
        self._sketch.push_transform()
        self._sketch.push_style()
        
        self._sketch.translate(START_X_COLLEGE, START_Y_COLLEGE)
        
        for occupation in self._data.get_docc03_vals(): 
            print(occupation)
            self.draw_occupation(occupation)
        
        self._sketch.pop_style()
        self._sketch.pop_transform()

    def draw_occupation(self, occupation):
        """Given an occupation, draws a bar representing the distribution of education history."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        y = self.vert_scale.get_position(occupation)
        self._sketch.translate(0, y)
        
        query = data_model.Query()
        query.set_docc03(occupation)
        
        # gets counts for each educ cat and converts to percentages
        educ_counts = []
        for educ in sorted(self._data.get_educ_vals()): 
            query.set_educ(educ)
            educ_counts.append(self._data.get_size(query))
        
        total = sum(educ_counts)
        percents = [x/total for x in educ_counts]
        
        # draws percentage bar
        self._sketch.clear_stroke()
        self._sketch.set_rect_mode('corner')
        
        self._sketch.set_text_font(FONT, 12)
        self._sketch.set_fill(LIGHT_TEXT_COLOR)
        self._sketch.set_text_align('right', 'bottom')
        occupation_label = occupation.replace(' occupations', '')
        self._sketch.draw_text(self._width, -1, occupation_label)
        
        prev_x = 0
        for percent_educ, color in zip(percents, self.colors): 
            self._sketch.set_fill(color)
            width = self._width * percent_educ - 1
            self._sketch.draw_rect(prev_x, 0, width, 20)
            prev_x = prev_x + width
        
        self._sketch.pop_style()
        self._sketch.pop_transform()

sketch = Sketch2D(WIDTH, HEIGHT)
dataset = data_model.load_from_file(DATA)

vert = OccupationScale(dataset)
horz = WageScale(dataset)
graphic = Graphic(sketch, CollegeEducByOccupation(sketch, dataset, vert), MedianWageByGender(sketch, dataset, vert, horz))

graphic.draw()
