import ugfx
import os
import pyb
import stm
import buttons
import dialogs
from database import *
from filesystem import *
from app import *
import uio
import sys
import gc
import onboard

ugfx.init()
ugfx.clear()

width = ugfx.width()
height = ugfx.height()
buttons.init()
buttons.disable_menu_reset()

# Create visual elements
win_header = ugfx.Container(0,0,width,30)
win_files = ugfx.Container(0,33,int(width/2),height-33)
win_preview = ugfx.Container(int(width/2)+2,33,int(width/2)-2,height-33)
components = [win_header, win_files, win_preview]
ugfx.set_default_font(ugfx.FONT_TITLE)
components.append(ugfx.Label(3,3,width-10,29,"Choose App",parent=win_header))
ugfx.set_default_font(ugfx.FONT_MEDIUM)
options = ugfx.List(0,30,win_files.width(),win_files.height()-30,parent=win_files)
btnl = ugfx.Button(5,3,20,20,"<",parent=win_files)
btnr = ugfx.Button(win_files.width()-7-20,3,20,20,">",parent=win_files)
btnr.attach_input(ugfx.JOY_RIGHT,0)
btnl.attach_input(ugfx.JOY_LEFT,0)
components.append(options)
components.append(btnr)
components.append(btnl)
ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
l_cat = ugfx.Label(30,3,100,20,"",parent=win_files)
components.append(l_cat)
components.append(ugfx.Button(10,win_preview.height()-25,20,20,"A",parent=win_preview))
components.append(ugfx.Label(35,win_preview.height()-25,50,20,"Run",parent=win_preview))
components.append(ugfx.Button(80,win_preview.height()-25,20,20,"B",parent=win_preview))
components.append(ugfx.Label(105,win_preview.height()-25,100,20,"Back",parent=win_preview))
components.append(ugfx.Button(10,win_preview.height()-50,20,20,"M",parent=win_preview))
components.append(ugfx.Label(35,win_preview.height()-50,100,20,"Pin/Unpin",parent=win_preview))
ugfx.set_default_font(ugfx.FONT_SMALL)
author = ugfx.Label(1,win_preview.height()-78,win_preview.width()-3,20,"by: ",parent=win_preview)
desc = ugfx.Label(3,1,win_preview.width()-10,win_preview.height()-83,"",parent=win_preview,justification=ugfx.Label.LEFTTOP)
components.append(author)
components.append(desc)

categories = get_local_app_categories()
category_index = 0
pinned = database_get("pinned", [])

to_run = None

def update_options():
	options.disable_draw()
	while options.count():
		options.remove_item(0)

	l_cat.text(categories[category_index])

	out = []
	for app in get_local_apps(categories[category_index]):
		if app.get_attribute("built-in") == "hide":
			continue

		if app.folder_name in pinned:
			options.add_item("*%s" % app)
		else:
			options.add_item("%s" % app)
		out.append(app)

	last_selected_index = -1
	options.selected_index(0)
	options.enable_draw()
	return out

try:
	win_header.show()
	win_files.show()
	win_preview.show()

	displayed_apps = update_options()

	last_selected_index = -1

	while True:
		pyb.wfi()
		ugfx.poll()

		if buttons.is_triggered("JOY_LEFT"):
			category_index = max(0, category_index - 1)
			displayed_apps = update_options()
			last_selected_index = -1

		if buttons.is_triggered("JOY_RIGHT"):
			category_index = min(len(categories) - 1, category_index + 1)
			displayed_apps = update_options()
			last_selected_index = -1

		app = displayed_apps[options.selected_index()]
		if last_selected_index != options.selected_index():
			if options.selected_index() < len(displayed_apps):
				author.text("by: %s" % app.user)
				desc.text(app.description)
			last_selected_index = options.selected_index()

		if buttons.is_triggered("BTN_MENU"):
			if app.folder_name in pinned:
				pinned.remove(app.folder_name)
			else:
				pinned.append(app.folder_name)
			update_options()
			database_set("pinned", pinned)

		if buttons.is_triggered("BTN_B"):
			break

		if buttons.is_triggered("BTN_A"):
			to_run = app
			break

finally:
	for component in components:
		component.destroy()

if to_run:
	print("Running: %s" % to_run)
	buttons.enable_menu_reset()
	gc.collect()
	try:
		to_run.run()
	except Exception as e:
		s = uio.StringIO()
		sys.print_exception(e, s)
		u=pyb.USB_VCP()
		if u.isconnected():
			raise(e)
		else:
			ugfx.clear()
			ugfx.set_default_font(ugfx.FONT_SMALL)
			w=ugfx.Container(0,0,ugfx.width(),ugfx.height())
			l=ugfx.Label(0,0,ugfx.width(),ugfx.height(),s.getvalue(),parent=w)
			w.show()
			while True:
				pyb.wfi()
				if (buttons.is_triggered("BTN_B")) or (buttons.is_triggered("BTN_B")) or (buttons.is_triggered("BTN_MENU")):
					break
	onboard.semihard_reset()

