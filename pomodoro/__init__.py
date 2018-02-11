#! /usr/bin/python3

from tkinter import *
from tinydb import *
import time


class Pomodoro(object):
    '''Main app class for the pomodoro program'''
    def __init__(self, project=None):
        if project is None:
            print('New')


class Settings(object):
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

    def toDict(self):
        return vars(self)

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
        b3 = Button(root, text='Quit', command=root.quit)
        b3.pack(side=LEFT, padx=5, pady=5)
        # Button to enter info. Same as return key
        b1 = Button(root, text='Enter', command=(
            lambda e=ents: self.fetch(e, root)))
        b1.pack(side=RIGHT, padx=5, pady=5)
        # # Button to remove jobs
        # rmvjob = Button(
        #     root, text='Remove', command=lambda r=root: self.removeJob(root))
        # rmvjob.pack(side=LEFT, padx=5, pady=5)
        root.mainloop()


class GoalForm(object):
    """docstring for ClassName"""

    def __init__(self, p=''):
        self.project = p
        self.challenge = ['', '']
        self.steps = ['', '', '']
        self.sessions = 1
        self.makeform()

    def fetch(self, entries, root):
        # print(type(root))
        # print(type(entries))
        for entry in entries:
            if entry[0] == 'Project':
                self.project = entry[1].get()
            elif entry[0] == '\ta)':
                self.challenge[0] = entry[1].get()
            elif entry[0] == '\tb)':
                self.challenge[1] = entry[1].get()
            elif entry[0] == '\t1.':
                self.steps[0] = entry[1].get()
            elif entry[0] == '\t2.':
                self.steps[1] = entry[1].get()
            elif entry[0] == '\t3.':
                self.steps[2] = entry[1].get()
            elif entry[0] == 'Sessions':
                self.sessions = entry[1].get()
            # # TODO: Move to settings form
            # elif entry[0] == 'Time':
            #     self.time = entry[1].get()
            # elif entry[0] == 'Short Break':
            #     self.shortBreak = entry[1].get()
            # elif entry[0] == 'Long Break':
            #     self.longBreak = entry[1].get()
        root.destroy()

    def printEntries(self):
        print("\n**************************")
        print(self.project)
        print(self.challenge[0])
        print(self.challenge[1])
        print(self.steps[0])
        print(self.steps[1])
        print(self.steps[2])
        print(self.sessions)
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
        fields = ['Project', 'Challenge:', '\ta)', '\tb)',
                  'Steps:', '\t1.', '\t2.', '\t3.', 'Sessions']
        text = [self.project, None, self.challenge[0], self.challenge[1],
                None, self.steps[0], self.steps[1], self.steps[2],
                self.sessions]
        root = Tk()
        entries = []
        for f, t in zip(fields, text):
            row = Frame(root)
            lab = Label(row, width=15, text=f, anchor='w')
            if t is not None:
                ent = Entry(row, width=45)
                ent.insert(END, t)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((f, ent))

        ents = entries
        ents[0][1].focus_set()

        # Task type radio button
        self.type = StringVar()
        self.type.set('task')
        Label(root, text="Session Type",
              justify=LEFT, anchor='w').pack(side=LEFT, fill=X, padx=5, pady=5)
        Radiobutton(root, text="Task", padx=20, variable=self.type,
                    value='task').pack(anchor=W, side=LEFT)
        Radiobutton(root, text="Learn", padx=20, variable=self.type,
                    value='learn').pack(anchor=W, side=LEFT)

        root.bind('<Return>', (lambda event, e=ents: self.fetch(e, root)))
        # Button to close window
        enterButton = Button(root, text='Enter', command=(
            lambda e=ents: self.fetch(e, root)))
        enterButton.pack(side=RIGHT, padx=5, pady=5)

        quitButton = Button(root, text='Quit', command=root.quit)
        quitButton.pack(side=RIGHT, padx=5, pady=5)
        # Button to enter info. Same as return key
        # # Button to remove jobs
        # rmvjob = Button(
        #     root, text='Remove', command=lambda r=root: self.removeJob(root))
        # rmvjob.pack(side=LEFT, padx=5, pady=5)
        root.mainloop()

    # def loadForm(self):


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
        b3 = Button(root, text='Quit', command=root.quit)
        b3.pack(side=LEFT, padx=5, pady=5)
        # Button to enter info. Same as return key
        b1 = Button(root, text='Enter', command=(
            lambda e=ents: self.fetch(e, root)))
        b1.pack(side=RIGHT, padx=5, pady=5)
        # # Button to remove jobs
        # rmvjob = Button(
        #     root, text='Remove', command=lambda r=root: self.removeJob(root))
        # rmvjob.pack(side=LEFT, padx=5, pady=5)
        root.mainloop()


class MyText(Text):
    def __init__(self, master, **kw):
        Text.__init__(self, master, kw)
        # self.bind("<Return>", lambda e: None)
        # self.bind("<Tab>", self.focus_next_window)
        # self.bind("<Control-Return>", lambda e: '\n')

    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return("break")


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
        b3 = Button(root, text='Quit', command=root.quit)
        b3.pack(side=LEFT, padx=5, pady=5)
        # Button to enter info. Same as return key
        b1 = Button(root, text='Enter', command=(
            lambda e=ents: self.fetch(e, root)))
        b1.pack(side=RIGHT, padx=5, pady=5)
        # # Button to remove jobs
        # rmvjob = Button(
        #     root, text='Remove', command=lambda r=root: self.removeJob(root))
        # rmvjob.pack(side=LEFT, padx=5, pady=5)
        root.mainloop()


class MenuForm(object):
    """docstring for ClassName"""

    def __init__(self):
        self.makeform()

    def fetch(self, entries, root):
        # print(type(root))
        # print(type(entries))
        for entry in entries:
            if entry[0] == 'Project':
                self.project = entry[1].get()
        root.destroy()

    def addGoalForm(self):
        f = GoalForm()

    def selectProject(self, root):
        p = self.mylist.get(ACTIVE)
        print(p)
        root.destroy()
        f = GoalForm(p)

    def makeform(self):
        projects = ['Pomodoro', 'TempSensor', 'PoolPumpControl', 'FutureAuthoring', 'Website']
        # project = 'Default'
        root = Tk()
        root.title('Menu')
        root.geometry('{}x{}'.format(300, 300))

        scrollbar = Scrollbar(root)

        self.mylist = Listbox(root, yscrollcommand=scrollbar.set)
        for p in projects:
            self.mylist.insert(END, p)

        # print(type(mylist.get(ACTIVE)))
        # print(mylist.get(ACTIVE))
        # print(type(mylist.curselection()))
        # print(mylist.curselection())

        selectButton = Button(root, text='Start', command=(lambda :self.selectProject(root)))
        selectButton.pack()
        selectButton.place(bordermode=INSIDE,
                           relx=0.05,
                           x=-5,
                           rely=0.1,
                           relheight=.2,
                           relwidth=.3,
                           anchor=NW)

        addButton = Button(root, text='New', command=self.addGoalForm)
        addButton.pack()
        addButton.place(bordermode=INSIDE,
                        relx=0.05,
                        x=-5,
                        rely=0.3,
                        relheight=.2,
                        relwidth=.3,
                        anchor=NW)

        removeButton = Button(root, text='Remove')
        removeButton.pack()
        removeButton.place(bordermode=INSIDE,
                           relx=0.05,
                           x=-5,
                           rely=0.5,
                           relheight=.2,
                           relwidth=.3,
                           anchor=NW)

        quitButton = Button(root, text='Quit', command=root.quit)
        quitButton.pack()
        quitButton.place(bordermode=INSIDE,
                         relx=0.05,
                         x=-5,
                         rely=0.7,
                         relheight=.2,
                         relwidth=.3,
                         anchor=NW)

        scrollbar.pack()
        scrollbar.place(bordermode=OUTSIDE, relheight=1, relx=1, anchor=NE)
        self.mylist.pack()
        self.mylist.place(bordermode=OUTSIDE,
                          relx=1,
                          x=-15,
                          rely=0,
                          relheight=1,
                          relwidth=.6,
                          anchor=NE)

        scrollbar.config(command=self.mylist.yview)
        root.mainloop()


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
        continueBtn = Button(root, text='Continue', command=(
            lambda: self.addSession()))
        continueBtn.pack(side=RIGHT, padx=5, pady=5)
        quitBtn = Button(root, text='Quit', command=root.quit)
        quitBtn.pack(side=LEFT, padx=5, pady=5)

        root.mainloop()

goals = TinyDB('test_goals.json')
sessions = TinyDB('test_sessions.json')

settings = {}
settings['project'] = 'Project'
settings['sessions'] = 1
settings['time'] = 25
settings['shortBreak'] = 2
settings['longBreak'] = 10

# s = Settings()
# print(s.toDict())
f = GoalForm()
start = int(time.time())
pom = {'project': f.project,
       'challenge': f.challenge,
       'steps': f.steps,
       'sessions': f.sessions,
       'type': f.type.get()}
proj = goals.table(f.project)

pomID = proj.insert(pom)

# print(vars(f))
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
# l = LearnForm(settings)
# m = MenuForm()
# print(vars(f))
# goals.insert(vars(f))



# t = LearnForm(vars(f))
# t.printEntries()
# task.insert(vars(t))
