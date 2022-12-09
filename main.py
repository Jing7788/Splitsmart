from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFloatingActionButton
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import ThreeLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.core.text.markup import MarkupLabel
from kivy.uix.label import Label
from kivymd.toast import toast
from kivymd.uix.pickers import MDDatePicker
from kivy.utils import platform

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE INPUT FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set the date_text label to today's date when user first opens dialog box
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))
        self._noofpeople = "3"
        self.final = 0

    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """This functions gets the date from the date picker and converts its it a
        more friendly form then changes the date label on the dialog to that"""

        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

    def noofpeople_increment(self):
        """This function will get make the plus sign button work"""
        self._noofpeople = MarkupLabel(self._noofpeople).markup
        self._noofpeople = int(self._noofpeople[0])
        self._noofpeople += 1
        self._noofpeople = f'{self._noofpeople}'
        self.ids.noofpeople.text = self._noofpeople

    def noofpeople_decrement(self):
        """This function will get make the minus sign button work"""
        self._noofpeople = MarkupLabel(self._noofpeople).markup
        self._noofpeople = int(self._noofpeople[0])
        if self._noofpeople > 2:
            self._noofpeople -= 1
        self._noofpeople = f'{self._noofpeople}' 
        self.ids.noofpeople.text = self._noofpeople


    def show_popup(self):
        """define a toast message for the input to input the total amount of bills"""
        if self.ids.amount.text== '': 
            toast("Please input the total amount of bills")

    def final_calc(self):
        """Thia is the calculation part"""
        if self.ids.amount.text== '':
            def show_popup(self):
                 toast("Please input the total amount of bills")
        else:
            #convert amount input from user into float
            numofinput = float(self.ids.amount.text)
            self._noofpeople = MarkupLabel(self.ids.noofpeople.text).markup
            #convert no of people into integer
            self._noofpeople = int(self._noofpeople[0])
            #compute
            self.final = round(((numofinput)/(self._noofpeople)), 1)
            self._noofpeople = f'{self._noofpeople}'
            self.ids.noofpeople.text = self._noofpeople
            #convert the result into string so that can be display
            last_bill =  str(self.final)
            #change the label in total_bill into the result
            self.ids.total_bill.text = last_bill

class ListItemWithCheckbox(ThreeLineAvatarIconListItem):
    '''Custom list item'''

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk


    def mark(self, check, the_list_item):
        '''mark the task as complete or incomplete'''
        if check.active == True:
            # add strikethrough to the text if the checkbox is active
            the_list_item.text = '[s]'+the_list_item.text+'[/s]'
        else:

            pass

    def delete_item(self, the_list_item):
        '''Delete the task'''
        self.parent.remove_widget(the_list_item)



class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''


class MainApp(MDApp):
    task_list_dialog = None
    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.primary_palette = "Indigo"

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Bill",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()


    def add_task(self, name, bill_date , total_bill, amount, no_of_people):
        '''Add task to the list of tasks'''

        print(name.text, bill_date, total_bill.text, no_of_people.text)
        self.root.ids['container'].add_widget(ListItemWithCheckbox(text='[b]'+name.text+'[/b]', 
        secondary_text=bill_date ,  tertiary_text="bills to pay per person: " + total_bill.text + " | " + no_of_people.text + " people"))
        name.text = '' # set the dialog entry to an empty string(clear the text entry)
        total_bill.text = '0' # set the total bill display on screen to become 0
        amount.text = ''


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

if __name__ == '__main__':
    app = MainApp()
    app.run()
