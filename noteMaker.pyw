import re
import subprocess
import json
from tkinter import *
import tkinter.messagebox as fmsg
import tkinter.filedialog as fd
from tkfontchooser import askfont
from tkinter.colorchooser import askcolor
import tkinter.font as tkf

file_name = None
issaved = False
isopenedfile = False
cbg = '#ffffff'
cfg = '#000000'
font_family = 'arial'
font_size = 20
font_style = 'normal'
d = re.compile(r"\d+")
disable_enter = False
tabs_Num = ""
Line_Num = 0
hascode = False
select_text = ""
def configure():
	global font_family,font_size,font_style
	try:
		with open('conf.json','r') as f:
			confes = json.loads(f.read())
	except Exception as e:
		return
	font_size = int(confes['font_size'])
	font_family = confes['font_family']
	font_style = confes['font_style']
	if confes["wrap"] == 1:
		wraps.set(1)
		setText_wrap()
	colors = confes["theme"].split("/")
	try:
		theme_update(colors[0],colors[1])
	except Exception as e:
		pass

def theme_night_owl():
	global cfg,cbg
	cbg = '#282c34'
	cfg = '#ffffff'
	theme_update('#282c34','#ffffff')

def custom_Background():
	global cbg,cfg
	color = askcolor()
	cbg = color[1]
	theme_update(cbg,cfg)

def custom_Foreground():
	global cbg, cfg
	color = askcolor()
	cfg = color[1]
	theme_update(cbg, cfg)

def theme_update(tbg_para,tfg_para):
	try:
		main_textarea.config(bg=tbg_para,fg=tfg_para,insertbackground=tfg_para)
	except Exception as e:
		global cbg,cfg
		cbg = tbg_para
		cfg = tfg_para


def exit_window():
	global cbg,cfg,font_family,font_size,font_style,isopenedfile
	with open('conf.json','w') as f:
		conf = json.dumps({
		"font_family":font_family,
		"font_size":font_size,
		"font_style":font_style,
		"theme":f"{cbg}/{cfg}",
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
	insert = main_textarea.index(INSERT)
	matches = getIndex()
	start_row=int(matches[1])
	while start_row is not 0:
		s = main_textarea.get(f'{matches[0]}.{start_row-1}',f'{matches[0]}.{start_row}')
		if (not checkChar(s) or start_row is 0):
			start_row+=1
			break
		start_row-=1
	main_textarea.delete(f'{matches[0]}.{start_row}',insert)

def backspace_shorcuts(event):
	index = getIndex()
	if index[1] == "3" and Line_Num==0 and not hascode:
		main_textarea.delete(f'{int(index[0])}.0',INSERT)

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

def Undo_write(event):
	index = getIndex()
	main_textarea.delete('1.0',END)
	try:
		with open('temp.txt','r') as f:
			main_textarea.insert(INSERT,f.read())
		main_textarea.mark_set('insert',f"{index[0]}.{index[1]}")
	except Exception as e:
		with open('temp.txt','x') as f:
			pass

def save_shortcut(event):
	if isopenedfile:
		Save_file()
	else:
		create_file()

def check_shortcut(event):
	global issaved,isopenedfile,tabs_Num,Line_Num,hascode
	if checkChar(event.char):
		issaved = False
	index = getIndex()
	if not hascode and check_tree_line(get_curr_line(index[0])) is None and tabs_Num!="":
		tabs_Num=""
		Line_Num=0
		return

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
			tabs_Num = get_space(line[0])
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
	valid_char = re.compile('[a-zA-Z0-9]')
	try:
		valid_char.match(x).group()
		return True
	except Exception as e:
		return False

def Return_shortcuts(event):
	global  tabs_Num,hascode,Line_Num
	index = getIndex()
	if index[1] == "3" and Line_Num==0 and not hascode:
		main_textarea.delete(f'{index[0]}.0', INSERT)

	# change apply here
	if main_textarea.get(f'{index[0]}.{int(index[1]) - 9}',INSERT) == "startcode":
		tabs_Num = "\t"
		hascode = True

	if hascode:
		tabs_Num =  get_space(main_textarea.get(f"{index[0]}.0",INSERT))[0:-1]
		return

	# change apply here
	if main_textarea.get(f"{index[0]}.{int(index[1]) - 1}", INSERT) == "{":
		tabs_Num = get_space(get_curr_line(index[0]))
		pos = main_textarea.index(INSERT)
		main_textarea.insert(INSERT, '\n'+tabs_Num)
		main_textarea.mark_set('insert', pos)
		return
	# change apply here
	if main_textarea.get(f"{index[0]}.{int(index[1]) - 1}", INSERT) == ":":
		tabs_Num += "\t"
		Line_Num = 1
		return

	line = check_tree_line(get_curr_line(int(index[0])))
	if line is not None:
		sync_lines_in_tree(int(index[0]),line)
		return

def get_space(line):
	try:
		return re.compile("\\s+").match(line).group()
	except Exception as e:
		return "\t"

def keyrelease_shortcuts(event):
	global disable_enter,tabs_Num,Line_Num,hascode
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
		Undo_save()
		if main_textarea.get(f'{start_column}.{start_row - 2}', f'{start_column}.{start_row}') == ".N" and checkChar(event.char):
			main_textarea.delete(f'{start_column}.{start_row-2}',f'{start_column}.{start_row}')
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

		# change apply here
		if main_textarea.get(f'{start_column}.{start_row - 6}', f'{start_column}.{start_row}') == ".cexit" and checkChar(event.char):
			main_textarea.delete(f'{start_column}.{start_row - 6}', f'{start_column}.{start_row}')
			hascode = False
			tabs_Num = ""
			Line_Num = 0
			return
	except Exception as e:
		pass


def Return_Rlease_shortcut(event):
	global  disable_enter,tabs_Num,Line_Num,hascode
	if disable_enter:
		disable_enter = False
	elif tabs_Num != "" or hascode:
		if hascode:
			main_textarea.insert(INSERT,tabs_Num+"\t")
		else:
			main_textarea.insert(INSERT,tabs_Num)
			main_textarea.insert(INSERT,f"{len(tabs_Num)}.{Line_Num} >")
			Line_Num+=1
	else:
		event.widget.insert(INSERT,">> ")


def selection_shorcuts(event):
	try:
		select_text = main_textarea.selection_get()
		index = getIndex()
		if event.char == "[":
			main_textarea.insert(INSERT, event.char + select_text + "]")
			main_textarea.delete(f"{index[0]}.{int(index[1])-1}",INSERT)
		elif event.char == "{":
			main_textarea.insert(INSERT, event.char + select_text + "}")
			main_textarea.delete(f"{index[0]}.{int(index[1])-1}",INSERT)
		elif event.char == "(":
			main_textarea.insert(INSERT, event.char + select_text + ")")
			main_textarea.delete(f"{index[0]}.{int(index[1])-1}",INSERT)
		else:
			main_textarea.insert(INSERT, event.char + select_text)
	except Exception as e:
		pos = main_textarea.index(INSERT)
		if event.char == "[":
			main_textarea.insert(INSERT, "]")
		elif event.char == "{":
			main_textarea.insert(INSERT, "}")
		elif event.char == "(":
			main_textarea.insert(INSERT, ")")
		else:
			main_textarea.insert(INSERT,event.char)
		main_textarea.mark_set('insert',pos)

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

def Open_file_shortcut(event):
	Open_file()

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
		root.geometry(f"1000x{height+55}+200+{565-height}")
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
theme.add_command(label='Dark mode',command = theme_night_owl)
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
main_textarea = Text(text_frame,insertbackground=cfg,tabs="0.5i",bg=cbg,fg=cfg,font=(font_family,font_size,font_style),yscrollcommand=sc_y.set,xscrollcommand=sc_x.set,wrap=NONE)
main_textarea.pack(fill='both',expand=True)
sc_y.config(command=main_textarea.yview)
sc_x.config(command=main_textarea.xview)
main_textarea.bind("<KeyRelease>",keyrelease_shortcuts)
main_textarea.bind("<Key>",check_shortcut)
main_textarea.bind("<Control-BackSpace>",delete_to_space)
main_textarea.bind("<MouseWheel>",zoom_in_out)
main_textarea.bind("<Control-s>",save_shortcut)
main_textarea.bind("<Control-z>",Undo_write)
main_textarea.bind("<Control-o>",Open_file_shortcut)
main_textarea.bind("<KeyRelease-Return>", Return_Rlease_shortcut)
# main_textarea.bind("<Motion>",draging_textarea)
main_textarea.bind("<BackSpace>",backspace_shorcuts)
main_textarea.bind("<Return>",Return_shortcuts)
main_textarea.bind("<'>",selection_shorcuts)
main_textarea.bind("<{>",selection_shorcuts)
main_textarea.bind('<">',selection_shorcuts)
main_textarea.bind('<[>',selection_shorcuts)
main_textarea.bind('<`>',selection_shorcuts)
main_textarea.bind('<(>',selection_shorcuts)
# main_textarea.bind('<KeyRelease-{>',selection_Release_shortcut)
# main_textarea.bind('<KeyRelease-(>',selection_Release_shortcut)
# main_textarea.bind('<KeyRelease-[>',selection_Release_shortcut)

root.config(menu=menu)
root.mainloop()
