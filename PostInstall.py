import gi
import yaml
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

MyDict = yaml.load(open('config.yml'))

Install = []
Shell = []
Gsettings = []

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self)

        self.set_size_request(600, 400)

        self.set_position(Gtk.WindowPosition.CENTER)

        Gtk.Window.__init__(self, title="Ubuntu Post Install")
        self.set_border_width(10)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        dictlen = MyDict["categories"].__len__()

        for x in range(0, dictlen):
            row = Gtk.ListBoxRow()
            text = MyDict["categories"][x].title()
            label = Gtk.Label(xalign=0)
            label.set_markup("<big><b>{}</b></big>".format(text))
            row.add(label)
            listbox.add(row)
            catlen = MyDict[MyDict["categories"][x]].__len__()
            for y in range(0, catlen):
                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                label = Gtk.Label(MyDict[MyDict["categories"][x]][y][list(MyDict[MyDict["categories"][x]][y].keys())[0]], xalign=0)
                check = Gtk.CheckButton()
                typelen = list(MyDict[MyDict["categories"][x]][y].keys()).__len__()
                for z in range(1, typelen):
                    check.connect("toggled", self.on_toggled, MyDict[MyDict["categories"][x]][y][list(MyDict[MyDict["categories"][x]][y].keys())[z]], list(MyDict[MyDict["categories"][x]][y].keys())[z])
                hbox.pack_start(label, True, True, 0)
                hbox.pack_start(check, False, True, 0)
                listbox.add(row)

        row = Gtk.ListBoxRow()
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(vbox)
        button = Gtk.Button.new_with_label("Install")
        button.connect("clicked", self.on_button_clicked)
        vbox.pack_end(button, False, False, 100)
        listbox.add(row)

    def on_button_clicked(self, button):
        print(Install)

    def on_toggled(self, button, install, type):
        if button.get_active():
            state = "on"
            add_value(self, install, type)
        else:
            state = "off"
            remove_value(self, install, type)
        print("Typ:", type, "  Komenda:", install, "Stan: {}".format(state))

def add_value(self, var, type):
    if type == "install":
        Install.append(var)
    if type == "sh":
        Shell.append(var)
    if type == "gsettings":
        Gsettings.append(var)

def remove_value(self, var, type):
    if type == "install":
        Install.remove(var)
    if type == "sh":
        Shell.remove(var)
    if type == "gsettings":
        Gsettings.remove(var)

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
