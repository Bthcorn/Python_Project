import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import calendar
import time
import abc
import pickle

class NoInput(Exception):
    def __init__(self):
        messagebox.showerror("Input Error", "Please enter month and year")

class NoTask(Exception):
    def __init__(self):
        messagebox.showerror("Task Error", "Please enter task")

class NoFile(Exception):
    def __init__(self):
        messagebox.showerror("File Error", "Please select file")

class NoTaskSelected(Exception):
    def __init__(self):
        messagebox.showerror("Select Error", "Please select task")
        
class NoTaskToDelete(Exception):
    def __init__(self):
        messagebox.showerror("Delete Error", "Please select task to delete")

class ErrorYear(Exception):
    def __init__(self):
        messagebox.showerror("Year Error", "Please enter year between 1900-3000")

class Data(abc.ABC):
    def __init__(self, month, year, data, task_history=[]):
        self.month = month
        self.year = year
        self.date = calendar.Calendar()
        self.task_history = task_history
        self.data = data

        self.head_font = ('Leelawadee UI', 20)
        self.body_font = ('Leelawadee UI Semilight', 12)

        if data == {}:
            for day in self.date.itermonthdays(self.year, self.month):
                if day != 0:
                    self.data[day] = []
        else:
            self.data = data


class Task_manager(Data):
    def __init__(self, month, year, data, task_history=[], day=0):
        Data.__init__(self, month, year, data, task_history)
        self.window = tk.Tk()
        self.window.title("Task Manager")
        self.window.configure(bg="#FFFFFF")

        self.view = tk.Frame(self.window, bg="#FFFFFF")
        self.view.configure(bg="#FFFFFF")
        self.view.pack(expand=True, fill="both", side='left', padx=10, pady=10)

        self.data = data
        self.day = day
        self.count = 0

        label = tk.Label(self.view, text=f"Day: {self.day}",
                         font=self.head_font, bg="#FFFFFF")
        label.pack(expand=True, fill="both")

        tree_scroll = ttk.Scrollbar(self.view)
        tree_scroll.pack(side="right", fill="y")
        self.my_tree = ttk.Treeview(
            self.view, yscrollcommand=tree_scroll.set, selectmode="browse", height=10, padding=10)
        self.my_tree['columns'] = ("Task", "Status", "Tag", "Time added")
        tree_scroll.config(command=self.my_tree.yview)

        self.my_tree.column("#0", width=0, stretch=False)
        self.my_tree.column("Task", anchor="w", width=120, stretch=True)
        self.my_tree.column("Status", anchor="center",
                            width=120, stretch=True)
        self.my_tree.column("Tag", anchor="center", width=120, stretch=True)
        self.my_tree.column("Time added", anchor="center",
                            width=120, stretch=True)

        self.my_tree.heading("#0", text="")
        self.my_tree.heading("Task", text="Task", anchor="w")
        self.my_tree.heading("Status", text="Status", anchor="center")
        self.my_tree.heading("Tag", text="Tag", anchor="center")
        self.my_tree.heading("Time added", text="Time added", anchor="center")
        self.my_tree.pack(expand=True, fill="both", side='top', pady=20)

        for task in self.data[self.day]:
            self.count = len(self.my_tree.get_children())
            if task[1] == "Not started":
                self.my_tree.insert(
                    parent='', index='end', iid=self.count, values=task, tags=('not started',))
            elif task[1] == "In progress":
                self.my_tree.insert(
                    parent='', index='end', iid=self.count, values=task, tags=('in progress',))
            elif task[1] == "Done":
                self.my_tree.insert(parent='', index='end',
                                    iid=self.count, values=task, tags=('done',))

        self.my_tree.tag_configure('not started', background='#FFE2DD')
        self.my_tree.tag_configure('in progress', background='#FDECC8')
        self.my_tree.tag_configure('done', background='#DBEDDB')

        self.add_frame = tk.Frame(self.view, bg="#FFFFFF")
        self.add_frame.pack(expand=True, fill="both", side='bottom',
                            anchor='center', padx=10, pady=10)

        task_label = tk.Label(self.add_frame, text="Task", font=self.body_font)
        task_label.grid(row=0, column=0, columnspan=2, sticky='NSEW')
        status_label = tk.Label(
            self.add_frame, text="Status", font=self.body_font)
        status_label.grid(row=0, column=3, columnspan=2, sticky='NSEW')
        tag_label = tk.Label(self.add_frame, text="Tag", font=self.body_font)
        tag_label.grid(row=0, column=6, columnspan=2, sticky='NSEW')

        self.task_box = ttk.Entry(
            self.add_frame, font=self.body_font, width=20)
        self.task_box.grid(row=1, column=0, columnspan=2, sticky='NSEW')
        status = tk.StringVar()
        list_status = ["Not started", "In progress", "Done"]
        status.set("Not started")
        self.status_box = ttk.Combobox(self.add_frame, textvariable=status,
                                       values=list_status, font=self.body_font, width=20, state="readonly")
        self.status_box.grid(row=1, column=3, columnspan=2, sticky='NSEW')
        self.tag_box = ttk.Entry(self.add_frame, font=self.body_font, width=20)
        self.tag_box.grid(row=1, column=6, columnspan=2, sticky='NSEW')

        tk.Button(self.add_frame, text="Add", font=self.body_font, bg='#4CAF50',
                  fg='#FFFFFF', activebackground='#3E8E41', relief='groove', command=self.add_task,).grid(
            row=2, column=1, columnspan=3, padx=10, pady=5, sticky='NSEW')
        # select task
        tk.Button(self.add_frame, text="Select", font=self.body_font, bg='#4CAF50',
                  fg='#FFFFFF', activebackground='#3E8E41', relief='groove', command=self.select_task).grid(
            row=2, column=4, columnspan=3, padx=10, pady=5, sticky='NSEW')
        tk.Button(self.add_frame, text="Delete", font=self.body_font, bg="#FA8072", activebackground="#DD4124",
                  relief='groove', command=self.delete_task).grid(row=3, column=1, columnspan=3, padx=10, pady=5, sticky='NSEW')
        tk.Button(self.add_frame, text="Delete All", font=self.body_font, bg="#FA8072", activebackground="#DD4124",
                  relief='groove', command=self.delete_all).grid(row=3, column=4, columnspan=3, padx=10, pady=5, sticky='NSEW')
        tk.Button(self.add_frame, text="Share", font=self.body_font, command=self.share_text).grid(
            row=4, column=1, columnspan=6, padx=10, pady=5, sticky='NSEW')

        self.window.mainloop()

    def add_task(self):
        task = self.task_box.get()
        status = self.status_box.get()
        tag = self.tag_box.get()
        # add error handling
        try:
            if task == "":
                raise NoTask
            else:
                self.count = len(self.my_tree.get_children())
                item_id = f"{status.lower()}_{self.count}"
                self.my_tree.insert(parent='', index='end', iid=item_id,
                                    values=(task, status, tag, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), tags=(status.lower(),))
                self.data[self.day].append(
                    (task, status, tag, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                self.task_history.insert(0, [task, status, tag, self.day, 'add', time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime())])
        except NoTask:
            pass
        self.task_box.delete(0, "end")
        self.tag_box.delete(0, "end")
        self.status_box.set("Not started")

    def select_task(self):
        try:
            selected = self.my_tree.focus()
            # add error handling
            if selected == "":
                raise NoTaskSelected
            else:
                values = self.my_tree.item(selected, "values")
                self.task_box.delete(0, "end")
                self.task_box.insert(0, values[0])
                self.status_box.set(values[1])
                self.tag_box.delete(0, "end")
                self.tag_box.insert(0, values[2])
                self.my_tree.delete(selected)
                self.data[self.day].remove(values)
                self.task_history.insert(0, [values[0], values[1], values[2], self.day, 'select', time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime())])
        except NoTaskSelected:
            pass

    def delete_task(self):
        try:
            selected = self.my_tree.focus()
            # add error handling
            if selected == "":
                raise NoTaskToDelete
            else:
                values = self.my_tree.item(selected, "values")
                self.my_tree.delete(selected)
                self.data[self.day].remove(values)
                self.task_history.insert(0, [values[0], values[1], values[2], self.day, 'delete', time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime())])
        except NoTaskToDelete:
            pass

    def delete_all(self):
        try:
            if self.my_tree.get_children() == []:
                raise NoTaskToDelete
            for child in self.my_tree.get_children():
                self.my_tree.delete(child)
            self.data[self.day] = []
            self.task_history.append(['', '', '', self.day, 'delete_all', time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime())])
        except NoTaskToDelete:
            pass

    def share_text(self):
        self.share_window = tk.Tk()
        self.share_window.title("Share")
        self.share_window.configure(bg="#FFFFFF")

        self.text = tk.Text(self.share_window, height=10,
                            width=70, font=self.body_font)
        self.text.pack(expand=True, fill="both", side='left', padx=10, pady=10)

        scrollbarr = tk.Scrollbar(self.share_window, command=self.text.yview)
        scrollbarr.pack(side="right", fill="y")
        self.text['yscrollcommand'] = scrollbarr.set

        self.text.insert(
            'end', f"Tasks of {self.day}/{self.month}/{self.year}\n\n")
        for task in self.data[self.day]:
            self.text.insert(
                'end', f" ☐ {task[0]} - {task[1]} - {task[2]} - {task[3]}\n")
        self.text.update()

        tk.Button(self.share_window, text="Save to Text", font=self.body_font, command=self.write_to_file).pack(
            expand=True, fill="both", side='bottom', padx=10, pady=10)
        tk.Button(self.share_window, text="Copy", font=self.body_font, command=self.copy).pack(
            expand=True, fill="both", side='bottom', padx=10, pady=10)

        self.share_window.mainloop()

    def write_to_file(self):
        try:
            file = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes=(
                ("Text file", "*.txt"), ("All files", "*.*")))
            if file is None:
                raise NoFile
            else:
                with open(file.name, 'w') as file:
                    file.write(self.text.get(1.0, 'end-1c'))
                    file.close()
                    messagebox.showinfo("Success", "File saved")
        except NoFile:
            pass

    def copy(self):
        self.share_window.clipboard_clear()
        self.share_window.clipboard_append(self.text.get(1.0, 'end-1c'))
        self.share_window.update()
        messagebox.showinfo("Success", "Copied to clipboard")


class Statistics(Data):
    def __init__(self, month, year, data, task_history=[]):
        super().__init__(month, year, data, task_history)
        self.window = tk.Tk()
        self.window.title("Statistics")
        self.window.configure(bg="#FFFFFF")
        self.window.geometry("900x500")
        self.stat_frame = tk.LabelFrame(
            self.window, text="Summary", font=self.body_font, width=300, height=150, bg="#FFFFFF",)
        self.stat_frame.pack(expand=True, fill="both",
                             side='left', padx=10, pady=10)
        self.canvas = tk.Canvas(
            self.window, width=700, height=300)
        self.canvas.pack(expand=True, fill="both",
                         side='top', padx=10, pady=10)
        self.history_frame = tk.LabelFrame(
            self.window, text="History", font=self.body_font, width=100, height=50, bg="#FFFFFF",)
        self.history_frame.pack(expand=True, fill="both",
                                side='bottom', padx=10, pady=10)

        completed = self.count_task("Done")
        in_progress = self.count_task("In progress")
        not_started = self.count_task("Not started")

        completed_label = tk.Label(
            self.stat_frame, text=f"Completed: {completed}", font=self.body_font, bg="#DBEDDB")
        completed_label.pack(expand=True, fill="both",
                             side='top', padx=10, pady=5)
        in_progress_label = tk.Label(
            self.stat_frame, text=f"In progress: {in_progress}", font=self.body_font, bg="#FDECC8")
        in_progress_label.pack(expand=True, fill="both",
                               side='top', padx=10, pady=5)
        not_started_label = tk.Label(
            self.stat_frame, text=f"Not started: {not_started}", font=self.body_font, bg="#FFE2DD")
        not_started_label.pack(expand=True, fill="both",
                               side='top', padx=10, pady=5)
        total = tk.Label(
            self.stat_frame, text=f"Total: {completed + in_progress + not_started}", font=self.body_font, bg="#E3E2E0")
        total.pack(expand=True, fill="both", side='top', padx=10, pady=5)

        # history
        self.history_list = tk.Listbox(
            self.history_frame, font=self.body_font, width=10, height=50)
        self.history_list.pack(expand=True, fill="both",
                               side='left', padx=10, pady=10)
        scrollbar = tk.Scrollbar(
            self.history_frame, command=self.history_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_list['yscrollcommand'] = scrollbar.set

        for task in self.task_history:
            self.insert_task(task)

        data_points = []
        for i in self.data.keys():
            x = 50 + int(i) * 20
            y = 250 - self.productivity(i, 'Done') / 100 * 200
            data_points.append((x, y))

        # plot points
        self.draw_graph(data_points)

        self.window.mainloop()

    def productivity(self, x, status):
        if self.data[x] == []:
            return 0
        else:
            count = 0
            for task in self.data[x]:
                if len(task) > 1 and task[1] == status:
                    count += 1
            return count / len(self.data[x]) * 100

    def draw_graph(self, points):

        self.canvas.create_line(50, 250, 700, 250, width=2)  # X-axis
        self.canvas.create_line(50, 250, 50, 50, width=2)  # Y-axis

        self.canvas.create_text(
            350, 20, text="Productivity Graph", font=self.body_font)
        self.canvas.create_text(
            20, 150, text="Completed (%)", font=self.body_font, angle=90)

        # x-axis and y-axis scale
        for i in self.data.keys():
            self.canvas.create_text(
                50 + int(i) * 20, 270, text=i, font=self.body_font)

        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, width=2, fill="blue")
            self.canvas.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill="red")
            self.canvas.create_text(
                x1, y1 - 10, text=f"{self.productivity((x1 - 50) / 20, 'Done'):.2f}%", font=self.body_font, fill="#9b9b9b")
            self.canvas.create_oval(x2 - 2, y2 - 2, x2 + 2, y2 + 2, fill="red")
            self.canvas.create_text(
                x2, y2 - 10, text=f"{self.productivity((x2 - 50) / 20, 'Done'):.2f}%", font=self.body_font, fill="#9b9b9b")

    def count_task(self, status):
        count = 0
        for tasks in self.data.values():
            for task in tasks:
                if task[1] == status:
                    count += 1
        return count

    def insert_task(self, task):
        self.history_list.insert(
            'end', f"{task[4]} - {task[0]} - {task[1]} - {task[2]} - Day: {task[3]} - {task[5]}")
        self.history_list.update()


class Category(Data):
    def __init__(self, month, year, data, task_history=[]):
        super().__init__(month, year, data, task_history)
        self.window = tk.Tk()
        self.window.title("Category")
        self.window.configure(bg="#FFFFFF")

        tags = []
        for tasks in self.data.values():
            for task in tasks:
                if task[2] not in tags:
                    tags.append(task[2])

        status = tk.StringVar()
        tag = tk.StringVar()

        tk.Label(self.window, text="Status", font=self.body_font, bg="#FFFFFF").pack(
            expand=True, fill="both", padx=10, pady=5)
        self.status_box = ttk.Combobox(self.window, textvariable=status, values=[
                                       "All", "Not started", "In progress", "Done"], font=self.body_font, state="readonly")
        self.status_box.pack(expand=True, fill="both", padx=10, pady=5)
        tk.Label(self.window, text="Tag", font=self.body_font, bg="#FFFFFF").pack(
            expand=True, fill="both", padx=10, pady=5)
        self.tag_box = ttk.Combobox(
            self.window, textvariable=tag, values=tags + ['All'], font=self.body_font, state="readonly")
        self.tag_box.pack(expand=True, fill="both", padx=10, pady=5)
        tk.Button(self.window, text="Show", font=self.body_font, command=self.show).pack(
            expand=True, fill="both", padx=10, pady=5)

        self.category = tk.Listbox(
            self.window, font=self.body_font, width=70, height=10)
        self.category.pack(expand=True, fill="both",
                           side='left', padx=10, pady=10)
        scrollbar = tk.Scrollbar(self.window, command=self.category.yview)
        scrollbar.pack(side="right", fill="y")
        self.category['yscrollcommand'] = scrollbar.set

        self.window.mainloop()

    def show(self):
        self.category.delete(0, 'end')

        try:
            status = self.status_box.get()
            tag = self.tag_box.get()
            if status == "" and tag == "":
                raise NoInput
            
            if status == "All" and tag == "All":
                for (day, tasks) in self.data.items():
                    for task in tasks:
                        self.category.insert(
                            'end', f"Day: {day} - {task[0]} - {task[1]} - {task[2]} - {task[3]}")
            elif status == "All" and tag != "":
                for (day, tasks) in self.data.items():
                    for task in tasks:
                        if task[2] == tag:
                            self.category.insert(
                            'end', f"Day: {day} - {task[0]} - {task[1]} - {task[2]} - {task[3]}")
            elif status != "All" and tag == "All":
                for (day, tasks) in self.data.items():
                    for task in tasks:
                        if task[1] == status:
                            self.category.insert(
                            'end', f"Day: {day} - {task[0]} - {task[1]} - {task[2]} - {task[3]}")
            elif status != "All" and tag == "":
                for (day, tasks) in self.data.items():
                    for task in tasks:
                        if task[1] == status:
                            self.category.insert(
                            'end', f"Day: {day} - {task[0]} - {task[1]} - {task[2]} - {task[3]}")
            else:
                for (day, tasks) in self.data.items():
                    for task in tasks:
                        if task[1] == status and task[2] == tag:
                            self.category.insert(
                            'end', f"Day: {day} - {task[0]} - {task[1]} - {task[2]} - {task[3]}")
            self.category.update()
        except NoInput:
            pass
    
    def share_text(self):
        pass

class Generate_Calendar(Data):
    def __init__(self, month, year, data, task_history):
        super().__init__(month, year, data, task_history)
        self.window = tk.Tk()
        self.window.configure(bg="#FFFFFF")
        self.topic = tk.Frame(self.window, bg="#FFFFFF")
        self.topic.grid(row=0, columnspan=7)
        self.table = tk.Frame(self.window, bg="#FFFFFF")
        self.table.grid(row=1)

        self.button1 = tk.Frame(self.window, bg="#FFFFFF")
        self.button1.grid(row=2)
        self.button2 = tk.Frame(self.window, bg="#FFFFFF")
        self.button2.grid(row=3)

        self.label = tk.Label(self.topic, text=f"Month: {self.month} Year: {self.year}",
                              font=self.head_font, bg="#FFFFFF")
        self.label.pack(expand=True, fill="both")
        self.bts = []

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i in range(7):
            day_label = tk.Label(
                self.table, text=days[i], font=self.body_font, bg="#FFFFFF", width=10, height=1)
            day_label.grid(row=1, column=i)

        for (i, day) in enumerate(self.date.itermonthdays(self.year, self.month)):
            if day != 0:
                bt = tk.Button(self.table, text=day, height=4, width=10, font=self.body_font, anchor='center',
                               padx=2, pady=1, command=lambda day=day: self.show_task(day), bg='#FFFFFF', relief='groove')
                bt.grid(row=i//7 + 2, column=i % 7, sticky='NSEW')
                self.bts.append(bt)

    @abc.abstractmethod
    def show_task(self, day):
        pass


class Calendar(Task_manager, Generate_Calendar):
    def __init__(self, month, year, data, task_history):
        Generate_Calendar.__init__(self, month, year, data, task_history)
        self.window.title("Calendar")
        self.window.configure(bg="#FFFFFF")

        tk.Button(self.button1, text="Category", height=1, width=10, bg='#2383E2', fg='#FFFFFF', relief='groove',
                  activebackground='#1b65af', font=self.body_font, command=self.category).grid(row=1, column=0, padx=10, pady=5, sticky='NSEW')
        tk.Button(self.button1, text="Statistics", height=1, width=10, bg='#2383E2', fg='#FFFFFF', relief='groove',
                  activebackground='#1b65af', font=self.body_font, command=self.statistics).grid(row=1, column=1, padx=10, pady=5, sticky='NSEW')
        tk.Button(self.button1, text="Share", height=1, width=10, bg='#4CAF50', activebackground="#357c38", relief='groove', fg='#FFFFFF',
                  font=self.body_font, command=self.share_text).grid(row=1, column=2, padx=10, pady=5, sticky='NSEW')
        tk.Button(self.button1, text="Save", height=1, width=10, bg='#4CAF50', fg='#FFFFFF', activebackground='#357c38', relief='groove', command=self.save,
                  font=self.body_font,).grid(row=1, column=3, padx=10, pady=5, sticky='NSEW')
        tk.Button(self.button1, text="Check", height=1, width=10, relief='groove', activebackground='#c1814b', bg='#F4A460', command=self.check,
                  font=self.body_font).grid(row=1, column=4, padx=10, pady=5, sticky='NSEW')
        # next month button
        tk.Button(self.button2, text="Next", height=1, width=10, bg='#2383E2', fg='#FFFFFF', relief='groove',
                    activebackground='#1b65af', font=self.body_font, command=self.next_month).grid(row=1, column=1, padx=10, pady=5, sticky='NSEW')
        # previous month button
        tk.Button(self.button2, text="Previous", height=1, width=10, bg='#2383E2', fg='#FFFFFF', relief='groove',
                    activebackground='#1b65af', font=self.body_font, command=self.previous_month).grid(row=1, column=2, padx=10, pady=5, sticky='NSEW')
        # reset button 
        tk.Button(self.button2, text="Reset", height=1, width=10, bg='#FA8072', activebackground='#DD4124', relief='groove',
                    font=self.body_font, command=self.reset).grid(row=1, column=3, padx=10, pady=5, sticky='NSEW')
        # exir button
        tk.Button(self.button2, text="Exit", height=1, width=10, bg='#FA8072', activebackground='#DD4124', relief='groove',
                    font=self.body_font, command=self.window.destroy).grid(row=1, column=4, padx=10, pady=5, sticky='NSEW')
        
        self.window.mainloop()
    
    def update_calendar(self):
        for bt in self.bts:
            bt.destroy()
        self.bts = []
        for (i, day) in enumerate(self.date.itermonthdays(self.year, self.month)):
            if day != 0:
                bt = tk.Button(self.table, text=day, height=4, width=10, font=self.body_font, anchor='center',
                               padx=2, pady=1, command=lambda day=day: self.show_task(day), bg='#FFFFFF', relief='groove')
                bt.grid(row=i//7 + 2, column=i%7, sticky='NSEW')
                self.bts.append(bt)
    
    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.update_calendar()
        self.label['text'] = f"Month: {self.month} Year: {self.year}"

    def previous_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.update_calendar()
        self.label['text'] = f"Month: {self.month} Year: {self.year}"
        
    def reset(self):
        for day in self.data.keys():
            self.data[day] = []
        self.update_calendar()
        messagebox.showinfo("Success", "Reset completed")

    def show_task(self, day):
        self.task = Task_manager(self.month, self.year, self.data, self.task_history, day)

    def statistics(self):
        self.stat = Statistics(self.month, self.year, self.data, self.task_history)

    def category(self):
        self.cat = Category(self.month, self.year, self.data, self.task_history)

    def share_text(self):
        self.share_window = tk.Tk()
        self.share_window.title("Share")
        self.share_window.configure(bg="#FFFFFF")

        self.text = tk.Text(self.share_window, height=10,
                            width=70, font=self.body_font)
        self.text.pack(expand=True, fill="both",side='left', padx=10, pady=10)

        scrollbarr = tk.Scrollbar(self.share_window, command=self.text.yview)
        scrollbarr.pack(side="right", fill="y")
        self.text['yscrollcommand'] = scrollbarr.set

        self.text.insert(
            'end', f"Tasks of {self.month}/{self.year}\n\n")
        for day in self.data.keys():
            self.text.insert('end', f"Day: {day}\n")
            for task in self.data[day]:
                self.text.insert(
                    'end', f" ☐ {task[0]} - {task[1]} - {task[2]} - {task[3]}\n")
        self.text.update()

        tk.Button(self.share_window, text="Save to Text", font=self.body_font, command=self.write_to_file).pack(
            expand=True, fill="both", side='bottom', padx=10, pady=10)
        tk.Button(self.share_window, text="Copy", font=self.body_font, command=self.copy).pack(
            expand=True, fill="both", side='bottom', padx=10, pady=10)

        self.share_window.mainloop()

    def save(self):
        try:
            file = filedialog.asksaveasfile(mode='wb', defaultextension=".pkl", filetypes=(
                ("Pickle file", "*.pkl"), ("All files", "*.*")))
            if file is None:
                raise NoFile
            else:
                with open(file.name, 'wb') as file:
                    pickle.dump([self.month, self.year, self.data,
                                self.task_history], file)
                    file.close()
                    messagebox.showinfo("Success", "File saved")
        except NoFile:
            pass

    def check(self):
        for i, bt in enumerate(self.bts):
            done_percent = self.productivity(i+1, 'Done')
            not_done_percent = self.productivity(
                i+1, 'Not started') + self.productivity(i+1, 'In progress')
            color = '#FFFFFF'
            level = 'Not started'
            if done_percent == 0 and not_done_percent == 0:
                color = '#FFFFFF'
                level = 'Not started'
            elif not_done_percent > 0 and done_percent == 0:
                color = '#FA8072'
                level = 'Unfinished'
            elif 0 < done_percent <= 25:
                color = '#FF0000'
                level = 'Low'
            elif 25 < done_percent <= 50:
                color = '#FFA500'
                level = 'Moderate'
            elif 50 < done_percent <= 75:
                color = '#FFFF00'
                level = 'High'
            elif 75 < done_percent <= 100:
                color = '#00FF00'
                level = 'Excellent'
            bt.config(bg=color, text=f"{i+1}\n{level}\n{done_percent:.2f}%")

    def productivity(self, x, status):
        if self.data[x] == []:
            return 0
        else:
            count = 0
            for task in self.data[x]:
                if task[1] == status:
                    count += 1
            return count / len(self.data[x]) * 100


class Select_Month(Calendar):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Select Month")
        self.window.configure(bg="#FFFFFF")
        self.window.geometry("350x250")

        self.data = {}
        self.task_history = []

        self.head_font = ('Leelawadee UI', 20)
        self.body_font = ('Leelawadee UI', 12)

        tk.Label(self.window, text="Choose Month ad Year", anchor='center', font=self.head_font, bg="#D99E82").pack(
            expand=True, fill="both", padx=10, pady=5)
        tk.Label(self.window, text="Month", font=self.body_font, bg="#FFFFFF").pack(
            expand=True, fill="both", padx=10, pady=5)
        self.m = ttk.Entry(self.window, font=self.body_font, width=20)
        self.m.pack(expand=True, fill="both", padx=10, pady=5)
        tk.Label(self.window, text="Year", font=self.body_font, bg="#FFFFFF").pack(
            expand=True, fill="both", padx=10, pady=5)
        self.y = ttk.Entry(self.window, font=self.body_font, width=20)
        self.y.pack(expand=True, fill="both", padx=10, pady=5)

        tk.Button(self.window, text="Submit", font=self.body_font, bg='#4CAF50', fg='#FFFFFF', activebackground='#3E8E41',
                  relief='groove', command=self.submit).pack(expand=True, fill="both", padx=10, pady=5)

        self.window.mainloop()

    def submit(self):
        try:
            month = self.m.get()
            year = self.y.get()
            # add error handling
            if month == "" or year == "":
                raise NoInput
            elif int(year) < 1900 or int(year) > 3000:
                raise ErrorYear
            elif not month.isnumeric() or not year.isnumeric():
                raise ValueError
            else:
                self.window.destroy()
                self.cal = Calendar.__init__(self, int(month), int(
                    year), self.data, self.task_history)
        except NoInput:
            pass
        except calendar.IllegalMonthError:
            messagebox.showerror("Month Error", "Please enter month between 1-12")
        except ValueError:
            messagebox.showerror("Value Error", "Please enter month and year in number")
            

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Todo App")
        self.window.configure(bg="#F7F7F5")
        self.window.geometry("400x150")

        self.head_font = ('Leelawadee UI', 20)
        self.body_font = ('Leelawadee UI', 12)

        tk.Label(self.window, text="Todo App", font=self.head_font,
                 bg="#F0E68C").pack(expand=True, fill="both", padx=10, pady=5)
        new_button = tk.Button(self.window, text="New File", font=self.body_font, bg='#4CAF50', fg='#FFFFFF',
                               activebackground='#3E8E41', relief='groove', command=self.new)
        new_button.pack(expand=True, fill="both", padx=10, pady=5)
        open_button = tk.Button(self.window, text="Open File", font=self.body_font, bg='#FA8072', fg='#FFFFFF',
                                activebackground='#DD4124', relief='groove', command=self.open)
        open_button.pack(expand=True, fill="both", padx=10, pady=5)

        self.window.mainloop()

    def new(self):
        # self.window.destroy()
        self.cal = Select_Month()

    def open(self):
        try:
            file = filedialog.askopenfile(mode='rb', defaultextension=".pkl", filetypes=(
                ("Pickle file", "*.pkl"), ("All files", "*.*")))
            if file is None:
                raise NoFile
            else:
                with open(file.name, 'rb') as file:
                    data = pickle.load(file)
                    file.close()
                    self.window.destroy()
                    self.cal = Calendar(data[0], data[1], data[2], data[3])
        except NoFile:
            pass


if __name__ == "__main__":
    app = App()
