05/21/2024

So the menu is created by:

- rendering a page in display.py
- button/menu state handled in menu.py with update_state
- menu repainted with update_menu in menu.py

Wanted to use nested JSON definitions to render menus

Also has to be dynamic with regard to screen sizes which rotation is an issue eg. a display that is portrait
