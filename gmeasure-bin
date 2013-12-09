#!/usr/bin/env python3

from gi.repository import Gtk

from gmeasure import Config
from gmeasure.Handler import Handler


def main():
    builder = Gtk.Builder()
    builder.add_from_file(Config.GLADE_FILE)

    handler = Handler(builder)
    builder.connect_signals(handler)
    handler.run()


if __name__ == '__main__':
    main()
