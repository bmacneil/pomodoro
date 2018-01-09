#! /usr/bin/python3

from tkinter import *


class Form(object):
    """docstring for ClassName"""

    def __init__(self):
        self.company = ''
        self.jobTitle = ''
        self.location = ''
        self.address = ''
        self.makeform()

    def fetch(self, entries, root):
        print(type(root))
        print(type(entries))
        for entry in entries:
            if entry[0] == 'Company Name':
                print("\n**************************")
                self.company = entry[1].get()
                print(self.company)
            elif entry[0] == 'Job Title':
                self.jobTitle = entry[1].get()
                print(self.jobTitle)
            elif entry[0] == 'Location':
                self.location = entry[1].get()
                print(self.location)
            elif entry[0] == 'Address (st #, City, Prov PC)':
                add = entry[1].get().split(',', 1)
                self.address = [a.lstrip() for a in add]
                print(self.address)
            else:
                print("\nFORM FETCH ERROR\n")
        root.destroy()

    def openLink(self):
        if self.link == "LINK":
            print("No Link Available")
        else:
            # Open a new webpage for each link
            print(self.link)
            # Add escape characters to the link to avoid issues with cmd line
            safelink = self.link.replace('&', '\&').replace('(', '\(').replace(')', '\)')
            subprocess.call("google-chrome --incognito {0}".format(safelink), shell=True)
            # subprocess.call("netsurf {0}".format(safelink), shell=True)
            # webbrowser.open(self.link, new=2, autoraise=True)

    def removeJob(self, root):
        self.company = "REMOVED"
        self.jobTitle = "REMOVED"
        self.location = "REMOVED"
        self.address = ["REMOVED", "REMOVED"]
        self.link = "REMOVED"
        self.path = "REMOVED"
        print("Job Removed")
        root.destroy()

    def makeform(self):
        fields = ['Project', 'a)', 'b)', '1.', '2.', '3.']
        text = [self.project, self.challenge[0], self.challenge[1], self.steps[0], self.steps[1], self.steps[2], self.address]
        root = Tk()
        entries = []
        for f, t in zip(fields, text):
            row = Frame(root)
            lab = Label(row, width=25, text=f, anchor='w')
            ent = Entry(row)
            ent.insert(END, t)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((f, ent))

        ents = entries
        ents[0][1].focus_set()
        root.bind('<Return>', (lambda evnet, e=ents: self.fetch(e, root)))
        # Button to open posting link
        b2 = Button(root, text='Link', command=self.openLink)
        b2.pack(side=LEFT, padx=5, pady=5)
        # Button to close window
        b3 = Button(root, text='Quit', command=root.quit)
        b3.pack(side=LEFT, padx=5, pady=5)
        # Button to enter info. Same as return key
        b1 = Button(root, text='Enter', command=(
            lambda e=ents: self.fetch(e, root)))
        b1.pack(side=RIGHT, padx=5, pady=5)
        # Button to remove jobs
        rmvjob = Button(
            root, text='Remove', command=lambda r=root: self.removeJob(root))
        rmvjob.pack(side=LEFT, padx=5, pady=5)
        root.mainloop()


f = Form()
