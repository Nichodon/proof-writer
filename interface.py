from Tkinter import *

tk = Tk()
tk.wm_title("ProofR v0")

statements = []
reasons = []
line_nums = []

codes = ["`a", "`t", "`s", "`r", "`l"]
latex = ["angle", "triangle", "overline", "overrightarrow", "overleftrightarrow"]
bracketed = ["`s", "`r", "`l"]


def insert():
    m = Label(tk, text=str(len(statements)+1)+".")
    m.grid(row=len(statements)+4, column=0)

    en1 = Entry(tk, width=50)
    en1.grid(row=len(statements)+4, column=1)

    en2 = Entry(tk, width=50)
    en2.grid(row=len(statements)+4, column=2)

    line_nums.append(m)
    statements.append(en1)
    reasons.append(en2)


def remove():
    try:
        line_nums[-1].grid_forget()
        statements[-1].grid_forget()
        reasons[-1].grid_forget()

        line_nums.pop()
        statements.pop()
        reasons.pop()
    except IndexError:
        pass

e1 = Entry(tk, width=100)
e1.grid(row=1, column=1, columnspan=2)

e2 = Entry(tk, width=100)
e2.grid(row=2, column=1, columnspan=2)

p = Spinbox(tk, from_=1, to=1000, width=3)
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
            stage += 1
            parsing = not parsing
            try:
                line += "\\" + latex[codes.index(command)]
            except ValueError:
                pass
            if stage == 3:
                stage = 0
                if command in bracketed:
                    line += "{" + inset + "}"
                else:
                    line += inset
                command = ""
                inset = ""
        if l[j] == ' ' and parsing:
            stage += 1
            print command
        if stage == 1:
            command = command + l[j]
        if stage == 2:
            inset += l[j]
        if stage == 0 and not l[j] == "`":
            line = line + l[j]
    return line


def really_important():
    full = "\\begin{enumerate}\\setcounter{enumi}{"
    full += str(p.get()) + "}\\item " + parse(e1.get()) + "\\\\" + parse(e2.get())
    full += "\\\\\\\\\\renewcommand{\\arraystretch}{1.5}%\n\\begin{tabular}{l|l}\\multicolumn{1}{l}{Statements}&Reasons\\\\\\hline\n"
    for i in range(0, len(statements), 1):
        full += str(i+1) + ". "
        full += parse(statements[i].get()) + "&"
        full += reasons[i].get() + "\\\\"
    full += "\\end{tabular}\\end{enumerate}"
    print full


b1 = Button(tk, text="Insert line", command=insert, width=20, height=2, background="#FFFFBF")
b1.grid(row=3, column=1)

b2 = Button(tk, text="Remove line", command=remove, width=20, height=2, background="#FFBFBF")
b2.grid(row=3, column=2)

d = Button(tk, text="Export LaTeX", command=really_important, width=20, height=2, background="#BFFFBF")
d.grid(row=0, column=0, columnspan=3)

print parse("")

mainloop()
