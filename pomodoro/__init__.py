# ! /usr/bin/python3
from tinydb import *
from pomodoro.tkform import *
from pomodoro.pom import *
import time
from functools import partial
import schedule
import tkinter as tk
import logging
import argparse


logging.basicConfig(level=logging.WARNING,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--debug', action='store_true', default=False, dest='debug',
                help='Add a new project page or blog page.')
ap.add_argument('-i', '--info', action='store_true', default=False, dest='info',
                help='Update page contents. Enter [all] to update all pages')
args = ap.parse_args()


class GoalForm(Form):
    """docstring for ClassName"""

    def __init__(self, parent, pom):
        Form.__init__(self, parent)
        self.title('Pomodoro')
        self.make(pom)
        self.withdraw()
        self.focus = partial(self.getFocus, pom)

    def make(self, pom):
        for attr in pom.iterGoals():
            self.addRow(EntryRow, attr.label, var=attr.var)

        typeRb = RadioRow(self.btnsFr, pom.type.label)
        typeRb.add('Task', 'task', pom.type.var)
        typeRb.add('Learn', 'learn', pom.type.var)

    def getFocus(self, pom):
        if pom.project.get() == '':
            self.rows[pom.project.label].focus()
        else:
            self.rows[pom.chalA.label].focus()

    def open(self):
        '''Initilize and open form'''
        self.focus()
        self.pack()
        self.center()
        self.update()
        self.deiconify()


class TaskForm(Form):
    """docstring for ClassName"""

    def __init__(self, parent, pom):
        self.pom = pom
        # self.openFrame = partial(self.setFrame, newPom.type.var)
        Form.__init__(self, parent)
        self.title('Pomodoro - Task')
        self.make(pom)

    def make(self, pom):

        for attr in pom.iterGoals():
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

    def setFrame(self):
        self.setLabels()
        if self.pom.type.get() == 'learn':
            self.learnFr.pack(side=tk.TOP, fill=tk.X, pady=5)
            self.taskFr.pack_forget()
            self.rows['Summary'].focus()
            self.formSize(600, 400)
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
        logging.debug('TaskForm.close(): Timer Callback called')
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
        pom.timeData.sec2HMS()
        pom.timeData.getDuration()
        self.addRow(LabelRow, 'Project:', var=pom.form.project.var)
        self.addRow(LabelRow, 'Sessions:', var=pom.timeData.sessions)
        self.addRow(LabelRow, 'Start Time:', text=pom.timeData.startTime)
        self.addRow(LabelRow, 'End Time:', text=pom.timeData.endTime)
        self.addRow(LabelRow, 'Duration:', text=pom.timeData.duration)


class MenuForm(Form):
    ''' Main menu form of Pom app with a project list loaded from db

        [description]
        '''

    def __init__(self, parent, projects=None):
        Form.__init__(self, parent)
        self.title('Pomodoro - Menu')
        self.formSize(300, 300)
        self.make()
        self.withdraw()

    def getActiveProject(self):
        return self.mylist.get(tk.ACTIVE)

    def setProjectList(self, projects):
        self.mylist.delete(0, tk.END)
        for p in projects:
            self.mylist.insert(tk.END, p)

    def addCallback(self, callback):
        self.timerCallback = callback

    def open(self):
        self.timerCallback()
        super().open()

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
    ''' Tracks and records the work and break duration for each Pom

        Starts a time for both work time and break time using the args for duration
        Records the data in a SessionTime object
        Manintains a state of the next timer session type

        Args:
            tData: (SessionTime): SessionTime object to record start and end time
            workTime: (LabeledAttribute): work duration setting
            shortBreak: (LabeledAttribute): short break duration setting
            longBreak: (LabeledAttribute): long break duration setting
            state:  (String): next timer session type (default: {'work'})
        '''

    def __init__(self, tData, workTime, shortBreak, longBreak):
        self.tData = tData
        self.workTime = workTime
        self.shortBreak = shortBreak
        self.longBreak = longBreak
        self.state = 'work'
        self.callback = {}

    def __repr__(self):
        ''' Return: Class name '''
        return self.__class__.__name__

    def resetState(self):
        ''' Reset the timer session type to 'work' '''
        self.state = 'work'

    def addCallback(self, form, callback):
        ''' Add a function to the callback dict using form name as the key '''
        self.callback[form] = callback

    def open(self):
        ''' Open the timer and start a session based on state '''
        if self.state == 'work':
            self.startWork()
        else:
            self.startBreak()

    def close(self):
        ''' Closer the timer and open the next form determined by state '''
        if self.state == 'work':
            self.state = 'break'
            self.callback['task']()
        else:
            self.state = 'work'
            self.callback['goal']()

    def runTimer(self):
        ''' Activate timer. Deactivate with Ctrl-C '''
        try:
            while schedule.jobs:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        self.close()

    def startWork(self):
        ''' Load timer with work duration and run timer, save start time '''
        self.tData.startSec.set(int(time.time()))
        schedule.every(self.workTime.get()).minutes.do(schedule.CancelJob)
        logging.info('Timer.startWork(): startSec {0}'.format(self.tData.startSec.get()))
        self.runTimer()

    def startBreak(self):
        ''' Load timer with break duration and run timer '''
        schedule.every(self.shortBreak.get()).minutes.do(schedule.CancelJob)
        logging.info('Timer.startBreak(): shortBreak')
        self.runTimer()

    def stopWork(self):
        ''' Callback function to stop timer, save end time and append tData to Pom '''
        self.tData.endSec.set(int(time.time()))
        logging.info('Timer.stopWork(): endSec {0}'.format(self.tData.endSec.get()))
        self.tData.sessions.set(1 + self.tData.sessions.get())
        self.tData.append()


class Controller(object):
    def __init__(self, root):
        settings = Settings()
        self.pom = Pom(settings.directory)
        timer = Timer(self.pom.timeData, *settings.timer())
        root.iconphoto(True, tk.PhotoImage(
            file='/home/brad/Projects/Python/pomodoro/pomodoro/tomato.png'))

        goal = GoalForm(root, self.pom.form)
        menu = MenuForm(root)
        stats = StatsForm(root, self.pom)
        task = TaskForm(root, self.pom.form)
        settings = SettingsForm(root, settings)
        overview = StatsForm(root, self.pom)

        openMenu = partial(self.open, menu)
        openProj = partial(self.open, goal, menu)
        openNew = partial(self.open, goal)
        openTimer = partial(self.open, timer)
        openStats = partial(self.open, stats)
        openTask = partial(self.open, task)
        openSettings = partial(self.open, settings)
        openOverview = partial(self.open, overview)

        closeGoal = partial(self.close, goal, openMenu)
        closeTask = partial(self.close, task, openMenu)
        closeOverview = partial(self.close, overview, openMenu)
        closeSettings = partial(self.close, settings, openMenu)

        timer.addCallback('task', openTask)
        timer.addCallback('goal', openNew)
        task.addCallback(timer.stopWork)
        menu.addCallback(timer.resetState)

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
        logging.debug('open(): form: {0} menu: {1}'.format(repr(form), menu))
        if repr(form) == 'Timer':
            logging.debug('Timer State - {0}'.format(form.state))
        if menu:
            menu.setProjectList(self.pom.projects)
            self.pom.form.project.set(menu.getActiveProject())
        try:
            form.setProjectList(self.pom.projects)
        except AttributeError:
            pass
        form.open()

    def close(self, form, menu=None):
        ''' Manage form close event based off current form

            Store current state of Pom data and write to database
            Close the currently active form and open the menu
            If menu is the current form close the app

            Args:
                form: (Form): Form object that is currentlcloseTasky open
                menu: (Form): Menu form object. If None close app (default: {None})
            '''
        logging.debug('close(): form: {0} menu: {1}'.format(repr(form), menu.__class__.__name__))
        form.close()
        if menu:
            self.pom.save()
            self.pom.clear()
            menu()


def main():
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    if args.debug:
        print('[DEBUG] - Opening Pomodoro')
        logging.getLogger().setLevel(logging.DEBUG)
        app.pom.dbFile = 'DB_test.json'
        app.pom.openDB()
        print('Using: {}'.format(app.pom.dbFile))
    elif args.info:
        print('[INFO] - Opening Pomodoro')
        logging.getLogger().setLevel(logging.INFO)
    else:
        print("Opening Pomodoro")

    logging.info('INFO messages on')
    logging.debug('DEBUG messages on')
    root.mainloop()


if __name__ == '__main__':
    main()
