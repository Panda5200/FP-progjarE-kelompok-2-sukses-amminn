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


class CustomItem(OneLineListItem, TouchBehavior):
    icon = StringProperty()
    name = StringProperty()
    _type = StringProperty()
    def __init__(self, **kwargs):
        super(CustomItem, self).__init__(**kwargs)
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


class CustomToolbar(
    ThemableBehavior, RectangularElevationBehavior, MDBoxLayout,
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.primary_color


class StorageScreen(Screen):
    menu_2 =ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.menu_2 = self.create_menu(
        #     [
        #         {"text": "rename"},
        #         {"text": "delete"},
        #         {"text": "download"}
        #     ], self.ids['pivot2']
        # )
    
    def DoRetrive(self, dt):
        self.retrive_folder_file(
            [
                {"icon":"folder-open", "name": "..", "_type":"folder"},
                {"icon":"folder-open", "name": "folder", "_type":"folder"},
                {"icon":"file", "name": "file", "_type":"file"},
                {"icon":"file-image", "name": "image", "_type":"image"},
                {"icon":"file-word", "name": "word", "_type":"word"},
                {"icon":"file-excel", "name": "excel", "_type":"excel"},
                {"icon":"file-powerpoint", "name": "powerpoint", "_type":"powerpoint"},
                {"icon":"file-pdf", "name": "pdf", "_type":"pdf"},
            ]
        )

    def on_enter(self):
        Clock.schedule_once(self.DoRetrive)

    def create_menu(self, menu_items, instance):
        return MDDropdownMenu(caller=instance, items=menu_items, callback=self.print_item, use_icon_item=False, width_mult=2)
        # menu = MDDropdownMenu()
        # menu.items.append(
        #     {"Viewclass":"MDMenuItem",
        #      "text":"option 1",
        #      "callback": self.print_item}
        # )
        # return menu
    
    def retrive_folder_file(self, items):
        # self.ids.item_warp.clear_widgets()
        for item in items:
            _i = CustomItem(**item)
            _i.bind(on_test=self.nyoba)
            self.ids.item_warp.add_widget(
               _i 
            )

    def nyoba(self, instance):
        # self.menu_2.caller = instance
        self.ids['pivot'].pos =[200,  200]  
        print(self.ids['pivot'].pos)
        # self.ids.pivot.pos = [50,  50] 
        print(self)
        # self.menu_2.open(self)

    def print_item(self, instance):
        print(instance.text)

class MyApp(MDApp):
    def build(self):
        return StorageScreen().screen

if __name__ == "__main__":
    MyApp().run()