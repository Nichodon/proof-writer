from Tkinter import *
import tkFileDialog
import tkMessageBox

tk = Tk()
tk.wm_title("LaTeX Proof Editor")

statements = []
reasons = []
line_nums = []
refs = []

codes = ["`a", "`t", "`s", "`r", "`l", "`c", "`par", "`per", "`q", "`nc", "`npar", "`nper", "`n"]
latex = ["angle", "triangle", "overline", "overrightarrow", "overleftrightarrow", "cong", "|", "perp", "square", "ncong", "nparallel", "not\\perp", "ne"]
bracketed = ["`s", "`r", "`l"]
actual = ["angle", "triangle", "segment", "ray", "line", "congruent", "parallel", "perpendicular", "quadrilateral", "not congruent", "not parallel", "not perpendicular", "not equal"]


def guide():
    out = "["

    for i in range(0, len(statements) - 1, 1):
        s = statements[i]
        r = reasons[i]
        f = refs[i]
        out += "[\'" + s.get() + "\',\'" + r.get() + "\',\'" + f.get() + "\'],"

    s = statements[-1]
    r = reasons[-1]
    f = refs[-1]
    out += "[\'" + s.get() + "\',\'" + r.get() + "\',\'" + f.get() + "\']]"

    filer = tkFileDialog.asksaveasfile(mode='w', defaultextension=".proof", filetypes=[("Proof File", "*.proof")])
    if filer is None:
        return
    filer.write(out)
    filer.close()


def open_file():
    filer = tkFileDialog.askopenfile(mode='r', defaultextension=".proof", filetypes=[("Proof File", "*.proof")])
    if filer is None:
        return
    try:
        global statements
        global reasons
        global line_nums
        global refs

        lines = eval(filer.read())

        if tkMessageBox.askyesno("Are you sure?", "All unsaved changes will be lost"):

            for i in range(0, len(statements), 1):
                line_nums[i].grid_forget()
                statements[i].grid_forget()
                reasons[i].grid_forget()
                refs[i].grid_forget()

            statements = []
            reasons = []
            line_nums = []
            refs = []

            for i in range(0, len(lines), 1):
                line_data = lines[i]

                m = Label(f3, text=str(len(statements)+1)+".", width=5)
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

    except TypeError:
        tkMessageBox.showerror("Oops!", "Unable to open file; use .proof file extension")
    except SyntaxError:
        tkMessageBox.showerror("Oops!", "Unable to open file; use .proof file extension")


def insert():
    m = Label(f3, text=str(len(statements)+1)+".", width=5)
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
    m = Label(f3, text=str(len(statements)+1)+".", width=5)
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

    for i in range(0, len(statements), 1):
        statements[i].grid(row=i, column=1, columnspan=3)
        reasons[i].grid(row=i, column=4, columnspan=3)
        refs[i].grid(row=i, column=7)


def remove():
    if len(line_nums) > 1:
        line_nums[-1].grid_forget()
        statements[int(p1.get()) - 1].grid_forget()
        reasons[int(p1.get()) - 1].grid_forget()
        refs[int(p1.get()) - 1].grid_forget()

        line_nums.pop()
        statements.pop(int(p1.get()) - 1)
        reasons.pop(int(p1.get()) - 1)
        refs.pop(int(p1.get()) - 1)

    for i in range(0, len(statements), 1):
        statements[i].grid(row=i, column=1, columnspan=3)
        reasons[i].grid(row=i, column=4, columnspan=3)
        refs[i].grid(row=i, column=7)


def really_important():
    try:
        full = "\\begin{enumerate}\\setcounter{enumi}{"
        full += str(int(p2.get()) - 1) + "}\\item " + parse(e1.get()) + "\\\\" + parse(e2.get())
        full += "\\\\\\\\\\renewcommand{\\arraystretch}{1.5}%\n\\begin{tabular}{rp{5cm}|p{5cm}l}\\multicolumn{2}{l}{Statements}&\\multicolumn{2}{l}{Reasons}\\\\\\hline\n"
        for i in range(0, len(statements), 1):
            full += str(i+1) + ".&"
            full += parse(statements[i].get()) + "&"
            full += translate(reasons[i].get()) + "&"
            if not refs[i].get() == "0":
                full += refs[i].get()
            full += "\\\\"
        full += "\\end{tabular}\\end{enumerate}"
        tk.clipboard_clear()
        tk.clipboard_append(full)
    except ValueError:
        tkMessageBox.showerror("Oops!", "Make sure all spin boxes have numbers only")

f1 = LabelFrame(tk, padx=10, pady=10, text="Options")
f1.grid(row=0, column=0, columnspan=100)

d = Button(f1, text="Copy LaTeX", command=really_important, width=10, height=1, background="#BFFFBF")
d.grid(row=0, column=0, padx=5)

h = Button(f1, text="Save as", command=guide, width=10, height=1, background="#BFFFFF")
h.grid(row=0, column=1, padx=5)

j = Button(f1, text="Open", command=open_file, width=10, height=1, background="#BFFFFF")
j.grid(row=0, column=2, padx=5)

b1 = Button(f1, text="Insert end", command=insert, width=10, height=1, background="#FFFFBF")
b1.grid(row=0, column=3, padx=5)

b3 = Button(f1, text="Insert at", command=insert_at, width=10, height=1, background="#FFFFBF")
b3.grid(row=0, column=4, padx=5)

b2 = Button(f1, text="Remove at", command=remove, width=10, height=1, background="#FFBFBF")
b2.grid(row=0, column=5, padx=5)

p1 = Spinbox(f1, from_=1, to=1000, width=5)
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


def parse(par):
    l = list(par)
    parsing = False
    command = ""
    line = ""
    stage = 0
    inset = ""
    for j in range(0, len(l), 1):
        if l[j] == '`':
            parsing = True
            if stage == 2:
                try:
                    line += "\\" + latex[codes.index(command)]
                except ValueError:
                    pass
                line += "{" + inset + "}"
                command = ""
                inset = ""
            stage = 1
            try:
                line += "\\" + latex[codes.index(command)]
            except ValueError:
                pass
                ''' if stage == 3:
                stage = 0
                line += "{" + inset + "}"
                command = ""
                inset = ""'''
        if stage == 2 and l[j] == "$":
            try:
                line += "\\" + latex[codes.index(command)]
            except ValueError:
                pass
            stage = 0
            line += "{" + inset + "}"
            command = ""
            inset = ""
        if l[j] == ' ' and parsing:
            stage += 1
            if command not in bracketed:
                stage = 0
                try:
                    line += "\\" + latex[codes.index(command)]
                except ValueError:
                    pass
                command = ""
                inset = ""
                parsing = False
            elif stage == 3:
                try:
                    line += "\\" + latex[codes.index(command)]
                except ValueError:
                    pass
                stage = 0
                line += "{" + inset + "}"
                command = ""
                inset = ""
        if stage == 1:
            command += l[j]
        if stage == 2 and not l[j] == ' ':
            inset += l[j]
        if stage == 0 and not l[j] == "`":
            line += l[j]
    try:
        line += "\\" + latex[codes.index(command)]
    except ValueError:
        pass
    if command in bracketed:
        line += "{" + inset + "}"
    return line


def translate(par):
    l = list(par)
    parsing = False
    command = ""
    line = ""
    stage = 0
    for j in range(0, len(l), 1):
        if l[j] == '`':
            parsing = True
            stage = 1
        if l[j] == ' ' and parsing:
            stage = 0
            try:
                line += actual[codes.index(command)]
            except ValueError:
                pass
            command = ""
            parsing = False
        if stage == 1:
            command += l[j]
        if stage == 0 and not l[j] == "`":
            line += l[j]
    if not command == "":
        line += actual[codes.index(command)]
    return line

insert()

mainloop()


