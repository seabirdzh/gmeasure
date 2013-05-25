#!/usr/bin/env python3

from gi.repository import Gtk


class Ruler:


    def __init__(self):
        self._init_window()

    def _init_window(self):
        self.window = Gtk.Window()
        self.window.set_decorated(False)
        self.window.connect('delete-event', self.on_app_exit)
        self.window.set_opacity(0.8)
        self.window.set_default_size(300, 200)

        label = Gtk.Label('Hello, world.')
        label.connect('drag-data-get', self.on_label_drag_data_get)
        self.window.add(label)

    def run(self):
        self.window.show_all()
        Gtk.main()

    def on_app_exit(self, widget, event=None):
        Gtk.main_quit()

    def on_label_drag_data_get(self, label):
        print(label)


if __name__ == '__main__':
    ruler = Ruler()
    ruler.run()
