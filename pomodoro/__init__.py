#! /usr/bin/python3

from tkinter import *


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


class SettingsForm(object):
    """docstring for ClassName"""

    def __init__(self):
        self.workTime = 25
        self.breakTime = 5
        self.workSessions = 1
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
        fields = ['Project', 'Worthy challenge:', '\ta)',
                  '\tb)', 'Steps to complete:', '\t1.', '\t2.', '\t3.']
        text = [self.project, None, self.challenge[0], self.challenge[1],
                None, self.steps[0], self.steps[1], self.steps[2]]
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


f = GoalForm()
print(f.printEntries())
