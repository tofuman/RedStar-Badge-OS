### Author: EMF Badge team
### Description: Change your name
### Category: Settings
### License: MIT
### Appname : Change name

import dialogs
from database import *
import buttons
import ugfx

ugfx.init()
buttons.init()

name = database_get("display-name", "")

name_new = dialogs.prompt_text("Enter your name", default=name, init_text = name, true_text="OK", false_text="Back", width = 310, height = 220)

database_set("display-name", name_new)
