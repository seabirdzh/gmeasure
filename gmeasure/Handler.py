#from gi.repository import cairo
import cairo
from gi.repository import Gdk
from gi.repository import Gtk

class Handler:

    def __init__(self, builder):
        self.builder = builder

        self.window = builder.get_object('main_window')
        self.screen = self.window.get_screen()
        self.gdk_window = self.screen.get_root_window()
        visual = self.screen.get_rgba_visual()
        if visual != None and self.screen.is_composited():
            self.window.set_visual(visual)

    def run(self):
        self.window.show_all()
        Gtk.main()

    def on_app_exit(self, widget, event=None):
        self._set_cursor(Gdk.CursorType.ARROW)
        Gtk.main_quit()

    def on_main_window_draw(self, window, cr):
        cr.set_source_rgba(0.2, 0.2, 0.2, 0.4)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

    def on_main_window_button_press_event(self, window, event):
        label_menu = self.builder.get_object('label_menu')
        if event.type != Gdk.EventType.BUTTON_PRESS:
            return False

        if event.button == 3:
            label_menu.popup(None, None, None, None, 
                    event.button, event.time)
        elif event.button == 1:
            move_or_resize, edge_type = self._check_move_or_resize(event)
            if move_or_resize == False:
                self.window.begin_move_drag(event.button, event.x_root,
                        event.y_root, event.time)
            else:
                self.window.begin_resize_drag(edge_type, event.button, 
                        event.x_root, event.y_root, event.time)

    def _check_move_or_resize(self, event):
        '''
        Return True when need to resize, else False.
        '''
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
        move_or_resize = mark != 1
        return (move_or_resize, edges[str(mark)])

    def _set_cursor(self, cursor_type):
        cursor = Gdk.Cursor(cursor_type)
        self.gdk_window.set_cursor(cursor)

    def on_main_window_enter_notify_event(self, window, event):
        self.do_change_cursor(window, event)

    def do_change_cursor(self, window, event):
        move_or_resize, edge_type = self._check_move_or_resize(event)
        cursors = {
                Gdk.WindowEdge.SOUTH: Gdk.CursorType.BOTTOM_SIDE,
                Gdk.WindowEdge.EAST: Gdk.CursorType.RIGHT_SIDE,
                Gdk.WindowEdge.SOUTH_EAST: Gdk.CursorType.BOTTOM_RIGHT_CORNER,
                }
        if move_or_resize == True:
            self._set_cursor(cursors[edge_type])
        else:
            self._set_cursor(Gdk.CursorType.HAND2)

    def on_main_window_motion_notify_event(self, window, event):
        self.do_change_cursor(window, event)

    def on_main_window_leave_notify_event(self, window, event):
        self._set_cursor(Gdk.CursorType.ARROW)
