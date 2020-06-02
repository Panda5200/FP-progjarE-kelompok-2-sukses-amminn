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

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


from functools import partial

# from chat import ChatService

import sys
sys.path.append("..")
from chat.chat import ChatService

KV = '''

'''
    
class Cek(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        self.add_widget(MDLabel(text="Placeholder:"))

        self.Placeholder = TextInput(multiline=False)
        self.add_widget(self.Placeholder)

class ChatBoxView(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

        

        # self.history = MDLabel(height=Window.size[0]*0.63, size_hint_y=None) #history chat
        self.history = ChatBoxView(height=Window.size[0]*0.63, size_hint_y=None, padding=["20dp", 0])
        # Label(text='blah blah '* 1000, height=Window.size[0]*0.63, size_hint_y=None)
        self.add_widget(self.history)

        self.new_message = TextInput(width=Window.size[0]*0.55, size_hint_x=None, multiline=False)# tempat input text
        self.send = MDRectangleFlatButton(text="Send")
        # self.send.bind(on_press=self.send_message)

        self.storage = MDRectangleFlatButton(id="storage_button", text="Storage")

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

class ChatPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_app = ChatApp()
        self.cs = None
        
        self.add_widget(self.chat_app)        

        buttoncallback = partial(self.ChangeScreen, 'StorageScreen')
        self.chat_app.storage.bind(on_press=buttoncallback)

        buttoncallback = partial(self.ChangeScreen, 'LiveNotepadPage')
        self.chat_app.notepad.bind(on_press=buttoncallback)

        buttoncallback = partial(self.ChangeScreen, 'TodoListScreen')
        self.chat_app.to_do_list.bind(on_press=buttoncallback)    
    
    def on_enter(self):
        self.manager = self.parent
        if self.cs == None:
            self.cs = ChatService(
                _user = self.manager.user,
                cb= self.chat_callback
            )
        print(self.manager.user)

        self.chat_app.send.bind(on_press=self.send_chat)

        # for i in range(20):
        #     label = Label(text='[color=ff3333]Hello[/color][color=3333ff]World[/color]', size_hint=(1.0, None), halign="right", valign="middle",
        #         markup = True)
        #     label.bind(size=label.setter('text_size')) 
        #     self.chat_app.history.ids.scroll.add_widget(
        #         label
        #     )
        # label = Label(text='blah blah '* 1000, size_hint=(1, None))
        # label.bind(
        #     width=lambda *x: label.setter('text_size')(label, (label.width, None),
        #     texture_size=lambda *x: label.setter('height')(label, label.texture_size[1])
        # )
    
    def send_chat(self, instance):
        msg = self.chat_app.new_message.text
        print(msg)
        if msg.replace(" ", "") == "":
            return
        self.cs.SendData(msg)
        self.chat_app.new_message.text = ""
        
    
    def chat_callback(self,sender,msg):
        if sender == self.manager.user:
            print ("You ", msg)
            label = Label(text='[color=4f4f4f]{}[/color][b][color=00ea04]   :You[/color][/b]'.format(msg), 
                size_hint=(1.0, None), 
                halign="right", 
                valign="middle",
                height= "40dp",
                markup = True
            )
        else:
            print ("{} ".format(sender), msg)
            label = Label(text='[b][color=3333ff]{}:   [/color][/b][color=4f4f4f]{}[/color]'.format(sender,msg), 
                size_hint=(1.0, None), 
                halign="left", 
                valign="middle",
                height= "40dp",
                markup = True
            )
        label.bind(size=label.setter('text_size')) 
        self.chat_app.history.ids.scroll.add_widget(
            label
        )
        self.chat_app.history.ids.scroll.scroll_y = 0

    def ChangeScreen(self, *args):
        self.parent.transition.direction = 'left'
        self.parent.current=args[0]
    
    # def Tes(self):
    #     print(self.chat_app.ids)

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
