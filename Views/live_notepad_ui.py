from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

from kivy.uix.textinput import TextInput

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem

from kivymd.uix.behaviors import TouchBehavior
from kivy.uix.screenmanager import Screen

# from notepad_client import NotepadLive

import threading
import time

import sys
sys.path.append("..")
from LiveNotepad.notepad_client import NotepadLive

class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        self.charList = []

        super().__init__(**kwargs)
        self.notepadThread = NotepadLive(
            cb1 = self.set_text
        )
        self.notepadThread.start()

    def keyboard_on_key_down(self, window, keycode, text, modifiers):                
        if keycode[1] == 'backspace':
            myinput = '\x08'
        elif keycode[1] == 'enter':
            myinput = '\r'
        elif keycode[1] == 'spacebar':
            myinput = ' '
        elif keycode[0] in range(97,122):
            myinput = keycode[1]
        else:
            return
        super(CustomTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)
        th = threading.Thread(target=self.check_input, args=(myinput)).start()

    def insert_text(self, substring, from_undo=False):
        # s = substring.upper()
        return super(CustomTextInput, self).insert_text(substring, from_undo=from_undo)

    def check_input(self,myinput):
        myinput = bytes(myinput, 'utf-8')
        self.notepadThread.input(myinput) 

    def set_text(self, text):
        self.text = text

class CustomToolbar2(
    ThemableBehavior, RectangularElevationBehavior, MDBoxLayout,
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.primary_color


class LiveNotepadPage(Screen):
    menu_2 =ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

if __name__ == "__main__":
    Test().run()