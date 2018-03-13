#! /usr/bin/python3

import tkinter as tk
from tinydb import *
import time
import schedule


class SessionTimer(object):
    '''Session Timer'''

    def __init__(self, project=None):
        if project is None:
            print('New')


class LabelRow(tk.Frame):
    def __init__(self, master, label, t=None):
        row = tk.Frame(master)
        lab = tk.Label(row, width=15, text=label, anchor='w')
        self.ent = tk.Label(row, width=10, anchor='w')
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        self.ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    def set(self, text):
        self.ent.config(text=text)


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
        tk.Text.__init__(self, master, kw)
        # self.bind("<Return>", lambda e: None)
        # self.bind("<Tab>", self.focus_next_window)
        # self.bind("<Control-Return>", lambda e: '\n')

    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return("break")


class TextRow(tk.Frame):
    def __init__(self, master, label):
        row = tk.Frame(master)
        lab = tk.Label(row, width=15, text=label, anchor='w')
        self.ent = MyText(row, width=45, height=10)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT, fill=tk.BOTH)
        self.ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    def get(self):
        return self.ent.get("1.0", 'end-2c')


# View - Base Class for all forms
class Form(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)


class GoalForm(tk.Toplevel):
    """docstring for ClassName"""

    projEnt = ''
    chalEnt = ['', '']
    stepEnt = ['', '', '']

    def __init__(self, master):
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
        # self.withdraw()


class AdditionalForm(tk.Toplevel):
    """docstring for ClassName"""

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.makeform()

    def makeform(self):
        self.title('Continue Session')
        self.projLab = LabelRow(self, 'Project:')
        self.chalLab = [LabelRow(self, 'Challenge:\t    a)'),
                        LabelRow(self, '\t    b)')]
        self.stepLab = [LabelRow(self, 'Steps:\t    1.'),
                        LabelRow(self, '\t    2.'),
                        LabelRow(self, '\t    3.')]
        self.sessLab = LabelRow(self, 'Sessions:')

        self.quitBtn = tk.Button(self, text='Quit')
        self.quitBtn.pack(side=tk.RIGHT, padx=5, pady=5)
        # Button to enter info. Same as return key
        self.enterBtn = tk.Button(self, text='Start')
        self.enterBtn.pack(side=tk.LEFT, padx=5, pady=5)


class TaskForm(tk.Toplevel):
    """docstring for ClassName"""

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.makeform()

    def makeform(self):
        self.title('Task')
        self.projLab = LabelRow(self, 'Project:')
        self.chalLab = [LabelRow(self, 'Challenge:\t    a)'),
                        LabelRow(self, '\t    b)')]
        self.stepLab = [LabelRow(self, 'Steps:\t    1.'),
                        LabelRow(self, '\t    2.'),
                        LabelRow(self, '\t    3.')]
        self.sessLab = LabelRow(self, 'Sessions:')
        self.compEnt = EntryRow(self, 'Completed')
        self.todoEnt = EntryRow(self, 'Todo')

        self.onTask = tk.IntVar()
        self.onTask.set(1)
        tk.Label(self, text="Remained on task for this session",
                 justify=tk.LEFT, anchor='w').pack(side=tk.LEFT,
                                                   fill=tk.X, padx=5, pady=5)
        tk.Radiobutton(self, text="Yes", padx=20, variable=self.onTask,
                       value=1).pack(anchor=tk.W, side=tk.LEFT)
        tk.Radiobutton(self, text="No", padx=20, variable=self.onTask,
                       value=2).pack(anchor=tk.W, side=tk.LEFT)

        self.compEnt.ent.focus_set()
        # self.bind('<Return>', (lambda event, e=ents: self.fetch(e, self)))
        # Button to close window
        self.quitBtn = tk.Button(self, text='Quit')
        self.quitBtn.pack(side=tk.LEFT, padx=5, pady=5)
        # Button to enter info. Same as return key
        self.enterBtn = tk.Button(self, text='Enter')
        self.enterBtn.pack(side=tk.RIGHT, padx=5, pady=5)


class LearnForm(tk.Toplevel):
    """docstring for ClassName"""

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.makeform()

    def makeform(self):
        self.title('Learn')
        self.projLab = LabelRow(self, 'Project:')
        self.chalLab = [LabelRow(self, 'Challenge:\t    a)'),
                        LabelRow(self, '\t    b)')]
        self.stepLab = [LabelRow(self, 'Steps:\t    1.'),
                        LabelRow(self, '\t    2.'),
                        LabelRow(self, '\t    3.')]
        self.sessLab = LabelRow(self, 'Sessions:')
        self.summText = TextRow(self, 'Summary')

        self.onTask = tk.IntVar()
        self.onTask.set(1)
        tk.Label(self, text="Remained on task for this session",
                 justify=tk.LEFT, anchor='w').pack(side=tk.LEFT,
                                                   fill=tk.X, padx=5, pady=5)
        tk.Radiobutton(self, text="Yes", padx=20, variable=self.onTask,
                       value=1).pack(anchor=tk.W, side=tk.LEFT)
        tk.Radiobutton(self, text="No", padx=20, variable=self.onTask,
                       value=2).pack(anchor=tk.W, side=tk.LEFT)

        self.summText.ent.focus_set()
        # self.bind('<Return>', (lambda event, e=ents: self.fetch(e, self)))
        # Button to close window
        self.quitBtn = tk.Button(self, text='Quit')
        self.quitBtn.pack(side=tk.LEFT, padx=5, pady=5)
        # Button to enter info. Same as return key
        self.enterBtn = tk.Button(self, text='Enter')
        self.enterBtn.pack(side=tk.RIGHT, padx=5, pady=5)


class Settings(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

        self.makeform()

    def makeform(self):
        self.title('Settings')
        self.time = EntryRow(self, 'Time')
        self.shortBreak = EntryRow(self, 'Short Break')
        self.longBreak = EntryRow(self, 'Long Break')
        self.directory = EntryRow(self, 'Directory')

        self.time.ent.focus_set()
        # Button to close window
        self.quitBtn = tk.Button(self, text='Quit')
        self.quitBtn.pack(side=tk.RIGHT, padx=5, pady=5)
        # Button to enter info. Same as return key
        self.enterBtn = tk.Button(self, text='Enter')
        self.enterBtn.pack(side=tk.RIGHT, padx=5, pady=5)


class MenuForm(tk.Toplevel):
    """docstring for ClassName"""

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.makeform()

    def selectProject(self, root):
        p = self.mylist.get(tk.ACTIVE)
        self.withdraw()

    def makeform(self):
        self.title('Pomodoro')

        self.geometry('{}x{}'.format(300, 300))

        leftFrame = tk.Frame(self)
        leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, padx=1, pady=5)
        rightFrame = tk.Frame(self)
        rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=1, pady=5)

        scrollbar = tk.Scrollbar(rightFrame)

        self.mylist = tk.Listbox(rightFrame, width=30, height=20,
                                 yscrollcommand=scrollbar.set)

        self.selectBtn = tk.Button(leftFrame, text='Start')
        self.selectBtn.pack(fill=tk.X)

        self.addBtn = tk.Button(leftFrame, text='New')
        self.addBtn.pack(fill=tk.X)

        self.settingsBtn = tk.Button(leftFrame, text='Settings')
        self.settingsBtn.pack(fill=tk.X)

        self.quitBtn = tk.Button(leftFrame, text='Quit', command=self.quit)
        self.quitBtn.pack(fill=tk.X)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mylist.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=self.mylist.yview)
        # self.withdraw()


class StatsForm(tk.Toplevel):
    ''' '''

    def __init__(self, master, pom):
        tk.Toplevel.__init__(self, master)
        self.makeform(pom)

    def sec2Days(self, sec):
        return sec // (60 * 60 * 24)

    def setTimeLabels(self, start, end):
        startTime = time.strftime("%H:%M:%S", time.localtime(start))
        if self.sec2Days(start) == self.sec2Days(time.time()):
            pass
        endTime = (time.strftime("%H:%M:%S", time.localtime(end)))
        td = end - start
        m, s = (td // 60, td % 60)
        h, m = (m // 60, m % 60)
        duration = '{0}:{1}:{2}'.format(h, m, s)

        self.starLab.set(startTime)
        self.endLab.set(endTime)
        self.durLab.set(duration)

    def makeform(self, pom):
        self.title('Session Summary')

        self.projLab = LabelRow(self, 'Project:').set(pom.project)
        self.starLab = LabelRow(self, 'Start Time:')
        self.endLab = LabelRow(self, 'End Time:')
        self.durLab = LabelRow(self, 'Duration:')
        self.setTimeLabels(pom.start[pom.sessions], pom.end[pom.sessions])

        # Button to enter info. Same as return key
        self.continueBtn = tk.Button(self, text='Continue')
        self.continueBtn.pack(side=tk.LEFT, padx=5, pady=5)

        self.quitBtn = tk.Button(self, text='Quit')
        self.quitBtn.pack(side=tk.LEFT, padx=5, pady=5)


# Controller - Coordinates between model and view
class Pomodoro(object):
    '''Controller class for the MVC implemntation'''

    directory = '/home/brad/Projects/Python/pomodoro/'
    workTime = 25
    shortBreak = 5
    longBreak = 20
    docKeys = ['challenge', 'completed', 'end', 'sessions',
               'start', 'steps', 'summary', 'todo', 'type']

    def __init__(self, root):
        self.completed = []
        self.todo = []
        self.summary = []
        self.start = []
        self.end = []
        self.sessions = 0
        self.root = root
        root.iconphoto(True, tk.PhotoImage(
            file='/home/brad/Projects/Python/pomodoro/pomodoro/tomato-1.png'))
        self.db = TinyDB('{0}pomodoro.json'.format(self.directory))

        self.menu = MenuForm(self.root)
        self.menu.addBtn.config(command=lambda: self.openGoalForm())
        self.menu.selectBtn.config(command=lambda: self.openGoalForm(1))
        self.menu.settingsBtn.config(command=lambda: self.openSettings())
        self.openMenu()
        # projects = ['Pomodoro', 'TempSensor',
        # 'PoolPumpControl', 'FutureAuthoring', 'Website']

    def openMenu(self, child=None):
        self.menu.mylist.delete(0, tk.END)
        for p in self.db.tables():
            self.menu.mylist.insert(tk.END, p)
        self.center(self.menu)
        if child:
            child.destroy()

    def openSettings(self):
        self.sett = Settings(self.root)
        self.sett.protocol('WM_DELETE_WINDOW', lambda: self.openMenu(self.sett))
        self.sett.bind('<Return>', (lambda event: self.getSettings()))
        self.sett.enterBtn.config(command=(lambda: self.getSettings()))
        self.sett.quitBtn.config(command=(lambda: self.openMenu(self.sett)))

        self.sett.time.set(self.workTime)
        self.sett.shortBreak.set(self.shortBreak)
        self.sett.longBreak.set(self.longBreak)
        self.sett.directory.set(self.directory)

        self.menu.withdraw()
        self.center(self.sett)
        self.sett.focus_force()

    def getSettings(self):
        self.workTime = int(self.sett.time.get())
        self.shortBreak = int(self.sett.shortBreak.get())
        self.longBreak = int(self.sett.longBreak.get())
        self.openMenu(self.sett)

    def openGoalForm(self, proj=None):
        self.pom = GoalForm(self.root)
        self.pom.protocol('WM_DELETE_WINDOW', lambda: self.openMenu(self.pom))
        self.pom.bind('<Return>', (lambda event: self.getGoal()))
        self.pom.enterBtn.config(command=(lambda: self.getGoal()))
        self.pom.quitBtn.config(command=(lambda: self.openMenu(self.pom)))

        if proj:
            self.pom.projEnt.set(self.menu.mylist.get(tk.ACTIVE))
            self.pom.chalEnt[0].ent.focus()
        else:
            self.pom.projEnt.set('')

        self.menu.withdraw()
        self.center(self.pom)
        self.pom.focus_force()

    def getGoal(self):
        # Press enter on goal form
        self.project = self.pom.projEnt.get()
        self.challenge = [self.pom.chalEnt[0].get(),
                          self.pom.chalEnt[1].get()]
        self.steps = [self.pom.stepEnt[0].get(),
                      self.pom.stepEnt[1].get(),
                      self.pom.stepEnt[2].get()]
        self.type = self.pom.type.get()
        # destroy goal form
        self.pom.withdraw()

        # Open done form
        self.openDoneForm()

    def openDoneForm(self, child=None):
        # Schedule work period
        if child:
            child.withdraw()
        schedule.every(self.workTime).minutes.do(self.job)
        # record start time
        self.start.append(int(time.time()))
        # Start working
        self.runPendingJobs()
        # Work time ends

        # Enter what was done
        if self.type == 'task':
            self.done = TaskForm(self.root)
        else:
            self.done = LearnForm(self.root)

        self.done.projLab.set(self.project)
        self.done.chalLab[0].set(self.challenge[0])
        self.done.chalLab[1].set(self.challenge[1])
        self.done.stepLab[0].set(self.steps[0])
        self.done.stepLab[1].set(self.steps[1])
        self.done.stepLab[2].set(self.steps[2])
        self.done.sessLab.set(str(self.sessions))

        self.done.protocol('WM_DELETE_WINDOW', lambda: self.openMenu(self.done))
        self.done.quitBtn.config(command=(lambda: self.openMenu(self.done)))

        # Enter Key and Enter Button direct to getDone method
        self.done.bind('<Return>', (lambda event: self.getDone()))
        self.done.enterBtn.config(command=(lambda: self.getDone()))

        self.center(self.done)
        self.done.focus_force()
        # Press enter

    def getDone(self):
        # Append done and todo to list
        if self.type == 'task':
            self.completed.append(self.done.compEnt.get())
            self.todo.append(self.done.todoEnt.get())
        else:
            self.summary.append(self.done.summText.get())

        self.onTask = self.done.onTask.get()
        self.end.append(int(time.time()))

        self.done.withdraw()
        self.openStats()

    def openStats(self):
        self.stat = StatsForm(self.root, self)
        self.stat.protocol('WM_DELETE_WINDOW', lambda: self.endSession(self.stat))
        self.stat.quitBtn.config(command=(lambda: self.endSession(self.stat)))

        self.stat.bind('<Return>', (lambda event: self.addSession()))
        self.stat.continueBtn.config(command=(lambda: self.addSession()))

        # increment session counter
        self.sessions += 1

        self.center(self.stat)
        self.stat.focus_force()

    def addSession(self):
        # Schedule Break period
        if self.sessions % 4 == 0:
            breakTime = self.longBreak
        else:
            breakTime = self.shortBreak
        schedule.every(breakTime).minutes.do(self.startBreak)
        # record start time
        # self.breakStart = int(time.time())
        # Start working
        self.stat.withdraw()
        self.runPendingJobs()
        # Break time ends
        self.openAdditional()

    def openAdditional(self):
        self.add = AdditionalForm(self.root)

        self.add.projLab.set(self.project)
        self.add.chalLab[0].set(self.challenge[0])
        self.add.chalLab[1].set(self.challenge[1])
        self.add.stepLab[0].set(self.steps[0])
        self.add.stepLab[1].set(self.steps[1])
        self.add.stepLab[2].set(self.steps[2])
        self.add.sessLab.set(str(self.sessions))

        self.add.protocol('WM_DELETE_WINDOW', lambda: self.endSession(self.add))
        self.add.quitBtn.config(command=(lambda: self.endSession(self.add)))

        # Enter Key and Enter Button direct to getDone method
        self.add.bind('<Return>', (lambda event: self.openDoneForm(self.add)))
        self.add.enterBtn.config(command=(lambda: self.openDoneForm(self.add)))

        self.center(self.add)
        self.add.focus_force()

    def endSession(self, child=None):
        # Continue task or new?
        # Continue: start break timer
        # New: open menu
        # record in db
        # Remove any item not in docKeys list
        d = vars(self)
        # Create a new dict to avoid altering Pomodoro object
        entry = {k: d[k] for k in d if k in self.docKeys}
        # Write to the project table in the database
        projTB = self.db.table(self.project)
        projTB.insert(entry)

        self.openMenu(child)
        # Reinitialize lists
        self.completed = []
        self.todo = []
        self.summary = []
        self.start = []
        self.end = []
        self.sessions = 0

    def center(self, root):
        root.withdraw()
        root.update_idletasks()
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.geometry("+%d+%d" % (x, y))
        root.deiconify()

    def job(self):
        return schedule.CancelJob

    def runPendingJobs(self):
        try:
            while schedule.jobs:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def startBreak(self):
        return schedule.CancelJob


def main():
    root = tk.Tk()
    root.withdraw()
    app = Pomodoro(root)
    root.mainloop()


if __name__ == '__main__':
    main()
