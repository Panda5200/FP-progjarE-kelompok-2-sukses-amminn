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
from kivy.uix.floatlayout import FloatLayout


class LoginPage(Screen):
   def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.toolbar = MDToolbar(pos_hint={'top': 1}, elevation=10, title="Simple Team Collaborative Tools") #toolbar
        self.toolbar.left_action_items = [
            ["menu", lambda x: self.nav_drawer.toggle_nav_drawer()]]
        self.nav_drawer = MDNavigationDrawer(elevation=0)    
        self.add_widget(self.toolbar)
        
class MainApp(MDApp):
    def build(self):
        self.screen = Builder.load_file("login.kv")
        self.screen_manager = ScreenManager()

        self.login_page = LoginPage()
        screen = Screen(name="LoginPage")
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)
        return self.screen_manager

if __name__ == "__main__":
    MainApp = MainApp()
    MainApp.run()