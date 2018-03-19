import tkinter as tk
import logging


class Row(tk.Frame):
    ''' Row base class to position main widgets

        Row class has a left packed label and can be extended
        with a right packed widget
        Args:
            parent: (Tk): Parent Tk object
            label: (str): Left packed label
        '''

    def __init__(self, parent, label):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab = tk.Label(self, width=15, text=label, anchor='w')
        lab.pack(side=tk.LEFT)


class LabelRow(Row):
    ''' Label row widget with a settable label on the right

        Args:
                parent: (Tk): Parent Tk object
                label: (str): Left side label
                text: (str): Right side label (default: {None})
        '''

    def __init__(self, parent, label, text=None, var=None):
        Row.__init__(self, parent, label)
        self.lab = tk.Label(self, width=10, anchor='w', text=text, textvariable=var)
        self.lab.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)


class EntryRow(Row):
    ''' Entry row widget with an entry box on the right

        Args:
            parent: (Tk): Parent Tk object
            label: (str): Left side label
            var: (StrinkVar): Tk StringVar to store entered text
        '''

    def __init__(self, parent, label, text=None, var=None):
        Row.__init__(self, parent, label)
        self.ent = tk.Entry(self, width=45, textvariable=var)
        self.ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        # self.set(var.get())

    # def set(self, text):
    #     self.ent.delete(0, tk.END)
    #     self.ent.insert(tk.END, text)

    def focus(self):
        '''Set cursor focus on the entry widget'''
        self.ent.focus_set()


class RadioRow(Row):
    ''' Radio button widget with configurable radio buttons

        Args:
            parent: (Tk): Parent Tk object
            label: (str): Left side label
        '''

    def __init__(self, parent, label):
        Row.__init__(self, parent, label)
        self.pack(side=tk.LEFT)

    def add(self, lab, val, var):
        ''' Append addition radio buttons to RadioRow

            Args:
                lab: (str): Left side label
                val: (str): Value when selected
                var: (StringVar): Tk StringVar to store selected value
            '''
        self.rbtn = tk.Radiobutton(self, text=lab, padx=20, variable=var, value=val)
        self.rbtn.pack(anchor=tk.W, side=tk.LEFT)


class TextRow(Row):
    ''' Large text entry widget with custom key bindings from MyText class

        Args:
            parent: (Tk): Parent Tk object
            label: (str): Left side label
            var: (StrinkVar): Tk StringVar to store entered text

        Usage:
            <Enter> : Insert newline at cursor position
            <Tab>   : Insert indentation at cursor position
            <Ctrl-Enter> : Apply top level enter event
            <Ctrl-Tab>   : Switch focus to next widget
        '''

    def __init__(self, parent, label, text=None, var=None):
        Row.__init__(self, parent, label)
        self.ent = MyText(self, width=45, height=10)
        self.ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    def get(self):
        ''' Get the formatted string from the Text widget'''
        return self.ent.get("1.0", 'end-2c')

    def clear(self, data):
        self.ent.delete('1.0', tk.END)

    def focus(self):
        '''Set cursor focus on the Text box widget'''
        self.ent.focus_set()


class MyText(tk.Text):
    ''' Tk Text Widget class with custom key bindings

        Class to over ride Text widget key bindings to simplify test input
        My text also over-rides parent return key bindings

        Usage:
            <Enter> : Insert newline at cursor position
            <Tab>   : Insert indentation at cursor position
            <Ctrl-Enter> : Apply top level enter event
            <Ctrl-Tab>   : Switch focus to next widget
        '''

    def __init__(self, parent, **kw):
        tk.Text.__init__(self, parent, kw)
        self.bind("<Return>", lambda e: self.newline(e))
        self.bind("<Control-Return>", lambda e: self.enter())

    def enter(event):
        '''Over rides <Return> key binding and allows parent binding'''
        pass

    def newline(self, event):
        ''' Insert newline at the cursor and break other actions'''
        self.insert(tk.INSERT, '\n')
        return("break")


class Form(tk.Toplevel):
    '''Tk form base class to simplify form creation

        Form class applies a generic form layout with enter and
        quit buttons

        Attributes:
            formFr (Frame): Main Form Frame
            btnsFr (Frame): Button Frame
            radioFr (Frame): Radio button frame
            rows (dict): dict of form rows
            btns (dict): Dict of form buttons
            width (int):  Form width in pixels
            height (int):  Form height in pixels

        Usage:
            >>>root = tk.Tk()
            >>>root.withdraw()
            >>>f = Form(root)
            >>>f.bindBtns(otherForm.open())
            >>>f.open()
            >>>root.mainloop()
        '''

    def __init__(self, parent):
        '''Form initilizer function

            Set default title and form size
            Initilize frams and element dicts
            Center the form in the screen
            Form closed on initilization

            Args:
                parent: (Tk): Parent Tkinter object
            '''
        tk.Toplevel.__init__(self, parent)
        self.title('Form')
        self.formSize(600, 250)
        self.formFr = tk.Frame(self)
        self.btnsFr = tk.Frame(self)
        self.radioFr = tk.Frame(self.btnsFr)
        self.btns = {}
        self.btns['order'] = []
        self.rows = {}
        self.rows['order'] = []
        self.withdraw()

    def __repr__(self):
        return self.__class__.__name__

    def open(self):
        '''Initilize and open form'''
        self.pack()
        self.center()
        self.update()
        self.deiconify()

    def close(self):
        '''Withdraw current form'''
        self.withdraw()

    def pack(self):
        '''Pack all form frames'''
        self.formFr.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.btnsFr.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.radioFr.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)
        for r in self.rows['order']:
            self.rows[r].pack(side=tk.TOP)
        for b in self.btns['order']:
            self.btns[b].pack(side=tk.RIGHT)

    def bindKeys(self, formControlFunc, quitFunc=None):
        ''' Bind the keyboard keys to control form

            Bind the return and ctrl-return key press event to formControlFunc
            Bind the window close event to quit the app

            Args:
               formControlFunc: (function): App form control function
               quitFunc: (Function): Function that closes current form
                                     returns to a main window (default: {None})
            '''
        if quitFunc:
            self.protocol('WM_DELETE_WINDOW', quitFunc)
        else:
            self.protocol('WM_DELETE_WINDOW', lambda: self.quit())
        self.bind('<Return>', formControlFunc)
        self.bind("<Control-Return>", formControlFunc)

    def bindBtns(self, cont, quit=None):
        ''' Bind buttons and keys to other form events

            Bind enter button and return key to close current form and
            open the next form
            Bind the quit button and form close event to quit the app or
            advance to a pre-close form ie menu

            Args:
                cont: (Form): The next form to be opened
                quit: (Form): Form to open after current
                                  form is quit (default: {None})
            '''
        self.addBtn('Enter', lambda: (self.close(), cont()))
        if quit:
            self.addBtn('Quit', lambda: (self.close(), quit()))
            self.bindKeys(lambda e: (self.close(), cont()),
                          lambda: (quit()))
        else:
            self.addBtn('Quit', self.quit)
            self.bindKeys(lambda e: (self.close(), cont.open()))

    def addRow(self, Row, label, text=None, var=None, frame=None):
        ''' Add row object to form frame and attach Tk var

            Add Row object to form frame.
            Append row to rows dict  attribute using text as the key.
            Row order is stored in rows['order'] list.

            Args:
                Row: (class): tkform Row class
                text: (str): Row label and rows dict key
                var: (Tk Var): Tk variable class: StringVar or IntVar (default: {None})

            Returns:
                # TODO: this is to support old code. Remove this after refactoring
                Returns Row object
                Row Class Object
            '''
        if not frame:
            frame = self.formFr
        row = Row(frame, label, text, var)
        self.rows[label] = row
        self.rows['order'].append(label)
        return row

    def addBtn(self, text, cmd=None):
        ''' Add button object to the button frame with command

            Add button to button frame, append button to btns dict attribute
            using text as the key. Order of buttons is saved by key in
            btns['order'] list
            Args:
                text: (str): Button text and btns dict key
                cmd: (function): Command to execute on button press (default: {None})
            '''
        btn = tk.Button(self.btnsFr, text=text, command=cmd)
        self.btns[text] = btn
        self.btns['order'].append(text)

    def formSize(self, w, h):
        ''' Set the width and height of the form.

            Scale the form based off the width and height args and
            save the args as attributes

            Args:
                w: (int): Form width in pixels
                h: (int): Form height in pixels
            '''
        self.width = w
        self.height = h
        self.geometry('{}x{}'.format(self.width, self.height))

    def center(self):
        ''' Center the form in the screen

            Calculate the center point of the form using width and height
            attributes. Align form center point with screen center point.
            '''
        x = int((self.winfo_screenwidth() - self.width) / 2)
        y = int((self.winfo_screenheight() - self.height) / 2)
        self.geometry("+{}+{}".format(x, y))
