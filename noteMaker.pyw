import re
import json
from tkinter import *
import tkinter.messagebox as fmsg
import tkinter.filedialog as fd
from tkfontchooser import askfont
from tkinter import ttk
import tkinter.font as tkf


file_name = "Untitled - NoteMaker"
issaved = False
isopenedfile = False
tbg = '#ffffff'
tfg = '#000000'
sbg = '#ffffff'
sfg = '#000000'
ibg = '#000000'
currTheme = 'notepad'
font_family = 'arial'
font_size = 20
font_style = 'normal'
d = re.compile(r"\d+")
disable_enter = False
has_Colun = False
tabs_Num = 0
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
	if(confes["custom"] != "null"):
		colors = confes["custom"].split("/")
		try:
			theme_update(colors[0],colors[1],colors[2],colors[3],colors[4])
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
	setTheme = theme_list[currTheme]
	setTheme()

def theme_red_rose():
	global currTheme
	currTheme = "red_rose"
	theme_update('#ffe2f3','#980058','#bf006f','#980058','#980058')

def theme_notepad():
	global currTheme
	currTheme = "notepad"
	theme_update('#ffffff','#000000','#ffffff','#000000','#000000')

def theme_nature_green():
	global currTheme
	currTheme = "nature_green"
	theme_update('#edffef','#009211','#00af14','#ffffff','#009211')

def theme_soft_cream():
	global currTheme
	currTheme = "soft_cream"
	theme_update('#fdf6e3','#ffba00','#efe8d5','#ffffff','#ffba00')

def theme_winter_blue():
	global currTheme
	currTheme = "winter_blue"
	theme_update('#e5f9ff','#007092','#34b0d5','#ffffff','#007092')

def theme_night_owl():
	global currTheme
	currTheme = "night_owl"
	theme_update('#282c34','#ffffff','#282c34','#8e9a87','#ffffff')

def theme_update(tbg_para,tfg_para,sbg_para,sfg_para,ibg_para):
	try:
		staus.config(bg=sbg_para,fg=sfg_para)
		main_textarea.config(bg=tbg_para,fg=tfg_para,insertbackground=ibg_para)
	except Exception as e:
		global tbg,tfg,sbg,sfg,ibg
		tbg = tbg_para
		tfg = tfg_para
		sbg = sbg_para
		sfg = sfg_para
		ibg = ibg_para


configure()

def exit_window():
	global currTheme,font_family,font_size,font_style,isopenedfile
	with open('conf.json','w') as f:
		conf = json.dumps({
		"use custom color":"color in hexa_decimal like :- tbg/tfg/sbg/sfg/ibg",
		"theme":currTheme,
		"font_family":font_family,
		"font_size":font_size,
		"font_style":font_style,
		"custom":"null"
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
	fmsg.showinfo('NoteMaker - Create Efficient notes',f'developer name:- prashant maurya\nVersion :- 7.1\nThanks To using this notemaker plese loving this.')

def delete_to_space(event):
	sign = [" ","#","=","$",'@',"&",",",":"]
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
	file_name = "Untitled - NoteMaker"
	root.title(file_name)
	isopenedfile = False
	issaved = False

def Save_file():
	global issaved,isopenedfile
	if isopenedfile and file_name is not "Untitled - NoteMaker":
		f = open(file_name,'w')
		f.write(main_textarea.get("1.0",END).strip())
		f.close()
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
	global issaved,isopenedfile,has_Colun,tabs_Num
	if (event.state==12 or event.state==4) and event.keysym=='z':
		print('undo_write is called')
		Undo_write()
		return
	if (event.state==12 or event.state==4) and event.keysym=='s':
		if isopenedfile:
			Save_file()
		else:
			create_file()
	matches = getIndex()
	start_row=int(matches[1])
	start_column=int(matches[0])
	if event.keysym=='Return' and event.widget.get(INSERT,f"{start_column}.{start_row+3}") == ">> ":
		main_textarea.delete(f'{start_column}.0',f'{start_column}.{start_row+3}')
	if event.keysym=="Return" and start_row==3:
		main_textarea.delete(f'{start_column}.0',f'{start_column}.{start_row}')
		return
	if (event.state==12 or event.state==4) and event.keysym=="o":
		Open_file()
	if issaved:
		root.title(file_name)
	elif event.keysym>="a" and event.keysym<="z":
		root.title('*'+file_name)
		staus.update()
	previos_char = main_textarea.get(f'{start_column}.{start_row - 1}', INSERT)
	if previos_char==">" and event.keysym=="BackSpace" and tabs_Num!=0:
		delete_to_space(event)
		tabs_Num=0
	if previos_char ==":" and event.keysym=="Return":
		has_Colun = True
		tabs_Num += 1
	staus.config(anchor="w")
	Editor_state.set("Tabs_num : "+str(tabs_Num))
	issaved = False


def getIndex():
	return d.findall(main_textarea.index(INSERT))

def insert_next_line(event):
	global disable_enter,has_Colun,tabs_Num
	if event.keysym > 'a' and event.keysym < 'z':
		print('undo_save is called',event.keysym)
		Undo_save()
	pos = main_textarea.index(INSERT)
	matches = getIndex()
	start_row=int(matches[1])
	start_column=int(matches[0])
	if has_Colun:
		for i in range(tabs_Num):
			main_textarea.insert(INSERT, "\t")
		for i in range(tabs_Num):
			main_textarea.insert(INSERT, ">")
		has_Colun = False
		return

	if event.keysym=="Return" and not disable_enter:
		if tabs_Num != 0:
			for i in range(tabs_Num):
				main_textarea.insert(INSERT,"\t")
			for i in range(tabs_Num):
				main_textarea.insert(INSERT,">")
		else:
			event.widget.insert(INSERT,">> ")
		return
	if main_textarea.get(f'{start_column}.{start_row - 3}', f'{start_column}.{start_row}') == ".nn":
		main_textarea.delete(f'{start_column}.{start_row-3}',f'{start_column}.{start_row}')
		main_textarea.insert(INSERT,"NOTE :- ")
		return
	if main_textarea.get(f'{start_column}.{start_row - 5}', f'{start_column}.{start_row}') == ".exit":
		exit_window()
		return

	if event.keysym=='parenleft':
		main_textarea.insert(INSERT,')')
	elif event.keysym=='braceleft':
		main_textarea.insert(INSERT,'}')
	elif event.keysym=='bracketleft':
		main_textarea.insert(INSERT,']')
	elif event.keysym=="quoteright":
		main_textarea.insert(INSERT,"'")
	elif event.keysym=='quotedbl':
		main_textarea.insert(INSERT,'"')
	main_textarea.mark_set("insert",pos)
	disable_enter = False

def create_file():
	global file_name,isopenedfile,disable_enter,issaved
	if isopenedfile:
		Save_file()
		close_file()
		isopenedfile = False
		root.title("Untitled - NoteMaker")
	disable_enter = True
	opened_file = fd.asksaveasfile(filetypes=[('Text Files','*.txt')],defaultextension='*.note')
	if opened_file is None:
		return
	opened_file.write(main_textarea.get("1.0",END).strip())
	opened_file.close()
	isopenedfile = True
	file_name = opened_file.name
	root.title(file_name)
	issaved = True

def Open_file():
	global isopenedfile,file_name,issaved
	if isopenedfile:
		Save_file()
		close_file()
		isopenedfile = False
	main_textarea.delete('0.0',END)
	root.title("Untitled - NoteMaker")
	staus.update()
	opened_file = fd.askopenfile(mode='r',filetypes=[('Text Files','*.txt')])
	if opened_file is None:
		return
	for line in opened_file :
		main_textarea.insert(INSERT,line)
	opened_file.close()
	isopenedfile = True
	file_name = opened_file.name
	root.title(file_name)

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
# root.bind('Configure',check_typer_mode)
# root.resizable(False,False)
root.wm_iconbitmap('noteMakerIco.ico')
Editor_state = StringVar()
root.protocol("WM_DELETE_WINDOW", exit_window)
typer_mode = IntVar()
wraps = IntVar()
root.title('Untitled - NoteMaker')
Editor_state.set("Welcome sir")

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
# m2.add_command(label='Typer Mode',command=change_screen)
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
m2.add_cascade(label='Theme',menu=theme)
menu.add_cascade(label='Edit',menu=m2)

# creating submenu tools
m3 = Menu(menu,tearoff=0)
m3.add_command(label='about		',command=about)
menu.add_cascade(label='help',menu=m3)

# creating status bar by label
staus = Label(root, textvariable=Editor_state, bg=sbg, fg=sfg, font='sarif 15 normal',height=1)
staus.pack(fill=X,side=BOTTOM)

text_frame = Frame(root)
text_frame.pack(side=TOP,fill="x")

# creating scrolbar fot main text_area
sc_y = Scrollbar(text_frame,troughcolor="red")
sc_y.pack(side=RIGHT,fill=Y)

sc_x = Scrollbar(text_frame,orient=HORIZONTAL,width=20)
sc_x.pack(side=BOTTOM,fill=X)

# creating textarea
main_textarea = Text(text_frame,insertbackground=ibg,tabs="0.5i",bg=tbg,fg=tfg,font=(font_family,font_size,font_style),yscrollcommand=sc_y.set,xscrollcommand=sc_x.set,wrap=NONE)
main_textarea.pack(fill='both',expand=True)
sc_y.config(command=main_textarea.yview)
sc_x.config(command=main_textarea.xview)
main_textarea.bind("<KeyRelease>",insert_next_line)
main_textarea.bind("<Key>",check_shortcut)
main_textarea.bind("<Control-BackSpace>",delete_to_space)
main_textarea.bind("<MouseWheel>",zoom_in_out)


root.config(menu=menu)
root.mainloop()
del tbg,tfg,sbg,sfg,ibg