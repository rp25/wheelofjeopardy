import QCASystem
import gamelogic

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty

class QuestionButton(Button):
    '''TODO: just make this hold the QCA object
        to make everything much cleaner and less redundant
    '''
    def __init__(self, q, a, pts, cat, qlabel, **kwargs):
        super(QuestionButton, self).__init__(**kwargs)
        self.qq = qlabel
        self.question = q
        self.answer = a
        self.points = pts
        self.text = self.points
        self.category = cat
        self.background_color = (1, 1, 1, 0.9)

    # For now just display quesiton if button is clicked
    def on_press(self):
        self.qq.text = self.question

class QuestionMatrix(GridLayout):
    # TODO: Don't pass around the 'qq' it's ugly
    def __init__(self, qcaDict, qlabel, **kwargs):
        super(QuestionMatrix, self).__init__(**kwargs)
        self.cols = 6
        self.rows = 6
        self.orientation = 'horizontal'

        self.questionButtons = []
        self.categoryButtons = []
        self.buildMatrix(qcaDict, qlabel)

    def buildMatrix(self, qcaDict, qq):
        # TODO: The grid fills in left to right
        # so the categories correspond to rows right now...
        # fix this

        # Fill top row with categories
        for category, questions in qcaDict.items():
            button = Button()
            button.text = str(category)
            button.background_color = (1, 0, 0, 1)
            self.categoryButtons.append(button)
            self.add_widget(button)
        
        # Fill remaining rows with question data
        for index in range(self.cols - 1):
            print(f"[i] questions: {questions[index]} ")
            for questions in qcaDict.values():
                questionButton = QuestionButton(
                    str(questions[index][0]),
                    str(questions[index][1]),
                    f'{100*(index+1)}',
                    str(category),
                    qq
                )
                self.questionButtons.append(questionButton)
                self.add_widget(questionButton)
                
                


class WheelofJeopardy(Widget):
    mainBox = ObjectProperty()
    question = ObjectProperty()

    def __init__(self, **kwargs):
        super(WheelofJeopardy, self).__init__(**kwargs)
        
        # Load quesitons from QCASystem
        self.qcaSystem = QCASystem.QCASystem('default')
        self.qcaSystem.loadDefaultQCA()
        qca = self.qcaSystem.db.getQCA()
  
        # Build matrix of questions
        qtest = QuestionMatrix(qca, self.question)
        qtest.size_hint = (0.9, 0.5)
        qtest.pos = self.mainBox.center
        self.mainBox.add_widget( qtest)

    def changeText(self, label):
        label.text = gamelogic.getOneSector(
            self.qcaSystem.db.getAllCategories())
        
class WheelofJeopardyApp(App):
    def build(self):
        return WheelofJeopardy()

if __name__ == "__main__":
    WheelofJeopardyApp().run()
