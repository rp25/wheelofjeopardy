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
    '''
    This class will hold the question and answer button info

    '''
    def __init__(self, q, a, pts, cat, **kwargs):
        super(QuestionButton, self).__init__(**kwargs)
        
        self.question = q
        self.answer = a
        self.points = pts
        self.text = self.points
        self.category = cat
        self.hasBeenAsked = False
        self.background_color = (1, 1, 1, 1)
    
    def hasBeenAsked(self):
        return self.hasBeenAsked

    def askQuestion(self):
        self.hasBeenAsked = True

class QuestionMatrix(GridLayout):
    
    def __init__(self, qcaDict, **kwargs):
        super(QuestionMatrix, self).__init__(**kwargs)
        self.cols = 5
        self.rows = 6
        self.orientation = 'horizontal'

        self.questionButtons = []
        self.categoryButtons = []
        self.buildMatrix(qcaDict)

    def buildMatrix(self, qcaDict):
        for category, questions in qcaDict.items():
            button = Button()
            button.text = str(category)
            button.background_color = (1, 0, 0, 1)
            self.categoryButtons.append(button)

            self.add_widget(button)
        
        for questions in qcaDict.values():
            for qa in questions:
                questionButton = QuestionButton(
                    str(qa[1]),
                    str(qa[0]),
                    str(qa[2]),
                    str(category)
                )
                print(f"[i] {questionButton.text}")
                self.questionButtons.append(questionButton)
                self.add_widget(questionButton)


class WheelofJeopardy(Widget):
    mainBox = ObjectProperty()

    def __init__(self, **kwargs):
        super(WheelofJeopardy, self).__init__(**kwargs)

        testDict = {
            'cat1' : [
                ('a1', 'q1', '100'),
                ('a2', 'q2', '200'),
                ('a3', 'q3', '300'),
                ('a4', 'q4', '400'),
                ('a5', 'q5', '500'),
            ],
            'cat2' : [
                ('a1', 'q1', '100'),
                ('a2', 'q2', '200'),
                ('a3', 'q3', '300'),
                ('a4', 'q4', '400'),
                ('a5', 'q5', '500'),
            ],
            'cat3' : [
                ('a1', 'q1', '100'),
                ('a2', 'q2', '200'),
                ('a3', 'q3', '300'),
                ('a4', 'q4', '400'),
                ('a5', 'q5', '500'),
            ],
            'cat4' : [
                ('a1', 'q1', '100'),
                ('a2', 'q2', '200'),
                ('a3', 'q3', '300'),
                ('a4', 'q4', '400'),
                ('a5', 'q5', '500'),
            ],
            'cat5' : [
                ('a1', 'q1', '100'),
                ('a2', 'q2', '200'),
                ('a3', 'q3', '300'),
                ('a4', 'q4', '400'),
                ('a5', 'q5', '500'),
            ]
        }
        qtest = QuestionMatrix(testDict)
        qtest.size_hint = (0.7, 0.5)
        qtest.pos = self.mainBox.center
        self.mainBox.add_widget( qtest)

    def changeText(self, label):
        label.text = gamelogic.getOneSector()
        
class WheelofJeopardyApp(App):
    def build(self):
        return WheelofJeopardy()

if __name__ == "__main__":
    WheelofJeopardyApp().run()