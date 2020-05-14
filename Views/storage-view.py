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
        on_release: app.menu_1.open()

    MDLabel:
        text: "Storage"
        pos_hint: {"center_y": .5}
        size_hint_x: None
        width: self.texture_size[0]
        text_size: None, None
        font_style: 'H6'

    Widget:

    MDIconButton:
        id: "new_folder"
        icon: "folder-plus"
        pos_hint: {"center_y": .5}

    MDIconButton:
        id: "upload"
        icon: "upload"
        pos_hint: {"center_y": .5}

    MDIconButton:
        id: button_2
        icon: "dots-vertical"
        pos_hint: {"center_y": .5}
        on_release: app.menu_2.open()

<CustomItem>:

    MDBoxLayout:
        id: box_top
        spacing: "10dp"
        adaptive_height: True
        pos_hint: {"center_y": .5}

        MDIconButton:
            icon: root.icon
            pos_hint: {"center_y": .5}

        MDLabel:
            text: root.name

Screen:
    BoxLayout:
        orientation: "vertical"
        # spacing: "10dp"

        CustomToolbar:
            id: toolbar
            elevation: 10
            pos_hint: {"top": 1}

        BoxLayout:
            size_hint_y: None
            height: "30dp"
            padding: ["10dp", "10dp"]

            canvas:
                Color:
                    rgba: app.theme_cls.primary_light
                Rectangle:
                    pos: self.pos
                    size: self.size

            MDLabel:
                id: ts
                text: "./root/folder/"
                pos_hint: {"center_y": .5}

        ScrollView:

            MDList:
                id: item_warp

    FloatLayout:

        BoxLayout:
            id: pivot
            size_hint: None, None
            size: "60dp", "60dp"

            canvas:
                Color:
                    rgba: app.theme_cls.primary_color
                Rectangle:
                    pos: self.pos
                    size: self.size
        
            BoxLayout:
                id: pivot2
                size_hint: None, None
                size: "30dp", "30dp"
                pos: [10, 10]

                canvas:
                    Color:
                        rgba: app.theme_cls.primary_light
                    Rectangle:
                        pos: self.pos
                        size: self.size
'''

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


class Test(MDApp):
    menu_2 =ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        # self.menu_1 = self.create_menu(
        #     "Button menu", self.screen.ids.toolbar.ids.button_1
        # )
        self.menu_2 = self.create_menu(
            [
                {"text": "rename"},
                {"text": "delete"},
                {"text": "download"}
            ], self.screen.ids['pivot2']
        )

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
        self.screen.ids.item_warp.clear_widgets()
        for item in items:
            _i = CustomItem(**item)
            _i.bind(on_test=self.nyoba)
            self.screen.ids.item_warp.add_widget(
               _i 
            )

    def nyoba(self, instance):
        # self.menu_2.caller = instance
        self.screen.ids['pivot'].pos =[200,  200]  
        print(self.screen.ids['pivot'].pos)
        # self.screen.ids.pivot.pos = [50,  50] 
        print(self.screen)
        # self.menu_2.open(self.screen)

    def print_item(self, instance):
        print(instance.text)

    def build(self):
        return self.screen


Test().run()