# ! /usr/bin/python3
from tinydb import *
from tkform import *
from tuptest import *
import time
from functools import partial
import schedule
import tkinter as tk
from warnings import warn


class PomOld(object):
    '''
    pom session data and settings

    Pom object is a data class that coordinated the input data from user
    forms with the TindDB database.

    Attributes:
        project: ([type]): project name
        challenges: (list): StringVar list of challenges
        steps: (list): StringVar list of steps
        type: (StringVar): Session type: task or learn
        onTask: (StringVar): On task for session: yes or no
        done: (function): Completed during task session
        todo: (StringVar): Left todo after a task session
        summ: (StringVar): Summary of a learn session
        startSec: (IntVar): Start time in seconds since epoch
        endSec: (IntVar): End time in seconds since epoch
        dones: (list): List of completed tasks
        todos: (list): List of todos
        summs: (list): List of learn session summaries
        start: (list): List of session start times
        end: (list): List of session end times
        sessions: (int): Number of sessions
        directory: (StringVar): path to the tinyDB directory
        workTime: (IntVar): Session duration in minutes
        shortBreak: (IntVar): Short break duration in minutes
        longBreak: (IntVar): Long break duration in minutes
    '''

    def __init__(self, project=None):
        '''
        Pom object initilizer

        Initilizes a pom object as either a new project or
        as an existing project when the project name is an arg
        Args:
            project: (str): Project name for pom session (default: {None})
        '''
        self.project = tk.StringVar(value=project)
        self.challenges = [tk.StringVar(), tk.StringVar()]
        self.steps = [tk.StringVar(),
                      tk.StringVar(),
                      tk.StringVar()]
        self.type = tk.StringVar(value='task')
        self.onTask = tk.StringVar(value='yes')
        self.done = tk.StringVar()
        self.todo = tk.StringVar()
        self.summ = tk.StringVar()
        self.startSec = tk.IntVar(value=1518721735)
        self.endSec = tk.IntVar(value=1518730947)
        self.dones = []
        self.todos = []
        self.summs = []
        self.start = []
        self.end = []
        self.sessions = 0

        self.directory = tk.StringVar(
            value='/home/brad/Projects/Python/pomodoro/')
        self.workTime = tk.IntVar(value=25)
        self.shortBreak = tk.IntVar(value=5)
        self.longBreak = tk.IntVar(value=20)
        # self.db = TinyDB('{0}pomodoro.json'.format(self.directory.get()))
        # self.projects = self.db.tables()

    def __repr__(self):
        return self.__class__.__name__

    def append(self):
        '''
        Append pom data to session lists

        Appends the pom data
        '''
        self.dones.append(self.done.get())
        self.todos.append(self.todo.get())
        self.summs.append(self.summ.get())
        self.start.append(self.startSec.get())
        self.end.append(self.endSec.get())
        self.done.set('')
        self.todo.set('')
        self.summ.set('')
        self.startSec.set(0)
        self.endSec.set(0)

    def save(self):
        print('Saving Pom state')

    def stats(self):
        print()

    def print(self):
        print('Project ', self.project.get())
        print('Challenge:\t    a) ', self.challenges[0].get())
        print('\t    b)', self.challenges[1].get())
        print('Steps:\t    1. ', self.steps[0].get())
        print('\t    2. ', self.steps[1].get())
        print('\t    3. ', self.steps[2].get())
        print('type ', self.type.get())
        print(self.dones)
        print(self.todos)
        print(self.summs)
        print(self.start)
        print(self.end)
        print('Settings')
        print(self.workTime.get())
        print(self.shortBreak.get())
        print(self.longBreak.get())


class GoalForm(Form):
    """docstring for ClassName"""

    def __init__(self, parent, pom):
        Form.__init__(self, parent)
        self.title('Pomodoro')
        self.make(pom)
        self.withdraw()

    def make(self, pom):
        for attr in pom:
            self.addRow(EntryRow, attr.label, var=attr.var)
        if pom.project.get() == '':
            self.rows[pom.project.label].focus()
        else:
            self.rows[pom.chalA.label].focus()

        typeRb = RadioRow(self.btnsFr, pom.type.label)
        typeRb.add('Task', 'task', pom.type.var)
        typeRb.add('Learn', 'learn', pom.type.var)


class TaskForm(Form):
    """docstring for ClassName"""

    def __init__(self, parent, pom):
        self.pom = pom
        # self.openFrame = partial(self.setFrame, newPom.type.var)
        Form.__init__(self, parent)
        self.title('Pomodoro - Task')
        self.make(pom)

    def make(self, pom):

        for attr in pom:
            self.addRow(LabelRow, attr.label, var=attr.var)

        self.learnFr = tk.Frame(self.formFr)
        self.addRow(TextRow, pom.summ.label, var=pom.summ.var, frame=self.learnFr)

        self.taskFr = tk.Frame(self.formFr)
        for attr in (pom.done, pom.todo):
            self.addRow(EntryRow, attr.label, var=attr.var, frame=self.taskFr)

        typeRb = RadioRow(self.radioFr, pom.onTask.label)
        typeRb.add('Yes', 'yes', pom.onTask.var)
        typeRb.add('No', 'no', pom.onTask.var)

    def addCallback(self, callback):
            self.timerCallback = callback

    def setLabels(self):
        pass
        # self.rows['Project'].set(self.pom.project.get())

    def setFrame(self):
        self.setLabels()
        if self.pom.type.get() == 'learn':
            self.learnFr.pack(side=tk.TOP, fill=tk.X, pady=5)
            self.taskFr.pack_forget()
            self.rows['Summary'].focus()
            self.formSize(600, 450)
        else:
            self.taskFr.pack(side=tk.TOP, fill=tk.X, pady=5)
            self.learnFr.pack_forget()
            self.rows['Completed'].focus()
            self.formSize(600, 300)

    def open(self):
        self.setFrame()
        self.pack()
        self.center()
        self.update()
        self.deiconify()

    def close(self):
        self.timerCallback()
        self.pom.summ.set(self.rows['Summary'].get())
        self.pom.append()
        self.rows['Summary'].clear('')
        self.withdraw()


class SettingsForm(Form):
    """docstring for ClassName"""

    def __init__(self, parent, settings):
        Form.__init__(self, parent)
        self.title('Pomodoro - Settings')
        self.formSize(400, 200)
        self.make(settings)
        # self.withdraw()

    def close(self):
        self.withdraw()

    def make(self, settings):
        for label, var in settings:
            self.addRow(EntryRow, label, var=var)


class StatsForm(Form):
    """docstring for ClassName"""

    def __init__(self, parent, pom):
        Form.__init__(self, parent)
        self.title('Pomodoro - Summary')
        self.formSize(400, 200)
        self.refresh = partial(self.make, pom)
        self.withdraw()

    def open(self):
        '''Initilize and open form'''
        self.refresh()
        self.pack()
        self.center()
        self.update()
        self.deiconify()

    def close(self):
        for child in self.formFr.winfo_children():
            child.destroy()
        self.withdraw()

    def make(self, pom):
        print('Made Stats Form')
        pom.timeData.sec2HMS()
        pom.timeData.getDuration()
        print(pom.timeData.startTime)
        print(pom.timeData.endTime)
        self.addRow(LabelRow, 'Project:', var=pom.form.project.var)
        self.addRow(LabelRow, 'Sessions:', var=pom.timeData.sessions)
        self.addRow(LabelRow, 'Start Time:', text=pom.timeData.startTime)
        self.addRow(LabelRow, 'End Time:', text=pom.timeData.endTime)
        self.addRow(LabelRow, 'Duration:', text=pom.timeData.duration)


class MenuForm(Form):
    """docstring for ClassName"""

    def __init__(self, parent, projects=None):
        Form.__init__(self, parent)
        self.title('Pomodoro - Task')
        self.formSize(300, 300)
        self.make()
        self.withdraw()

    def getActiveProject(self):
        return self.mylist.get(tk.ACTIVE)

    def setProjectList(self, projects):
        self.mylist.delete(0, tk.END)
        for p in projects:
            self.mylist.insert(tk.END, p)

    def make(self):
        self.scrollbar = tk.Scrollbar(self.formFr)
        self.mylist = tk.Listbox(self.formFr, width=30, height=20,
                                 yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.mylist.yview)

    def pack(self):
        '''Pack all form frames'''
        self.btnsFr.pack(side=tk.LEFT, fill=tk.BOTH, padx=1, pady=5)
        for b in self.btns['order']:
            self.btns[b].pack(fill=tk.X)
        self.formFr.pack(side=tk.RIGHT, fill=tk.BOTH, padx=1, pady=5)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mylist.pack(side=tk.LEFT, fill=tk.BOTH)

    def bindBtns(self, openProj, openNew, openSettings, openStats):
        ''' Bind buttons and keys to other form events

            Bind enter button and return key to close current form and
            open the next form
            Bind the quit button and form close event to quit the app

            Args:
                nextForm: (Form): The next form to be opened
            '''
        self.addBtn('Start', lambda: (self.close(), openProj()))
        self.addBtn('New', lambda: (self.close(), openNew()))
        self.addBtn('Stats', lambda: (self.close(), openStats()))
        self.addBtn('Settings', lambda: (self.close(), openSettings()))
        self.addBtn('Quit', self.quit)
        self.bindKeys(lambda e: (self.close(), openProj()))


class Timer(object):
    def __init__(self, tData, workTime, shortBreak, longBreak):
        self.tData = tData
        self.workTime = workTime
        self.shortBreak = shortBreak
        self.longBreak = longBreak
        self.state = 'work'
        self.callback = {}

    def addCallback(self, form, callback):
        self.callback[form] = callback

    def open(self):
        if self.state == 'work':
            self.startWork()
        else:
            self.startBreak()

    def close(self):
        if self.state == 'work':
            self.state = 'break'
            self.callback['task']()
        else:
            self.state = 'work'
            self.callback['goal']()

    def runPendingJobs(self):
        try:
            while schedule.jobs:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        self.close()

    def startWork(self):
        schedule.every(self.workTime.get()).seconds.do(schedule.CancelJob)
        self.tData.startSec.set(int(time.time()))
        print('Work Started', self.tData.startSec.get())
        self.runPendingJobs()

    def startBreak(self):
        schedule.every(self.shortBreak.get()).seconds.do(schedule.CancelJob)
        self.runPendingJobs()

    def stopWork(self):
        self.tData.endSec.set(int(time.time()))
        print('Work Stopped', self.tData.endSec.get())
        self.tData.sessions.set(1 + self.tData.sessions.get())
        self.tData.append()


class Controller(object):
    def __init__(self, root):
        self.pom = PomOld()
        self.pomNew = Pom()
        settings = Settings()
        timer = Timer(self.pomNew.timeData, *settings.timer())
        root.iconphoto(True, tk.PhotoImage(file='tomato-1.png'))

        goal = GoalForm(root, self.pomNew.form)
        menu = MenuForm(root)
        stats = StatsForm(root, self.pomNew)
        task = TaskForm(root, self.pomNew.form)
        settings = SettingsForm(root, settings)
        overview = StatsForm(root, self.pomNew)

        openMenu = partial(self.open, menu)
        openProj = partial(self.open, goal, menu)
        openNew = partial(self.open, goal)
        openTimer = partial(self.open, timer)
        openStats = partial(self.open, stats)
        openTask = partial(self.open, task)
        openSettings = partial(self.open, settings)
        openOverview = partial(self.open, overview)

        closeGoal = partial(self.close, goal, menu)
        closeTask = partial(self.close, task, menu)
        closeOverview = partial(self.close, overview, menu)
        closeSettings = partial(self.close, settings, menu)

        timer.addCallback('task', openTask)
        timer.addCallback('goal', openNew)
        task.addCallback(timer.stopWork)

        menu.bindBtns(openProj, openNew, openSettings, openStats)
        goal.bindBtns(cont=openTimer, quit=closeGoal)
        task.bindBtns(cont=openOverview, quit=closeTask)
        overview.bindBtns(cont=openTimer, quit=closeOverview)
        settings.bindBtns(cont=closeSettings, quit=openMenu)
        stats.bindBtns(cont=openProj, quit=openMenu)
        self.open(menu)

    def open(self, form, menu=None):
        ''' Open the next form object

            Open the next form object
            If form is a Menu object populate project list
            If menu parameter is given add active project to Pom

            Args:
                form: (Form): Next form object to open
                menu: (Form): Menu form object. read active project (default: {None})
            '''
        if menu:
            self.pomNew.form.project.set(menu.getActiveProject())
            # print(menu.getActiveProject())
        try:
            [print(x) for x in self.pomNew.projects]
            form.setProjectList(self.pomNew.projects)
        except AttributeError:
            print('No Go')
        form.open()

    def close(self, form, menu=None):
        ''' Manage form close event based off current form

            Store current state of Pom data and write to database
            Close the currently active form and open the menu
            If menu is the current form close the app

            Args:
                form: (Form): Form object that is currently open
                menu: (Form): Menu form object. If None close app (default: {None})
            '''
        form.close()
        if menu:
            # self.pom.save()
            self.pomNew.save()
            self.pomNew.clear()
            self.pomNew.print()
            menu.open()


def main():
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()

    # pom.print()
    # # print(app.summText.get())


if __name__ == '__main__':
    # main()
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
