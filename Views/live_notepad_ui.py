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

KV = '''

<CustomToolbar>:
    size_hint_y: None
    height: self.theme_cls.standard_increment
    padding: "5dp"
    spacing: "3dp"

    MDIconButton:
        id: button_1
        icon: "keyboard-backspace"
        pos_hint: {"center_y": .5}
        # on_release: app.menu_1.open()

    MDLabel:
        text: "Notepad Title"
        pos_hint: {"center_y": .5}
        size_hint_x: None
        width: self.texture_size[0]
        text_size: None, None
        font_style: 'H6'

    Widget:

<CustomTextInput>:

Screen:
    BoxLayout:
        orientation: "vertical"

        CustomToolbar:
            id: toolbar
            elevation: 10
            pos_hint: {"top": 1}

        BoxLayout:
            orientation: "vertical"

            CustomTextInput:
                id: myInput

            # canvas:
            #     Color:
            #         rgba: app.theme_cls.primary_light
            #     Rectangle:
            #         pos: self.pos
            #         size: self.size
'''

class CustomTextInput(TextInput):

    def insert_text(self, substring, from_undo=False):
        # s = substring.upper()
        return super(CustomTextInput, self).insert_text(substring, from_undo=from_undo)

class CustomToolbar(
    ThemableBehavior, RectangularElevationBehavior, MDBoxLayout,
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.primary_color


class Test(MDApp):
    menu_2 =ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)

    def build(self):
        return self.screen


Test().run()