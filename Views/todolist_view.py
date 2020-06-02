from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem

from kivymd.uix.behaviors import TouchBehavior

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivymd.uix.card import MDCardSwipe

import itertools  
from functools import partial

# from c_todo import todolistClient
import sys
sys.path.append("..")
from todolist_lama.c_todo import todolistClient


class TodoItem(MDCardSwipe):
    _id = NumericProperty()
    file = StringProperty()
    text = StringProperty()
    date = StringProperty()
    isComplete = BooleanProperty()

    def __init__(self, **kwargs):
        print("Tes")
        print(kwargs)
        super(TodoItem, self).__init__(**kwargs)


class TodoListToolbar(
    ThemableBehavior, RectangularElevationBehavior, MDBoxLayout,
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.primary_color

class Container(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True

class TodoListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = []
        self.tdClient = todolistClient()
    
    def on_enter(self):
        self.retrive_folder()
    
    def on_swipe_delete(self, root, instance):
        self.ids.item_warp.remove_widget(root)
        self.tdClient.DeleteTask(root.file)
    
    def on_update_todo(self, root, instance):
        pass

    def on_complete_todo(self, root, instance):
        root.isComplete = not root.isComplete
        self.tdClient.SetTaskComplete(root.file, root.isComplete)
        self.retrive_folder()

    def retrive_folder(self):
        self.container.clear()
        self.ids.item_warp.clear_widgets()
        data = self.tdClient.GetTask()

        # data = {
        #         'files': ['~10e1f092-2942-456d-bb49-92dec187aa26.txt', '8de9467f-48c8-476e-b64f-dd8bdd524161.txt'], 
        #         'tasks': ['Our Task~3-Nov-2020', 'Our Task 2~2-Nov-2020']
        #         }
        _id =  0
        for (file, task) in zip(data['files'], data['tasks']): 
            ts = task.partition("~")
            fss = file.split("~")
            myDict = {"_id":_id, "file":file , "text":ts[0], "date":ts[2]}
            print(fss)
            if len(fss)>1:
                myDict['isComplete'] = True
            else:
                myDict['isComplete'] = False
            
            self.container.append(myDict)
            a = TodoItem(**myDict)

            buttoncallback = partial(self.on_swipe_delete, a)
            a.ids.delete_btn.bind(on_press=buttoncallback)

            buttoncallback = partial(self.on_complete_todo, a)
            a.ids.complete_btn.bind(on_press=buttoncallback)

            self.ids.item_warp.add_widget(a)
            _id = _id + 1
            

class MyApp(MDApp):
    def build(self):
        return StorageScreen().screen

if __name__ == "__main__":
    MyApp().run()