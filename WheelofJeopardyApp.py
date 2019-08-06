import QCASystem
import gameLogic

import kivy
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from kivy.graphics.transformation import Matrix
from kivy.animation import Animation

# Main colors used in color theme
_COLOR_1 = (199/255, 0, 57/255, 1)
_COLOR_2 = (199/255, 0, 57/255, 1)

_NUM_CATS = 6
_QUES_PER_CAT = 5

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        self.name = 'home'

        self.title = Label(text='Wheel of Jeopardy!!')
        self.title.pos_hint = {'center_x': 0.5, 'top': 1}
        self.title.size_hint = (1, .20)
        self.title.color = (0, 0, 0, 1)
        self.title.bold = True 
        self.title.font_size = 90

        self.play_button = Button()
        self.play_button.text = "PLAY"
        self.play_button.pos_hint = {'center_x': 0.5, 'top': 0.75}
        self.play_button.size_hint = (0.4, 0.2)

        self.edit_button = Button()
        self.edit_button.text = "Edit Questions"
        self.edit_button.pos_hint = {'center_x': 0.5, 'top': 0.35}
        self.edit_button.size_hint = (0.4, 0.2)

        self.add_widget(self.title)
        self.add_widget(self.play_button)
        self.add_widget(self.edit_button)

class GameOptionsScreen(Screen):
    def __init__(self, **kwargs):
        super(GameOptionsScreen, self).__init__(**kwargs)
        self.name = 'options'
        
        self.home_button = Button(text='home')
        self.home_button.size_hint = (1/8, 1/12)
        self.home_button.pos_hint = {'x':0.02, 'y': 0.02}
        self.home_button.background_color = _COLOR_1

        self.start_button = Button(
            text = 'start',
            size_hint = (1/8, 1/12),
            pos_hint = {'right': 0.98, 'y': 0.02},
            background_color = _COLOR_1
        )
        
        self.build_num_teams_drop_down()
        self.build_question_selection_drop_down()
        self.add_widget(self.home_button)
        self.add_widget(self.start_button)
        

    def build_num_teams_drop_down(self):
        MAX_TEAMS = 3
        self.main_button = Button()
        self.main_button.text = "Select Number of Teams"
        self.main_button.size_hint = (0.4, 0.15)
        self.main_button.pos_hint = {'center_x': 0.5, 'top': 0.8}
        self.main_button.font_size = 30
        self.main_button.background_color = _COLOR_1

        self.drop_down = DropDown()  
        for i in range(MAX_TEAMS):
            btn = Button(
                text = f"{i + 1}",
                size_hint_y = None,
                height = 30
            )
            btn.bind(on_press=lambda btn: self.drop_down.select(btn.text))

            self.drop_down.add_widget(btn)

        self.main_button.bind(on_release=self.drop_down.open)
        self.drop_down.bind(
            on_select=lambda instance, x: setattr(self.main_button, 'text', x)
        )
        self.add_widget(self.main_button)

    def build_question_selection_drop_down(self):
        '''
        need to hook this up to QCA system to query
        all the questions that are available
        '''

        # Temp list of random names to simulate QCA querry result
        self.set_list = ['set1', 'set2', 'set3', 'set4', 'set5', 'set6']
        self.question_button = Button()
        self.question_button.text = "Select Question Set"
        self.question_button.size_hint = (0.4, 0.15)
        self.question_button.pos_hint = {'center_x': 0.5, 'top': 0.45}
        self.question_button.font_size = 30
        self.question_button.background_color = _COLOR_1

        self.question_drop_down = DropDown()  
        for name in self.set_list:
            btn = Button(
                text = name,
                size_hint_y = None,
                height = 30
            )
            btn.bind(
                on_press=lambda btn: self.question_drop_down.select(btn.text)
            )
            self.question_drop_down.add_widget(btn)

        self.question_button.bind(on_release=self.question_drop_down.open)
        self.question_drop_down.bind(
            on_select=lambda instance, x: setattr(self.question_button, 'text', x)
        )
        self.add_widget(self.question_button)

class GamePlayScreen(Screen):
    number_of_teams = 3
    team_names = ['team1', 'team1', 'team3']
    team_scores = [0, 0, 0]
    cur_round = 1
    
    def __init__(self, **kwargs):
        super(GamePlayScreen, self).__init__(**kwargs)

        self.build_layout()
        self.add_widget(self.game_play_float_layout)

    def build_layout(self):
        self.game_play_float_layout = RelativeLayout()
        self.size_hint = (1, 1)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.home_button = Button(
            text = 'home',
            size_hint = (1/8, 1/12),
            pos_hint = {'x': 0.02, 'y': 0.02},
            background_color = _COLOR_1
        )
        self.score_label = Label(
            text = f'round {self.cur_round}'
        )

        # holds the scores
        self.box_scores = BoxLayout(
            size_hint = (0.2, 0.2),
            pos_hint = {'left': 0.95, 'top': 0.95},
            orientation = 'vertical'
        )
        self.score_label = Label(
            text = 'Scores',
            bold = True,
            size_hint = (1, 1/3),
            pos_hint = {'top': 1}
        )

        self.build_score_grid()
        self.box_scores.add_widget(self.score_label)
        self.box_scores.add_widget(self.score_grid)
        self.game_play_float_layout.add_widget(self.home_button)
        self.game_play_float_layout.add_widget(self.box_scores)
        
    def build_score_grid(self):
        self.score_grid = GridLayout(
            cols = self.number_of_teams,
            size_hint = (1, 2/3),
            pos_hint = {'bottom': 1}
        )

        for i in range(self.number_of_teams):
            lbl = Label()
            lbl.text = self.team_names[i]
            self.score_grid.add_widget(lbl)

        for i in range(self.number_of_teams):    
            score = Label()
            score.text = f'{self.team_scores[i]}'
            self.score_grid.add_widget(score)

        


        
        
    
    def update_round(self, rnd):
        self.cur_round = rnd
        self.score_label.text = f'round {self.cur_round}'
    
    def update_score(self, team, points):
        pass

class QuestionAnswerButton(Button):
    def __init__(self, **kwargs):
        super(QuestionAnswerButton, self).__init__(**kwargs)
        self.question = 'not assigned'
        self.answer = 'not assigned'
        self.category = 'not assigned'
        self.point_value = ''
        self.text = str(self.point_value)

class QuestionScreen(Screen):
    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)
        self.name = 'questions'
        self.current_question_button = QuestionAnswerButton()

        self.build_necessary_widgets()
        self.build_question_popup()
        self.build_answer_popup()
        self.build_question_grid()

        self.add_widget(self.grid)
        self.add_widget(self.continue_button)

    def build_necessary_widgets(self):
        self.continue_button = Button(
            text = 'continue',
            size_hint = (1/8, 1/12),
            pos_hint = {'x': 0.02, 'y': 0.02},
            background_color = _COLOR_1
        )
        
    def show_question_popup(self, instance):
        self.current_question_button = instance
        self.question_popup.size_hint = (0.5 , 0.5)
        self.question_popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.question_label.size_hint = (1.0, 0.8)
        self.question_label.text_size = self.question_label.size
        self.question_label.text = self.current_question_button.question
        self.question_popup.open()

    def build_question_popup(self):
        self.question_popup = Popup(
            title = "Question",
            size_hint = (0.5, 0.5),
            pos_hint = {'center_x': 0.5, 'bottom': 0.5}
        )
        self.question_float_layout = FloatLayout()
        self.question_label = Label(
            text = '',
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            font_size = 20,
            valign = 'center',
            halign = 'center'
        )
        self.show_answer_button = Button(
            text = 'show answer',
            size_hint = (1/3, 1/6),
            pos_hint = {'center_x': 0.5, 'y': 0.01},
            on_press = self.show_answer_popup,
            background_color = _COLOR_1
        )

        self.question_float_layout.add_widget(self.question_label)
        self.question_float_layout.add_widget(self.show_answer_button)
        self.question_popup.content = self.question_float_layout

    def build_answer_popup(self):
        self.answer_popup = Popup(
            title = "Answer",
            size_hint = (0.5, 0.5),
            pos_hint = {'center_x': 0.5, 'bottom': 1}
        )
        self.answer_float_layout = FloatLayout()
        self.answer_label = Label(
            text = '',
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            font_size = 20,
            valign = 'center',
            halign = 'center'
        )
        self.answer_float_layout.add_widget(self.answer_label)
        self.answer_popup.content = self.answer_float_layout

    def show_answer_popup(self, instance):
        self.question_popup.dismiss()
        self.answer_popup.size_hint = (0.5 , 0.5)
        self.answer_popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.answer_label.size_hint = (1.0, 0.8)
        self.answer_label.text_size = self.answer_label.size
        self.answer_label.text = self.current_question_button.answer
        self.answer_popup.open()

    def build_question_grid(self):
        self.grid = GridLayout(
            size_hint = (0.85, 0.85),
            pos_hint = {'center_x': 0.5, 'center_y': 0.55 },
            cols = _NUM_CATS
        )
        count = 0
        for cat in range(_NUM_CATS):
            cat = Button()
            cat.text = f'A category {count}'
            cat.background_color = _COLOR_1
            cat.bold = True

            self.grid.add_widget(cat)
            for question in range(_QUES_PER_CAT):
                qbtn = QuestionAnswerButton()
                qbtn.point_value = (question + 1) * 100
                qbtn.text = str(qbtn.point_value)
                qbtn.bind(on_press=self.show_question_popup)
                self.grid.add_widget(qbtn)
                count += 1
        
class EditQuestionScreen(Screen):
    def __init__(self, **kwargs):
        super(EditQuestionScreen, self).__init__(**kwargs)
        self.name = 'edit'
        self.questoin_dictionary = {}

        self.grid = GridLayout()
        self.grid.orientation = 'horizontal'
        self.grid.size_hint = (0.8, 0.8)
        self.grid.pos_hint = {'center_x': 0.5, 'center_y': 0.55 }
        self.grid.cols = _NUM_CATS
        self.build_question_grid()

        self.home_button = Button(
            text = 'home',
            size_hint = (1/8, 1/12),
            pos_hint = {'x': 0.02, 'y': 0.02},
            background_color = _COLOR_1
        )

        self.save_button = Button(
            text = 'save',
            size_hint = (1/8, 1/12),
            pos_hint = {'right': 0.98, 'y': 0.02},
            background_color = _COLOR_1
        )

        self.build_edit_entry_popup()

        self.add_widget(self.grid)
        self.add_widget(self.home_button)
        self.add_widget(self.save_button)

    def build_edit_entry_popup(self):
        self.edit_entry_popup = Popup(
            size_hint = (0.5, 0.5),
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            title = "Enter Question & Answer"
        )
        self.edit_float_layout = FloatLayout(
            size_hint = (1, 1), 
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
        )

        self.question_entry = TextInput(
            multiline = True,
            size_hint = (0.9, 0.30),
            pos_hint = {'center_x': 0.5, 'center_y': 0.75},
            hint_text_color = (0, 0, 0, 0.5),
            hint_text = "type question here"
        )

        self.answer_entry = TextInput(
            multiline = True,
            size_hint = (0.9, 0.30),
            pos_hint = {'center_x': 0.5, 'center_y': 0.35},
            hint_text_color = (0, 0, 0, 0.5),
            hint_text = "type answer here"
        )

        self.apply_button = Button(
            text = 'apply',
            size_hint = (1, 0.1),
            pos_hint = {'center_x': 0.5, 'y': .02}
        )

        self.edit_float_layout.add_widget(self.question_entry)
        self.edit_float_layout.add_widget(self.answer_entry)
        self.edit_float_layout.add_widget(self.apply_button)
        self.edit_entry_popup.content = self.edit_float_layout

    
    def show_edit_entry_popup(self, instance):
        self.current_selection = instance
        self.edit_entry_popup.open()

    def add_question_ans_to_qca(self, instance):
        index = int(instance.point_value / 100 )
        self.questoin_dictionary[instance.category][index] = (
            instance.answer,
            instance.question
        )        

    def build_question_grid(self):
        for cat in range(_NUM_CATS):
            cat = Button()
            cat.text = 'A category'
            cat.bold = True
            cat.background_color = _COLOR_1
            cat.disable = True

            self.grid.add_widget(cat)
            for question in range(_QUES_PER_CAT):
                qbtn = QuestionAnswerButton()
                qbtn.point_value = (question + 1) * 100
                qbtn.text = str(qbtn.point_value)
                qbtn.bind(on_press=self.show_edit_entry_popup)
                self.grid.add_widget(qbtn)


## ROOT WIDGET
class WheelofJeopardy(ScreenManager):
    def __init__(self, **kwargs):
        super(WheelofJeopardy, self).__init__(**kwargs)

        self.home = HomeScreen()
        self.game_options = GameOptionsScreen()
        self.game_play = GamePlayScreen()
        self.edit = EditQuestionScreen()
        self.questions = QuestionScreen()

        # self.populate_question_board()

        self.add_widget(self.home)
        self.add_widget(self.game_options)
        self.add_widget(self.questions)
        self.add_widget(self.game_play)
        self.add_widget(self.edit)

        # Setup buttons from screen transitions
        self.home.play_button.bind(on_press=self.go_to_options)
        self.home.edit_button.bind(on_press=self.go_to_edit)
        self.edit.home_button.bind(on_press=self.go_home)
        self.game_options.home_button.bind(on_press=self.go_home)
        self.game_options.start_button.bind(on_press=self.go_to_game_play)
        self.game_play.home_button.bind(on_press=self.go_to_question)
        self.questions.continue_button.bind(on_press=self.go_to_game_play)

        

    def go_to_options(self, instance):
        self.switch_to(self.game_options)
    def go_home(self, instance):
        self.switch_to(self.home)
    def go_to_game_play(self, instance):
        self.switch_to(self.game_play)
    def go_to_edit(self, instance):
        self.switch_to(self.edit)
    def go_to_question(self, instance):
        self.switch_to(self.questions)

    def populate_question_board(self):
        self.qca_system = QCASystem.QCASystem('qca')
        self.qca_system.loadDefaultQCA()
        self.qca = self.qca_system.db.getQCA()

        keys = list(self.qca.keys())
        key_count = 0
        q_count = 0
        for child in self.questions.grid.children:
            if type(child) == type(Button()):
                child.text = keys[key_count]
                key_count += 1 
            else:
                key = keys[key_count]
                child.category = key
                child.question = self.qca[key][q_count][1]
                child.answer = self.qca[key][q_count][0]
                q_count += 1

            if q_count == _QUES_PER_CAT - 1:
                q_count = 0    

class WheelofJeopardyApp(App):
    def build(self):
        self.root = WheelofJeopardy()
        self.root.bind(
            size=self._update_rect, 
            pos=self._update_rect
        )
        
        with self.root.canvas.before:
            Color(163/255, 228/255, 215/255, 1)
            self.rect = Rectangle(
                size=self.root.size,
                pos=self.root.pos
            )

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        self.root.current_screen.size = instance.size
        self.root.current_screen.pos = instance.pos
        self.root.questions.question_popup.size = (
            instance.size[0]/2, 
            instance.size[1]/2
        )
        self.root.questions.answer_popup.size = (
            instance.size[0]/2, 
            instance.size[1]/2
        )
        if self.root.current_screen == self.root.game_play:
            self.root.game_play.animate()

if __name__ == "__main__":
    WheelofJeopardyApp().run()