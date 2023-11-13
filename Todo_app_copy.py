import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import calendar
import datetime
import time
import abc
import pickle


class Data(abc.ABC):
    def __init__(self, month, year, data, task_history=[]):
        self.month = month
        self.year = year
        self.date = calendar.Calendar()
        self.task_history = task_history
        self.data = data

        self.head_font = ('Leelawadee UI', 20)
        self.body_font = ('Leelawadee UI', 12)

        if data == {}:
            for day in self.date.itermonthdays(self.year, self.month):
                if day != 0:
                    self.data[day] = []
        else:
            self.data = data


class Task_manager(Data):
    def __init__(self, month, year, data, day, task_history=[]):
        Data.__init__(self, month, year, data, task_history)
        self.window = tk.Tk()
        self.window.title("Task Manager")
        self.window.configure(bg="#FFFFFF")

        self.view = tk.Frame(self.window, bg="#FFFFFF")
        self.view.configure(bg="#FFFFFF")
        self.view.pack(expand=True, fill="both", padx=10, pady=10)

        self.day = day
        self.count = 0

        label = tk.Label(self.view, text="Task Manager",
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
        self.my_tree.pack(expand=True, fill="both", pady=20)

        self.my_tree.tag_configure("not_started", background="#FFE2DD")
        self.my_tree.tag_configure("in_progress", background="#FDECC8")
        self.my_tree.tag_configure("done", background="#DBEDDB")

        for task in self.data[self.day]:
            self.count = len(self.my_tree.get_children())
            if task[1] == "Not started":
                self.my_tree.insert(
                    parent='', index='end', idd=self.count, values=task, tags=("not_started"))
            elif task[1] == "In progress":
                self.my_tree.insert(
                    parent='', index='end', idd=self.count, values=task, tags=("in_progress"))
            elif task[1] == "Done":
                self.my_tree.insert(parent='', index='end',
                                    idd=self.count, values=task, tags=("done"))

        self.add_frame = tk.Frame(self.view, bg="#FFFFFF")
        self.add_frame.pack(expand=True, fill="both",
                            anchor='center', padx=10, pady=10)

        task_label = tk.Label(self.add_frame, text="Task", font=self.body_font)
        task_label.grid(row=0, column=0, columnspan=2, sticky='NSEW')
        status_label = tk.Label(
            self.add_frame, text="Status", font=self.body_font)
        status_label.grid(row=0, column=3, columnspan=2, sticky='NSEW')
        tag_label = tk.Label(self.add_frame, text="Tag", font=self.body_font)
        tag_label.grid(row=0, column=6, columnspan=2, sticky='NSEW')

        self.task_box = tk.Entry(self.add_frame, font=self.body_font, width=20)
        self.task_box.grid(row=1, column=0, columnspan=2, sticky='NSEW')
        status = tk.StringVar()
        list_status = ["Not started", "In progress", "Done"]
        status.set("Not started")
        self.status_box = ttk.Combobox(self.add_frame, textvariable=status,
                                       values=list_status, font=self.body_font, width=20, state="readonly")
        self.status_box.grid(row=1, column=3, columnspan=2, sticky='NSEW')
        self.tag_box = tk.Entry(self.add_frame, font=self.body_font, width=20)
        self.tag_box.grid(row=1, column=6, columnspan=2, sticky='NSEW')

        tk.Button(self.add_frame, text="Add", font=self.body_font, command=self.add_task).grid(
            row=2, column=1, columnspan=3, padx=10, pady=5, sticky='NSEW')
        # select task
        tk.Button(self.add_frame, text="Select", font=self.body_font, command=self.select_task).grid(
            row=2, column=4, columnspan=3, padx=10, pady=5, sticky='NSEW')
        tk.Button(self.add_frame, text="Delete", font=self.body_font, command=self.delete_task).grid(
            row=3, column=1, columnspan=3, padx=10, pady=5, sticky='NSEW')
        tk.Button(self.add_frame, text="Delete All", font=self.body_font, command=self.delete_all).grid(
            row=3, column=4, columnspan=3, padx=10, pady=5, sticky='NSEW')
        tk.Button(self.add_frame, text="Share", font=self.body_font, command=self.share).grid(
            row=4, column=1, columnspan=6, padx=10, pady=5, sticky='NSEW')

        self.window.mainloop()

    def add_task(self):
        task = self.task_box.get()
        status = self.status_box.get()
        tag = self.tag_box.get()
        if task == "":
            messagebox.showerror("Error", "Please enter task")
        else:
            self.count = len(self.my_tree.get_children())
            item_id = f"{status.lower()}_{self.count}"
            self.my_tree.insert(parent='', index='end', idd=item_id,
                                values=(task, status, tag, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), tags=(status.lower()))
            self.data[self.day].append(
                (task, status, tag, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            self.task_history.append([task, status, tag, self.day, 'add', time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime())])
            self.task_box.delete(0, "end")
            self.tag_box.delete(0, "end")
            self.status_box.set("Not started")

    def select_task(self):
        selected = self.my_tree.focus()
        if selected == "":
            messagebox.showerror("Error", "Please select task")
        else:
            values = self.my_tree.item(selected, "values")
            self.task_box.delete(0, "end")
            self.task_box.insert(0, values[0])
            self.status_box.set(values[1])
            self.tag_box.delete(0, "end")
            self.tag_box.insert(0, values[2])
            self.my_tree.delete(selected)
            self.data[self.day].remove(values)
            self.task_history.append([values[0], values[1], values[2], self.day, 'select', time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime())])

    def delete_task(self):
        selected = self.my_tree.focus()
        if selected == "":
            messagebox.showerror("Error", "Please select task")
        else:
            values = self.my_tree.item(selected, "values")
            self.my_tree.delete(selected)
            self.data[self.day].remove(values)
            self.task_history.append([values[0], values[1], values[2], self.day, 'delete', time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime())])

    def delete_all(self):
        for child in self.my_tree.get_children():
            self.my_tree.delete(child)
        self.data[self.day] = []
        self.task_history.append(['', '', '', self.day, 'delete_all', time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime())])

    def share(self):
        self.share_window = tk.Tk()
        self.share_window.title("Share")
        self.share_window.configure(bg="#FFFFFF")

        self.text = tk.Text(self.share_window, height=10,
                            width=70, font=self.body_font)
        self.text.pack(expand=True, fill="left", padx=10, pady=10)

        scrollbarr = tk.Scrollbar(self.share_window, command=self.text.yview)
        scrollbarr.pack(side="right", fill="y")
        self.text['yscrollcommand'] = scrollbarr.set

        self.text.insert(
            'end', f"Task history of {self.day}/{self.month}/{self.year}\n\n")
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
        file = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes=(
            ("Text file", "*.txt"), ("All files", "*.*")))
        if file is None:
            return
        else:
            with open(file.name, 'w') as file:
                file.write(self.text.get(1.0, 'end-1c'))
                file.close()
                messagebox.showinfo("Success", "File saved")

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

        self.stat_frame = tk.LabelFrame(
            self.window, text="Summary", font=self.body_font, bg="#FFFFFF", width=300, height=300)
        self.stat_frame.pack(expand=True, fill="both",
                             side='left', padx=10, pady=10)
        self.history_frame = tk.LabelFrame(
            self.window, text="History", font=self.body_font, bg="#FFFFFF", width=100, height=200)
        self.history_frame.pack(expand=True, fill="both",
                                side='bottom', padx=10, pady=10)

        self.completed = 0
        self.in_progress = 0
        self.not_started = 0
        for tasks in self.data.values():
            for task in tasks:
                if task[1] == "Done":
                    self.completed += 1
                elif task[1] == "In progress":
                    self.in_progress += 1
                elif task[1] == "Not started":
                    self.not_started += 1

        completed_label = tk.Label(
            self.stat_frame, text=f"Completed: {self.completed}", font=self.body_font, bg="#FFFFFF")
        completed_label.grid(row=0, column=0, padx=10, pady=10, sticky='NSEW')
        in_progress_label = tk.Label(
            self.stat_frame, text=f"In progress: {self.in_progress}", font=self.body_font, bg="#FFFFFF")
        in_progress_label.grid(row=1, column=0, padx=10,
                               pady=10, sticky='NSEW')
        not_started_label = tk.Label(
            self.stat_frame, text=f"Not started: {self.not_started}", font=self.body_font, bg="#FFFFFF")
        not_started_label.grid(row=2, column=0, padx=10,
                               pady=10, sticky='NSEW')
        total = tk.Label(
            self.stat_frame, text=f"Total: {self.completed + self.in_progress + self.not_started}", font=self.body_font, bg="#FFFFFF")
        total.grid(row=3, column=0, padx=10, pady=10, sticky='NSEW')

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
            self.history_list.insert(
                'end', f"{task[4]} - {task[0]} - {task[1]} - {task[2]} - Day: {task[3]} - {task[5]}")
        self.history_list.update()

        self.canvas = tk.Canvas(
            self.window, bg="#FFFFFF", width=700, height=500)
        self.canvas.pack(expand=True, fill="both",
                         side='right', padx=10, pady=10)
        self.canvas.create_line(50, 250, 700, 250, width=2)  # X-axis
        self.canvas.create_line(50, 250, 50, 50, width=2)  # Y-axis

        self.canvas.create_text(
            350, 20, text="Productivity Graph", font=self.body_font)
        self.canvas.create_text(
            20, 150, text="Completed (%)", font=self.body_font, angle=90)

        # x-axis and y-axis scale
        data_points = []
        for x in self.data.keys():
            self.canvas.create_text(
                50 + (x * 20), 270, text=x, font=self.body_font)
            x = 50 + (int(x) * 20)
            y = 250 - self.productivity(x, 'Done') / 100 * 200
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
                if task[1] == status:
                    count += 1
            return count / len(self.data[x]) * 100

    def draw_graph(self, points):
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, width=2, fill="blue")
            self.canvas.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill="red")
            self.canvas.create_text(
                x1, y1 - 10, text=f"{self.productivity(x1, 'Done'):.2f}%", font=self.body_font)
            self.canvas.create_oval(x2 - 2, y2 - 2, x2 + 2, y2 + 2, fill="red")
            self.canvas.create_text(
                x2, y2 - 10, text=f"{self.productivity(x2, 'Done'):.2f}%", font=self.body_font)


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
            self.window, textvariable=tag, values=tags, font=self.body_font, state="readonly")
        self.tag_box.pack(expand=True, fill="both", padx=10, pady=5)
        tk.Button(self.window, text="Show", font=self.body_font, command=self.show).pack(
            expand=True, fill="both", padx=10, pady=5)

        self.category = tk.Listbox(
            self.window, font=self.body_font, width=70, height=10)
        self.category.pack(expand=True, fill="both", padx=10, pady=10)
        scrollbar = tk.Scrollbar(self.window, command=self.category.yview)
        scrollbar.pack(side="right", fill="y")
        self.category['yscrollcommand'] = scrollbar.set

        self.window.mainloop()

    def show(self):
        self.category.delete(0, 'end')

        status = self.status_box.get()
        tag = self.tag_box.get()
        if status == "" and tag == "":
            messagebox.showerror("Error", "Please select status or tag")

        if status == "All" and tag == "":
            for tasks in self.data.values():
                for task in tasks:
                    self.category.insert(
                        'end', f"Day: {task[3]} - {task[0]} - {task[1]} - {task[2]}")
        elif status == "All" and tag != "":
            for tasks in self.data.values():
                for task in tasks:
                    if task[2] == tag:
                        self.category.insert(
                            'end', f"Day: {task[3]} - {task[0]} - {task[1]} - {task[2]}")
        elif status != "All" and tag == "":
            for tasks in self.data.values():
                for task in tasks:
                    if task[1] == status:
                        self.category.insert(
                            'end', f"Day: {task[3]} - {task[0]} - {task[1]} - {task[2]}")
        else:
            for tasks in self.data.values():
                for task in tasks:
                    if task[1] == status and task[2] == tag:
                        self.category.insert(
                            'end', f"Day: {task[3]} - {task[0]} - {task[1]} - {task[2]}")
        self.category.update()


class Generate_Calendar(Data):
    def __init__(self, month, year, data, task_history=[]):
        super().__init__(month, year, data, task_history)
        self.window = tk.Tk()
        self.window.configure(bg="#FFFFFF")
        self.topic = tk.Frame(self.window, bg="#FFFFFF")
        self.topic.grid(row=0, columnspan=7)
        self.table = tk.Frame(self.window, bg="#FFFFFF")
        self.table.grid(row=1)

        self.button1 = tk.Frame(self.window, bg="#FFFFFF")
        self.button1.grid(row=2)

        self.label = tk.Label(self.topic, text=f"Month: {self.month} Year: {self.year}",
                 font=self.head_font, bg="#FFFFFF")
        self.label.pack(expand=True, fill="both")
        self.bts = []

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i in range(7):
            day = tk.Label(self.table, text=days[i], font=self.body_font, bg="#FFFFFF", width=10)
            day.grid(row=1, column=i)

        # get local month and year
        now = datetime.datetime.now()
        self.month = now.month
        self.year = now.year

        for (i, day) in enumerate(self.date.itermonthdays(self.year, self.month)):
            if day != 0:
                bt = tk.Button(self.table, text=day, height=4, width=10, font=self.body_font, anchor='center',
                               padx=2, pady=1, command=lambda day=day: self.show_task(day), bg='#FFFFFF', relief='groove')
                bt.grid(row=i//7 + 2, column=i%7, sticky='NSEW')
                self.bts.append(bt)


    @abc.abstractmethod
    def show_task(self, day):
        pass

    def update(self):
        # clear all button
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
        self.update()
        # update label
        self.label['text'] = f"Month: {self.month} Year: {self.year}"

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.update()
        self.label['text'] = f"Month: {self.month} Year: {self.year}"

    def next_year(self):
        self.year += 1
        self.update()
        self.label['text'] = f"Month: {self.month} Year: {self.year}"

    def prev_year(self):
        self.year -= 1
        self.update()
        self.label['text'] = f"Month: {self.month} Year: {self.year}"

    def save(self):
        file = filedialog.asksaveasfile(mode='wb', defaultextension=".pkl", filetypes=(
            ("Pickle file", "*.pkl"), ("All files", "*.*")))
        if file is None:
            return
        else:
            pickle.dump(self.data, file)
            file.close()
            messagebox.showinfo("Success", "File saved")

    def load(self):
        file = filedialog.askopenfile(mode='rb', defaultextension=".pkl", filetypes=(
            ("Pickle file", "*.pkl"), ("All files", "*.*")))
        if file is None:
            return
        else:
            self.data = pickle.load(file)
            file.close()
            messagebox.showinfo("Success", "File loaded")
            self.update()

    def reset(self):
        self.data = {}
        self.update()
        messagebox.showinfo("Success", "Reset completed")

    def exit(self):
        self.window.destroy()


class Calendar(Generate_Calendar, Task_manager, Statistics, Category):
    def __init__(self, month, year, data, task_history=[]):
        Generate_Calendar.__init__(self, month, year, data, task_history)
        self.window.title("Calendar")
        self.window.configure(bg="#FFFFFF")

        tk.Button(self.button1, text="Next Month", font=self.body_font, command=self.next_month).grid(
            row=0, column=0, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Previous Month", font=self.body_font,
                  command=self.prev_month).grid(row=0, column=1, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Next Year", font=self.body_font, command=self.next_year).grid(
            row=0, column=2, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Previous Year", font=self.body_font,
                  command=self.prev_year).grid(row=0, column=3, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Save", font=self.body_font, command=self.save).grid(
            row=0, column=4, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Load", font=self.body_font, command=self.load).grid(
            row=0, column=5, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Reset", font=self.body_font, command=self.reset).grid(
            row=0, column=6, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Exit", font=self.body_font, command=self.exit).grid(
            row=0, column=7, padx=10, pady=10, sticky='NSEW')

        self.window.mainloop()

    def show_task(self, day):
        self.task = Task_manager.__init__(
            self, self.month, self.year, self.data, self.task_history, day)
        self.data = self.task.data
        self.task_history = self.task.task_history
        self.update()


class Calendar_Statistics(Generate_Calendar):
    def __init__(self, month, year, data, task_history=[]):
        super().__init__(month, year, data, task_history)
        self.window.title("Calendar Statistics")
        self.window.configure(bg="#FFFFFF")

        tk.Button(self.button1, text="Next Month", font=self.body_font, command=self.next_month).grid(
            row=0, column=0, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Previous Month", font=self.body_font,
                  command=self.prev_month).grid(row=0, column=1, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Next Year", font=self.body_font, command=self.next_year).grid(
            row=0, column=2, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Previous Year", font=self.body_font,
                  command=self.prev_year).grid(row=0, column=3, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Save", font=self.body_font, command=self.save).grid(
            row=0, column=4, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Load", font=self.body_font, command=self.load).grid(
            row=0, column=5, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Reset", font=self.body_font, command=self.reset).grid(
            row=0, column=6, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Exit", font=self.body_font, command=self.exit).grid(
            row=0, column=7, padx=10, pady=10, sticky='NSEW')

    def show_task(self, day):
        self.task = Statistics(self.month, self.year,
                               self.data, self.task_history, day)
        self.data = self.task.data
        self.task_history = self.task.task_history
        self.update()


class Calendar_Category(Generate_Calendar):
    def __init__(self, month, year, data, task_history=[]):
        super().__init__(month, year, data, task_history)
        self.window.title("Calendar Category")
        self.window.configure(bg="#FFFFFF")

        tk.Button(self.button1, text="Next Month", font=self.body_font, command=self.next_month).grid(
            row=0, column=0, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Previous Month", font=self.body_font,
                  command=self.prev_month).grid(row=0, column=1, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Next Year", font=self.body_font, command=self.next_year).grid(
            row=0, column=2, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Previous Year", font=self.body_font,
                  command=self.prev_year).grid(row=0, column=3, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Save", font=self.body_font, command=self.save).grid(
            row=0, column=4, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Load", font=self.body_font, command=self.load).grid(
            row=0, column=5, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Reset", font=self.body_font, command=self.reset).grid(
            row=0, column=6, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Exit", font=self.body_font, command=self.exit).grid(
            row=0, column=7, padx=10, pady=10, sticky='NSEW')

    def show_task(self, day):
        self.task = Category(self.month, self.year,
                             self.data, self.task_history, day)
        self.data = self.task.data
        self.task_history = self.task.task_history
        self.update()


class Calendar_Statistics_Category(Generate_Calendar):
    def __init__(self, month, year, data, task_history=[]):
        super().__init__(month, year, data, task_history)
        self.window.title("Calendar Statistics Category")
        self.window.configure(bg="#FFFFFF")

        tk.Button(self.button1, text="Next Month", font=self.body_font, command=self.next_month).grid(
            row=0, column=0, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Previous Month", font=self.body_font,
                  command=self.prev_month).grid(row=0, column=1, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Next Year", font=self.body_font, command=self.next_year).grid(
            row=0, column=2, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Previous Year", font=self.body_font,
                  command=self.prev_year).grid(row=0, column=3, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Save", font=self.body_font, command=self.save).grid(
            row=0, column=4, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Load", font=self.body_font, command=self.load).grid(
            row=0, column=5, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Reset", font=self.body_font, command=self.reset).grid(
            row=0, column=6, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Exit", font=self.body_font, command=self.exit).grid(
            row=0, column=7, padx=10, pady=10, sticky='NSEW')

    def show_task(self, day):
        self.task = Statistics(self.month, self.year,
                               self.data, self.task_history, day)
        self.data = self.task.data
        self.task_history = self.task.task_history
        self.update()
        self.task = Category(self.month, self.year,
                             self.data, self.task_history, day)
        self.data = self.task.data
        self.task_history = self.task.task_history
        self.update()


class Calendar_Task_manager(Generate_Calendar):
    def __init__(self, month, year, data, task_history=[]):
        super().__init__(month, year, data, task_history)
        self.window.title("Calendar Task Manager")
        self.window.configure(bg="#FFFFFF")

        tk.Button(self.button1, text="Next Month", font=self.body_font, command=self.next_month).grid(
            row=0, column=0, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Previous Month", font=self.body_font,
                  command=self.prev_month).grid(row=0, column=1, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Next Year", font=self.body_font, command=self.next_year).grid(
            row=0, column=2, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Previous Year", font=self.body_font,
                  command=self.prev_year).grid(row=0, column=3, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Save", font=self.body_font, command=self.save).grid(
            row=0, column=4, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Load", font=self.body_font, command=self.load).grid(
            row=0, column=5, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Reset", font=self.body_font, command=self.reset).grid(
            row=0, column=6, padx=10, pady=10, sticky='NSEW')
        tk.Button(self.button1, text="Exit", font=self.body_font, command=self.exit).grid(
            row=0, column=7, padx=10, pady=10, sticky='NSEW')

    def show_task(self, day):
        self.task = Task_manager(
            self.month, self.year, self.data, self.task_history, day)
        self.data = self.task.data
        self.task_history = self.task.task_history
        self.update()

Calendar(11, 2023, {})