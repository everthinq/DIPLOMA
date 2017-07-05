import Tkinter
import ttk
import tkMessageBox

from Tkinter import *
import SQLite_selects
import csvWriter

class AutocompleteCombobox(ttk.Combobox):

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, Tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,Tkinter.END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,Tkinter.END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(Tkinter.INSERT), Tkinter.END)
                        self.position = self.index(Tkinter.END)
                if event.keysym == "Left":
                        if self.position < self.index(Tkinter.END): # delete the selection
                                self.delete(self.position, Tkinter.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, Tkinter.END)
                if event.keysym == "Right":
                        self.position = self.index(Tkinter.END) # go to end (no selection)
                if len(event.keysym) == 1:
                        self.autocomplete()
                # No need for up/down, we'll jump to the popup
                # list at the position of the autocompletion

class GUI:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        cities_list = SQLite_selects.cities_select()
        self.combo_city = AutocompleteCombobox(frame)
        self.combo_city.set_completion_list(cities_list)
        self.combo_city.current(644)
        self.combo_city.pack()

        self.combo_daypart = AutocompleteCombobox(frame)
        self.combo_daypart.set_completion_list(['night', 'morning', 'day', 'evening'])
        self.combo_daypart.current(2)
        self.combo_daypart.pack()
        
        dates_list = SQLite_selects.dates_select()
        self.combo_startdate = AutocompleteCombobox(frame)
        self.combo_startdate.set_completion_list(dates_list)
        self.combo_startdate.current(0)
        self.combo_startdate.pack()

        self.combo_enddate = AutocompleteCombobox(frame)
        self.combo_enddate.set_completion_list(dates_list)
        self.combo_enddate.current(len(dates_list) - 1)
        self.combo_enddate.pack()

        self.slogan = Button(frame, text = "Create file", command = self.create_file)
        self.slogan.pack(fill = 'both')


    def create_file(self):
        city        = self.combo_city.get()
        dayPart     = self.combo_daypart.get()
        start_date  = self.combo_startdate.get()
        end_date    = self.combo_enddate.get()

        weather_array = SQLite_selects.rows_select(city, dayPart, start_date, end_date)
        csvWriter.write_rows(weather_array, city + ';' + dayPart)
        tkMessageBox.showinfo('Info', 'file "' + city + ';' + dayPart + '" created or rewritten in raw_data directory')


def main():
    root = Tk()
    app = GUI(root)

    root.bind('<Control-Q>', lambda event=None: root.destroy())
    root.bind('<Control-q>', lambda event=None: root.destroy())

    root.mainloop()


if __name__ == '__main__':
    main()
