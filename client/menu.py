from uuid import uuid1
from .panel import Panel
from .menu_enum import Alignment
import curses

NEW_LINE = 10
CARRIAGE_RETURN = 13

class MenuItem:
     def __init__(self, label, data, selected=False):
          self.id = str(uuid1())
          self.data = data
          self.label = label

          def return_id(self):
               return self.data.get('id'), self.data.get('uri')

          self.action = return_id
          self.selected = selected 
     
     def __eq__(self, other):
         return self.id == other.id

     def __len__(self):
          return len(self.label)

     def __str__(self):
          self.label


class Menu(Panel):
     def __init__(self, title, dimensions, align=Alignment.LEFT,items = []):
          super(title, dimensions)
          self._align = align
          self.items = items

     def get_currently_selected(self):
          items = [x for x in self.items if x.selected]
          return None if not items else items[0]
     
     def _select(self, expr):
          current = self.get_currently_selected()
          index = self.items.index(current)
          new_index = expr(index)
          if new_index < 0:
               return
          if new_index > index and new_index >= len(self.items):
               return
          self.items[index].selected = False
          self.items[new_index].selected = True
     
     def next(self):
          self._select(lambda index: index +1 )

     def previous(self):
          self._select(lambda index: index -1)

     def _initialize_items(self):
          longest_label_item = max(self.items, key=len)
          for item in self.items:
               if item != longest_label_item:
                    padding = (len(longest_label_item) - len(item)) * ' '
               item.label = (f'{item}{padding}' if self._align == Alignment.LEFT else f'{padding}{item}')

               if not self.get_currently_selected():
                    self.items[0].selected = True

     def init(self):
          self._initialize_items()
     
     def handle_events(self, key):
          if key == curses.KEY_UP:
               self.previous()
          elif key == curses.KEY_DOWN:
               self.next()
          elif key == curses.KEY_ENTER or key == NEW_LINE or key ==CARRIAGE_RETURN:
               selected_item = self.get_currently_selected()
          return selected_item.action
     
     def __iter__(self):
          return iter(self.items)

     def update(self):
          pos_x = 1
          pos_y = 2
          for item in self.items:
               self._win.addstr(pos_x, pos_y, item.label, curses.A_REVERSE if item.selected else curses.A_NORMAL)
               pos_x += 1
          self._win.refresh()






