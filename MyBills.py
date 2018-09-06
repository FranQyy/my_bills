from tkinter import *
import shelve
from datetime import *


LARGE_FONT = ('Avenir Next', 14)


class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('MyBills')
        self.geometry('550x350')
        global container
        container = Frame(self)
        container.pack(side=TOP, fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.refresh(container)
        self.show_frame(StartPage)  # let the first page is StartPage

    def refresh(self, c):
        for F in (StartPage, PageOne, PageTwo, PageThree):  # for each page
            frame = F(c, self)  # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0, sticky='NSEW')  # grid it to container


    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()


    def center(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg='#3E4149')

        label = Label(self, text='Welcome to the MyBills 1.0', font=LARGE_FONT)
        label.pack(pady=10, padx=10)  # center alignment
        label = Label(self, text='menu', font=('Avenir Next', 40), bg='#19A56F', fg='#FFFFFF')
        label.pack(pady=10, padx=10, fill=X)

        button1 = Button(self, text='Add', highlightbackground='#3E4149', font=LARGE_FONT, width=20,
                            # when click on this button, call the show_frame method to make PageOne appear
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()
        button2 = Button(self, text='Delete', highlightbackground='#3E4149', font=LARGE_FONT, width=20,
                            # when click on this button, call the show_frame method to make PageOne appear
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        button3 = Button(self, text='Show', highlightbackground='#3E4149', font=LARGE_FONT, width=20,
                            # when click on this button, call the show_frame method to make PageOne appear
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()  # pack it in

        button4 = Button(self, text='Quit', highlightbackground='#3E4149', font=LARGE_FONT, width=20,
                            # when click on this button, call the show_frame method to make PageOne appear
                            command=lambda: app.destroy())
        button4.pack()  # pack it in




class PageOne(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg='#3E4149')

        label = Label(self, text='Adding bills',  bg='#19A56F', fg='#FFFFFF', font='Avenir_Next 22 ')
        label.grid(row=0, columnspan=2, sticky=EW)

        label1 = Label(self, text="Type the bill to pay: ", bg='#3E4149', fg='#FFFFFF')
        label1.grid(row=1, sticky = E, pady=5, padx=7)
        nazwa = Entry(self, width=30)
        nazwa.grid(row=1, column=1)

        label2 = Label(self, text='Type the amount: ', bg='#3E4149', fg='#FFFFFF')
        label2.grid(row=2, sticky = E, pady=5, padx=7)
        kwota = Entry(self, width=30)
        kwota.grid(row=2, column=1)

        label3 = Label(self, text='Type the date d/m/y: ', bg='#3E4149', fg='#FFFFFF')
        label3.grid(row=3, sticky = E, pady=5, padx=7)
        data = Entry(self, width=30)
        data.grid(row=3, column=1)


        Zatwierdz = Button(self, text='Confirm', command=lambda: self.Koniec(nazwa, kwota, data), highlightbackground='#3E4149', font=LARGE_FONT)
        Zatwierdz.grid(row=4, column=1, sticky=E)

        self.grid_rowconfigure(5, minsize=150)

        button1 = Button(self, text='Back to menu', highlightbackground='#3E4149', font=LARGE_FONT,  # likewise StartPage
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=9, column=1, sticky=E)


    def Koniec(self, n, k, d):
        nn = n.get()
        kk = k.get()
        dd = d.get()
        if '/' not in dd:
            canvas = Canvas(self, height=70, width=500, highlightthickness=0)  # highlightthickness=0!!!
            canvas.create_rectangle(0, 0, 500, 70, fill='red', width=0)
            canvas.pack(side=TOP, pady=75)
            canvas.create_text(250,
                               35,
                               text="BAD DATA FORMAT. Program is closing...", font="Avenir_Next")
            canvas.after(3500, lambda: app.destroy())

        else:
            db = shelve.open('databaseMyBills',  writeback=True)
            db[nn] = [kk, dd]
            db.close()
            n.delete(0, END)
            k.delete(0, END)
            d.delete(0, END)

            canvas = Canvas(self, height=70, width=200, highlightthickness=0) #highlightthickness=0!!!
            canvas.create_rectangle(0, 0, 200, 70, fill='chartreuse2', width=0)
            canvas.pack(side=TOP, pady=75)
            canvas.create_text(100,
                          35,
                          text="ADDED", font="Avenir_Next")
            canvas.after(1500, lambda: canvas.destroy())

            n.focus()



class PageTwo(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg='#3E4149')
        self.grid_columnconfigure(0, minsize=170)
        self.grid_columnconfigure(2, minsize=70)

        label = Label(self, text='Deleting bills', font=('Avenir Next', 22), bg='#19A56F', fg='#FFFFFF')
        label.grid(row=1, column=0, columnspan=4, sticky=EW)

        listbox = Listbox(self)
        listbox.grid(row=2, column=1, pady=10)

        db=shelve.open('databaseMyBills', writeback=True)
        for item in db:
            listbox.insert(END, item)
        db.close()
        Zatwierdz = Button(self, text='Confirm', command=lambda: self.koniec(listbox), highlightbackground='#3E4149', font=LARGE_FONT)
        Zatwierdz.grid(row=3, column=1, sticky=E)

        button1 = Button(self, text='Back to menu', highlightbackground='#3E4149', font=LARGE_FONT,  # likewise StartPage
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=4, column=3)

        button1 = Button(self, text='Refresh', highlightbackground='#3E4149', font=LARGE_FONT,
                         # likewise StartPage
                         command=self.odswiez)
        button1.grid(row=4, column=1, sticky=E)

    def koniec(self, lb):
        db=shelve.open('databaseMyBills', writeback=True)
        cs=lb.get(ACTIVE)
        del db[cs]
        lb.delete(ANCHOR)
        db.close()

        canvas = Canvas(self, height=70, width=200, highlightthickness=0)  # highlightthickness=0!!!
        canvas.create_rectangle(0, 0, 200, 70, fill='red', width=0)
        canvas.pack(side=TOP, pady=75)
        canvas.create_text(100,
                           35,
                           text="USUNIĘTO", font="Avenir_Next")
        canvas.after(1500, lambda: canvas.destroy())

    def odswiez(self):
        app.refresh(container)
        app.show_frame(PageTwo)

class PageThree(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg='#3E4149')
        self.grid_columnconfigure(0, minsize=100)
        self.grid_columnconfigure(5, minsize=165)
        self.grid_columnconfigure(1, minsize=100)

        db = shelve.open('databaseMyBills',  writeback=True)
        i = 3
        label = Label(self, text='Things to pay:', font=('Avenir Next', 22), bg='#19A56F', fg='#FFFFFF')
        label.grid(row=0, columnspan=6, sticky=EW, )

        naglowek = Label(self, text='Name', font='Helvetica 18 bold', bg='#3E4149', fg='#FFFFFF')
        naglowek.grid(row=2, column=1, sticky=W)
        naglowek2 = Label(self, text='Amount', font='Helvetica 18 bold', bg='#3E4149', fg='#FFFFFF')
        naglowek2.grid(row=2, column=2, sticky=W)
        naglowek3 = Label(self, text='Date', font='Helvetica 18 bold', bg='#3E4149', fg='#FFFFFF')
        naglowek3.grid(row=2, column=3, sticky=W)
        naglowek3 = Label(self, text='Dates', font='Helvetica 18 bold', bg='#3E4149', fg='#FFFFFF')
        naglowek3.grid(row=2, column=4, sticky=W)


        for item in db.keys():
            label = Label(self, text='{0}'.format(item), bg='#3E4149', fg='#FFFFFF')
            label.grid(row=i, column=1, sticky=W)
            i = i + 1

        i = 3
        for item in db:
            label = Label(self, text='{0}'.format((db[item])[0]), bg='#3E4149', fg='#FFFFFF')
            label.grid(row=i, column=2, sticky=E)
            i = i + 1

        i = 3
        for item in db:
            label = Label(self, text='{0}'.format((db[item])[1]), bg='#3E4149', fg='#FFFFFF')
            label.grid(row=i, column=3, sticky=E)
            i = i + 1

        i = 3

        for item in db:
            today = date.today()
            t=(db[item])[1].rsplit('/')
            x=int(t[0])
            y=int(t[1])
            z=int(t[2])
            if (date(z,y,x)-today).days > 7:
                label = Label(self, text='{0}'.format((date(z,y,x)-today).days), bg='#3E4149', fg='#FFFFFF')
                label.grid(row=i, column=4, sticky=E)
                i = i + 1
            else:
                label = Label(self, text='{0}'.format((date(z, y, x) - today).days), bg='#3E4149', fg='red')
                label.grid(row=i, column=4, sticky=E)
                i = i + 1
        db.close()
        button1 = Button(self, text='Refresh', highlightbackground='#3E4149', font=LARGE_FONT,
                         # likewise StartPage
                         command=self.odswiez)
        button1.grid(row=13, column=3, sticky=W)

        button1 = Button(self, text='Back to menu', highlightbackground='#3E4149', font=LARGE_FONT,  # likewise StartPage
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=13, column=4, columnspan=2, sticky=W)

    def odswiez(self):
        app.refresh(container)
        app.show_frame(PageThree)




app = MainWindow()
app.center()
app.mainloop()