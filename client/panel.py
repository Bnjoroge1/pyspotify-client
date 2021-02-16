import curses
import curses.panel
from uuid import uuid1

class Panel:
     def __init__(self, title, dimension):
          height, width, y_axis, x_axis = dimension

          self._win = curses.newwin(height, width, y_axis, x_axis)
          self._win.box()
          self._panel = curses.panel.new_panel(self._win)
          self.title = title
          self._id = uuid1()

          self._set_title()
          self.hide()

     def hide(self):
          self._panel.hide()

     def _set_title(self):
          formatted_title = f' {self._title} '
          self._win.addstr(0, 2, formatted_title, curses.A_REVERSE)
     
     def show(self):
          self._win.clear()
          self._win.box()
          self._set_title()
          curses.curs_set(0)
          self._panel.show()

     def cursor_is_visible(self):
          return not self._panel.hidden()

     def __eq__(self, other):
          return self._id  == other._id


