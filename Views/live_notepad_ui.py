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


class CustomTextInput(TextInput):

    def insert_text(self, substring, from_undo=False):
        # s = substring.upper()
        return super(CustomTextInput, self).insert_text(substring, from_undo=from_undo)

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