import QCASystem
import gameLogic
import QAL
import player

import random
import copy
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
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
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
        # self.build_question_selection_drop_down()
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
            btn.bind(on_press=self.get_team_names)

            self.drop_down.add_widget(btn)

        self.main_button.bind(on_release=self.drop_down.open)
        self.drop_down.bind(
            on_select=lambda instance, x: setattr(self.main_button, 'text', x)
        )
        self.add_widget(self.main_button)

    def get_team_names(self, instance):
        self.drop_down.select(instance.text)
        try:
            self.team_name_grid.clear_widgets()
        except:
            self.team_name_grid = GridLayout()
            self.add_widget(self.team_name_grid)
    
        self.team_name_grid.rows = int(instance.text)
        self.team_name_grid.size_hint = (0.3 , 0.1 * int(instance.text))
        self.team_name_grid.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        for i in range(int(instance.text)):
            text = TextInput()
            text.hint_text = (f"Enter Team {i + 1} name")
            self.team_name_grid.add_widget(text)


    def update_team_names(self):
        children = self.team_name_grid.children
        self.parent.game_play.team_names = []
        self.parent.game_play.teams = []
        for child in children:
            self.parent.game_play.team_names.append(child.text)

        # make players:
        for child in children:
            plyr = player.player(f'{child.text}')
            self.parent.game_play.teams.append(plyr)
        
        self.parent.game_play.number_of_teams = len(self.parent.game_play.teams)

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

class MyLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        self.bkg_color = _COLOR_1
        with self.canvas.before:
            Color(
                self.bkg_color[0],
                self.bkg_color[1], 
                self.bkg_color[2], 
                0.25
            )
            Rectangle(pos=self.pos, size=self.size)

class GamePlayScreen(Screen):
    number_of_teams = 3
    team_names = ['team1', 'team2', 'team3']
    teams = []
    round1Scores = []
    cur_round = 1
    spins = 0
    qca_dict = {}
    gLogic = gameLogic.gameLogic()
    turn = 0 #integer from 0 - len(teams) - 1 indicating turn
    
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
        self.question_button = Button(
            text = 'go to questions',
            size_hint = (1/8, 1/12),
            pos_hint = {'right': 0.98, 'y': 0.02},
            background_color = _COLOR_1
        )

        self.turn_label = Label(
            text = "team 1",
            size_hint = (1/8, 1/12),
            pos_hint = {'top': 0.91, 'right': 0.95},
            color = _COLOR_1
        )

        self.free_turn_button = Button(
            text = "free turns",
            size_hint = (1/2, 1/10),
            pos_hint = {'y': 0.05, 'center_x': 0.5},
            background_color = _COLOR_1,
            on_press = self.update_free_turn_btn,
            disabled = True
        )

        # holds the scores
        self.box_scores = BoxLayout(
            size_hint = (0.2, 0.2),
            pos_hint = {'right': .25, 'top': 0.95},
            orientation = 'vertical',
            spacing = 5
        )
        self.score_label = MyLabel(
            text = 'Scores',
            bold = True,
            size_hint = (1, 1/3),
            pos_hint = {'top': 1}, 
            color = (0, 0, 0, 1)
        )

        self.round_label = Label(
            text = f'round {self.cur_round}: spin count {self.spins}',
            bold = True,
            size_hint = (1/5, 1/5),
            pos_hint = {'top': 1.0, 'right': .98}, 
            color = (0, 0, 0, 1)
        )

        self.build_score_grid()
        self.build_wheel()
        self.box_scores.add_widget(self.score_label)
        self.box_scores.add_widget(self.score_grid)
        self.game_play_float_layout.add_widget(self.home_button)
        self.game_play_float_layout.add_widget(self.box_scores)
        self.game_play_float_layout.add_widget(self.turn_label)
        self.game_play_float_layout.add_widget(self.spin_result_label)
        self.game_play_float_layout.add_widget(self.free_turn_button)
        self.game_play_float_layout.add_widget(self.spin_button)
        self.game_play_float_layout.add_widget(self.question_button)
        self.game_play_float_layout.add_widget(self.round_label)
        
    def update_free_turn_btn(self, instance):
        
        if self.teams[self.turn - 1].getTurn() > 0:
            self.teams[self.turn - 1].setTurn(-1)
            print(f"team: {self.teams[self.turn -1].name}, turns: {self.teams[self.turn -1].getTurn()}")
            if self.turn - 1 < 0:
                self.turn == len(self.teams) - 1
            else:
                self.turn -= 1
            
            self.update_team_names()

    def build_score_grid(self):
        try:
            self.box_scores.remove_widget(self.score_grid)
        except:
            pass

        self.score_grid = GridLayout(
            cols = self.number_of_teams,
            size_hint = (1, 2/3),
            pos_hint = {'bottom': 1},
            spacing = (0, 5)
        )

        for i in range(self.number_of_teams):
            lbl = MyLabel()
            lbl.text = self.team_names[i]
            self.score_grid.add_widget(lbl)

        for i in range(self.number_of_teams):    
            score = MyLabel()

            try:
                score.text = f'{self.teams[i].getScore()}'
            except:
                score.text = '0'

            self.score_grid.add_widget(score)

    def update_team_names(self):
        
        self.build_score_grid()
        self.box_scores.add_widget(self.score_grid)
        
        children = self.score_grid.children
        for i in range(len(self.team_names)):
            children[i + len(self.team_names)].text = self.team_names[i]
            children[i].text = str(self.teams[i].getScore())
        # update turn label name:
        self.turn_label.text = f"team { self.teams[self.turn ].name} spins next"

        if self.spins < 1 or self.spin_result_label.text == 'bankrupt':
            self.free_turn_button.disabled = True
        else:
            self.free_turn_button.disabled = False
            self.free_turn_button.text = (f"team {self.teams[self.turn-1].getName()}"
                + f" has {self.teams[self.turn-1].getTurn()} free turns, click to use")
        
        
        
        if(self.cur_round != 2 and self.spins == 50): #set back to 50
            self.cur_round = 2
            self.spins = 0
            
            self.round1Scores = copy.deepcopy(self.teams)
            
            for i in range(len(self.team_names)):
                self.teams[i].setScore(0)
                   
#            for i in range(len(self.team_names)):
#                print('check')
#                print(self.round1Scores[i].getScore())
                
        self.round_label.text = f'round {self.cur_round}: spin count {self.spins}'
        #print(self.cur_round)
        #print(self.spins)
        
        
        
        if (self.cur_round == 2 and self.spins == 50):
            
            self.round_label.text = f'GAME FINISHED!'
            self.spin_button.disabled = True
            
#            for i in range(len(self.team_names)):
#                print('round1Scores')
#                print(self.round1Scores[i].getScore())
                

            
            for i in range(len(self.team_names)):
                self.teams[i].setScore(self.teams[i].getScore() + self.round1Scores[i].getScore())
                
            
            scoreList = []
            Winners = ''
            
            for i in range(len(self.team_names)):
                scoreList.append(self.teams[i].getScore())
                
            for i in range(len(self.team_names)):
                if self.teams[i].getScore() == max(scoreList):
                   Winners += (self.teams[i].name + ' & ')
                
            self.turn_label.text = f"team {Winners[:-3]} won!"
                











    def end_game(self):
        self.spins = 500
        self.update_team_names()

    def build_wheel(self):
        self.spin_result_label = Label(
            text = 'spin result',
            size_hint = (1/6, 1/6),
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            color = (0, 0, 0, 1)
        )

        self.spin_button = Button(
            text = "spin",
            size_hint = (1/8, 1/8),
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            on_press = self.spin
        )
    
    def update_spin_result(self, int_result):
        sectors = list(self.qca_dict.keys())
        sectors += [
            'bankrupt',
            "player's choice",
            "opponent's choice",
            "double points",
            "lose turn",
            "free turn"
        ]
        if int_result:
            self.spin_result_label.text = sectors[int_result]
        
    def spin(self, instance):
        sector = self.gLogic.getOneSector()
        self.update_spin_result(sector)
        self.spins += 1
        

        result = self.spin_result_label.text
        # check for bankrupt
        if (result == 'bankrupt' and 
            self.teams[self.turn].getScore() > 0):
            
            self.teams[self.turn].setScore(0)
        
        # check for double points
        if result == 'double points':
            cur = self.teams[self.turn].getScore()
            self.teams[self.turn].setScore(cur * 2)
        
        if result == 'free turn':
            self.teams[self.turn].setTurn(1)

        # update free turn button text
        self.free_turn_button.text = (f"team {self.teams[self.turn].getName()}"
            + f" has {self.teams[self.turn].getTurn()} free turns, click to use")

        self.turn = (self.turn + 1) % len(self.teams)
        self.turn_label.text = f"{self.teams[self.turn ].name}'s turn"
        self.update_team_names()
    
    def update_score(self, points):
        self.teams[self.turn-1].setScore(points + self.teams[self.turn-1].getScore())
        self.update_team_names()

class QuestionAnswerButton(Button):
    def __init__(self, **kwargs):
        super(QuestionAnswerButton, self).__init__(**kwargs)
        self.question = 'not assigned'
        self.answer = 'not assigned'
        self.category = 'not assigned'
        self.point_value = ''
        self.text = str(self.point_value)

class Timer(Label):
    a = NumericProperty(30)  # seconds

    def __init__(self, inst, **kwargs):
        super(Timer, self).__init__(**kwargs)
        self.inst = inst

    def start(self):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(a=0, duration=self.a)
        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = "FINISHED"
            self.inst.show_answer_button.disabled = True
        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

    def on_a(self, instance, value):
        self.text = f'Time Remaining: {round(value, 1)}'

    def stop(self):
        self.anim.stop(self)
        self.anim.duration = self.a
    
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
        self.add_widget(self.reset_button)

    def build_necessary_widgets(self):
        self.continue_button = Button(
            text = 'continue',
            size_hint = (1/8, 1/12),
            pos_hint = {'x': 0.02, 'y': 0.02},
            background_color = _COLOR_1
        )
        self.reset_button = Button(
            text = 'reset questions',
            size_hint = (1/8, 1/12),
            pos_hint = {'right': 0.98, 'y': 0.02},
            background_color = _COLOR_1,
            on_press = self.reset_questions
        )
    
    def check_if_all_qustions_answered(self):
        
        for child in self.grid.children:
            if type(child) == type(Button()):
                continue
            if child.disabled == False:
                return # we still have some quesitons left
        
        self.parent.game_play.end_game()

        

        
    def show_question_popup(self, instance):
        self.current_question_button = instance
        self.question_popup.size_hint = (0.5 , 0.5)
        self.question_popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.question_label.size_hint = (1.0, 0.8)
        self.question_label.text_size = self.question_label.size
        self.question_label.text = self.current_question_button.question
        self.question_popup.open()
        
        try:
            self.question_float_layout.remove_widget(self.timer)
        except:
            pass
        
        self.timer = Timer(self)
        self.timer.pos_hint = {'center_x': 0.5, 'top': 1}
        self.timer.size_hint = (0.2, 0.2)
        self.question_float_layout.add_widget(self.timer)
        self.show_answer_button.disabled = False
        self.timer.start()
        
    def disable_show_answer(self):
        self.show_answer_button.disabled = True

    def reset_questions(self, instance):
        for child in self.grid.children:
            child.disabled = False

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
        self.correct_button = Button(
            text = 'correct',
            size_hint = (1/3, 1/6),
            pos_hint = {'center_x': 0.2, 'y': 0.01},
            on_press = self.increase_points,
            background_color = _COLOR_1
        )
        self.incorrect_button = Button(
            text = 'incorrect',
            size_hint = (1/3, 1/6),
            pos_hint = {'center_x': 0.8, 'y': 0.01},
            on_press = self.decrease_points,
            background_color = _COLOR_1
        )
        self.answer_float_layout.add_widget(self.answer_label)
        self.answer_float_layout.add_widget(self.correct_button)
        self.answer_float_layout.add_widget(self.incorrect_button)
        self.answer_popup.content = self.answer_float_layout

    def increase_points(self, instance):
        self.check_if_all_qustions_answered()
        self.parent.game_play.update_score(
            self.current_question_button.point_value * self.parent.game_play.cur_round)
        print(f"You earned: {self.current_question_button.point_value} points")
        self.answer_popup.dismiss()

        self.parent.go_back_to_game_play(Button())


    def decrease_points(self, instance):
        self.check_if_all_qustions_answered()
        self.parent.game_play.update_score(
            -(self.current_question_button.point_value * self.parent.game_play.cur_round))
        print(f"You lost: {self.current_question_button.point_value} points")
        self.answer_popup.dismiss()

        self.parent.go_back_to_game_play(Button())

    def show_answer_popup(self, instance):
        self.question_popup.dismiss()
        self.answer_popup.size_hint = (0.5 , 0.5)
        self.answer_popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.answer_label.size_hint = (1.0, 0.8)
        self.answer_label.text_size = self.answer_label.size
        self.answer_label.text = self.current_question_button.answer
        self.current_question_button.disabled = True
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
            cat.bold = True,

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
        self.qca_dict = None
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
            background_color = _COLOR_1,
            on_press = self.save_to_db
        )

        self.build_edit_entry_popup()
        self.build_category_popup()

        self.add_widget(self.grid)
        self.add_widget(self.home_button)
        self.add_widget(self.save_button)

    def build_category_popup(self):
        self.edit_cat_popup = Popup(
            size_hint = (0.5, 0.5),
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            title = "Enter Category Name"
        )
        self.edit_cat_float_layout = FloatLayout(
            size_hint = (1, 1), 
            pos_hint = {'center_x': 0.2, 'center_y': 0.2},
        )

        self.cat_entry = TextInput(
            multiline = False,
            size_hint = (0.9, 0.50),
            pos_hint = {'center_x': 0.5, 'center_y': 0.75},
            hint_text_color = (0, 0, 0, 0.5),
            hint_text = "type category name here",
            on_text_validate = self.apply_cat
        )
        self.apply_cat_button = Button(
            text = 'apply',
            size_hint = (1, 0.1),
            pos_hint = {'center_x': 0.5, 'top': 0.42}
        )
        self.apply_cat_button.bind(on_press=self.apply_cat)

        self.edit_cat_float_layout.add_widget(self.cat_entry)
        self.edit_cat_float_layout.add_widget(self.apply_cat_button)
        self.edit_cat_popup.content = self.edit_cat_float_layout

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
        self.apply_button.bind(on_press=self.apply_question)

        self.edit_float_layout.add_widget(self.question_entry)
        self.edit_float_layout.add_widget(self.answer_entry)
        self.edit_float_layout.add_widget(self.apply_button)
        self.edit_entry_popup.content = self.edit_float_layout

    
    def show_edit_entry_popup(self, instance):
        self.current_selection = instance
        if instance.question != "not assigned":
            self.question_entry.text = instance.question
        else:
            self.question_entry.text = '' 
        if instance.answer != "not assigned":
            self.answer_entry.text = instance.answer
        else:
            self.answer_entry.text = ''
            
        self.edit_entry_popup.open()

    def show_cat_entry_popup(self, instance):
        self.current_selection = instance
        if instance.text != 'A category':
            self.cat_entry.text = self.current_selection.text
        else:
            self.cat_entry.text = ''

        self.edit_cat_popup.open()

    def apply_cat(self, instance):
        children = self.grid.children
        cur_index = children.index(self.current_selection)
        self.current_selection.text = self.cat_entry.text
        self.edit_cat_popup.dismiss()

        # update cat name for quesitons in cat
        for index, child in enumerate(children):
            if index < cur_index and index > cur_index - _NUM_CATS:
                child.category = self.current_selection.text

    def save_to_db(self, instance):
        children = self.grid.children
        self.qca_dict = {}
        for index, child in enumerate(children):
            keys = list(self.qca_dict.keys())
            if (index + 1) % 6 != 0:
                if child.category in keys:
                    self.qca_dict[child.category].append(
                        QAL.QAL(child.question, child.answer, 1)
                    )
                else:
                    self.qca_dict[child.category] = [
                        QAL.QAL(child.question, child.answer, 1)
                    ]        

        self.parent.go_home(instance)

    def apply_question(self, instance):
        children = self.grid.children
        cur_index = children.index(self.current_selection)
        cat_index = int((cur_index + 1) / _NUM_CATS) * _NUM_CATS + _NUM_CATS - 1
        self.current_selection.question = self.question_entry.text
        self.current_selection.answer = self.answer_entry.text
        self.current_selection.category = children[cat_index].text
        self.current_selection.background_color = (216/255, 211/255, 211/255, .5)
        self.edit_entry_popup.dismiss()      

    def build_question_grid(self):
        for cat_index in range(_NUM_CATS):
            cat = Button()
            cat.text = f'cat {cat_index + 1}'
            cat.bold = True
            cat.background_color = _COLOR_1
            cat.bind(on_press=self.show_cat_entry_popup)

            self.grid.add_widget(cat)
            for question in range(_QUES_PER_CAT):
                qbtn = QuestionAnswerButton()
                qbtn.point_value = (question + 1) * 100
                qbtn.text = str(qbtn.point_value)
                qbtn.category = cat.text
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
        self.game_play.home_button.bind(on_press=self.go_home)
        self.game_play.question_button.bind(on_press=self.go_to_question)
        self.questions.continue_button.bind(on_press=self.go_back_to_game_play)
        

        

    def go_to_options(self, instance):
        self.switch_to(self.game_options)
    def go_home(self, instance):
        self.switch_to(self.home)
    def go_to_game_play(self, instance):
        self.switch_to(self.game_play)
        self.populate_question_board()
        self.game_options.update_team_names()
        self.game_play.update_team_names()
    def go_back_to_game_play(self, instance):
        self.switch_to(self.game_play)
    def go_to_edit(self, instance):
        self.switch_to(self.edit)
    def go_to_question(self, instance):
        self.switch_to(self.questions)

    def populate_question_board(self):
        if self.edit.qca_dict == None:
            self.qca_system = QCASystem.QCASystem('sys')
            self.qca_system.db.loadDB('default3.p')
            self.qca = self.qca_system.db.getCategories()
        else:
            self.qca = self.edit.qca_dict
        keys = list(self.qca.keys())
        key_count = 0
        q_count = 0
        for child in self.questions.grid.children:
            # categories are buttons so filter on buttons
            if type(child) == type(Button()):
                child.text = keys[key_count]
                key_count += 1 

            # Q&A are not default buttons
            else:
                key = keys[key_count]
                child.category = key
                child.question = self.qca[key][q_count].getAnswer()
                child.answer = self.qca[key][q_count].getQuestion()
                q_count += 1

            if q_count == _QUES_PER_CAT:
                q_count = 0    
        
        self.game_play.qca_dict = dict( (k, self.qca[k]) for k in (keys[0:6]) )

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

if __name__ == "__main__":
    WheelofJeopardyApp().run()
