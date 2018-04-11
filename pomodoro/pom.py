import tkinter as tk
from collections import namedtuple
from tinydb import *
import time
import logging
import os
import sys


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
    def __init__(self, workTime=25, shortBreak=5, longBreak=20):
        path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.workTime = LabeledAttribute('Work Time', tk.IntVar(value=workTime))
        self.shortBreak = LabeledAttribute('Short Break', tk.IntVar(value=shortBreak))
        self.longBreak = LabeledAttribute('Long Break', tk.IntVar(value=longBreak))
        self.directory = LabeledAttribute('Directory', tk.StringVar(value=path))

        if os.path.isfile(os.path.join(path, 'settings.json')):
            tdb = TinyDB('{0}'.format(os.path.join(path, 'settings.json'))
                         ).table().get(doc_id=1)
            self.workTime.set(tdb['workTime'])
            self.shortBreak.set(tdb['shortBreak'])
            self.longBreak.set(tdb['longBreak'])
            self.directory.set(tdb['directory'])
        else:
            tdb = TinyDB('{0}'.format(os.path.join(path, 'settings.json')))
            print(path)
            logging.debug(os.path.join(path, 'settings.json'))
            logging.info({l: v.get() for l, v in vars(self).items()})
            tdb.insert({l: v.get() for l, v in vars(self).items()})

    def __iter__(self):
        yield self.workTime
        yield self.shortBreak
        yield self.longBreak
        yield self.directory

    def timer(self):
        return (self.workTime, self.shortBreak, self.longBreak)


class SessionTime(object):
    def __init__(self):
        self.sessions = LabeledAttribute('Sessions', 0)
        self.startSec = LabeledAttribute('Start', 0)
        self.endSec = LabeledAttribute('End', 0)

        self.start = []
        self.end = []

    # def print(self):
    #     [print(l, v) for l, v in vars(self).values()]

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
        self.duration = '{0}:{1:02d}:{2:02d}'.format(h, m, s)

    def formatDate(self, sec):
        return time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(sec))


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
        self.dbFile = 'DB.json'
        self.openDB()
        self.updateProjectsList()

    def openDB(self):
        logging.info('Opening DB {}'.format(self.dbFile))
        self.db = TinyDB('{0}'.format(os.path.join(self.directory.get(), self.dbFile)))

    def save(self):
        keys = ['challenge', 'steps', 'type', 'completed', 'todo', 'summary', 'onTask']
        entry = {k: d for d, k in zip(self.form.iterDump(), keys)}
        entry['start'] = self.timeData.start
        entry['end'] = self.timeData.end
        entry['sessions'] = self.timeData.sessions.get()
        if entry['sessions'] > 0 and entry['end'] != []:
            print('Saving Pom state')
            logging.info(self.logString())

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

    # def stats(self):
        # print()

    # def print(self):
    #     print(self.form.project.get())
    #     [print(x) for x in self.form.iterDump()]
    #     print('Start: {}'.format(self.timeData.start))
    #     print('End: {}'.format(self.timeData.end))

    def logString(self):
        string = '\n'.join([x.get() for x in self.form.iterGoals()])

        string += '\n' + '{}'.format(self.form.dones)
        string += '\n' + '{}'.format(self.form.todos)
        string += '\n' + '{}'.format(self.form.summs)
        string += '\n' + '{}'.format(self.form.onTasks)

        string += '\n' + 'Start: {}'.format(self.timeData.start)
        string += '\n' + 'End: {}'.format(self.timeData.end)
        return string
