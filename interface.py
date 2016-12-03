from Tkinter import *
import tkFileDialog
import tkMessageBox

tk = Tk()
tk.wm_title("ProofR v0.3")

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

    filer = tkFileDialog.asksaveasfile(mode='w', defaultextension=".proof")
    if filer is None:
        return
    filer.write(out)
    filer.close()


def open_file():
    filer = tkFileDialog.askopenfile(mode='r', defaultextension=".proof")
    if filer is None:
        return
    try:
        global statements
        global reasons
        global line_nums
        global refs

        lines = eval(filer.read())

        if tkMessageBox.askyesno("Are you sure?", "All unsaved changes will be lost"):
            statements = []
            reasons = []
            line_nums = []
            refs = []

            for i in range(0, len(lines), 1):
                line_data = lines[i]

                m = Label(tk, text=str(len(statements)+1)+".", width=5)
                m.grid(row=len(statements)+6, column=0)

                en1 = Entry(tk, width=50)
                en1.grid(row=len(statements)+6, column=1, columnspan=3)
                en1.insert(END, line_data[0])

                en2 = Entry(tk, width=50)
                en2.grid(row=len(statements)+6, column=4, columnspan=3)
                en2.insert(END, line_data[1])

                sb = Entry(tk, width=10)
                sb.grid(row=len(statements)+6, column=7)
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
    m = Label(tk, text=str(len(statements)+1)+".", width=5)
    m.grid(row=len(statements)+6, column=0)

    en1 = Entry(tk, width=50)
    en1.grid(row=len(statements)+6, column=1, columnspan=3)

    en2 = Entry(tk, width=50)
    en2.grid(row=len(statements)+6, column=4, columnspan=3)

    sb = Entry(tk, width=10)
    sb.grid(row=len(statements)+6, column=7)

    line_nums.append(m)
    statements.append(en1)
    reasons.append(en2)
    refs.append(sb)


def insert_at():
    m = Label(tk, text=str(len(statements)+1)+".", width=5)
    m.grid(row=len(statements)+6, column=0)

    en1 = Entry(tk, width=50)
    en1.grid(row=int(q.get())+5, column=1, columnspan=3)

    en2 = Entry(tk, width=50)
    en2.grid(row=int(q.get())+5, column=4, columnspan=3)

    sb = Entry(tk, width=10)
    sb.grid(row=int(q.get())+5, column=7)

    line_nums.append(m)
    statements.insert(int(q.get()) - 1, en1)
    reasons.insert(int(q.get()) - 1, en2)
    refs.insert(int(q.get()) - 1, sb)

    for i in range(0, len(statements), 1):
        statements[i].grid(row=i+6, column=1, columnspan=3)
        reasons[i].grid(row=i+6, column=4, columnspan=3)
        refs[i].grid(row=i+6, column=7)


def remove():
    if len(line_nums) > 1:
        line_nums[-1].grid_forget()
        statements[int(q.get()) - 1].grid_forget()
        reasons[int(q.get()) - 1].grid_forget()
        refs[int(q.get()) - 1].grid_forget()

        line_nums.pop()
        statements.pop(int(q.get()) - 1)
        reasons.pop(int(q.get()) - 1)
        refs.pop(int(q.get()) - 1)

    for i in range(0, len(statements), 1):
        statements[i].grid(row=i+6, column=1, columnspan=3)
        reasons[i].grid(row=i+6, column=4, columnspan=3)
        refs[i].grid(row=i+6, column=7)


def really_important():
    try:
        full = "\\begin{enumerate}\\setcounter{enumi}{"
        full += str(int(p.get()) - 1) + "}\\item " + parse(e1.get()) + "\\\\" + parse(e2.get())
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

d = Button(tk, text="Copy LaTeX", command=really_important, width=10, height=1, background="#BFFFBF")
d.grid(row=0, column=1)

h = Button(tk, text="Save as", command=guide, width=10, height=1, background="#BFFFFF")
h.grid(row=0, column=2)

j = Button(tk, text="Open", command=open_file, width=10, height=1, background="#BFFFFF")
j.grid(row=0, column=3)

b1 = Button(tk, text="Insert end", command=insert, width=10, height=1, background="#FFFFBF")
b1.grid(row=0, column=4)

b3 = Button(tk, text="Insert at", command=insert_at, width=10, height=1, background="#FFFFBF")
b3.grid(row=0, column=5)

b2 = Button(tk, text="Remove at", command=remove, width=10, height=1, background="#FFBFBF")
b2.grid(row=0, column=6)

q = Spinbox(tk, from_=1, to=1000, width=5)
q.grid(row=0, column=7)

p = Spinbox(tk, from_=1, to=1000, width=5)
p.grid(row=2, column=0)

e1 = Entry(tk, width=115)
e1.grid(row=2, column=1, columnspan=7)

e2 = Entry(tk, width=115)
e2.grid(row=3, column=1, columnspan=7)


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
    try:
        line += actual[codes.index(command)]
    except ValueError:
        pass
    return line

insert()

mainloop()


