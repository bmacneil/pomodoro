#! /usr/bin/python3

from tkinter import *
from tinydb import *

class GoalForm(object):
    """docstring for ClassName"""

    def __init__(self):
        self.project = ''
        self.challenge = ['', '']
        self.steps = ['', '', '']
        self.sessions = 1
        self.time = 25
        self.shortBreak = 5
        self.longBreak = 20
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
            elif entry[0] == 'Time':
                self.time = entry[1].get()
            elif entry[0] == 'Short Break':
                self.shortBreak = entry[1].get()
            elif entry[0] == 'Long Break':
                self.longBreak = entry[1].get()
            # else:
            #     print("\nFORM FETCH ERROR\n")
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
        print(self.time)
        print(self.shortBreak)
        print(self.longBreak)
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
        fields = ['Project', 'Worthy challenge:', '\ta)', '\tb)',
                  'Steps to complete:', '\t1.', '\t2.', '\t3.', 'Sessions',
                  'Time', 'Short Break', 'Long Breaks']
        text = [self.project, None, self.challenge[0], self.challenge[1],
                None, self.steps[0], self.steps[1], self.steps[2],
                self.sessions, self.time, self.shortBreak, self.longBreak]
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

    # def loadForm(self):



class TaskForm(object):
    """docstring for ClassName"""

    def __init__(self, settings):
        self.project = settings['project']
        self.start = 'Start Time'
        self.end = 'End Time'
        self.completed = ''
        self.todo = ''
        self.sessions = settings['sessions']
        self.time = settings['time']
        self.shortBreak = settings['shortBreak']
        self.longBreak = settings['longBreak']
        self.makeform()

    def fetch(self, entries, root):
        # print(type(root))
        # print(type(entries))
        for entry in entries:
            if entry[0] == 'Project':
                self.project = entry[1].get()
            elif entry[0] == '\ta)':
                self.challenge[0] = entry[1].get()
            # else:
            #     print("\nFORM FETCH ERROR\n")
        root.destroy()

    def printEntries(self):
        print("\n**************************")
        print(self.project)
        print(self.challenge[0])
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
        fields = [self.project, self.start, self.end, 'Completed', 'Todo']
        text = [None, None, None, self.completed, self.todo]
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
            if t is not None:
                ent.pack(side=RIGHT, expand=YES, fill=X)
                entries.append((f, ent))

        self.onTask = IntVar().set(0)
        self.onTask.set(1)
        Label(root, text="Remained on task for this session",
              justify=LEFT, anchor='w').pack(side=LEFT, fill=X, padx=5, pady=5)
        Radiobutton(root, text="Yes", padx=20, variable=self.onTask,
                    value=1).pack(anchor=W, side=LEFT)
        Radiobutton(root, text="No", padx=20, variable=self.onTask,
                    value=2).pack(anchor=W, side=LEFT)

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

    def __init__(self, settings):
        self.project = settings['project']
        self.start = 'Start Time'
        self.end = 'End Time'
        self.summary = ''
        self.sessions = settings['sessions']
        self.time = settings['time']
        self.shortBreak = settings['shortBreak']
        self.longBreak = settings['longBreak']
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
        fields = [self.project, self.start, self.end, 'Summary']
        text = [None, None, None, self.summary]
        root = Tk()
        entries = []
        for f, t in zip(fields, text):
            row = Frame(root)
            lab = Label(row, width=15, text=f, anchor='w')
            if t is not None:
                ent = MyText(row, width=45, height=10)
                ent.insert(END, t)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT, fill=BOTH)
            if t is not None:
                ent.pack(side=RIGHT, expand=YES, fill=X)
                entries.append((f, ent))

        self.onTask = IntVar()
        self.onTask.set()
        Label(root, text="Remained on task for this session",
              justify=LEFT, anchor='w').pack(side=LEFT, fill=X, padx=5, pady=5)
        Radiobutton(root, text="Yes", padx=20, variable=self.onTask,
                    value=1).pack(anchor=W, side=LEFT)
        Radiobutton(root, text="No", padx=20, variable=self.onTask,
                    value=2).pack(anchor=W, side=LEFT)

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


goals = TinyDB('test_goals.json')
sessions = TinyDB('test_sessions.json')

f = GoalForm()
print(vars(f))
# goals.insert(vars(f))

t = LearnForm(vars(f))
t.printEntries()
task.insert(vars(t))
