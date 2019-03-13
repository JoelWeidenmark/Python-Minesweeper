"""
MAIN VERISON

Joel Weidenmark
CMETE1
joelwei@kth.se
"""


from tkinter import *
from tkinter.messagebox import showinfo
import pickle
from operator import *
from time import *
import random

class Model:
    """Model handels all calculations """

    def __init__(self, master, name, mines, rows, columns):
        self.name = name
        self.mines = mines
        self.rows = rows
        self.columns = columns
        self.master = master
        self.flag_counter_number = mines
        self.bug_fix = 0
        self.counter = 0
        self.flag_counter = 0
        self.correct_flag = 0
        self.mine_counter = 0
        self.correct_mine = 0
        self.start_time = time()
        self.end_time = 0
        self.game = Toplevel(self.master)
        self.gameGrid = {}
        self.cellStatus = {}
        self.start_game()

    """ Method called when the game starts """
    def start_game(self):
        self.place_mines()
        self.button_values()

    """ Method called in the beginning which places all mines in random cells """
    def place_mines(self):
        for a in range(self.mines):
            x = random.randint(0, self.rows-1)
            y = random.randint(0, self.columns-1)
            while (x, y) in self.gameGrid.keys():
                x = random.randint(0, self.rows-1)
                y = random.randint(0, self.columns-1)
            self.gameGrid[(x, y)] = 'Mine'
            self.cellStatus[(x, y)] = 'Closed'
            VC.build_button(self.master, self, self.game, x, y, '')

    """ Method called after mines are placed that will give all cells appropriate values """
    def button_values(self):
        for x in range(self.rows):
            for y in range(self.columns):
                if (x, y) not in self.gameGrid.keys():
                    self.counter = 0
                    for a in range(3):
                        for b in range(3):
                            if 0 <= (x+a-1) < self.rows and 0 <= (y+b-1) < self.columns:
                                if (x+a-1, y+b-1) in self.gameGrid.keys():
                                    if self.gameGrid[(x+a-1, y+b-1)] == 'Mine':
                                        self.counter += 1
                    self.gameGrid[(x, y)] = self.counter
                    self.cellStatus[(x, y)] = 'Closed'
                    VC.build_button(self.master, self, self.game, x, y, '')

    """ Method called when a button is pressed"""
    def click(self, x, y, leftRight):
        if leftRight == 'left' and self.gameGrid[(x, y)] == 'Mine' and self.bug_fix != 1:
            self.fail()
        else:
            if leftRight == 'left' and (self.cellStatus[(x, y)] == 'Closed' or self.cellStatus[(x, y)] == 'Flagged'):
                if self.cellStatus[(x, y)] == 'Flagged':
                    Model.remove_flag(self, x, y)
                else:
                    if self.gameGrid[(x, y)] == 0:
                        Model.open_empty(self, x, y)
                        Model.victory_open(self)
                    else:
                        Model.open(self, x, y)
                        Model.victory_open(self)
            if leftRight == 'right' and self.cellStatus[(x, y)] == 'Flagged':
                Model.remove_flag(self, x, y)
            elif leftRight == 'right' and (self.cellStatus[(x, y)] == 'Closed' or self.cellStatus[(x, y)] == 'Flagged'):
                Model.flag(self, x, y)
                Model.victory_flags(self)

    """ Method called when a button is to be opened """
    def open(self, x, y):
        if self.gameGrid[(x, y)] == 0:
            VC.build_button(self.master, self, self.game, x, y, self.gameGrid[(x, y)])
            self.cellStatus[(x, y)] = 'Open'
            Model.open_empty(self, x, y)
        else:
            self.cellStatus[(x, y)] = 'Open'
            VC.build_button(self.master, self, self.game, x, y, self.gameGrid[(x, y)])

    """ Method called from Click to place a flag """
    def flag(self, x, y):
        value = '?'
        self.cellStatus[(x, y)] = 'Flagged'
        self.flag_counter_number = self.flag_counter_number - 1
        VC.build_button(self.master, self, self.game, x, y, value)

    """ Method called from Click to remove a flag """
    def remove_flag(self, x, y):
        self.cellStatus[(x, y)] = 'Closed'
        self.flag_counter_number = self.flag_counter_number + 1
        VC.build_button(self.master, self, self.game, x, y, '')


    """ Method that opens all surrounding empty cells if an empty cell is pressed """
    def open_empty(self, x, y):
        VC.build_button(self.master, self, self.game, x, y, self.gameGrid[(x, y)])
        self.cellStatus[(x, y)] = 'Open'
        for a in range(3):
            for b in range(3):
                if 0 <= (x+a-1) < self.rows and 0 <= (y+b-1) < self.columns:
                    if self.cellStatus[(x+a-1, y+b-1)] == 'Closed':
                        Model.open(self, x+a-1, y+b-1)

    """ Method that checks if the player has won through opening all cells """
    def victory_open(self):
        self.mine_counter = 0
        self.correct_mine = 0
        for x in range(self.rows):
            for y in range(self.columns):
                if self.cellStatus[(x, y)] == 'Closed':
                    self.mine_counter += 1
        for x in range(self.rows):
            for y in range(self.columns):
                if self.gameGrid[(x, y)] == 'Mine':
                    self.correct_mine += 1
                    if self.mine_counter == self.mines == self.correct_mine:
                        for x in range(self.rows):
                            for y in range(self.columns):
                                self.open(x, y)
                        showinfo('You Won!', 'You won by not clicking on any mines in the field')
                        self.master.grab_set()
                        self.end_time = time()
                        self.calculate_score()
        return False

    """ Method that checks if the player has flagged all mines"""
    def victory_flags(self):
        self.flag_counter = 0
        self.correct_flag = 0
        for x in range(self.rows):
            for y in range(self.columns):
                if self.cellStatus[(x, y)] == 'Flagged':
                    self.flag_counter += 1
        for x in range(self.rows):
            for y in range(self.columns):
                if self.cellStatus[(x, y)] == 'Flagged' and self.gameGrid[(x, y)] == 'Mine':
                    self.correct_flag += 1
                    if self.flag_counter == self.correct_flag == self.mines:
                        for x in range(self.rows):
                            for y in range(self.columns):
                                if self.cellStatus[(x, y)] != 'Flagged':
                                    self.open(x, y)
                        self.bug_fix = 1
                        showinfo('You Won!', 'You won by flagging all mines in the field')
                        self.master.grab_set()
                        self.end_time = time()
                        self.calculate_score()
        return False

    """ Method called when a mine is pressed. The game will end"""
    def fail(self):
        for x in range(self.rows):
            for y in range(self.columns):
                self.open(x, y)
        showinfo('You lost!', 'You have clicked on a mine and lost the game')
        self.game.destroy()
        self.master.deiconify()

    """ Method called when the player wins to calculate the score """
    def calculate_score(self):
        time = self.end_time - self.start_time
        self.score = int((self.mines * self.rows * self.columns * 100)/time)
        Model.highscore(self)

    """ Method called to create a highscore file and sort it """
    def highscore(self):
        try:
            file = open('highscore.txt', 'rb')
            score_list = pickle.load(file)
            file.close()
        except FileNotFoundError:
            file = open('highscore.txt', 'w+')
            file = open('highscore.txt', 'rb')
            score_list = []
            file.close()
        score_list.append((self.name, self.score))
        score_list = sorted(score_list, key=itemgetter(1), reverse=True)[:10]
        file = open('highscore.txt', 'wb')
        pickle.dump(score_list, file)
        file.close()
        VC.show_highscore(self.master, self)

class VC():
    """ VC handels all graphic content (VC = ViewControl) """

    def __init__(self, master):
        self.master = master
        self.window = Frame(self.master)
        self.window.pack()
        VC.menu_field(self)
        VC.menu_buttons(self)

    """ Method called in the beginning to set out all menu text-boxes """
    def menu_field(self):
        self.label = Label(self.window, text='Choose number of rows, columns and mines!', height=2, width=45)
        self.label.pack()
        boxWindow = Frame(self.window)
        boxWindow.pack()
        self.entryName = Entry(boxWindow, width=20)
        self.entryName.insert(0, 'Enter your name')
        self.entryName.pack()
        self.labelMines = Label(boxWindow, text='Mines')
        self.labelMines.pack()
        self.boxMines = Spinbox(boxWindow, width=10, from_=1, to=500)
        self.boxMines.pack()
        self.labelRows = Label(boxWindow, text='Rows')
        self.labelRows.pack()
        self.boxRows = Spinbox(boxWindow, width=10, from_=1, to=500)
        self.boxRows.pack()
        self.labelColumns = Label(boxWindow, text='Columns')
        self.labelColumns.pack()
        self.boxColumns = Spinbox(boxWindow, width=10, from_=1, to=500)
        self.boxColumns.pack()


    """ Method called to add all buttons in the menu """
    def menu_buttons(self):
        self.buttonWindow = Frame(self.window)
        self.buttonWindow.pack()
        self.errorInput = Label(self.buttonWindow)
        self.errorInput.pack(side=BOTTOM)
        self.buttonPlay = Button(text='Play', height=2, command=self.send_values)
        self.buttonPlay.pack()
        self.buttonQuit = Button(text='Quit', height=2, command=self.master.destroy)
        self.buttonQuit.pack()

    """ Method that checks all values before sending them to Model """
    def send_values(self):
        try:
            name = self.entryName.get()
            if self.boxRows.get().isdigit() and 1 <= int(self.boxRows.get()) <= 10:
                self.boxRows.configure(fg="black")
                rows = int(self.boxRows.get())
            else:
                self.boxRows.configure(fg="red")

            if self.boxColumns.get().isdigit() and 1 <= int(self.boxColumns.get()) <= 10:
                self.boxColumns.configure(fg="black")
                columns = int(self.boxColumns.get())
            else:
                self.boxColumns.configure(fg="red")
            if self.boxMines.get().isdigit():
                self.boxMines.configure(fg="black")
            else:
                self.boxMines.configure(fg="red")
            if 0 < int(self.boxMines.get()) < int(self.boxRows.get()) * int(self.boxColumns.get()):
                self.boxMines.configure(fg="black")
                mines = int(self.boxMines.get())
            else:
                self.boxMines.configure(fg="red")

            Model(self.master, name, mines, rows, columns)
            self.master.withdraw()

        except (UnboundLocalError, ValueError):
            self.errorInput.configure(text='You can only use numbers to define Mines, Rows and Columns \n '
                                           'The maximum amount of rows and columns is 10 \n '
                                           'You cannot have a field with only mines')

    """ Method called when a button is to be built """
    def build_button(self, obj, frame, x, y, value):
        if value == '':
            cell = Label(frame, text=value, height=2, width=3, bg='white', relief=RAISED)
        elif value == 'Mine':
            cell = Label(frame, text='*', height=2, width=3, bg='black', fg='red', relief=SUNKEN)
        elif value == 0:
            cell = Label(frame, text='', height=2, width=3, bg='grey', relief=SUNKEN)
        else:
            cell = Label(frame, text=value, height=2, width=3, bg='white', relief=SUNKEN)
        cell.grid(row=x, column=y)
        cell.bind('<Button-2>', lambda event: Model.click(obj, x, y, 'right'))
        cell.bind('<Button-1>', lambda event: Model.click(obj, x, y, 'left'))
        flag_counter_label = Label(frame, text=obj.flag_counter_number, height=2, width=3)
        flag_counter_label.grid(row=obj.rows+1, column=0)

    """ Method called to show the highscore after a successful run """
    def show_highscore(self, obj):
        self.highscore_window = Toplevel(self.master)
        obj.game.destroy()
        self.highscore_label = Label(self.highscore_window, text='Highscores', height=2, width=40)
        self.highscore_label.pack()
        self.my_score = Label(self.highscore_window, text=('Your score: ' + obj.name + ' - ' + str(obj.score)), height = 3)
        self.my_score.pack()
        file = open('highscore.txt', 'rb')
        score_list = pickle.load(file)
        score_list_size = len(score_list)
        for a in range(score_list_size):
            score_row = str(score_list[a])
            score_row = score_row.replace("',", ' - ')
            self.score = Label(self.highscore_window, text=(a+1, score_row))
            self.score.pack()
        file.close()
        obj.master.grab_release()
        obj.master.deiconify()

""" Function that starts the game """
def main():
    root = Tk()
    root.title('Minesweeper')
    program = VC(root)
    root.mainloop()


if __name__ == '__main__':
    main()