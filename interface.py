from Tkinter import *

tk = Tk()
tk.wm_title("ProofR v0.1")

statements = []
reasons = []
line_nums = []
refs = []

codes = ["`a", "`t", "`s", "`r", "`l", "`c", "`par", "`per", "`q"]
latex = ["angle", "triangle", "overline", "overrightarrow", "overleftrightarrow", "cong", "|", "perp", "square"]
bracketed = ["`s", "`r", "`l"]
actual = ["angle", "triangle", "segment", "ray", "line", "congruent", "parallel", "perpendicular", "quadrilateral"]


def insert():
    m = Label(tk, text=str(len(statements)+1)+".", width=5)
    m.grid(row=len(statements)+4, column=0)

    en1 = Entry(tk, width=50)
    en1.grid(row=len(statements)+4, column=1)

    en2 = Entry(tk, width=50)
    en2.grid(row=len(statements)+4, column=2)

    sb = Entry(tk, width=10)
    sb.grid(row=len(statements)+4, column=3)

    line_nums.append(m)
    statements.append(en1)
    reasons.append(en2)
    refs.append(sb)


def remove():
    if len(line_nums) > 1:
        line_nums[-1].grid_forget()
        statements[-1].grid_forget()
        reasons[-1].grid_forget()
        refs[-1].grid_forget()

        line_nums.pop()
        statements.pop()
        reasons.pop()
        refs.pop()

e1 = Entry(tk, width=115)
e1.grid(row=1, column=1, columnspan=3)

e2 = Entry(tk, width=115)
e2.grid(row=2, column=1, columnspan=3)

p = Spinbox(tk, from_=1, to=1000, width=5)
p.grid(row=1, column=0)


def parse(par):
    l = list(par)
    parsing = False
    command = ""
    line = ""
    stage = 0
    inset = ""
    for j in range(0, len(l), 1):
        if l[j] == '`':
            parsing = not parsing
            stage += 1
            try:
                line += "\\" + latex[codes.index(command)]
            except ValueError:
                pass
            if stage == 3:
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
        if stage == 1:
            command += l[j]
        if stage == 2 and not l[j] == ' ':
            inset += l[j]
        if stage == 0 and not l[j] == "`":
            line += l[j]
    return line


def really_important():
    full = "\\begin{enumerate}\\setcounter{enumi}{"
    full += str(int(p.get()) - 1) + "}\\item " + parse(e1.get()) + "\\\\" + parse(e2.get())
    full += "\\\\\\\\\\renewcommand{\\arraystretch}{1.5}%\n\\begin{tabular}{rp{5cm}|p{5cm}l}\\multicolumn{2}{l}{Statements}&\\multicolumn{2}{l}{Reasons}\\\\\\hline\n"
    for i in range(0, len(statements), 1):
        full += str(i+1) + ".&"
        full += parse(statements[i].get()) + "&"
        full += parse(reasons[i].get()) + "&"
        if not refs[i].get() == "0":
            full += refs[i].get()
        full += "\\\\"
    full += "\\end{tabular}\\end{enumerate}"
    tk.clipboard_clear()
    tk.clipboard_append(full)


def guide():
    what = Tk()

    h1 = Label(what, text="ProofR Guide", font=("Helvetica", 24))
    h1.grid(row=0, column=0, columnspan=2)

    h2 = Label(what, text="List of symbols", font=("Helvetica", 16))
    h2.grid(row=1, column=0, columnspan=2)

    h3 = Label(what, text="`a: Angle\n`t: Triangle\n`c: Congruent\n`par: Parallel\n`per: Perpendicular", font=("Times", 12), justify=LEFT)
    h3.grid(row=2, column=0)

    h4 = Label(what, text="`s xx`: Segment\n`r xx`: Ray\n`l xx`: Line", font=("Times", 12), justify=LEFT)
    h4.grid(row=2, column=1)

    h5 = Label(what, text="Syntax", font=("Helvetica", 16))
    h5.grid(row=3, column=0, columnspan=2)

    h6 = Label(what, text="$`a ABC$ is right", font=("Times", 12), justify=LEFT)
    h6.grid(row=4, column=0)

    h7 = Label(what, text="$`s AB``c `s CD`$ ", font=("Times", 12), justify=LEFT)
    h7.grid(row=4, column=1)

    what.wm_title("ProofR Guide")

    mainloop()

b1 = Button(tk, text="Insert line", command=insert, width=20, height=2, background="#FFFFBF")
b1.grid(row=3, column=1)

b2 = Button(tk, text="Remove line", command=remove, width=20, height=2, background="#FFBFBF")
b2.grid(row=3, column=2)

d = Button(tk, text="Export LaTeX", command=really_important, width=20, height=2, background="#BFFFBF")
d.grid(row=0, column=1)

h = Button(tk, text="ProofR Guide", command=guide, width=20, height=2, background="#BFFFFF")
h.grid(row=0, column=2)

insert()

mainloop()
