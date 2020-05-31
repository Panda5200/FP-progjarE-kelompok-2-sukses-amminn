from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem

from kivymd.uix.behaviors import TouchBehavior

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock


class TodoItem(OneLineListItem, TouchBehavior):
    icon = StringProperty()
    name = StringProperty()
    _type = StringProperty()
    def __init__(self, **kwargs):
        super(TodoItem, self).__init__(**kwargs)
        self.register_event_type('on_test')
        for key, value in kwargs.items():
            print("{} is {}".format (key,value))
    
    def on_test(self):
        pass

    def on_long_touch(self, touch, *args):
        print("<on_long_touch> {}".format(self.name))
        self.dispatch('on_test')
    #     super(CustomItem, self).on_touch_down(touch) 
    #     if self.collide_point(touch.x, touch.y):
    #         print("tes")


class TodoListToolbar(
    ThemableBehavior, RectangularElevationBehavior, MDBoxLayout,
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.primary_color


class TodoListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MyApp(MDApp):
    def build(self):
        return StorageScreen().screen

if __name__ == "__main__":
    MyApp().run()