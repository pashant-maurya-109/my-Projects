import re
import subprocess
import json
from tkinter import *
import tkinter.messagebox as fmsg
import tkinter.simpledialog as sd
import tkinter.filedialog as fd
from tkfontchooser import askfont
from tkinter.colorchooser import askcolor
from tkinter import ttk
import tkinter.font as tkf
import os

file_name = None
issaved = False
isopenedfile = False
tbg = '#ffffff'
tfg = '#000000'
cbg = 'null'
cfg = 'null'
currTheme = 'notepad'
font_family = 'arial'
font_size = 20
font_style = 'normal'
d = re.compile(r"\d+")
disable_enter = False
tabs_Num = 0
Line_Num = 0
hascode = False
def configure():
	global currTheme,font_family,font_size,font_style
	try:
		file = open('conf.json','r')
	except Exception as e:
		return
	with file as f:
		confes = json.loads(f.read())
	currTheme = confes["theme"]
	font_size = int(confes['font_size'])
	font_family = confes['font_family']
	font_style = confes['font_style']
	if confes["wrap"] is 1:
		wraps.set(1)
	if(confes["custom"] != "null/null"):
		colors = confes["custom"].split("/")
		try:
			if colors[0]=='null' and colors[1]!='null':
				theme_update(colors[0],'#000000')
			elif colors[0]=='null' and colors[1]!='null':
				theme_update('#ffffff',colors[1])
			else:
				theme_update(colors[0],colors[1])
		except Exception as e:
			pass
		return
	theme_list = {
	"red_rose":theme_red_rose,
	"winter_blue":theme_winter_blue,
	"soft_cream":theme_soft_cream,
	"nature_green":theme_nature_green,
	"notepad":theme_notepad,
	"night_owl":theme_night_owl
	}
	try:
		setTheme = theme_list[currTheme]
	except Exception as e:
		setTheme = theme_list["notepad"]
	setTheme()

def theme_red_rose():
	global currTheme
	currTheme = "red_rose"
	theme_update('#ffe2f3','#980058')

def theme_notepad():
	global currTheme
	currTheme = "notepad"
	theme_update('#ffffff','#000000')

def theme_nature_green():
	global currTheme
	currTheme = "nature_green"
	theme_update('#edffef','#009211')

def theme_soft_cream():
	global currTheme
	currTheme = "soft_cream"
	theme_update('#fdf6e3','#ffba00')

def theme_winter_blue():
	global currTheme
	currTheme = "winter_blue"
	theme_update('#e5f9ff','#007092')

def theme_night_owl():
	global currTheme
	currTheme = "night_owl"
	theme_update('#282c34','#ffffff')

def custom_Background():
	global cbg
	color = askcolor()
	cbg = color[1]
	main_textarea.config(fg=color[1],insertbackground=color[1])

def custom_Foreground():
	global cfg
	color = askcolor()
	cfg = color[1]
	main_textarea.config(fg=color[1],insertbackground=color[1])

def theme_update(tbg_para,tfg_para):
	try:
		main_textarea.config(bg=tbg_para,fg=tfg_para,insertbackground=tfg_para)
	except Exception as e:
		global tbg,tfg
		tbg = tbg_para
		tfg = tfg_para


def exit_window():
	global currTheme,font_family,font_size,font_style,isopenedfile
	with open('conf.json','w') as f:
		conf = json.dumps({
		"WARING":"PLESE DO NOT EDIT ANY FIELD INSTED OF CUSTOM",
		"use custom color":"color in hexa_decimal like :- tbg/tfg",
		"theme":currTheme,
		"font_family":font_family,
		"font_size":font_size,
		"font_style":font_style,
		"custom":f"{cbg}/{cfg}",
		'wrap':wraps.get()
		})
		num = len(conf)
		f.write("{\n")
		for index , line in enumerate(conf[1:(num-1)].split(",")):
			if(index==len(conf[1:(num-1)].split(","))-1):
				f.write(line+"\n")
			else:
				f.write(line+",\n")
		f.write("}")

	if isopenedfile:
		Save_file()
		close_file()
		isopenedfile = False
	root.destroy()

def about():
	fmsg.showinfo('NoteMaker - Create Efficient notes','Developer name:- Prashant maurya\nVersion :- 9.4\nThanks To using this notemaker plese loving this.')

def delete_to_space(event):
	sign = [" ","#","=","$",'@',"&",",",":",".","%","'",'"',";"]
	insert = main_textarea.index(INSERT)
	matches = d.findall(insert)
	start_row=int(matches[1])
	start_column=int(matches[0])
	s = main_textarea.get(f'{start_column}.{start_row-1}',f'{start_column}.{start_row}')
	while start_row is not 0:
		s = main_textarea.get(f'{start_column}.{start_row-1}',f'{start_column}.{start_row}')
		if (s in sign or start_row is 0):
			break
		start_row-=1
	main_textarea.delete(f'{start_column}.{start_row}',insert)

def close_file():
	global isopenedfile,file_name,issaved
	file_name = None
	root.title("Untitled - NoteMaker")
	isopenedfile = False
	issaved = False

def Save_file():
	global issaved,isopenedfile
	if isopenedfile and file_name is not None:
		with open(file_name,'w') as f:
			f.write(main_textarea.get("1.0",END).strip())
		root.title(file_name)
		issaved = True
	else:
		create_file()

def Undo_save():
	try:
		with open('temp.txt','w') as f:
			f.write(main_textarea.get('1.0',END))
	except Exception as e:
		with open('temp.txt','x') as f:
			f.write(main_textarea.get('1.0',END))

def Undo_write():
	main_textarea.delete('1.0',END)
	try:
		with open('temp.txt','r') as f:
			main_textarea.insert(INSERT,f.read())
	except Exception as e:
		with open('temp.txt','x') as f:
			pass


def check_shortcut(event):
	global issaved,isopenedfile,tabs_Num,Line_Num,hascode
	if checkChar(event.char):
		issaved = False

	if (event.state==12 or event.state==4) and event.keysym=='z':
		Undo_write()
		return
	if (event.state==12 or event.state==4) and event.keysym=='s':
		if isopenedfile:
			Save_file()
		else:
			create_file()
	valid_line = re.compile("\\s+\\d+\.\\d+")
	matches = getIndex()
	start_row=int(matches[1])
	start_column=int(matches[0])

	if event.char=='{':
		main_textarea.insert(INSERT,'}')
		main_textarea.mark_set('insert',f"{start_column}.{start_row}")
		return
	elif event.char == '(':
		main_textarea.insert(INSERT, ')')
		main_textarea.mark_set('insert',f"{start_column}.{start_row}")
		return
	elif event.char == '[':
		main_textarea.insert(INSERT, ']')
		main_textarea.mark_set('insert',f"{start_column}.{start_row}")
		return
	elif event.char == "'":
		main_textarea.insert(INSERT, "'")
		main_textarea.mark_set('insert',f"{start_column}.{start_row}")
		return
	elif event.char == '"':
		main_textarea.insert(INSERT, '"')
		main_textarea.mark_set("insert", f"{start_column}.{start_row}")
		return

	if event.keysym=='Return' and event.widget.get(INSERT,f"{start_column}.{start_row+3}") == ">> ":
		main_textarea.delete(f'{start_column}.0',f'{start_column}.{start_row+3}')
		return

	if event.keysym=="Return" and start_row==3:
		main_textarea.delete(f'{start_column}.0',f'{start_column}.{start_row}')
		return

	if (event.state==12 or event.state==4) and event.keysym=="o":
		Open_file()
		return

	if main_textarea.get(f'{start_column}.{start_row - 9}', f'{start_column}.{start_row}') == "startcode" and event.keysym == "Return":
		tabs_Num += 1
		hascode = True
		return

	previos_char = main_textarea.get(f'{start_column}.{start_row - 1}', INSERT)

	if check_tree_line(get_curr_line(start_column)) is None and tabs_Num!=0:
		tabs_Num=0
		Line_Num=0
		return

	if previos_char =="{" and event.keysym== "Return":
		tabs_Num+=1
		pos = main_textarea.index(INSERT)
		main_textarea.insert(INSERT,'\n')
		for i in range(tabs_Num-1):
			main_textarea.insert(INSERT,"\t")
		main_textarea.mark_set('insert',pos)

	if previos_char ==":" and event.keysym=="Return":
		tabs_Num += 1
		Line_Num=1
		return
	try:
		line = check_tree_line(get_curr_line(start_column))
		if line is not None and event.keysym == "Return":
			sync_lines_in_tree(start_column,line)
	except Exception as e:
		pass
	del start_row,start_column,matches,line

def get_number_in_line(line,n):
	return re.compile("\\d+").findall(line)[n]

def check_tree_line(line):
	return  re.compile("\\s+\\d+\.\\d+").match(line)

def get_curr_line(start_column):
	return main_textarea.get(f'{start_column}.0',INSERT)

def sync_lines_in_tree(start_column,line):
	global tabs_Num,Line_Num
	try:
			line = line.group().split(".")
			check = line[0]
			tabs_Num = int(line[0])
			Line_Num = int(line[1])+1
			block = len(line[0])+1
			diff = 1
			start_column+=1
			line = main_textarea.get(f'{start_column}.0', f"{start_column}.100")
			if int(get_number_in_line(line,1)) != Line_Num:
				while check_tree_line(line) is None:
					start_column+=1
					line = main_textarea.get(f'{start_column}.0', f"{start_column}.100")
				diff= (int(get_number_in_line(line,1))-Line_Num)-1
			while check_tree_line(line) is not None :
				block_line = get_number_in_line(line,1)
				if check==line[0:block-1] and diff is 1:
					main_textarea.delete(f"{start_column}.{block}",f"{start_column}.{block+len(block_line)}")
					main_textarea.insert(f"{start_column}.{block}",f"{int(block_line)+1}")
				elif check==line[0:block-1] and diff is not 1:
					main_textarea.delete(f"{start_column}.{block}", f"{start_column}.{block + len(block_line)}")
					main_textarea.insert(f"{start_column}.{block}", f"{int(block_line) - diff}")
				if line[0]==">":
					break
				start_column+=1
				line = main_textarea.get(f'{start_column}.0',f"{start_column}.100")
			return
	except Exception as e:
		pass

def getIndex():
	return d.findall(main_textarea.index(INSERT))

def checkChar(x):
	valid_char = re.compile('[a-zA-Z0-9:;@!#%^&*\.\s]')
	try:
		valid_char.match(x).group()
		return True
	except Exception as e:
		return False

def insert_next_line(event):
	global disable_enter,has_Colun,tabs_Num,Line_Num,hascode
	try:
		matches = getIndex()
		start_row=int(matches[1])
		start_column=int(matches[0])
		if issaved:
			root.title(file_name)
		elif checkChar(event.char):
			if file_name is None:
				root.title('*' + 'Untitled - NoteMaker')
			else:
				root.title("*"+file_name)
		if checkChar(event.char):
			Undo_save()
		if main_textarea.get(f'{start_column}.{start_row - 3}', f'{start_column}.{start_row}') == ".nn" and checkChar(event.char):
			main_textarea.delete(f'{start_column}.{start_row-3}',f'{start_column}.{start_row}')
			main_textarea.insert(INSERT,"NOTE :- ")
			return
		if main_textarea.get(f'{start_column}.{start_row - 5}', f'{start_column}.{start_row}') == ".exit" and checkChar(event.char):
			main_textarea.delete(f'{start_column}.{start_row - 5}', f'{start_column}.{start_row}')
			exit_window()
			return
		if main_textarea.get(f'{start_column}.{start_row - 4}', f'{start_column}.{start_row}') == ".cmd" and checkChar(event.char):
			main_textarea.delete(f'{start_column}.{start_row - 4}', f'{start_column}.{start_row}')
			subprocess.run('start',shell=True,check=True)
			disable_enter = True
			return
		if main_textarea.get(f'{start_column}.{start_row - 6}', f'{start_column}.{start_row}') == ".cexit" and checkChar(event.char):
			main_textarea.delete(f'{start_column}.{start_row - 6}', f'{start_column}.{start_row}')
			hascode = False
			tabs_Num = 0
			Line_Num = 0
			return
	except Exception as e:
		pass

	if event.keysym=="Return" and not disable_enter:
		if tabs_Num != 0:
			for i in range(tabs_Num):
				main_textarea.insert(INSERT,"\t")
			if not hascode:
				main_textarea.insert(INSERT,f"{tabs_Num}.{Line_Num} >")
			Line_Num+=1
		else:
			event.widget.insert(INSERT,">> ")
		return


	if disable_enter:
		disable_enter = False

def create_file():
	global file_name,isopenedfile,disable_enter,issaved
	if isopenedfile:
		Save_file()
		close_file()
		isopenedfile = False
		root.title("Untitled - NoteMaker")
		file_name=None
		issaved = False
	disable_enter = True
	try:
		with fd.asksaveasfile(filetypes=[('Text Files','*.txt')],defaultextension='*.txt') as f:
			f.write(main_textarea.get("1.0", END).strip())
			file_name = f.name
		root.title(file_name)
		isopenedfile = True
		issaved = True
	except Exception as e:
			isopenedfile = False
			root.title("Untitled - NoteMaker")
			file_name = None
			issaved = False

def Open_file():
	global isopenedfile,file_name,issaved,disable_enter
	disable_enter = True
	if isopenedfile:
		Save_file()
		close_file()
		isopenedfile = False
		issaved = False
	main_textarea.delete('1.0',END)
	root.title("Untitled - NoteMaker")
	disable_enter = True
	try:
		with fd.askopenfile(mode='r',filetypes=[('Text Files','*.txt')]) as f:
			main_textarea.insert(INSERT,f.read())
			file_name = f.name
		isopenedfile = True
		root.title(file_name)
		issaved = True
	except Exception as e:
		isopenedfile = False
		issaved = True
		file_name = None

def change_font():
	global font_family,font_size,font_style
	f = askfont()
	if f is not '':
		font_family = f['family']
		font_size = int(f['size'])
		font_style = f['weight']
		main_textarea.config(font=(f['family'],f['size'],f['weight']))
		main_textarea.update()

def check_typer_mode():
	height = tkf.Font(font=main_textarea['font']).metrics('linespace')
	if typer_mode.get() is 1:
		root.geometry(f"1000x{height+55}+200+{555-height}")
	else:
		root.geometry("1000x500+190+100")

def zoom_in_out(event):
	global font_size,font_family,font_style
	if event.state==36 or event.state==38 or event.state==44 or event.state == 46:
		fmsg.showinfo("Error in zoom_in_out","Plese off your Scroll lock")

	if (event.state==12 or event.state ==4) and event.delta < 0 and font_size >= 10:
		font_size-=1
	elif (event.state==12 or event.state ==4) and event.delta > 0 and font_size <= 70:
		font_size+=1
	main_textarea.config(font = (font_family, font_size, font_style))
	main_textarea.update()

def setText_wrap():
	if wraps.get() == 1:
		main_textarea.config(wrap=WORD)
	else:
		main_textarea.config(wrap=NONE)

root = Tk()
root.geometry(f"1000x500+190+100")
root.title(file_name)
root.wm_iconbitmap('nmico.ico')
Editor_state = StringVar()
root.protocol("WM_DELETE_WINDOW", exit_window)
typer_mode = IntVar()
wraps = IntVar()
root.title('Untitled - NoteMaker')
configure()

# creating menu
menu = Menu(root)

# creating submenu file
m1 = Menu(menu,tearoff=0)
m1.add_command(label='New File',command=create_file)
m1.add_command(label='Open file',command=Open_file)
m1.add_command(label='save file',command=Save_file)
m1.add_command(label='close file',command=close_file)
m1.add_separator()
m1.add_command(label='Exit		',command=exit_window)


# creating submenu edit
menu.add_cascade(label='File',menu=m1)
m2 = Menu(menu,tearoff=0)
m2.add_command(label='Font',command=change_font)
m2.add_checkbutton(label='Typer mode',onvalue=1, offvalue=0,variable=typer_mode,command=check_typer_mode)
m2.add_checkbutton(label='Word Wrap',onvalue=1, offvalue=0,variable=wraps,command=setText_wrap)

# creating theme menu in edit
theme = Menu(m2,tearoff=0)
theme.add_command(label='Red Rose',command = theme_red_rose)
theme.add_command(label='Nature green',command = theme_nature_green)
theme.add_command(label='Winter Blue',command = theme_winter_blue)
theme.add_command(label='Night Owl',command = theme_night_owl)
theme.add_command(label='Soft Cream',command = theme_soft_cream)
theme.add_command(label='Notepad',command = theme_notepad)
theme.add_command(label="custom Background",command = custom_Background)
theme.add_command(label="custom Foreground",command = custom_Foreground)
m2.add_cascade(label='Theme',menu=theme)
menu.add_cascade(label='Edit',menu=m2)

# creating submenu tools
m3 = Menu(menu,tearoff=0)
m3.add_command(label='about		',command=about)
menu.add_cascade(label='help',menu=m3)

# creating status bar by label
# staus = Label(root, textvariable=Editor_state, bg=sbg, fg=sfg, font='sarif 15 normal',height=1)
# staus.pack(fill=BOTH,side=BOTTOM)

text_frame = Frame(root)
text_frame.pack(side=TOP,expand=True,fill="both")

# creating scrolbar fot main text_area
sc_y = Scrollbar(text_frame,troughcolor="red")
sc_y.pack(side=RIGHT,fill=Y)

sc_x = Scrollbar(text_frame,orient=HORIZONTAL,width=20)
sc_x.pack(side=BOTTOM,fill=X)

# creating textarea
main_textarea = Text(text_frame,insertbackground=tfg,tabs="0.5i",bg=tbg,fg=tfg,font=(font_family,font_size,font_style),yscrollcommand=sc_y.set,xscrollcommand=sc_x.set,wrap=NONE)
main_textarea.pack(fill='both',expand=True)
sc_y.config(command=main_textarea.yview)
sc_x.config(command=main_textarea.xview)
main_textarea.bind("<KeyRelease>",insert_next_line)
main_textarea.bind("<Key>",check_shortcut)
main_textarea.bind("<Control-BackSpace>",delete_to_space)
main_textarea.bind("<MouseWheel>",zoom_in_out)

del tbg,tfg

root.config(menu=menu)
root.mainloop()
