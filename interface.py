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

stops = ['.', ',', ';', '$', '{', '@']
codes = ['`a', '`t', '`s', '`r', '`l', '`c', '`par', '`per', '`q', '`nc', '`npar', '`nper', '`n', '`th', '`f', '`d']
latex = ['\\angle', '\\triangle', '\\overline', '\\overrightarrow', '\\overleftrightarrow', '\\cong', '\\parallel',
         '\\perp', '\\square', '\\ncong', '\\nparallel', 'not\\perp', '\\ne', '\\therefore', '\\frac', '^{\circ}']
bracketed = ['`s', '`r', '`l']
actual = ['angle', 'triangle', 'segment', 'ray', 'line', 'congruent', 'parallel', 'perpendicular', 'quadrilateral',
          'not congruent', 'not parallel', 'not perpendicular', 'not equal', 'therefore', 'fraction', 'degree']
shorts = ['N', 'O', 'S', 'P', 'Enter']

codes.extend([i.title() for i in codes])
latex.extend(latex)
actual.extend([i.title() for i in actual])


def save_call(event):
    event.widget.focus()
    save_file()


def save_file():
    out = '['

    for x in range(0, len(statements) - 1, 1):
        s = statements[x]
        r = reasons[x]
        f = refs[x]
        out += '[\'' + s.get() + '\',\'' + r.get() + '\',\'' + f.get() + '\'],'

    s = statements[-1]
    r = reasons[-1]
    f = refs[-1]
    out += '[\'' + s.get() + '\',\'' + r.get() + '\',\'' + f.get() + '\']]'

    filer = tkFileDialog.asksaveasfile(mode='w', defaultextension='.proof', filetypes=[('Proof File', '*.proof')])
    if filer is None:
        return
    filer.write(out)
    filer.close()
    
    
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

        lines = eval(filer.read())

        if tkMessageBox.askyesno('', 'Are you sure you want to open a file?\nAll unsaved changes will be lost.'):
            for x in range(0, len(statements), 1):
                line_nums[x].grid_forget()
                statements[x].grid_forget()
                reasons[x].grid_forget()
                refs[x].grid_forget()

            statements = []
            reasons = []
            line_nums = []
            refs = []

            for x in range(0, len(lines), 1):
                line_data = lines[x]

                m = Label(f3, text=str(len(statements)+1)+'.', width=5)
                m.grid(row=len(statements), column=0)

                en1 = Entry(f3, width=50)
                en1.grid(row=len(statements), column=1, columnspan=3)
                en1.insert(END, line_data[0])

                en2 = Entry(f3, width=50)
                en2.grid(row=len(statements), column=4, columnspan=3)
                en2.insert(END, line_data[1])

                sb = Entry(f3, width=10)
                sb.grid(row=len(statements), column=7)
                sb.insert(END, line_data[2])

                line_nums.append(m)
                statements.append(en1)
                reasons.append(en2)
                refs.append(sb)

            tk.wm_title('LaTeX Proof Editor: ' + os.path.basename(filer.name)[:-6])
    except TypeError:
        tkMessageBox.showerror('', 'Something went wrong reading file!\nThe file might be corrupted')
    except SyntaxError:
        tkMessageBox.showerror('', 'Something went wrong reading file!\nThe file might be corrupted')


def insert_call(event):
    event.widget.focus()
    insert()


def insert():
    m = Label(f3, text=str(len(statements)+1)+'.', width=5)
    m.grid(row=len(statements), column=0)

    en1 = Entry(f3, width=50)
    en1.grid(row=len(statements), column=1, columnspan=3)

    en2 = Entry(f3, width=50)
    en2.grid(row=len(statements), column=4, columnspan=3)

    sb = Entry(f3, width=10)
    sb.grid(row=len(statements), column=7)

    line_nums.append(m)
    statements.append(en1)
    reasons.append(en2)
    refs.append(sb)


def insert_at():
    m = Label(f3, text=str(len(statements)+1)+'.', width=5)
    m.grid(row=len(statements), column=0)

    en1 = Entry(f3, width=50)
    en1.grid(row=int(p1.get())-1, column=1, columnspan=3)

    en2 = Entry(f3, width=50)
    en2.grid(row=int(p1.get())-1, column=4, columnspan=3)

    sb = Entry(f3, width=10)
    sb.grid(row=int(p1.get())-1, column=7)

    line_nums.append(m)
    statements.insert(int(p1.get()) - 1, en1)
    reasons.insert(int(p1.get()) - 1, en2)
    refs.insert(int(p1.get()) - 1, sb)

    tab = [b1, b3, b2, p1, p2, e1, e2]

    for x in range(0, len(statements), 1):
        statements[x].grid(row=x, column=1, columnspan=3)
        reasons[x].grid(row=x, column=4, columnspan=3)
        refs[x].grid(row=x, column=7)
        tab.append(statements[x])
        tab.append(reasons[x])
        tab.append(refs[x])

    for x in tab:
        x.lift()


def remove():
    if len(line_nums) > 1 and int(p1.get()) <= len(line_nums):
        line_nums[-1].grid_forget()
        statements[int(p1.get()) - 1].grid_forget()
        reasons[int(p1.get()) - 1].grid_forget()
        refs[int(p1.get()) - 1].grid_forget()

        line_nums.pop()
        statements.pop(int(p1.get()) - 1)
        reasons.pop(int(p1.get()) - 1)
        refs.pop(int(p1.get()) - 1)

    for x in range(0, len(statements), 1):
        statements[x].grid(row=x, column=1, columnspan=3)
        reasons[x].grid(row=x, column=4, columnspan=3)
        refs[x].grid(row=x, column=7)


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

    f5 = LabelFrame(tl, text='Enumeration', padx=5, pady=5)
    f5.grid(row=0, column=0)

    v1 = IntVar()

    rb1 = Radiobutton(f5, text='Lonely Proof', variable=v1, value=0, padx=5, pady=5)
    rb1.grid(row=0, column=0)

    rb2 = Radiobutton(f5, text='Nested Proof', variable=v1, value=1, padx=5, pady=5)
    rb2.grid(row=1, column=0)

    v2 = StringVar()
    counter = '\\setcounter{enumi}{' + str(int(p2.get()) - 1) + '}'

    f6 = LabelFrame(tl, text='Set counter', padx=5, pady=5)
    f6.grid(row=0, column=1)

    cb = Checkbutton(f6, text='Enable', variable=v2, onvalue=counter, offvalue='', padx=5, pady=5)
    cb.grid(row=0, column=0)
    cb.select()

    b4 = Button(tl, text='Copy LaTeX', command=tl.destroy)
    b4.grid(row=1, column=0, columnspan=2)

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
    global statements
    global reasons
    global line_nums
    global refs

    if tkMessageBox.askyesno('', 'Are you sure you want to create a new file?\nAll unsaved changes will be lost.'):
        for x in statements:
            x.grid_forget()
        for x in reasons:
            x.grid_forget()
        for x in line_nums:
            x.grid_forget()
        for x in refs:
            x.grid_forget()

        statements = []
        reasons = []
        line_nums = []
        refs = []

        e1.delete(0, END)
        e2.delete(0, END)

        insert()


def closed():
    if tkMessageBox.askyesno('', 'Are you sure you want to exit this file?\nAll unsaved changes will be lost.'):
        tk.destroy()

f1 = LabelFrame(tk, relief=FLAT, padx=10, pady=10)
f1.grid(row=0, column=0, columnspan=100)

f4 = LabelFrame(f1, padx=10, pady=10, text='Edit')
f4.grid(row=0, column=1)

b1 = Button(f4, text='Insert end', command=insert, width=10, height=1, background='#FFFFBF')
b1.grid(row=0, column=3, padx=5)

b3 = Button(f4, text='Insert at', command=insert_at, width=10, height=1, background='#FFFFBF')
b3.grid(row=0, column=4, padx=5)

b2 = Button(f4, text='Remove at', command=remove, width=10, height=1, background='#FFBFBF')
b2.grid(row=0, column=5, padx=5)

p1 = Spinbox(f4, from_=1, to=1000, width=5)
p1.grid(row=0, column=6, padx=5)

f2 = LabelFrame(tk, relief=FLAT, padx=10, pady=10)
f2.grid(row=1, column=0, columnspan=100)

p2 = Spinbox(f2, from_=1, to=1000, width=5)
p2.grid(row=0, column=0)

e1 = Entry(f2, width=100)
e1.grid(row=0, column=1, columnspan=7)

e2 = Entry(f2, width=100)
e2.grid(row=1, column=1, columnspan=7)

f3 = LabelFrame(tk, relief=FLAT, padx=10, pady=10)
f3.grid(row=2, column=0, columnspan=100)

m1 = Menu(tk)

system = 'Ctrl-'

if sys.platform == 'darwin' or sys.platform[:2] == 'os':
    tk.bind_all('<Command-n>', new_call)
    tk.bind_all('<Command-o>', open_call)
    tk.bind_all('<Command-s>', save_call)
    tk.bind_all('<Command-p>', print_call)
    tk.bind_all('<Command-Return>', insert_call)
    system = 'Cmmd-'
else:
    tk.bind_all('<Control-n>', new_call)
    tk.bind_all('<Control-o>', open_call)
    tk.bind_all('<Control-s>', save_call)
    tk.bind_all('<Control-p>', print_call)
    tk.bind_all('<Control-Return>', insert_call)

m2 = Menu(m1, tearoff=0)
m2.add_command(label='New', command=new_file, accelerator=system + shorts[0])
m2.add_command(label='Open', command=open_file, accelerator=system + shorts[1])
m2.add_command(label='Save as', command=save_file, accelerator=system + shorts[2])
m2.add_separator()
m2.add_command(label='LaTeX', command=print_file, accelerator=system + shorts[3])

m3 = Menu(m1, tearoff=0)
m3.add_command(label='Insert End', command=insert, accelerator=system + shorts[4])

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

mainloop()
