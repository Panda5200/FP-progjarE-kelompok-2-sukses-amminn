import os

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty

Builder.load_string(
    """
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import StorageScreen storage_view.StorageScreen
#:import LoginPage login_ui.LoginPage
#:import RegisterPage login_ui.RegisterPage
#:import ChatPage chat_ui.ChatPage
#:import LiveNotepadPage live_notepad_ui.LiveNotepadPage
#:import TodoListScreen todolist_view.TodoListScreen

<ScreenManagement>:
    # transition: FadeTransition()
    LoginPage:
        name: 'LoginPage'
    RegisterPage:
        name: 'RegisterPage'
    StorageScreen:
        name: 'StorageScreen'
    ChatPage:
        name: 'ChatPage'
    LiveNotepadPage:
        name: 'LiveNotepadPage'
    TodoListScreen:
        name: 'TodoListScreen'
"""
)

KV_DIR = f"{os.path.dirname(__file__)}/kv"
for kv_file in os.listdir(KV_DIR):
    with open(os.path.join(KV_DIR, kv_file), encoding="utf-8") as kv:
        Builder.load_string(kv.read())

class ScreenManagement(ScreenManager):
    user = StringProperty()

class MainApp(MDApp):
    def build(self):
        sm = ScreenManagement()
        sm.current = 'LoginPage'
        return sm

if __name__ == "__main__":
    MainApp().run()