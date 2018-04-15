import pandas as pd
import pandas.io.sql
import pymssql
import os
import tkinter as tk
import time

master = tk.Tk()

tk.Label(master, text="Query").grid(row=2, column=1)
tk.Label(master, text="File Name").grid(row=4, column=1)

e = tk.Text(master, height=8, width=50)
e.grid(row=3, column=1)
e2 = tk.Entry(master)
e2.grid(row=5, column=1)
e.focus_set()
estr = str(master.focus_get().__class__)

conn = pymssql.connect(
    host=r"host",
    user=r"user",
    password="password",
    database="database"
)

pd.options.display.max_rows = 10000

#commands
def status():
    global top
    top = tk.Toplevel(master)
    top.title('Running')
    msg = tk.Message(top, text="Running Query...                                ", width=750)
    msg.grid(row=0, column=1)
    master.after(5000, top.destroy)

def run():
    try:
        sql = e.get('1.0', tk.END)
        filename = e2.get()
        file = "C:/Users/Desktop/REPORTS/" + filename + ".csv"
        if filename == '':
            global top
            top = tk.Toplevel(master)
            top.title('Error')
            msg = tk.Message(top, text="Please Provide File Name         ", width=750)
            msg.grid(row=0, column=1)
        else:
            df = pandas.io.sql.read_sql(sql, conn)
            df.to_csv("C:/Users/Desktop/REPORTS/" + filename + ".csv", index=False)
            os.startfile(file)
            top = tk.Toplevel(master)
            top.title('Finished')
            msg = tk.Message(top, text="Query Executed Successfully         ", width=750)
            msg.grid(row=0, column=1)
    except Exception as ex:
        top = tk.Toplevel(master)
        top.title('Error')
        msg = tk.Message(top, text=ex, width=750)
        msg.grid(row=0, column=1)

def comb(event=None):
    status()
    master.after(3000, run)
        
def close(event=None):
    top.destroy()

def closeAll(event=None):
    master.quit()

def reset(event=None):
   e.delete('1.0', tk.END)
   e2.delete(0, 'end')
   e.focus_set()

def selectNext(event):
    event.widget.tk_focusNext().focus()
    return("break")

menubar = tk.Menu(master)
menubar.add_command(label="Run", command=runFromMenu)
menubar.add_command(label="Reset", command=resetFromMenu)
menubar.add_command(label="Quit", command=master.quit)
master.bind('<Escape>', close)
master.bind('<F5>', comb)
master.bind('<Control-q>', closeAll)
master.bind('<F2>', reset)
master.bind('<Alt-space>', selectNext)
master.config(menu=menubar)
master.title("Query Database")
master.minsize(width=250, height=200)
master.mainloop()
