"""Visualization of employment data from the US census. 

Assignment 10 submission for Stat 198: Interactive Data Science course at UC Berkeley.

Author: Vy Ho
License: BSD-3-Clause
"""
from sketchingpy import Sketch2D
import data_model

WIDTH = 1000
HEIGHT = 1600

DATA  = 'income-gaps.csv'

#bar graph colors
OCCUP_COLORS = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']
WAGE_COLOR = '#2da1e2'
M_AGE_COLOR = '#1f719e'
F_AGE_COLOR = '#81c7ee'
LIGHT_AXIS = '#a3a3a3'

# text settings
FONT = 'PublicSans-Regular.otf'
DARK_TEXT_COLOR = '#000000'
LIGHT_TEXT_COLOR = '#666666'
OVERLAY_COLOR = '#1d1d35'

LEFT_PAD = 20
RIGHT_PAD = 20
TOP_PAD = 60
BOTTOM_PAD = 40
OFFSET_PAD = 10


START_X_COLLEGE = LEFT_PAD
END_X_COLLEGE = START_X_COLLEGE + 400

START_Y_COLLEGE = TOP_PAD 
END_Y_COLLEGE = START_Y_COLLEGE + 1150

BOX_SIZE = 10

START_X_WAGE = END_X_COLLEGE + 20
END_X_WAGE = START_X_WAGE + 500

START_Y_WAGE = TOP_PAD
END_Y_WAGE = START_Y_WAGE + 1150

AXIS_PAD = 10

TOTAL_WAGEDIFF = 18

START_X_UNEMP = LEFT_PAD
END_X_UNEMP = START_X_UNEMP + 400

START_Y_UNEMP = END_Y_COLLEGE + OFFSET_PAD + 40
END_Y_UNEMP = HEIGHT - BOTTOM_PAD

UNEMP_BAR_HEIGHT = END_Y_UNEMP - START_Y_UNEMP - 40
BAR_WIDTH = 40

START_X_AGE = END_X_COLLEGE + 20
END_X_AGE  = START_X_AGE + 500

START_Y_AGE = START_Y_UNEMP
END_Y_AGE = END_Y_UNEMP

class NumericScale: 
    """Creates a numeric scale for a given dataset"""
    def __init__(self, dataset, max_length): 
        self.max_length = max_length
    
    def get_position(self, value): 
        """Given a value, return the percentage of that value according to the maximum possible"""
        percent = value / self.max_length
        return percent* self._length
        
class WageScale(NumericScale): 
    """Creates a scale for the wage difference."""
    def __init__(self, dataset):
        super().__init__(dataset, TOTAL_WAGEDIFF)
        self._length = END_X_WAGE - START_X_WAGE
    
class CategoryScale:
    """Creates a scale for the categorical data."""
    def __init__(self, dataset, category): 
        self.categories = sorted(eval(f'dataset.get_{category}_vals()'))
        
    def get_position(self, category): 
        index = self.categories.index(category)
        index_offset = index + 0.5
        percent = index_offset / len(self.categories)
        return percent * self._length

class AgeScale(CategoryScale): 
    """Creates a scale for the age categories."""
    def __init__(self, dataset, category):
        super().__init__(dataset, category)
        
        # rearrange so the categories are in age order
        less_25 = self.categories[-1]
        self.categories= [less_25] + self.categories[:-1]
        
        self._length = END_X_AGE - START_X_AGE
        
        # sum for percentages 
        all_counts = []
        q = data_model.Query()
        
        for gender in [False, True]: 
            q.set_female(gender)
            counts = []
            for a in self.categories: 
                q.set_age(a)
                counts.append(dataset.get_size(q))
            all_counts.append(counts)
        
        self.m_total = sum(all_counts[0])
        self.f_total = sum(all_counts[1])
        
class EducScale(CategoryScale): 
    """Creates a scale for the education categories."""
    def __init__(self, dataset, category): 
        super().__init__(dataset, category)

        # rearrange from some educational history to advanced. 
        self.categories = ['Less than high school', 'High school', 'Some college', 'College', 'Advanced']

        self._length = END_X_UNEMP - START_X_UNEMP


class OccupationScale(CategoryScale):
    """Creates a scale for the different ocupations."""

    def __init__(self, dataset, category):
        super().__init__(dataset, category)
        self._length = END_Y_COLLEGE - START_Y_COLLEGE - AXIS_PAD

class Graphic: 
    """Main class that draws each component of the graphic."""
    
    def __init__(self, sketch, occup, wage, educ, age):
        self._sketch = sketch
        self.occup = occup
        self.wage = wage
        self.educ = educ
        self.age = age
        self._width = WIDTH
    
    def draw(self): 
        """Draws each subgraphic."""
        self.occup.draw()
        self.wage.draw()
        self.educ.draw()
        self.age.draw()
        
        self.draw_title()
        self._sketch.show()
        
    def draw_title(self):
        """Draws the title of each subgraphic."""
        self._sketch.clear_stroke()
        self._sketch.set_fill(DARK_TEXT_COLOR)
        self._sketch.set_text_align('center')
        self._sketch.set_text_font(FONT, 20)
        self._sketch.draw_text(self._width/2, TOP_PAD/2, 'Education, Gender Wage, and Unemployment Differences across Occupation')

class MedianWageByGender:
    """Draws the median wage difference subgraphic."""
    def __init__(self, sketch, data, vert, horz):
        self._sketch = sketch
        self._data = data
        self.vert_scale = vert
        self.horiz_scale = horz
        
        self._width = END_X_WAGE - START_X_WAGE
        self._total = TOTAL_WAGEDIFF
    
    def draw(self): 
        """Draws each component."""
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

        self._sketch.translate(START_X_WAGE, END_Y_WAGE)
        
        # draw line across bottom
        self._sketch.clear_stroke()
        self._sketch.set_stroke(LIGHT_TEXT_COLOR)
        self._sketch.draw_line(0, int(-AXIS_PAD), int(self._width), int(-AXIS_PAD))

         # draw bins
        self._sketch.clear_stroke()
        self._sketch.set_fill(LIGHT_TEXT_COLOR)
        self._sketch.set_text_align('center', 'top')
        self._sketch.set_text_font(FONT, 12)
        
        wage_width = self._total
        wage_bins = range(0, wage_width + 1, 5)
        for wage in wage_bins:
            x = self.horiz_scale.get_position(wage)
            self._sketch.draw_text(x, 0, f'${wage}')
        
        # sub graphic title
        self._sketch.set_fill(OVERLAY_COLOR)
        self._sketch.set_text_align('center', 'top')
        self._sketch.draw_text(self.horiz_scale.get_position(self._total / 2), AXIS_PAD*2, 'Dollar Median Wage Difference $(Male - Female)')

        self._sketch.pop_style()
        self._sketch.pop_transform()
    
    def draw_bars(self):
        """Draws each horizontal bar graph representing wage difference."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        self._sketch.translate(START_X_WAGE, START_Y_WAGE)
        
        # for each occupation, draw occupation
        for occupation in self._data.get_docc03_vals():
            self.draw_occupation(occupation)
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
        

    def draw_occupation(self, occupation):
        """Given an occupation, draws the bar graph of the wage difference."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        y = self.vert_scale.get_position(occupation)
        self._sketch.translate(0, y)
        
        # get wage dif values
        query = data_model.Query()
        query.set_docc03(occupation)
        
        query.set_female(False)
        male_wage = self._data.get_wageotc(query)
        
        query.set_female(True)
        female_wage = self._data.get_wageotc(query)
        
        wage_dif = male_wage - female_wage
        width = (wage_dif/self._total)*self._width - 1
        
        # draw bin
        self._sketch.clear_stroke()
        self._sketch.set_rect_mode('corner')
        self._sketch.set_fill(WAGE_COLOR)
        if width < 0: 
            self._sketch.translate(width, 0)
            self._sketch.draw_rect(0, 0, abs(width), 20)
            self._sketch.translate(-width, 0)
        else:
            self._sketch.draw_rect(0, 0, width, 20)
        
        # draw wage dif text
        self._sketch.set_text_font(FONT, 12)
        self._sketch.set_fill(OVERLAY_COLOR)
        self._sketch.set_text_align('left', 'top')
        wage_diff_label =f'${round(wage_dif, 2)}'
        self._sketch.draw_text(1, 6, wage_diff_label)
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
        
class CollegeEducByOccupation: 
    """Draws the college education graphic."""
    def __init__(self, sketch, data, vert): 
        self._sketch = sketch
        self._data = data
        self._width = END_X_COLLEGE - START_X_COLLEGE
        self.vert_scale = vert
        self.colors = OCCUP_COLORS

    def draw(self):
        """Draws the graphic."""
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
        
        # draw color key 
        educ_cat = sorted(self._data.get_educ_vals())
        offset =  (1 / len(educ_cat)) * self._width
        
        self._sketch.clear_stroke()
        self._sketch.set_text_font(FONT, 9)
        self._sketch.set_rect_mode('corner')
        
        x = 0 + offset / 2
        for educ, color in zip(educ_cat, self.colors):
            self._sketch.set_fill(color)
            self._sketch.draw_rect(x, 0, BOX_SIZE, BOX_SIZE)
            
            self._sketch.set_fill(LIGHT_TEXT_COLOR)
            self._sketch.set_text_align('center')
            self._sketch.draw_text(x, -10, f'{educ}')
            x = x + offset
        
        # draw percentage scale
        self._sketch.clear_stroke()
        self._sketch.set_stroke(LIGHT_TEXT_COLOR)
        self._sketch.set_stroke_weight(1)
        print(self._width*0.10)
        self._sketch.draw_line(0, int(self.vert_scale._length), int(self._width*0.10), int(self.vert_scale._length))
        
        self._sketch.clear_stroke()
        self._sketch.set_text_font(FONT, 12)
        self._sketch.set_text_align('left', 'top')
        self._sketch.draw_text(0, self.vert_scale._length + AXIS_PAD, '10 %')
        
        # subgraphic title
        self._sketch.clear_stroke()
        self._sketch.set_text_font(FONT, 12)
        self._sketch.set_fill(DARK_TEXT_COLOR)
        self._sketch.set_text_align('center')
        self._sketch.draw_text(self._width/2, self.vert_scale._length + 40, f'Education Level Distribution')
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
                    
    
    def draw_bars(self):
        """Draws all bars."""
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
        """Given an occupation, draws the corresponding bar graph."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        y = self.vert_scale.get_position(occupation)
        self._sketch.translate(0, y)
        
        query = data_model.Query()
        query.set_docc03(occupation)
        
        # gets counts for each educ category and converts to percentages
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

class UnempByEduc: 
    """Draws the unemployment rates subgraphic."""
    def __init__(self, sketch, data, horz):
        self._sketch = sketch
        self._data = data
        self._max_bar_height = UNEMP_BAR_HEIGHT
        self._bar_width = BAR_WIDTH
        self._width = END_X_UNEMP - START_X_UNEMP
        self._bar_y = END_Y_UNEMP - START_Y_UNEMP - 20
        self.horiz_scale = horz
        self.colors = OCCUP_COLORS
        
    def draw(self): 
        """Draws the graphic."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        self._sketch.translate(START_X_UNEMP, START_Y_UNEMP)
        
        self.draw_axis()
        self.draw_bars()
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
    
    def draw_bars(self): 
        """Draws the bar for each education category."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        for educ, color in zip(self._data.get_educ_vals(), self.colors): 
            self.draw_educ(educ, color)
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
    
    def draw_educ(self, educ, color):
        """Given an education level, draws the bar."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        x = self.horiz_scale.get_position(educ)
        self._sketch.translate(x, 0)
        
        query = data_model.Query()
        query.set_educ(educ)
        
        #bar height
        unemp = self._data.get_unemp(query) / 100
        bar_height = (unemp/0.25) * self._max_bar_height
        
        #draw bar
        self._sketch.clear_stroke()
        self._sketch.set_rect_mode('corner')
        self._sketch.set_fill(color)
        self._sketch.draw_rect(0, self._bar_y - bar_height, self._bar_width, bar_height)
        
        #add percentage
        self._sketch.set_fill(LIGHT_TEXT_COLOR)
        self._sketch.set_text_font(FONT, 12)
        self._sketch.set_text_align('left', 'bottom')
        self._sketch.draw_text(0, self._bar_y - bar_height, f'{round(unemp*100, 2)}%')
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
        
    def draw_axis(self): 
        """Draws the axis."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        # draw y-axis
        self._sketch.clear_stroke()
        self._sketch.set_stroke(LIGHT_TEXT_COLOR)
        self._sketch.set_stroke_weight(1)
        self._sketch.draw_line(int(AXIS_PAD/2), 0, int(AXIS_PAD/2), int(self._bar_y))
        
        # draw bins
        percent_bins = range(0, 26, 5)
        
        self._sketch.set_fill(LIGHT_TEXT_COLOR)
        self._sketch.set_text_font(FONT, 12)
        self._sketch.set_text_align('right', 'center')
        for percent in percent_bins: 
            self._sketch.clear_stroke()
            self._sketch.set_fill(LIGHT_TEXT_COLOR)
            self._sketch.draw_text(0, self._bar_y - (percent/25)*self._max_bar_height, str(percent))
            
            if percent:
                self._sketch.set_stroke(LIGHT_AXIS)
                self._sketch.set_stroke_weight(1)
                y_pos = int(self._bar_y - (percent//25)*self._max_bar_height)
                self._sketch.draw_line(0, y_pos, END_X_AGE, y_pos)
                print(percent)
        
        # subgraphic title
        self._sketch.clear_stroke()
        self._sketch.set_fill(DARK_TEXT_COLOR)
        self._sketch.set_text_align('center', 'bottom')
        self._sketch.draw_text(self._width/2, self._bar_y + 30, 'Unemployment Rates')
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
        

class AgeDistribution: 
    """Draws the age distribution subgraphic."""
    def __init__(self, sketch, data, horz):
        self._sketch = sketch
        self._data = data
        self._max_bar_height = UNEMP_BAR_HEIGHT
        self._bar_width = BAR_WIDTH
        self._width = END_X_AGE - START_X_AGE
        self._bar_y = END_Y_AGE - START_Y_AGE - 20
        self.horiz_scale = horz
        
    def draw(self): 
        """Draws the graphic."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        self._sketch.translate(START_X_AGE, START_Y_AGE)
        self.draw_bars()
        self.draw_axis()
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
        
    def draw_bars(self):
        """Draws the bar for each age group."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        for age in sorted(self._data.get_age_vals()): 
            self.draw_age(age)
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
        
    def draw_age(self, age):
        """Given an age, draws the bar graph."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        x = self.horiz_scale.get_position(age)
        self._sketch.translate(x, 0)
        
        # get male, female percents
        query = data_model.Query()
        query.set_age(age)
        
        query.set_female(False)
        male_percent = self._data.get_size(query) / self.horiz_scale.m_total
        
        query.set_female(False)
        female_percent = self._data.get_size(query) / self.horiz_scale.f_total
        
        male_bar_height = (male_percent/0.25) * self._max_bar_height
        female_bar_height = (female_percent/0.25) * self._max_bar_height
        
        # draw bars
        self._sketch.clear_stroke()
        self._sketch.set_rect_mode('corner')
        
        self._sketch.set_fill(M_AGE_COLOR)
        self._sketch.draw_rect(0, self._bar_y - male_bar_height, self._bar_width/2, male_bar_height)
        self._sketch.set_fill(F_AGE_COLOR)
        self._sketch.draw_rect(0 + self._bar_width/2, self._bar_y - female_bar_height, self._bar_width/2, female_bar_height)
        
        # draw percentage
        self._sketch.set_fill(LIGHT_TEXT_COLOR)
        self._sketch.set_text_font(FONT, 12)
        self._sketch.set_text_align('left', 'bottom')
        self._sketch.draw_text(0, self._bar_y - male_bar_height, f'{round(male_percent*100)}%')
        self._sketch.draw_text(0 + self._bar_width/2, self._bar_y - female_bar_height, f'{round(female_percent*100)}%')
        
        # draw bar label
        self._sketch.set_text_align('left', 'top')
        self._sketch.draw_text(0, self._bar_y + AXIS_PAD / 2, age)
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
        
        
    def draw_axis(self):
        """Draws the axis."""
        self._sketch.push_transform()
        self._sketch.push_style()
        
        # key 
        self._sketch.clear_stroke()
        self._sketch.set_text_font(FONT, 9)
        self._sketch.set_rect_mode('corner')
        
        offset = 40
        x, y = self.horiz_scale._length - 1.5*offset, 0 
        for gender, color in zip(['Male', 'Female'], [M_AGE_COLOR, F_AGE_COLOR]):
            self._sketch.set_fill(color)
            self._sketch.draw_rect(x, y, BOX_SIZE, BOX_SIZE)
            
            self._sketch.set_fill(LIGHT_TEXT_COLOR)
            self._sketch.set_text_align('center')
            self._sketch.draw_text(x, y-10, f'{gender}')
            x = x + offset
        
        # subgraphic title

        self._sketch.clear_stroke()
        self._sketch.set_fill(DARK_TEXT_COLOR)
        self._sketch.set_text_font(FONT, 12)
        self._sketch.set_text_align('center', 'bottom')
        self._sketch.draw_text(self._width/2, self._bar_y + 30, 'Age Distribution')
        
        self._sketch.pop_style()
        self._sketch.pop_transform()
        

sketch = Sketch2D(WIDTH, HEIGHT)
sketch.clear('#FFFFFF')

dataset = data_model.load_from_file(DATA, sketch=sketch)

vert = OccupationScale(dataset, 'docc03')
horz1 = WageScale(dataset)
horz2 = EducScale(dataset, 'educ')
horz3 = AgeScale(dataset, 'age')
graphic = Graphic(sketch, CollegeEducByOccupation(sketch, dataset, vert), 
                            MedianWageByGender(sketch, dataset, vert, horz1), 
                            UnempByEduc(sketch, dataset, horz2), 
                            AgeDistribution(sketch, dataset, horz3))

graphic.draw()

# graphic._sketch.save_image('')
