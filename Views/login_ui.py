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
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def loginbtn(self):
        self.reset()
        sm.current = "LoginPage"

    def regbtn(self):
        self.reset()
        sm.current = "RegisterPage"

    def reset(self):
        self.username.text = ""
        self.password.text = ""
        
class RegisterPage(Screen):
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def regisbtn(self):
        self.reset()
        sm.current = "RegisterPage"

    def logbtn(self):
        self.reset()
        sm.current = "LoginPage"

    def reset(self):
        self.username.text = ""
        self.email.text = ""
        self.password.text = ""

class ScreenM(ScreenManager):
    pass

kv = Builder.load_file("login.kv")

sm = ScreenM()



class MainApp(MDApp):
    def build(self):
        screens = [LoginPage(name="LoginPage"), RegisterPage(name="RegisterPage")]
        for screen in screens:
            sm.add_widget(screen)

        sm.current = "LoginPage"
        #self.screen_manager = ScreenManager()

        #self.login_page = LoginPage()
        #screen = Screen(name="LoginPage")
        #screen.add_widget(self.login_page)
        #self.screen_manager.add_widget(screen)

        #self.register_page = RegisterPage()
        #screen = Screen(name="registerPage")
        #screen.add_widget(self.register_page)
        #self.screen_manager.add_widget(screen)

        #self.screen_manager.current = "registerPage"

        return sm

if __name__ == "__main__":
    MainApp().run()