import gi
import yaml
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

MyDict = yaml.load(open('config.yml'))

Install = []
Shell = []
ShellSu = []
Gsettings = []

class MainWindow(Gtk.ApplicationWindow):

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self)
        self.set_border_width(10)
        self.set_size_request(600, 400)
        self.set_position(Gtk.WindowPosition.CENTER)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        header = Gtk.HeaderBar(title="Ubuntu PostInstall")
        header.set_subtitle("simple postinstall application")
        header.props.show_close_button = True

        button = Gtk.Button.new_with_label("Install")
        button.connect("clicked", self.on_button_clicked)

        header.pack_start(button)

        self.set_titlebar(header)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        dictlen = MyDict["categories"].__len__()

        scroll.add(listbox)

        self.add(scroll)
        self.show_all()

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
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(box)
                label = Gtk.Label(MyDict[MyDict["categories"][x]][y][list(MyDict[MyDict["categories"][x]][y].keys())[0]], xalign=0)
                check = Gtk.CheckButton()
                typelen = list(MyDict[MyDict["categories"][x]][y].keys()).__len__()
                for z in range(1, typelen):
                    check.connect("toggled", self.on_toggled, MyDict[MyDict["categories"][x]][y][list(MyDict[MyDict["categories"][x]][y].keys())[z]], list(MyDict[MyDict["categories"][x]][y].keys())[z])
                box.pack_start(label, True, True, 0)
                box.pack_start(check, False, True, 20)
                listbox.add(row)

    def on_button_clicked(self, button):
        subprocess.run("pkexec apt-get install {}".format(" ".join(Install)), shell=True, check=True)
        for x in range(0, Gsettings.__len__()):
            subprocess.run(Gsettings[x], shell=True, check=True)
        
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
    if type == "sh sudo":
        ShellSu.append(var)
    if type == "gsettings":
        Gsettings.append(var)

def remove_value(self, var, type):
    if type == "install":
        Install.remove(var)
    if type == "sh":
        Shell.remove(var)
    if type == "sh":
        ShellSu.remove(var)
    if type == "gsettings":
        Gsettings.remove(var)

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
