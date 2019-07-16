import QCASystem.py
import gamelogic.py

import kivy
from kivy.app import App
from kivy.uix.widget import Widget

class WheelofJeopardy(Widget):
    def __init__(self, **kwargs):
        super(WheelofJeopardy, self).__init__(**kwargs)


class WheelofJeopardyApp(App):
    def build(self):
        return WheelofJeopardy()

if __name__ == "__main__":
    WheelofJeopardyApp().run()