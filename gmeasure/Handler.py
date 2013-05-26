#from gi.repository import cairo
import cairo
from gi.repository import Gdk
from gi.repository import Gtk

from gmeasure import Config

class Handler:

    def __init__(self, builder):
        self.builder = builder
        self.conf = Config.load_conf()

        self.window = builder.get_object('main_window')
        self.window.resize(*self.conf['window']['size'])
        self.window.move(*self.conf['window']['pos'])
        self.screen = self.window.get_screen()
        self.gdk_window = self.screen.get_root_window()
        visual = self.screen.get_rgba_visual()
        if visual != None and self.screen.is_composited():
            self.window.set_visual(visual)

    def run(self):
        self.window.show_all()
        Gtk.main()

    def on_app_exit(self, widget, event=None):
        self.conf['window']['pos'] = self.window.get_position()
        self.conf['window']['size'] = self.window.get_size()
        self._set_cursor(Gdk.CursorType.ARROW)
        Config.dump_conf(self.conf)
        Gtk.main_quit()

    def on_main_window_draw(self, window, cr):
        cr.set_source_rgba(*self.conf['colors']['win'])
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

    def on_drawingarea_draw(self, window, cr):
        win_size = self.window.get_size()
        edge_length = max(win_size)

        cr.set_source_rgba(*self.conf['colors']['line'])
        cr.set_line_width(3)
        cr.move_to(0, 0)
        cr.line_to(edge_length, 0)
        cr.stroke()
        cr.move_to(0, 0)
        cr.line_to(0, edge_length)
        cr.stroke()

        cr.set_font_size(10)
        cr.select_font_face('Serif', cairo.FONT_SLANT_NORMAL,
                cairo.FONT_WEIGHT_BOLD)


        for i in range(0, edge_length, 5):
            if i % 100 == 0:
                length = 25
                if i != 0:
                    cr.set_source_rgba(*self.conf['colors']['num'])
                    cr.move_to(i+2, 2+length)
                    cr.show_text(str(i))

                    cr.move_to(2+length, i+2)
                    cr.show_text(str(i))
            elif i % 50 == 0:
                length = 15
            elif i % 10 == 0:
                length = 10
            else:
                length = 5

            cr.set_source_rgba(*self.conf['colors']['mark'])
            cr.set_line_width(1)
            cr.move_to(i, 0)
            cr.line_to(i, length)
            cr.stroke()
            cr.move_to(0, i)
            cr.line_to(length, i)
            cr.stroke()
     
    def show_about_dialog(self, btn):
        about = self.builder.get_object('aboutdialog')
        about.run()
        about.hide()

    # color selections
    def _select_color(self, color_type):
        title='Select a Color..'
        rgba = Gdk.RGBA(*self.conf['colors'][color_type])

        colorsel_dialog = Gtk.ColorSelectionDialog(title)
        colorsel = colorsel_dialog.get_color_selection()
        colorsel.set_has_opacity_control(True)
        colorsel.set_current_rgba(rgba)
        response = colorsel_dialog.run()
        colorsel_dialog.destroy()
        if response == Gtk.ResponseType.OK:
            rgba = colorsel.get_current_rgba()
            rgba = (rgba.red, rgba.green, rgba.blue, rgba.alpha)
            self.conf['colors'][color_type] = rgba
            w, h = self.window.get_size()
            self.window.resize(w+1, h+1)

    def on_background_color_activate(self, menuitem):
        self._select_color('win')

    def on_number_color_activate(self, menuitem):
        self._select_color('num')

    def on_line_color_activate(self, menuitem):
        self._select_color('line')

    def on_mark_color_activate(self, menuitem):
        self._select_color('mark')
