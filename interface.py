from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
import sys

tk = Tk()
tk.wm_title('LaTeX Proof Editor: New File')

statements = []
reasons = []
line_nums = []
refs = []
targets = []

log = []
history = 0

stops = ['.', ',', ';', '$', '{', '@', '}', '=']
codes = ['`a', '`t', '`s', '`r', '`l', '`c', '`par', '`per', '`q', '`nc', '`npar', '`nper', '`n', '`th', '`f', '`d',
         '`m', '`sq', '`sim']
latex = ['\\angle', '\\triangle', '\\overline', '\\overrightarrow', '\\overleftrightarrow', '\\cong', '\\parallel',
         '\\perp', '\\square', '\\ncong', '\\nparallel', 'not\\perp', '\\ne', '\\therefore', '\\frac', '^{\circ}',
         '\\times', '\\sqrt', '\\sim']
bracketed = ['`s', '`r', '`l', '`sq']
actual = ['angle', 'triangle', 'segment', 'ray', 'line', 'congruent', 'parallel', 'perpendicular', 'quadrilateral',
          'not congruent', 'not parallel', 'not perpendicular', 'not equal', 'therefore', 'fraction', 'degree',
          'multiplication', 'square root', 'similar']

selected = 0

codes.extend([i.title() for i in codes])
latex.extend(latex)
actual.extend([i.title() for i in actual])


def get_data():
    out = '['

    for x in range(0, len(statements) - 1, 1):
        s = parse(statements[x].get()).replace('\\', '\\\\')
        r = parse(reasons[x].get()).replace('\\', '\\\\')
        f = refs[x].get()
        out += '[\'' + s + '\',\'' + r + '\',\'' + f + '\'],'

    s = parse(statements[-1].get()).replace('\\', '\\\\')
    r = parse(reasons[-1].get()).replace('\\', '\\\\')
    f = refs[-1].get()
    out += '[\'' + s + '\',\'' + r + '\',\'' + f + '\']]'

    return out


def save_call(event):
    event.widget.focus()
    save_file()


def save_file():
    out = get_data()
    filer = tkFileDialog.asksaveasfile(mode='w', defaultextension='.proof', filetypes=[('Proof File', '*.proof')])
    if filer is None:
        return
    filer.write(out)
    filer.close()


def open_data(data):
    global statements
    global reasons
    global line_nums
    global refs
    global targets
    global selected

    lines = eval(data)

    for x in range(0, len(statements), 1):
        line_nums[x].grid_forget()
        statements[x].grid_forget()
        reasons[x].grid_forget()
        refs[x].grid_forget()
        targets[x].grid_forget()

    statements = []
    reasons = []
    line_nums = []
    refs = []
    targets = []

    for x in range(0, len(lines), 1):
        line_data = lines[x]

        for y in range(0, len(line_data), 1):
            for z in range(0, len(latex), 1):
                line_data[y] = line_data[y].replace(latex[z], codes[z])
            print line_data[y]

        l1 = Label(f3, text=str(len(statements)+1)+'.', width=5)
        l1.grid(row=len(statements), column=0)

        en1 = Entry(f3, width=50, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
        en1.grid(row=len(statements), column=1, padx=1)
        en1.insert(END, line_data[0])

        en2 = Entry(f3, width=50, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
        en2.grid(row=len(statements), column=2, padx=1)
        en2.insert(END, line_data[1])

        sb = Entry(f3, width=10, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
        sb.grid(row=len(statements), column=3, padx=1)
        sb.insert(END, line_data[2])

        l2 = Label(f3, width=5)
        l2.grid(row=len(statements), column=4)

        line_nums.append(l1)
        statements.append(en1)
        reasons.append(en2)
        refs.append(sb)
        targets.append(l2)
    
    
def open_call(event):
    event.widget.focus()
    open_file()


def open_file():
    filer = tkFileDialog.askopenfile(mode='r', defaultextension='.proof', filetypes=[('Proof File', '*.proof')])
    if filer is None:
        return
    try:
        global statements
        global reasons
        global line_nums
        global refs
        global targets
        global selected
        global log

        selected = 0
        if tkMessageBox.askyesno('', 'Are you sure you want to open a file?\nAll unsaved changes will be lost.'):
            open_data(filer.read())
            tk.wm_title('LaTeX Proof Editor: ' + os.path.basename(filer.name)[:-6])
            log = []
    except TypeError:
        tkMessageBox.showerror('', 'Something went wrong reading file!\nThe file might be corrupted')
    except SyntaxError:
        tkMessageBox.showerror('', 'Something went wrong reading file!\nThe file might be corrupted')
    update()


def insert_call(event):
    event.widget.focus()
    insert()


def insert():
    try:
        add_log(get_data())
    except IndexError:
        pass

    l1 = Label(f3, text=str(len(statements)+1)+'.', width=5)
    l1.grid(row=len(statements), column=0)

    en1 = Entry(f3, width=50, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
    en1.grid(row=len(statements), column=1, padx=1)

    en2 = Entry(f3, width=50, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
    en2.grid(row=len(statements), column=2, padx=1)

    sb = Entry(f3, width=10, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
    sb.grid(row=len(statements), column=3, padx=1)

    l2 = Label(f3, width=5)
    l2.grid(row=len(statements), column=4)

    line_nums.append(l1)
    statements.append(en1)
    reasons.append(en2)
    refs.append(sb)
    targets.append(l2)


def insert_at_call(event):
    event.widget.focus()
    insert_at()


def insert_at():
    add_log(get_data())

    l1 = Label(f3, text=str(len(statements)+1)+'.', width=5)
    l1.grid(row=len(statements), column=0)

    en1 = Entry(f3, width=50, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
    en1.grid(row=selected, column=1, padx=1)

    en2 = Entry(f3, width=50, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
    en2.grid(row=selected, column=2, padx=1)

    sb = Entry(f3, width=10, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
    sb.grid(row=selected, column=3, padx=1)

    l2 = Label(f3, width=5)
    l2.grid(row=len(statements), column=4)

    line_nums.append(l1)
    statements.insert(selected, en1)
    reasons.insert(selected, en2)
    refs.insert(selected, sb)
    targets.append(l2)

    tab = [p2, e1, e2]

    for x in range(0, len(statements), 1):
        statements[x].grid(row=x, column=1)
        reasons[x].grid(row=x, column=2)
        refs[x].grid(row=x, column=3)
        tab.append(statements[x])
        tab.append(reasons[x])
        tab.append(refs[x])

    for x in tab:
        x.lift()


def remove_call(event):
    event.widget.focus()
    remove()


def remove():
    if len(line_nums) > 1 and selected < len(line_nums):
        add_log(get_data())

        line_nums[-1].grid_forget()
        statements[selected].grid_forget()
        reasons[selected].grid_forget()
        refs[selected].grid_forget()
        targets[-1].grid_forget()

        line_nums.pop()
        statements.pop(selected)
        reasons.pop(selected)
        refs.pop(selected)
        targets.pop()

    for x in range(0, len(statements), 1):
        statements[x].grid(row=x, column=1)
        reasons[x].grid(row=x, column=2)
        refs[x].grid(row=x, column=3)

    update()


def alarm_call(event):
    event.widget.focus_force()


def alarm():
    pass


def print_call(event):
    event.widget.focus()
    print_file()


def print_file():
    if tkMessageBox.askyesno('', 'Save changes to file before copying LaTeX?'):
        save_file()

    tl = Toplevel()
    tl.title('LaTeX options')

    f5 = LabelFrame(tl, text='Enumeration', padx=10, pady=10)
    f5.grid(row=0, column=0, padx=10, pady=10)

    v1 = IntVar()

    rb1 = Radiobutton(f5, text='Lonely Proof', variable=v1, value=0, padx=5, pady=5)
    rb1.grid(row=0, column=0)

    rb2 = Radiobutton(f5, text='Nested Proof', variable=v1, value=1, padx=5, pady=5)
    rb2.grid(row=1, column=0)

    v2 = StringVar()
    counter = '\\setcounter{enumi}{' + str(int(p2.get()) - 1) + '}'

    f6 = LabelFrame(tl, text='Set counter', padx=10, pady=10)
    f6.grid(row=0, column=1, padx=10, pady=10)

    cb = Checkbutton(f6, text='Enable', variable=v2, onvalue=counter, offvalue='', padx=5, pady=5)
    cb.grid(row=0, column=0)
    cb.select()

    b4 = Button(tl, text='Continue', command=tl.destroy)
    b4.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    tl.bind('<FocusOut>', alarm_call)
    tl.focus_force()
    tl.protocol('WM_DELETE_WINDOW', alarm)
    tl.resizable(False, False)
    tl.transient(tk)
    tl.grab_set()
    tl.geometry('+' + str(tk.winfo_x()) + '+' + str(tk.winfo_y()))

    tk.wait_window(tl)

    lonely = v1.get() == 0

    try:
        full = ''
        if lonely:
            full += '\\begin{enumerate}'
        full += v2.get() + '\\item\\renewcommand{\\arraystretch}{1.5}\\begin{tabular}{rp{5cm}|p{5cm}l}'
        if not e1.get() == '':
            full += '\\multicolumn{4}{p{10cm}}{' + parse(e1.get()) + '}\\\\'
        if not e2.get() == '':
            full += '\\multicolumn{4}{p{10cm}}{' + parse(e2.get()) + '}\\\\'
        full += '\\multicolumn{2}{l}{Statements}&\\multicolumn{2}{l}{Reasons}\\\\\\hline'
        for x in range(0, len(statements), 1):
            full += str(x+1) + '.&'
            full += parse(statements[x].get()) + '&'
            if reasons[x].get() == '':
                full += 'Given'
            full += parse(reasons[x].get()) + '&'
            if not refs[x].get() == '0':
                full += refs[x].get()
            full += '\\\\'
        full += '\\end{tabular}'
        if lonely:
            full += '\\end{enumerate}'
        tk.clipboard_clear()
        tk.clipboard_append(full)
    except ValueError:
        tkMessageBox.showerror('', 'Make sure all number boxes only have numbers.')


def new_call(event):
    event.widget.focus()
    new_file()


def new_file():
    global log

    if tkMessageBox.askyesno('', 'Are you sure you want to create a new file?\nAll unsaved changes will be lost.'):
        open_data('[["","",""]]')
        log = []
        update()


def closed():
    if tkMessageBox.askyesno('', 'Are you sure you want to exit this file?\nAll unsaved changes will be lost.'):
        tk.destroy()


def up_call(event):
    event.widget.focus()
    up()


def up():
    global selected

    selected -= 1
    if selected == -1:
        selected = len(statements) - 1
    update()


def down_call(event):
    event.widget.focus()
    down()


def down():
    global selected

    selected += 1
    if selected == len(statements):
        selected = 0
    update()


def update():
    global selected

    if selected >= len(statements):
        selected = len(statements) - 1
    for x in range(len(statements)):
        if x == selected:
            targets[x].config(text='<')
        else:
            targets[x].config(text='')


def undo_call(event):
    event.widget.focus()
    undo()


def undo():
    global history
    if history > 0:
        history -= 1
        open_data(log[history])
        update()


def redo_call(event):
    event.widget.focus()
    redo()


def redo():
    global history
    if history < len(log) - 1:
        history += 1
        open_data(log[history])
        update()


def add_log(par):
    global log
    global history

    log = log[0:history]
    log.append(par)
    history += 1

f1 = Frame(tk, padx=10, pady=10)
f1.grid(row=0, column=0)

l3 = Label(f1, font=('TkDefaultFont', 16), text='LaTeX Proof Editor')
l3.grid(row=0, column=0)

f2 = LabelFrame(tk, relief=FLAT, padx=10, pady=10)
f2.grid(row=1, column=0, columnspan=100)

p2 = Spinbox(f2, from_=1, to=100, width=5, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
p2.grid(row=0, column=0, padx=1)

e1 = Entry(f2, width=100, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
e1.grid(row=0, column=1, padx=1, pady=1)

e2 = Entry(f2, width=100, borderwidth=0, highlightbackground='#cccccc', highlightthickness=1)
e2.grid(row=1, column=1, padx=1, pady=1)

f3 = LabelFrame(tk, relief=FLAT, padx=10, pady=10)
f3.grid(row=3, column=0, columnspan=100)

m1 = Menu(tk)

system = 'Ctrl+'

if sys.platform == 'darwin' or sys.platform[:2] == 'os':
    tk.bind_all('<Command-n>', new_call)
    tk.bind_all('<Command-o>', open_call)
    tk.bind_all('<Command-s>', save_call)
    tk.bind_all('<Command-p>', print_call)
    tk.bind_all('<Command-z>', undo_call)
    tk.bind_all('<Command-y>', redo_call)
    tk.bind_all('<Command-Up>', up_call)
    tk.bind_all('<Command-Down>', down_call)
    tk.bind_all('<Command-minus>', remove_call)
    tk.bind_all('<Command-equal>', insert_at_call)
    tk.bind_all('<Command-Return>', insert_call)
    system = 'Cmd-'
else:
    tk.bind_all('<Control-n>', new_call)
    tk.bind_all('<Control-o>', open_call)
    tk.bind_all('<Control-s>', save_call)
    tk.bind_all('<Control-p>', print_call)
    tk.bind_all('<Control-z>', undo_call)
    tk.bind_all('<Control-y>', redo_call)
    tk.bind_all('<Control-Up>', up_call)
    tk.bind_all('<Control-Down>', down_call)
    tk.bind_all('<Control-minus>', remove_call)
    tk.bind_all('<Control-equal>', insert_at_call)
    tk.bind_all('<Control-Return>', insert_call)

m2 = Menu(m1, tearoff=0)
m2.add_command(label='New', command=new_file, accelerator=system + 'N')
m2.add_command(label='Open', command=open_file, accelerator=system + 'O')
m2.add_command(label='Save as', command=save_file, accelerator=system + 'S')
m2.add_separator()
m2.add_command(label='LaTeX', command=print_file, accelerator=system + 'P')

m3 = Menu(m1, tearoff=0)
m3.add_command(label='Undo', command=undo, accelerator=system + 'Z')
m3.add_command(label='Redo', command=redo, accelerator=system + 'Y')
m3.add_separator()
m3.add_command(label='Target up', command=up, accelerator=system + 'Up')
m3.add_command(label='Target down', command=down, accelerator=system + 'Down')
m3.add_separator()
m3.add_command(label='Remove at', command=up, accelerator=system + '-')
m3.add_command(label='Insert at', command=down, accelerator=system + '=')
m3.add_command(label='Insert end', command=insert, accelerator=system + 'Enter')

m1.add_cascade(label='File', menu=m2)
m1.add_cascade(label='Edit', menu=m3)

tk.config(menu=m1)

tk.protocol('WM_DELETE_WINDOW', closed)
tk.resizable(False, True)
tk.attributes("-topmost", True)


def parse(par):
    l = list(par)
    parsing = False
    command = ''
    line = ''
    stage = 0
    inset = ''
    for j in range(0, len(l), 1):
        if l[j] == '`':
            if stage == 1:
                array = actual
                if parsing:
                    array = latex
                if command in codes:
                    line += array[codes.index(command)]
                command = ''
                inset = ''
            elif stage == 2:
                if command in codes:
                    line += latex[codes.index(command)] + '{' + inset + '}'
                command = ''
                inset = ''
            stage = 1
        elif stage == 0:
            line += l[j]
        if stage == 1:
            if l[j] in stops:
                array = actual
                if parsing:
                    array = latex
                if command in codes:
                    line += array[codes.index(command)]
                    if not l[j] == '@':
                        line += l[j]
                stage = 0
                command = ''
                inset = ''
            elif l[j] == ' ':
                stage = 2
                if parsing and command not in bracketed:
                    if command in codes:
                        line += latex[codes.index(command)] + ' '
                    stage = 0
                    command = ''
                    inset = ''
                elif not parsing:
                    if command in codes:
                        line += actual[codes.index(command)] + ' '
                    stage = 0
                    command = ''
                    inset = ''
            else:
                command += l[j]
        elif stage == 2:
            if l[j] in stops or l[j] == ' ':
                if command in codes:
                    line += latex[codes.index(command)] + '{' + inset + '}' + l[j]
                stage = 0
                command = ''
                inset = ''
            else:
                inset += l[j]
        if l[j] == '$':
            parsing = not parsing
    if command in codes:
        array = actual
        if parsing:
            array = latex
        line += array[codes.index(command)]
    if command in bracketed:
        line += '{' + inset + '}'
    return line

insert()
update()

mainloop()
