#! /usr/bin/python3

import tkinter as tk
from tinydb import *
import time


class SessionTimer(object):
    '''Main app class for the pomodoro program'''

    def __init__(self, project=None):
        if project is None:
            print('New')


class EntryRow(tk.Frame):
    def __init__(self, master, label):
        row = tk.Frame(master)
        lab = tk.Label(row, width=15, text=label, anchor='w')
        self.ent = tk.Entry(row, width=45)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        self.ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    def get(self):
        return self.ent.get()

    def set(self, text):
        self.ent.insert(tk.END, text)


class MyText(tk.Text):
    def __init__(self, master, **kw):
        Text.__init__(self, master, kw)
        # self.bind("<Return>", lambda e: None)
        # self.bind("<Tab>", self.focus_next_window)
        # self.bind("<Control-Return>", lambda e: '\n')

    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return("break")


class GoalForm(tk.Toplevel):
    """docstring for ClassName"""

    projEnt = ''
    chalEnt = ['', '']
    stepEnt = ['', '', '']
    sessEnt = 1

    def __init__(self, master):
        print('Goal Form Opened')
        tk.Toplevel.__init__(self, master)
        self.makeform()

    def makeform(self):
        self.title('Pomodoro')
        # self.geometry('{}x{}'.format(300, 300))

        self.projEnt = EntryRow(self, 'Project')
        self.chalEnt[0] = EntryRow(self, 'Challenge:\t    a)')
        self.chalEnt[1] = EntryRow(self, '\t    b)')
        self.stepEnt[0] = EntryRow(self, 'Steps:\t    1.')
        self.stepEnt[1] = EntryRow(self, '\t    2.')
        self.stepEnt[2] = EntryRow(self, '\t    3.')
        self.sessEnt = EntryRow(self, 'Sessions')

        self.projEnt.ent.focus_set()

        # Task type radio button
        self.type = tk.StringVar()
        self.type.set('task')
        tk.Label(self, text="Session Type", justify=tk.LEFT,
                 anchor='w').pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)
        tk.Radiobutton(self, text="Task", padx=20, variable=self.type,
                       value='task').pack(anchor=tk.W, side=tk.LEFT)
        tk.Radiobutton(self, text="Learn", padx=20, variable=self.type,
                       value='learn').pack(anchor=tk.W, side=tk.LEFT)

        # Button to close window
        self.enterBtn = tk.Button(self, text='Enter')
        self.enterBtn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.quitBtn = tk.Button(self, text='Quit')
        self.quitBtn.pack(side=tk.RIGHT, padx=5, pady=5)
        self.withdraw()


class TaskForm(object):
    """docstring for ClassName"""

    def __init__(self, pom):
        self.project = pom['project']
        self.challenge = pom['challenge']
        self.steps = pom['steps']
        self.sessions = pom['sessions']
        self.completed = ''
        self.todo = ''
        self.makeform()

    def fetch(self, entries, root):
        # print(type(root))
        # print(type(entries))
        for entry in entries:
            if entry[0] == 'Completed':
                self.completed = entry[1].get()
            elif entry[0] == 'Todo':
                self.todo = entry[1].get()
            # else:
            #     print("\nFORM FETCH ERROR\n")
        root.destroy()

    def printEntries(self):
        print("\n**************************")
        print(self.project)
        print(self.challenge[0])
        print("**************************\n")

    def makeform(self):

        fields = ['Project:', 'Challenge:', '\ta)', '\tb)', 'Steps:',
                  '\t1.', '\t2.', '\t3.', 'Sessions:', 'Completed', 'Todo']
        text = [self.project, None, self.challenge[0], self.challenge[1],
                None, self.steps[0], self.steps[1], self.steps[2],
                self.sessions, self.completed, self.todo]
        root = Tk()
        entries = []
        for f, t in zip(fields, text):
            row = Frame(root)
            lab = Label(row, width=12, text=f, anchor='w')
            if t is '':
                ent = Entry(row, width=45)
                ent.insert(END, t)
            elif t:
                ent = Label(row, width=10, text=t, anchor='w')
            row.pack(side=TOP, fill=X, padx=5, pady=2)
            lab.pack(side=LEFT)
            if t is not None:
                ent.pack(side=RIGHT, expand=YES, fill=X)
                entries.append((f, ent))

        self.onTask = IntVar()  # .set(0)
        self.onTask.set(1)
        Label(root, text="Remained on task for this session",
              justify=LEFT, anchor='w').pack(side=LEFT, fill=X, padx=5, pady=5)
        Radiobutton(root, text="Yes", padx=20, variable=self.onTask,
                    value=1).pack(anchor=W, side=LEFT)
        Radiobutton(root, text="No", padx=20, variable=self.onTask,
                    value=2).pack(anchor=W, side=LEFT)

        ents = entries
        ents[7][1].focus_set()
        root.bind('<Return>', (lambda event, e=ents: self.fetch(e, root)))
        # Button to close window
        b3 = tk.Button(root, text='Quit', command=root.quit)
        b3.pack(side=LEFT, padx=5, pady=5)
        # Button to enter info. Same as return key
        b1 = tk.Button(root, text='Enter', command=(
            lambda e=ents: self.fetch(e, root)))
        b1.pack(side=RIGHT, padx=5, pady=5)
        # # Button to remove jobs
        # rmvjob = tk.Button(
        #     root, text='Remove', command=lambda r=root: self.removeJob(root))
        # rmvjob.pack(side=LEFT, padx=5, pady=5)
        root.mainloop()


class LearnForm(object):
    """docstring for ClassName"""

    def __init__(self, pom):
        self.project = pom['project']
        self.challenge = pom['challenge']
        self.steps = pom['steps']
        self.sessions = pom['sessions']
        self.summary = ''
        self.makeform()

    def fetch(self, entries, root):
        # print(type(root))
        # print(type(entries))
        for entry in entries:
            if entry[0] == 'Summary':
                print(entry[1].get("1.0", 'end-2c'))
                self.summary = entry[1].get("1.0", 'end-2c')
            # else:
            #     print("\nFORM FETCH ERROR\n")
        root.destroy()

    def printEntries(self):
        print("\n**************************")
        print(self.project)
        print(self.start)
        print(self.end)
        print(self.summary)
        print("**************************\n")

    # def removeJob(self, root):
    #     self.company = "REMOVED"
    #     self.jobTitle = "REMOVED"
    #     self.location = "REMOVED"
    #     self.address = ["REMOVED", "REMOVED"]
    #     self.link = "REMOVED"
    #     self.path = "REMOVED"
    #     print("Job Removed")
    #     root.destroy()

    def makeform(self):

        fields = ['Project:', 'Challenge:', '\ta)', '\tb)', 'Steps:',
                  '\t1.', '\t2.', '\t3.', 'Sessions:']
        text = [self.project, None, self.challenge[0], self.challenge[1],
                None, self.steps[0], self.steps[1], self.steps[2],
                self.sessions]
        root = Tk()
        entries = []
        for f, t in zip(fields, text):
            row = Frame(root)
            lab = Label(row, width=12, text=f, anchor='w')
            if t is '':
                ent = Entry(row, width=45)
                ent.insert(END, t)
            elif t:
                ent = Label(row, width=10, text=t, anchor='w')
            row.pack(side=TOP, fill=X, padx=5, pady=2)
            lab.pack(side=LEFT)
            if t is not None:
                ent.pack(side=RIGHT, expand=YES, fill=X)
                entries.append((f, ent))

        f = 'Summary'
        t = self.summary
        # root = Tk()
        # entries = []
        # for f, t in zip(fields, text):
        row = Frame(root)
        lab = Label(row, width=15, text=f, anchor='w')
        ent = MyText(row, width=45, height=10)
        ent.insert(END, t)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT, fill=BOTH)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((f, ent))

        self.onTask = IntVar()
        self.onTask.set(1)
        Label(root, text="Remained on task for this session",
              justify=LEFT, anchor='w').pack(side=LEFT, fill=X, padx=5, pady=5)
        Radiobutton(root, text="Yes", padx=20, variable=self.onTask,
                    value=1).pack(anchor=W, side=LEFT)
        Radiobutton(root, text="No", padx=20, variable=self.onTask,
                    value=2).pack(anchor=W, side=LEFT)

        ents = entries
        ents[7][1].focus_set()
        root.bind('<Return>', (lambda event, e=ents: self.fetch(e, root)))
        # Button to close window
        b3 = tk.Button(root, text='Quit', command=root.quit)
        b3.pack(side=LEFT, padx=5, pady=5)
        # Button to enter info. Same as return key
        b1 = tk.Button(root, text='Enter', command=(
            lambda e=ents: self.fetch(e, root)))
        b1.pack(side=RIGHT, padx=5, pady=5)
        # # Button to remove jobs
        # rmvjob = tk.Button(
        #     root, text='Remove', command=lambda r=root: self.removeJob(root))
        # rmvjob.pack(side=LEFT, padx=5, pady=5)
        root.mainloop()


class Settings(tk.Toplevel):
    def __init__(self):
        self.dir = '/home/brad/Projects/Python/pomodoro/pomodoro'
        self.time = 25
        self.shortBreak = 5
        self.longBreak = 20
        self.makeform()

    def saveSettings(self):
        print(vars(self))
        db = TinyDB('settings.json')
        db.insert(vars(self))

    def fetch(self, entries, root):
            # print(type(root))
            # print(type(entries))
            for entry in entries:
                if entry[0] == 'Time':
                    self.time = entry[1].get()
                elif entry[0] == 'Short Break':
                    self.shortBreak = entry[1].get()
                elif entry[0] == 'Long Break':
                    self.longBreak = entry[1].get()
            # self.saveSettings()
            root.destroy()

    def makeform(self):
        fields = ['Session Time', 'Short Break', 'Long Breaks']
        text = [self.time, self.shortBreak, self.longBreak]
        root = Tk()
        entries = []
        for f, t in zip(fields, text):
            row = Frame(root)
            lab = Label(row, width=15, text=f, anchor='w')
            ent = Entry(row, width=45)
            ent.insert(END, t)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((f, ent))

        ents = entries
        ents[0][1].focus_set()
        root.bind('<Return>', (lambda event, e=ents: self.fetch(e, root)))
        # Button to close window
        b3 = tk.Button(root, text='Quit', command=root.quit)
        b3.pack(side=LEFT, padx=5, pady=5)
        # Button to enter info. Same as return key
        b1 = tk.Button(root, text='Enter', command=(
            lambda e=ents: self.fetch(e, root)))
        b1.pack(side=RIGHT, padx=5, pady=5)
        # # Button to remove jobs
        # rmvjob = tk.Button(
        #     root, text='Remove', command=lambda r=root: self.removeJob(root))
        # rmvjob.pack(side=LEFT, padx=5, pady=5)
        root.mainloop()


class MenuForm(tk.Toplevel):
    """docstring for ClassName"""

    def __init__(self, master):
        print('Menu Opened')
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.makeform()

    def selectProject(self, root):
        p = self.mylist.get(tk.ACTIVE)
        print('Need to send {0} to MainApp'.format(p))
        self.withdraw()

    def makeform(self):
        self.title('Pomodoro')
        self.geometry('{}x{}'.format(300, 300))

        leftFrame = tk.Frame(self)
        leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, padx=1, pady=5)
        rightFrame = tk.Frame(self)
        rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=1, pady=5)

        scrollbar = tk.Scrollbar(rightFrame)

        self.mylist = tk.Listbox(rightFrame, width=90,
                                 yscrollcommand=scrollbar.set)

        self.selectBtn = tk.Button(leftFrame, text='Start')
        self.selectBtn.pack(fill=tk.X)

        self.addBtn = tk.Button(leftFrame, text='New')
        self.addBtn.pack(fill=tk.X)

        self.removeBtn = tk.Button(leftFrame, text='Remove')
        self.removeBtn.pack(fill=tk.X)

        self.quitBtn = tk.Button(leftFrame, text='Quit', command=self.quit)
        self.quitBtn.pack(fill=tk.X)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mylist.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=self.mylist.yview)
        self.withdraw()


class StatsForm(object):
    def __init__(self, project, pom_id):
        self.project = project
        db = TinyDB('test_goals.json').table(self.project)
        pom = db.get(doc_id=pom_id)
        self.timeLabels(pom['start'], pom['end'])
        self.makeform()

    def sec2Days(self, sec):
        return sec // (60 * 60 * 24)

    def timeLabels(self, start, end):
        self.start = time.strftime("%H:%M:%S", time.localtime(start))
        if self.sec2Days(start) == self.sec2Days(time.time()):
            print('happend today')
        self.end = (time.strftime("%H:%M:%S", time.localtime(end)))
        td = end - start
        m, s = (td // 60, td % 60)
        h, m = (m // 60, m % 60)
        self.duration = '{0}:{1}:{2}'.format(h, m, s)

    def addSession(self):
        print('Add another session to the pom')

    def makeform(self):
        fields = ['Project:', 'Start Time', 'End Time', 'Duration']
        text = [self.project, self.start, self.end, self.duration]
        root = Tk()
        entries = []
        for f, t in zip(fields, text):
            row = Frame(root)
            lab = Label(row, width=12, text=f, anchor='w')
            if t is '':
                ent = Entry(row, width=45)
                ent.insert(END, t)
            elif t:
                ent = Label(row, width=10, text=t, anchor='w')
            row.pack(side=TOP, fill=X, padx=5, pady=2)
            lab.pack(side=LEFT)
            if t is not None:
                ent.pack(side=RIGHT, expand=YES, fill=X)
                entries.append((f, ent))

        root.bind('<Return>', (lambda event: root.destroy()))

        # Button to enter info. Same as return key
        continueBtn = tk.Button(root, text='Continue', command=(
            lambda: self.addSession()))
        continueBtn.pack(side=RIGHT, padx=5, pady=5)
        quitBtn = tk.Button(root, text='Quit', command=root.quit)
        quitBtn.pack(side=LEFT, padx=5, pady=5)

        root.mainloop()


class Pomodoro(object):
    '''Controller class for the MVC implemntation'''
    project = ''
    challenge = ['', '']
    steps = ['', '', '']
    sessions = ''
    pomType = ''
    completed = ''
    todo = ''
    summary = ''

    directory = '/home/brad/Projects/Python/pomodoro/pomodoro'
    workTime = 25
    shortBreak = 5
    longBreak = 20

    def __init__(self, root):
        self.root = root
        print('Main App Started')
        # print(self.var)
        self.menu = MenuForm(self.root)
        self.menu.addBtn.config(command=lambda: self.newGoalForm())
        self.menu.selectBtn.config(command=lambda: self.openGoalForm())

        self.pom = GoalForm(self.root)
        self.pom.protocol('WM_DELETE_WINDOW', self.openMenu)
        self.pom.bind('<Return>', (lambda event: self.getGoal(self)))
        self.pom.enterBtn.config(command=(lambda: self.getGoal(self)))
        self.pom.quitBtn.config(command=self.openMenu)

        print("Done Init")
        self.openMenu()
        projects = ['Pomodoro', 'TempSensor', 'PoolPumpControl', 'FutureAuthoring', 'Website']
        for p in projects:
            self.menu.mylist.insert(tk.END, p)

    def openMenu(self):
        self.menu.deiconify()
        self.pom.withdraw()

    def openGoalForm(self):
        self.pom.projEnt.set(self.menu.mylist.get(tk.ACTIVE))
        self.pom.sessEnt.set(1)
        self.pom.chalEnt[0].ent.focus()
        self.pom.deiconify()
        self.menu.withdraw()

    def newGoalForm(self):
        self.pom.projEnt.set('')
        self.pom.sessEnt.set(1)
        self.pom.deiconify()
        self.menu.withdraw()

    def getGoal(self, root):
        self.project = self.pom.projEnt.get()
        self.challenge[0] = self.pom.chalEnt[0].get()
        self.challenge[1] = self.pom.chalEnt[1].get()
        self.steps[0] = self.pom.stepEnt[0].get()
        self.steps[1] = self.pom.stepEnt[1].get()
        self.steps[2] = self.pom.stepEnt[2].get()
        self.sessions = self.pom.sessEnt.get()
        self.pom.destroy()
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Pomodoro(root)
    root.mainloop()
    print(app.project)
    print(app.challenge[0])
    print(app.challenge[1])
    print(app.steps[0])
    print(app.steps[1])
    print(app.steps[2])
    print(app.sessions)

'''
f = GoalForm()
start = int(time.time())
pom = {'project': f.project,
       'challenge': f.challenge,
       'steps': f.steps,
       'sessions': f.sessions,
       'type': f.type.get()}
proj = goals.table(f.project)

pomID = proj.insert(pom)

if pom['type'] == 'task':
    l = TaskForm(pom)
    end = int(time.time())
    session = {'completed': l.completed,
               'todo': l.todo,
               'start': start,
               'end': end}
else:
    l = LearnForm(pom)
    end = int(time.time())
    session = {'summary': l.summary,
               'start': start,
               'end': end}
proj.update(session, doc_ids=[pomID])

StatsForm('This', 1)
'''
