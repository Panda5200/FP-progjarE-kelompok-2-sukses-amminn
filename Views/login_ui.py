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

from storage_view import StorageScreen

class LoginPage(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def loginbtn(self):
        res = self.checkAuth()
        sm = self.parent
        if res != False:
            sm.user = res
            sm.current = "ChatPage"

    def regbtn(self):
        self.reset()
        self.current = "RegisterPage"
    
    def checkAuth(self):
        un = self.username.text.replace(" ", "")
        pw = self.password.text.replace(" ", "")

        if un == "" or pw == "":
            return False
        else:
            with open("akun.txt", "r") as a_file:
                for line in a_file:
                    stripped_line = line.strip()
                    data = stripped_line.split()
                    print(data, " ",un," ", pw)
                    if data[0] == un and data[2] == pw:
                        return un
                return False

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
        self.save_akun()
        self.reset()
        # sm.current = "RegisterPage"

    def save_akun (self):
        fileakun = open("akun.txt", "a")
        fileakun.write(str(self.username.text) + ' ' + str(self.email.text) + ' ' + str(self.password.text) + "\n")
        fileakun.close

    def logbtn(self):
        self.reset()
        # sm.current = "LoginPage"

    def reset(self):
        self.username.text = ""
        self.email.text = ""
        self.password.text = ""

class ScreenM(ScreenManager):
    pass



class MainApp(MDApp):
    def build(self):
        screens = [LoginPage(name="LoginPage"), RegisterPage(name="RegisterPage")]
        for screen in screens:
            sm.add_widget(screen)

        sm.add_widget(StorageScreen(name ="tes"))

        sm.current = "tes"
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
    kv = Builder.load_file("login.kv")
    sm = ScreenM()
    MainApp().run()