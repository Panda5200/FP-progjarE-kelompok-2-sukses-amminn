import os
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import OneLineAvatarListItem

from kivymd.uix.behaviors import TouchBehavior

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

# from storage import Storage
import sys
sys.path.append("..")

from Storage.storage import Storage
from kivymd.uix.label import MDLabel

class CustomItem(OneLineListItem, TouchBehavior):
    icon = StringProperty()
    name = StringProperty()
    _type = StringProperty()
    _id = NumericProperty()
    parent_instance =ObjectProperty()
    def __init__(self, **kwargs):
        super(CustomItem, self).__init__(**kwargs)
        # self.register_event_type('on_ChangeDirectory')
        # for key, value in kwargs.items():
        #     print("{} is {}".format (key,value))

    def on_press(self):
        if self._type == "folder":
            self.parent_instance.ChangeDirectory(self.name)

    def on_double_tap(self, touch, *args):
        # print("<on_long_touch> {}".format(self.name))
        self.parent_instance.container_idx = self._id
        self.parent_instance.show_dialog()
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
    isShownNewFolderMenu = BooleanProperty(False)
    isShownRenameMenu = BooleanProperty(False)
    workDir = StringProperty()
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = Storage()
        self.container = []
        self.cwd = ""
        self.container_idx = -1
        # self.menu_2 = self.create_menu(
        #     [
        #         {"text": "rename"},
        #         {"text": "delete"},
        #         {"text": "download"}
        #     ], self.ids['pivot2']
        # )
    
    def DoRetrive(self, dt):
        i = 0
        self.container.clear()
        self.workDir = self.storage.StorageMethods("PWD" )
        if self.workDir != "/":
            self.container.append({"icon":"folder-open", "name": "..", "_type":"folder", "_id":i})
            i = i+1

        files = self.storage.StorageMethods("LIST")
        for file in files:
            name, extension = os.path.splitext(file)
            if extension == '':
                icon="folder-open"
                _type="folder"
            elif extension in ['.jpg','.png','jpeg']:
                icon="file-image"
                _type="image"
            elif extension == '.pdf':
                icon="folder-pdf"
                _type="pdf"
            elif extension == '.txt':
                icon="note-text-outline"
                _type="text"
            elif extension in ['.docx','.doc']:
                icon="folder-word"
                _type="word"
            else:
                icon="file"
                _type="file"
            self.container.append({"icon":icon, "name": file, "_type":_type, "_id":i})
            i = i+1
        self.retrive_folder_file(self.container)

    def setShownNewFolderMenu(self):
        self.isShownNewFolderMenu = not self.isShownNewFolderMenu

    def setShownRenameMenu(self, instance):
        self.dialog.dismiss()
        self.isShownRenameMenu = not self.isShownRenameMenu

    def init(self, dt):
        self.ids.newfolder_create.bind(on_press=self.CreateNewFolder)
        self.ids.rename_create.bind(on_press=self.Rename)
        # self.ids.toolbar.ids.new_folder.bind(on_press= self.setShownNewFolderMenu())
        # self.ids.toolbar.ids.new_folder.bind(on_press=self.CreateNewFolder)

    def show_dialog(self):
        if self.dialog == None:
            self.rename = OneLineAvatarListItem(text="Rename")
            self.download = OneLineAvatarListItem(text="Download")

            self.rename.bind(on_release=self.setShownRenameMenu)
            # self.rename.bind(on_press=self.Rename)
            self.download.bind(on_release=self.Download)

            self.dialog = MDDialog(title="Actions",
                                    type="simple",
                                    items= [
                                        self.rename,
                                        self.download                                    
                                    ],
                                    auto_dismiss=False)

            # self.dialog.add_action_button("Dismiss",
            #                               action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def CreateNewFolder(self, *args):
        folder_name = self.ids.newfolder_name.text
        res = self.storage.StorageMethods("MKD "+folder_name)
        print(res)
        self.DoRetrive(1)
    
    def ChangeDirectory(self, folder_name):
        print(folder_name)
        res = self.storage.StorageMethods("CD "+folder_name)
        self.DoRetrive(1)

    def Rename(self, *args):
        item = self.container[self.container_idx]
        newname = self.ids.rename_name.text
        res = self.storage.StorageMethods("RENAME {} {}".format(item['name'],newname))
        self.DoRetrive(1)
    
    def Download(self, instance):
        item = self.container[self.container_idx]
        print(item)
        self.dialog.dismiss()
        if item['_type'] == "folder":
            res = self.storage.StorageMethods("DF "+item['name'])
        else:
            res = self.storage.StorageMethods("RETR "+item['name'])
        self.DoRetrive(1)
    
    #not yet
    def Upload(self):
        item = self.container[self.container_idx]
        res = self.storage.StorageMethods("STOR "+ item.name)
        self.DoRetrive(1)

    def on_enter(self):
        Clock.schedule_once(self.DoRetrive)
        Clock.schedule_once(self.init)

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
        self.ids.item_warp.clear_widgets()
        for item in items:
            item['parent_instance'] = self
            _i = CustomItem(**item)
            _i.bind(on_ChangeDirectory=self.ChangeDirectory)
            self.ids.item_warp.add_widget(
               _i 
            )

class MyApp(MDApp):
    def build(self):
        return StorageScreen().screen

if __name__ == "__main__":
    MyApp().run()