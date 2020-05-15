from kivymd.app import MDApp
from kivymd.uix.label import MDLabel #render text
from kivymd.uix.textfield import MDTextField #Text fields let users enter and edit text
from kivymd.theming import ThemeManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.toolbar import MDToolbar
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.navigationdrawer import MDNavigationDrawer, NavigationLayout
from kivymd.uix.list import OneLineIconListItem, MDList

KV = '''

'''
    
class Cek(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        self.add_widget(MDLabel(text="Placeholder:"))

        self.Placeholder = TextInput(multiline=False)
        self.add_widget(self.Placeholder)

class ChatApp(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.toolbar = MDToolbar(pos_hint={'top': 1}, elevation=10, title="Group Chat") #toolbar
        self.toolbar.left_action_items = [
            ["menu", lambda x: self.nav_drawer.toggle_nav_drawer()]]
        self.nav_drawer = MDNavigationDrawer(elevation=0)    
        self.add_widget(self.toolbar)
        self.history = MDLabel(height=Window.size[0]*0.63, size_hint_y=None) #history chat
        self.add_widget(self.history)

        self.new_message = TextInput(width=Window.size[0]*0.55, size_hint_x=None, multiline=False)# tempat input text
        self.send = MDRectangleFlatButton(text="Send")
        self.send.bind(on_press=self.send_message)

        self.storage = MDRectangleFlatButton(text="Storage")

        self.notepad = MDRectangleFlatButton(text="Notepad")

        self.to_do_list = MDRectangleFlatButton(text="To Do List")

        bottom_line = GridLayout(cols=5)
        bottom_line.add_widget(self.storage)
        bottom_line.add_widget(self.notepad)
        bottom_line.add_widget(self.to_do_list)
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.send)
        self.add_widget(bottom_line)
    
    def send_message(self, _):
        print("Send a")

class MainApp(MDApp):
    def build(self):
        self.screen = Builder.load_string(KV)
        self.screen_manager = ScreenManager()

        
        self.chat_app = ChatApp()
        screen = Screen(name="ChatPage")
        screen.add_widget(self.chat_app)
        self.screen_manager.add_widget(screen)
        return self.screen_manager

    #self.placeholder_app = Cek()
    #screen = Screen(name="PlaceholderPage")
    #screen.add_widget(self.placeholder_app)
    #self.screen_manager.add_widget(screen)

    

if __name__ == "__main__":
    chat_app = MainApp()
    chat_app.run()
