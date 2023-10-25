import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk. Frame):
    def __init__ (self, root):
        super().__init__ (root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg= '#d7d8e0', bd=2)
        toolbar.pack (side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='./add.png')
        self.bth_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd = 0, image = self.add_img, command=self.open_dialog)
        self.bth_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'money'), height=45, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)    
        self.tree.column('money', width=110, anchor=tk.CENTER)    


        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО') 
        self.tree.heading('tel', text='Телефон') 
        self.tree.heading('email', text='E-mail')
        self.tree.heading('money', text='Заработная плата')


        self.tree.pack(side=tk.LEFT) 

        self.update_img = tk.PhotoImage(file='./update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd = 0, image = self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)
    
        self.delete_img = tk.PhotoImage(file='./delete.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd = 0, image = self.delete_img, command=self.delete_record)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='./search.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd = 0, image = self.search_img, command=self.open_search_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)
 
        self.refresh_img = tk.PhotoImage(file='./refresh.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd = 0, image = self.refresh_img, command=self.view_records)
        btn_edit_dialog.pack(side=tk.LEFT)



    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def records(self, name, tel, email, money):
        self.db.insert_data(name, tel, email, money)
        self.view_records()

    def view_records(self):
        self.db.cur.execute('SELECT * FROM db')

        [self.tree.delete(i) for i in self.tree.get_children()]

        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def update_record(self, name, tel, email, money):
        self.db.cur.execute('''UPDATE db SET name = ?, tel = ?, email = ?, money = ? WHERE id =?''', (name, tel, email, money, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def delete_record(self):
        for select_item in self.tree.selection():
            self.db.cur.execute('DELETE FROM db WHERE id=?', self.tree.set(select_item, '#1'))

        self.db.conn.commit()
        self.view_records()

    def open_search_dialog(self):
        Search()

    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute('SELECT ** FROM db WHERE name LIKE ?', name)

        [self.tree.delete(i) for i in self.tree.get_children()]
        
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]






class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добваить')
        self.geometry('400x300')
        self.resizable(False, False)       
        self.grab_set()
        self.focus_set()

        lable_name = tk.Label(self, text='ФИО')
        lable_name.place(x=50, y=40)
        lable_select = tk.Label(self, text='Телефон:')
        lable_select.place(x=50, y=80)
        lable_sum = tk.Label(self, text='E-mail:')
        lable_sum.place(x=50, y=120)
        lable_money = tk.Label(self, text='Плата:')
        lable_money.place(x=50, y=160)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=40)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=120)
        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=160)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=270)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=270)
        
        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_email.get(),
                                           self.entry_tel.get(),
                                           self.entry_money.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать')
        self.btn_edit = ttk.Button(self, text='Редактировать')
        self.btn_edit.place(x=205, y=270)
        self.btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_email.get(),
                                              self.entry_tel.get(),
                                              self.entry_money.get()))
        
        self.btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.cur.execute('SELECT * FROM db WHERE id=?', (self.view.tree.set(self.view.tree.selection() [0], '#1'),))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_money.insert(0, row[4])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Имя')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cansel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cansel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind = ('<Button-1>', lambda event:
                           self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button - 1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db,db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS db (
            id INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT,
            money TEXT
        );
        ''')
        self.conn.commit()

    def insert_data(self, name, tel, email, money):
        self.cur.execute('INSERT INTO db (name, tel, email, money) VALUES (?, ?, ?, ?);', (name, tel, email, money))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()

    root.title('Ведомость рабочих')
    root.geometry('800x450')
    root.resizable(False, False)
    root.mainloop()