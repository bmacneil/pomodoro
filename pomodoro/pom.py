import tkinter as tk
from collections import namedtuple
from tinydb import *
import time


Attr = namedtuple('Attribute', ['label', 'var'])


class LabeledAttribute(object):
    def __init__(self, label, var):
        self.label = label
        self.var = var

    def set(self, data):
        try:
            self.var.set(data)
        except AttributeError:
            self.var = data

    def get(self):
        try:
            return self.var.get()
        except AttributeError:
            return self.var

    def __iter__(self):
        yield self.label
        yield self.var


class Settings(object):
    def __init__(self, workTime=0, shortBreak=0, longBreak=20):
        self.workTime = LabeledAttribute('Work Time', tk.IntVar(value=workTime))
        self.shortBreak = LabeledAttribute('Short Break', tk.IntVar(value=shortBreak))
        self.longBreak = LabeledAttribute('Long Break', tk.IntVar(value=longBreak))
        self.directory = LabeledAttribute('Directory', tk.StringVar(
            value='/home/brad/Projects/Python/pomodoro/'))

    def __iter__(self):
        yield self.workTime
        yield self.shortBreak
        yield self.longBreak
        yield self.directory

    def print(self):
        [print(l, v.get()) for l, v in self]

    def timer(self):
        return (self.workTime, self.shortBreak, self.longBreak)


class SessionTime(object):
    def __init__(self):
        self.sessions = LabeledAttribute('Sessions', 0)
        self.startSec = LabeledAttribute('Start', 0)
        self.endSec = LabeledAttribute('End', 0)

        self.start = []
        self.end = []

    def print(self):
        [print(l, v) for l, v in vars(self).values()]

    def __iter__(self):
        yield self.sessions
        yield self.startSec
        yield self.endSec

    def clear(self):
        for att in self:
            att.set(0)
        self.start.clear()
        self.end.clear()

    def append(self):
        self.start.append(self.startSec.get())
        self.end.append(self.endSec.get())

    def sec2Days(self, sec):
        return sec // (60 * 60 * 24)

    def sec2HMS(self):
        self.startTime = time.strftime("%H:%M:%S", time.localtime(self.startSec.get()))
        self.endTime = time.strftime("%H:%M:%S", time.localtime(self.endSec.get()))

    def getDuration(self):
        td = self.endSec.get() - self.startSec.get()
        m, s = (td // 60, td % 60)
        h, m = (m // 60, m % 60)
        self.duration = '{0}:{1}:{2}'.format(h, m, s)


class Fields(object):
    def __init__(self):
        keys = [('project', 'Project'),
                ('chalA', 'Challenge:\t    a)'),
                ('chalB', '\t    b)'),
                ('step1', 'Steps:\t    1.'),
                ('step2', '\t    2.'),
                ('step3', '\t    3'),
                ('done', 'Completed'),
                ('todo', 'Todo'),
                ('summ', 'Summary'),
                ('onTask', 'Remained on task'),
                ('type', 'Session Type')]
        self.__dict__ = {k: LabeledAttribute(v, tk.StringVar()) for k, v in keys}

        self.dones = []
        self.todos = []
        self.summs = []
        self.onTasks = []

    def append(self):
        self.dones.append(self.done.get())
        self.todos.append(self.todo.get())
        self.summs.append(self.summ.get())
        self.onTasks.append(self.onTask.get())

        self.done.set('')
        self.todo.set('')
        self.summ.set('')
        self.onTask.set('yes')

    def iterGoals(self):
        yield self.project
        yield self.chalA
        yield self.chalB
        yield self.step1
        yield self.step2
        yield self.step3

    def iterDump(self):
        # yield self.project.get()
        yield [self.chalA.get(), self.chalB.get()]
        yield [self.step1.get(), self.step2.get(), self.step3.get()]
        yield self.type.get()
        yield self.dones
        yield self.todos
        yield self.summs
        yield self.onTasks

    def clear(self):
        for k, v in self.__dict__.items():
            try:
                v.set('')
            except AttributeError:
                v.clear()


class Pom(object):

    def __init__(self, dbDir):
        '''
        Pom object initilizer

        Initilizes a pom object as either a new project or
        as an existing project when the project name is an arg
        Args:
            project: (str): Project name for pom session (default: {None})
        '''

        self.form = Fields()
        self.timeData = SessionTime()

        self.form.type.set('task')
        self.form.onTask.set('yes')

        self.directory = dbDir

        self.db = TinyDB('{0}DB_new.json'.format(self.directory.get()))
        self.updateProjectsList()

    def save(self):
        keys = ['challenge', 'steps', 'type', 'completed', 'todo', 'summary', 'onTask']
        entry = {k: d for d, k in zip(self.form.iterDump(), keys)}
        entry['start'] = self.timeData.start
        entry['end'] = self.timeData.end
        entry['sessions'] = self.timeData.sessions.get()
        if entry['sessions'] > 0 and entry['end'] != []:
            print('Saving Pom state')
            projTB = self.db.table(self.form.project.get())
            projTB.insert(entry)
            self.updateProjectsList()

    def clear(self):
        print('Clearing Pom state')
        self.form.clear()
        self.timeData.clear()
        self.form.type.set('task')
        self.form.onTask.set('yes')

    def updateProjectsList(self):
        self.projects = self.db.tables()

    def stats(self):
        print()

    def print(self):
        print(self.form.project.get())
        [print(x) for x in self.form.iterDump()]
        print('Start', self.timeData.start)
        print('End', self.timeData.end)
