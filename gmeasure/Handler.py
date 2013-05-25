from gi.repository import Gdk
from gi.repository import Gtk

class Handler:

    def __init__(self, builder):
        self.builder = builder

        self.window = builder.get_object('main_window')

    def run(self):
        self.window.show_all()
        Gtk.main()

    def on_app_exit(self, widget, event=None):
        Gtk.main_quit()

    def on_main_window_button_press_event(self, window, event):
        #print('button pressed')
        label_menu = self.builder.get_object('label_menu')
        if event.type != Gdk.EventType.BUTTON_PRESS:
            return False

        if event.button == 3:
            # right click
            label_menu.popup(None, None, None, None, 
                    event.button, event.time)
        elif event.button == 2:
            # middle clcick, current do nothing.
            pass
        elif event.button == 1:
            # left click, resize window.
            # first, get window edge.
            move_or_resize, edge_type = self._check_move_or_resize(event)
            if move_or_resize == False:
                self.window.begin_move_drag(event.button, event.x_root,
                        event.y_root, event.time)
            else:
                self.window.begin_resize_drag(edge_type, event.button, 
                        event.x_root, event.y_root, event.time)

    def _check_move_or_resize(self, event, cursor=False):
        cursors = {
                '1': None,
                '2': Gdk.CursorType.BOTTOM_SIDE,
                '4': Gdk.CursorType.RIGHT_SIDE,
                '8': Gdk.CursorType.BOTTOM_RIGHT_CORNER,
                }
        edges = {
                '1': None,
                '2': Gdk.WindowEdge.SOUTH,
                '4': Gdk.WindowEdge.EAST,
                '8': Gdk.WindowEdge.SOUTH_EAST,
                }
        width, height = self.window.get_size()
        MIN = 5
        mark = 1
        if width - MIN <= event.x <= width + MIN:
            mark *= 4
        if height - MIN <= event.y <= height + MIN:
            mark *= 2

        if mark == 1:
            move_or_resize = False
        else: 
            move_or_resize = True
        if cursor == False:
            side = edges[str(mark)]
        else:
            side = cursors[str(mark)]
        return (move_or_resize, side)

    def _set_cursor(self, cursor_type):
        screen = self.window.get_screen()
        gdk_window = screen.get_root_window()
        cursor = Gdk.Cursor(cursor_type)
        gdk_window.set_cursor(cursor)

    def on_main_window_enter_notify_event(self, window, event):
        move_or_resize, edge_type = self._check_move_or_resize(event)
        if move_or_resize == True:
            self._set_cursor(edge_type)
        else:
            self._set_cursor(Gdk.CursorType.HAND2)

    def on_main_window_motion_notify_event(self, window, event):
        self.on_main_window_enter_notify_event(window, event)

    def on_main_window_leave_notify_event(self, window, event):
        move_or_resize, cursor_type = self._check_move_or_resize(event, 
                cursor=True)
        if move_or_resize == True:
            self._set_cursor(cursor_type)
        else:
            self._set_cursor(Gdk.CursorType.ARROW)
