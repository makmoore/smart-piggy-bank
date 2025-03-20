#####################################################################################################################
# NAMES: Makenzie Moore and Hallie Burgess
# DATE: 4/25/2024
# PROJECT NAME: Smart Piggy Bank
# DESCRIPTION: This is a GUI for the Smart Piggy Bank financial tracker system. This product is geared towards children
# with the goal of teaching financial literacy & establishing healthy financial habits using the 3 Jar System.
#####################################################################################################################

from tkinter import *  # tkinter library for GUI
import tkinter.messagebox  # for displaying message boxes
from tkinter.ttk import *  # for styling buttons
from tkinter import scrolledtext  # for creating a scrollable text box
import os.path  # to manage files

DISPLAY = True  # this is to turn the use of display off & on. Set False to test GUI with a laptop (no LCD display)
if DISPLAY:  # if the system is hooked up to the LCD display
    from rpi_lcd import LCD  # imports library to use the LCD


if DISPLAY:  # if LCD is set up
    lcd = LCD()  # it initializes the LCD display
    lcd.clear()  # clears LCD


# the class that manages the GUI program
class GUI(Frame):
    # the constructor for the GUI
    def __init__(self, master, tot, goal):
        Frame.__init__(self, master)
        self.master = master
        self.total = tot  # initialize variable to keep track of the total balance
        self.goal = goal  # initialize variable to track the current savings goal

    # set up the structure and format of the main window.
    def setupGUI(self):
        # these were all used for resizing purposes since sizing on the pi was tricky & this was a quick way to adjust
        dollar = 4  # this is the row location for all dollar buttons, here for easy adjustment of the whole row
        cent = dollar+1  # the same as the above but the row for all cent buttons right bellow it
        pad_y = 33  # 15 # this is the vertical padding for all dollar and cent buttons
        bottom_buttons = cent+4  # this is for the row the bottom buttons are on (Save, Clear, Cancel, etc)
        # bellow are all different font sizes
        title_font= 40
        balance_font = 25
        check_font = 23
        self.button_font = 20
        history_font = 18

        # welcome message/title at the top
        l1 = Label(self.master, text="Welcome to the Smart Piggy Bank!", font=('Georgia', title_font, 'bold'))
        l1.grid(row=0, column=0, sticky=N+S+E+W, columnspan=5, padx=150, pady=20)

        # displays the current balance in the piggy bank
        l2 = Label(self.master, text="Current Balance:", font=('calibri', balance_font, 'bold'))
        l2.grid(row=1, column=1, sticky=E, columnspan=2, pady=30, padx=30)
        # the numbers for the current balance (different formatting so separate)
        l3 = Label(self.master, text="${:0.2f}".format(total_bal), font=('calibri', balance_font, 'bold'),
                   background="lightgrey")
        l3.grid(row=1, column=3, sticky=W)

        # set up radiobuttons for deposits/withdrawals
        style1 = Style() # this sets the style/format for both (and next line too)
        style1.configure('TRadiobutton', font=('calibri', check_font), foreground="black")
        self.check = StringVar(self.master, "1")  # checks for individual buttons
        # button 1: deposit
        check1 = Radiobutton(self.master, text="Deposit", variable=self.check, value="1")
        check1.grid(row=2, column=2, columnspan=2, sticky=W, pady=10, padx=80)
        # button 2: withdraw
        check2 = Radiobutton(self.master, text="Withdraw", variable=self.check, value="2")
        check2.grid(row=3, column=2, columnspan=2, sticky=W, pady=18, padx=80)
        # these are checked in the function buttonpress() to know whether to add or subtract

        # this is the style for the dollar buttons and coin buttons
        # they're the same right now but can be changed for style purposes
        style = Style()
        style.configure('Dollar.TButton', font=('calibri', self.button_font, 'bold'), foreground='black')
        coin_style = Style()
        coin_style.configure('Coin.TButton', font=('calibri', self.button_font, 'bold'), foreground='black')

        # the buttons for using dollar values
        b1 = Button(self.master, text="$1", style="Dollar.TButton", command=lambda: self.buttonpress(1))
                # command tells what to do when method is activated  ^^^  lambda allows adding an argument
        b1.grid(row=dollar, column=0, pady=pad_y) # only first button needs to be padded and the whole row will be

        b2 = Button(self.master, text="$5", style="Dollar.TButton", command=lambda: self.buttonpress(5))
        b2.grid(row=dollar, column=1)

        b3 = Button(self.master, text="$10", style="Dollar.TButton", command=lambda: self.buttonpress(10))
        b3.grid(row=dollar, column=2)

        b4 = Button(self.master, text="$20", style="Dollar.TButton", command=lambda: self.buttonpress(20))
        b4.grid(row=dollar, column=3)

        b5 = Button(self.master, text="$50", style="Dollar.TButton", command=lambda: self.buttonpress(50))
        b5.grid(row=dollar, column=4)

        # the buttons for adding coin values
        c1 = Button(self.master, text="$0.01", style="Coin.TButton", command=lambda: self.buttonpress(0.01))
        c1.grid(row=cent, column=0, pady=pad_y)

        c2 = Button(self.master, text="$0.05", style="Coin.TButton", command=lambda: self.buttonpress(0.05))
        c2.grid(row=cent, column=1)

        c3 = Button(self.master, text="$0.10", style="Coin.TButton", command=lambda: self.buttonpress(0.10))
        c3.grid(row=cent, column=2)

        c4 = Button(self.master, text="$0.25", style="Coin.TButton", command=lambda: self.buttonpress(0.25))
        c4.grid(row=cent, column=3)

        c5 = Button(self.master, text="$0.50", style="Coin.TButton", command=lambda: self.buttonpress(0.50))
        c5.grid(row=cent, column=4)

        # this displays the new balance to track changes
        l4 = Label(self.master, text="New Balance:    ", font=('calibri', balance_font, 'bold'))
        l4.grid(row=cent+1, column=2, sticky=E, columnspan=1, pady=50)
        self.l5 = Label(self.master, text="${:0.2f}".format(self.total), font=('calibri', balance_font, 'bold'),
                        background="lightgrey")
        self.l5.grid(row=cent+1, column=3, sticky=W)

        # this is the button to cancel without saving/making changes
        cancel_style = Style()
        cancel_style.configure('Cancel.TButton', font=('calibri', self.button_font), foreground='black')
        b6 = Button(self.master, text="Cancel", style="Cancel.TButton", command=self.cancelbutton)
        b6.grid(row=bottom_buttons, column=3)

        # this is the button to save changes made before quitting
        save_style = Style()
        save_style.configure('Save.TButton', font=('calibri', self.button_font, "bold"), foreground='black')
        b7 = Button(self.master, text="Save", style="Save.TButton", command=self.savebutton)
        b7.grid(row=bottom_buttons, column=4, pady=15)

        # this is the clear button to clear changes but keep working (in case of mistakes)
        clear_style = Style()
        clear_style.configure('Clear.TButton', font=('calibri', self.button_font), foreground="grey",
                              background='lightgrey')
        b8 = Button(self.master, text="Clear", style="Clear.TButton", command=self.clearbutton)
        b8.grid(row=bottom_buttons, column=2)

        # this is the button to open the window for budget information
        open_budget = Button(self.master, text="Budget", style="Cancel.TButton", command=lambda: self.open_window2())
        open_budget.grid(row=bottom_buttons, column=0)

        # this creates a scrollable text box to keep a running history of changes
        self.text = "This keeps track of \nthe changes you make!\n\n" + "+/-" + "\tBalance\n" + "-----\t-----------"
        self.text += "\n\t${:0.2f}\n".format(total_bal)
        self.history = scrolledtext.ScrolledText(self.master, height=27, width=20)
        self.history.place(x=1230, y=0)
        self.history.insert(END, self.text)
        self.history.configure(font=("Calibri", history_font))
        self.history.configure(state='disabled')  # disables it after the value is set to disallow users to edit

        ## this was temporary for testing a dollar box that you could enter any amount (decided to take this out but
        ## still works if you uncomment these lines)
        #input_dollar = Button(self.master, text="Dollar", style="Cancel.TButton", command=lambda: self.dollarwindow())
        #input_dollar.grid(row=bottom_buttons, column=1)

        ##########################################################################

    # calculates changes in the value when dollar/coin buttons are pushed on GUI
    def buttonpress(self, val):
        # this is for adding/depositing to the total
        if self.check.get() == "1":  # checks for radiobutton 1: deposit
            self.total += val  # adds the value
            self.l5["text"] = "${:0.2f}".format(self.total)  # displays the new balance
            if DISPLAY:  # updates LCD if it is being used
                lcd.text("Deposited ${:0.2f}".format(val), 1)
            if self.total > 0:
                self.l5["foreground"] = "green"  # if the balance is positive, the text is green
                self.l5["background"] = "lightgreen"
            # updates the text in the history box to the left
            self.text = "+ ${:0.2f}\n".format(val)
            self.text += "\t${:0.2f}\n".format(self.total)

            if DEBUG:
                print("Deposit button is checked")
                print(f"\t+ ${val}")
                print("New balance: ${:0.2f}".format(self.total))

        # this is for subtracting/withdrawing from the total
        elif self.check.get() == "2":  # checks for radiobutton 2: withdraw
            self.total -= val  # subtracts the value
            self.l5["text"] = "${:0.2f}".format(self.total)  # changes the new balance
            if DISPLAY:  # updates LCD if needed
                lcd.text("Withdrew ${:0.2f}".format(val), 1)
            if self.total < 0:  # if the total is negative, the text is red (cause that's bad)
                self.l5["foreground"] = "red"
                self.l5["background"] = "lightpink"
                tkinter.messagebox.showwarning("Warning", "You don't have that much money!")
            # updates text for history
            self.text = "- ${:0.2f}\n".format(val)
            self.text += "\t${:0.2f}\n".format(self.total)

            if DEBUG:
                print("Withdraw button is checked")
                print(f"\t- ${val}")
                print("New balance: ${:0.2f}".format(self.total))

        else:  # this isn't so much for radiobuttons, it was originally check boxes so this was here
            tkinter.messagebox.showinfo("Warning", "Please select one of the check boxes")
            if DEBUG:
                print("Warning: Check box error")

        # updates the entire new total after on the LCD
        if DISPLAY:
            lcd.text("Total: ${:0.2f}".format(self.total), 2)

        # updates the running history
        self.history['state'] = "normal"  # to open the text box "history" to edit
        self.history.insert(END, self.text)  # displays the new text
        self.history['state'] = "disabled"  # closes the text box so the user can't type in it
        #############


    # executes if the clear button is pressed
    def clearbutton(self):
        isYes = tkinter.messagebox.askokcancel("Clear New Balance?", "You entered ${:0.2f}. \nAre you sure you want "
                                               "to clear it?\nThis action can't be undone.".format(self.total))
        if isYes:  # checks if the user wants to clear ^^
            self.total = initialize_bal()  # reverts the total to the original before changes
            self.l5["text"] = "${:0.2f}".format(self.total)  # changes the displayed total
            self.l5["foreground"] = "black"  # changes font color to black again

            if DISPLAY:  # resets the display
                lcd.text("Total: ${:0.2f}".format(self.total), 2)
                lcd.text("Total cleared", 1)

            # clears the history and resets it
            self.history['state'] = "normal"
            self.history.delete(1.0, END)
            self.text = ("This keeps track of \nthe changes you make!\n\n" + "+/-" + "\tBalance\n"
                         + "-----\t-----------\n")
            self.text += "\t${:0.2f}\n".format(self.total)
            self.history.insert(END, self.text)
            self.history['state'] = "disabled"

            if DEBUG:
                print("Total Cleared.")
                print("New balance: ${:0.2f}".format(self.total))
        else:
            pass  # just goes back if user hits cancel

    # executes if the quit button is pressed
    def cancelbutton(self):
        isYes = tkinter.messagebox.askyesno("Cancel",
                                            "Are you sure you want to quit? Your changes won't be saved.")
        if isYes:  # asks the user if they are sure they want to cancel
            quit(0)  # if yes, it quits without saving
        else:
            pass  # if no, it just continues

    # executes if the save button is pressed
    def savebutton(self):
        isYes = tkinter.messagebox.askokcancel("Save",
                                            "Your final balance is ${:0.2f}."
                                            "\nAre you finished making changes?".format(self.total))
        if isYes == True:  # asks user if they are ready to save
            save_changes(self.total, self.goal)  # if yes, calls save_changes() functions which quits at the end
        else:
            pass  # if no, passes


    def dollarwindow(self):  # opens the dollar entry window, then calls dollar_add() to add to total
        # this whole thing didn't end up being used, but it's still an option if the button in GUI setup is uncommented
        self.dollar_window = Toplevel()
        self.dollar_window.title("Enter Dollar Amount")
        self.dollar_window.lift()
        if DEBUG:
            print("Dollar Window has opened")

        # Title/prompt
        dol_lbl = Label(self.dollar_window, text="Please Enter Your Dollar Amount:", font=("calibri", 30))
        dol_lbl.grid(row=0, column=0, columnspan=4, sticky=NSEW, padx=65, pady=30)

        # the dollar sign
        dol_sign = Label(self.dollar_window, text="$", font=("calibri", 24))
        dol_sign.grid(row=1, column=0, sticky=E, padx=15)

        # the entry box & its settings
        self.dollar_var = IntVar()
        self.dol_entry = Entry(self.dollar_window, font=("calibri", 24), width=15, textvariable=self.dollar_var)
        self.dol_entry.grid(row=1, column=1, sticky=W)
        self.dol_entry.focus_set()  # this sets the focus so the box is already ready to be typed in
        self.dol_entry.delete(0, END)  # IntVar shows a default 0 so this clears the box w/out causing an error
        self.dollar_window.bind('<Return>', lambda event: self.dollar_add()) # allows user to press enter to submit

        # the confirm and cancel buttons
        dol_style = Style()
        dol_style.configure('dol.TButton', font=("calibri", 15, "bold"))
        dol_cancel = Button(self.dollar_window, text="Cancel",style="dol.TButton", command=self.dollar_window.destroy)
        dol_cancel.grid(row=2, column=0, padx=40, pady=30)

        dol_submit = Button(self.dollar_window, text="Confirm", style="dol.TButton", command=lambda: self.dollar_add())
        dol_submit.grid(row=2, column=2, padx=40, sticky=E)

    def dollar_add(self):  # adds dollar amount from the entry box (dollarwindow()) to the total
        try: # checks if there is no error
            val = self.dollar_var.get()  # retrieves value from the text box

            isYes = tkinter.messagebox.askyesno("Confirm", f"You entered: ${val}. \nIs this correct?")
            if isYes == True:  # asks the user if they are sure they want to continue
                self.total += val  # adds the value
                self.l5["text"] = "${:0.2f}".format(self.total)  # displays the new balance
                if DISPLAY:
                    lcd.text("Deposited ${:0.2f}".format(val), 1)
                    lcd.text("Total: ${:0.2f}".format(self.total), 2)

                if self.total > 0:  # if the balance is positive, the text of current balance is green
                    self.l5["foreground"] = "green"
                    self.l5["background"] = "lightgreen"
                # updates the text in the side panel
                self.text = "+ ${:0.2f}\n".format(val)
                self.text += "\t${:0.2f}\n".format(self.total)
                if DEBUG:
                    print("Dollar amount added\n" + f"Number entered is {val}")
                    print("New balance: ${:0.2f}".format(self.total))

                self.history['state'] = "normal"  # to open the text box "history" before it is closed again
                self.history.insert(END, self.text)  # displays the text
                self.history['state'] = "disabled"  # closes the text box so the user can't type in it

                self.dollar_window.destroy()  # closes the dollar entry window after
            else:  # if user enters no, it just continues
                self.dollar_window.lift() # brings window back to front
                self.dol_entry.focus_set()
                pass
        except:  # runs if the entered value produces an error & allows user to retry
            tkinter.messagebox.showerror("Error", "Please enter a number in the box.")
            self.dollar_window.lift()  # brings window to the front after error message is closed
            self.dol_entry.focus_set()
            if DEBUG:
                print("There was an error entering the dollar amount")
                print("Most likely the amount entered wasn't a number or the box was empty")

    # this opens the budget window to display information
    def open_window2(self):  # budget window
        # these are all for resizing purposes
        title_font= 35
        balance_font = 28
        self.label_font = 25
        title2_font = 30
        label_y = 30
        x_space = 190

        # creates budgetting window
        self.window2 = Toplevel()
        self.window2.title("Budget Info")

        if DEBUG:
            print("Window 2 has opened")

        # this is the title of the page (can change this later)
        w2_l1 = Label(self.window2, text="This is Where You Budget!", font=('Georgia', title_font, 'bold'))
        w2_l1.grid(row=0, column=0, sticky=NSEW, columnspan=4, padx=x_space, pady=10)

        # show current total
        w2_l2 = Label(self.window2, text="\tCurrent Total: ${:0.2f}".format(self.total), font=('Calibri', balance_font,
                                                                                               'bold'))
        w2_l2.grid(row=1, column=0, sticky=NSEW, columnspan=4, padx=x_space, pady=25)

        # labels the different categories
        give_cat = Label(self.window2, text="Give", font=('Calibri', self.label_font, 'bold'))
        give_cat.grid(row=2, column=1, sticky=NSEW, pady=label_y, padx=58)
        save_cat = Label(self.window2, text="Save", font=('Calibri', self.label_font, 'bold'))
        save_cat.grid(row=2, column=2, sticky=NSEW, pady=label_y, padx=58)
        spend_cat = Label(self.window2, text="Spend", font=('Calibri', self.label_font, 'bold'))
        spend_cat.grid(row=2, column=3, sticky=NSEW, pady=label_y, padx=58)

        # shows the different percentages the money is divided by
        # in the future these percentages could be made changeable (not enough time)
        self.give_percent = 0.10
        self.save_percent = 0.20
        self.spend_percent = 0.70
        percents = Label(self.window2, text="Percentage:", font=('Calibri', self.label_font, 'bold'))
        percents.grid(row=3, column=0, sticky=NSEW, pady=label_y, padx=15)
        give_percent = Label(self.window2, text=f"{self.give_percent*100}%", font=('Calibri', self.label_font, 'bold',
                                                                                   'underline'))
        give_percent.grid(row=3, column=1, sticky=NSEW, pady=label_y, padx=60)
        save_percent = Label(self.window2, text=f"{self.save_percent*100}%", font=('Calibri', self.label_font, 'bold',
                                                                                   'underline'))
        save_percent.grid(row=3, column=2, sticky=NSEW, pady=label_y, padx=60)
        spend_percent = Label(self.window2, text=f"{self.spend_percent*100}%",
                              font=('Calibri', self.label_font, 'bold', 'underline'))
        spend_percent.grid(row=3, column=3, sticky=NSEW, pady=label_y, padx=60)

        # shows the amount of money in each category
        self.give = self.total * self.give_percent
        self.save = self.total * self.save_percent
        self.spend = self.total * self.spend_percent
        amounts = Label(self.window2, text="Amounts:", font=('Calibri', self.label_font, 'bold'))
        amounts.grid(row=4, column=0, sticky=NSEW, pady=label_y, padx=15)
        give_amount = Label(self.window2, text="${:0.2f}".format(self.give), font=('Calibri', self.label_font))
        give_amount.grid(row=4, column=1, sticky=NSEW, pady=label_y, padx=55)
        save_amount = Label(self.window2, text="${:0.2f}".format(self.save), font=('Calibri', self.label_font))
        save_amount.grid(row=4, column=2, sticky=NSEW, pady=label_y, padx=55)
        spend_amount = Label(self.window2, text="${:0.2f}".format(self.spend), font=('Calibri', self.label_font))
        spend_amount.grid(row=4, column=3, sticky=NSEW, pady=label_y, padx=55)

        # goal section with progress Bar
        goal_title = Label(self.window2, text="\tSavings Goal Progress:", font=('Calibri', title2_font, 'bold'))
        goal_title.grid(row=5, column=0, sticky=NSEW, columnspan=4, padx=x_space, pady=25)

        self.goalshow = Label(self.window2, text="${:0.2f} / ${:0.2f}".format(self.save, self.goal),
                     font=('Calibri', self.label_font))
        self.goalshow.grid(row=6, column=0, sticky=NSEW, pady=label_y, padx=15)

        self.bar_val = (self.save / self.goal) * 100
        self.save_bar = Progressbar(self.window2, length=570, value=self.bar_val, maximum=100)
        self.save_bar.grid(row=6, column=1, columnspan=3, pady=label_y, padx=55)

        # the bottom buttons
        w2_style = Style()
        w2_style.configure('w2.TButton', font=("Calibri", self.button_font))
        w2_setgoal = Button(self.window2, text="Adjust Goal", style="w2.TButton", command=lambda: self.set_goal())
        w2_setgoal.grid(row=8, column=0, pady=label_y)

        w2_cancel = Button(self.window2, text="Cancel",style="w2.TButton", command=self.window2.destroy)
        w2_cancel.grid(row=8, column=2, pady=label_y)

        w2_submit = Button(self.window2, text="OK", style="w2.TButton", command=self.window2.destroy)
        w2_submit.grid(row=8, column=3, padx=label_y)

        # if the goal is at or above 100% it calls a function
        if self.save_bar["value"] >= 100:
            self.goalreached()  # I made this a separate function so rewards or sound affects or something could
                                # be added in the future when the bar is filled


    def set_goal(self):  # this makes the new goal set window pop up
        # creates pop-up window to adjust the goal
        self.goalset_window = Toplevel()
        self.goalset_window.title("Enter New Goal")
        self.goalset_window.lift()
        if DEBUG:
            print("Goal Set Window has opened")

        # title/prompt
        goal_lbl = Label(self.goalset_window, text="Please Enter Your New Goal:", font=("calibri", 30))
        goal_lbl.grid(row=0, column=0, columnspan=4, sticky=NSEW, padx=65, pady=30)

        # dollar sign
        goal_sign = Label(self.goalset_window, text="$", font=("calibri", 24))
        goal_sign.grid(row=1, column=0, sticky=E, padx=15)

        # creates the entry box for the new goal
        self.goal_var = IntVar()
        self.goal_entry = Entry(self.goalset_window, font=("calibri", 24), width=15, textvariable=self.goal_var)
        self.goal_entry.grid(row=1, column=1, sticky=W)
        self.goal_entry.focus_set()  # this sets the focus so the box is already ready to be typed in
        self.goal_entry.delete(0, END)  # IntVar shows a default 0 so this clears the box w/out causing an error
        self.goalset_window.bind('<Return>', lambda event: self.new_goal())  # allows user to press enter to submit

        # the bottom buttons (cancel & confirm)
        goal_style = Style()
        goal_style.configure('goal.TButton', font=("calibri", 15, "bold"))
        goal_cancel = Button(self.goalset_window, text="Cancel", style="goal.TButton",
                             command=self.goalset_window.destroy)
        goal_cancel.grid(row=2, column=0, padx=40, pady=30)

        goal_submit = Button(self.goalset_window, text="Confirm", style="goal.TButton",
                             command=lambda: self.new_goal())
        goal_submit.grid(row=2, column=2, padx=40, sticky=E)


    def new_goal(self):  # this updates the budget window after the goal is set
        try: # checks if there is no error
            goal = self.goal_var.get()  # retrieves value from the text box

            isYes = tkinter.messagebox.askyesno("Confirm", f"You entered: ${goal}. \nIs this correct?")
            if isYes == True:  # asks the user if they are sure they want to continue
                self.goal = goal  # saves the entered number as the new goal
                if DEBUG:
                    print("Goal Changed")
                    print("New goal: ${:0.2f}".format(self.goal))
                self.goalset_window.destroy()  # closes the dollar entry window after
                self.window2.lift()  # lifts the budget window so it's not behind the main window
                self.goalshow["text"] = "${:0.2f} / ${:0.2f}".format(self.save, self.goal)  # updates label

                # updates the savings progress bar
                self.bar_val = (self.save/self.goal)*100
                self.save_bar["value"] = self.bar_val
                if self.save_bar["value"] >= 100:
                    self.goalreached()

            else:  # if user enters no, it just continues
                self.goalset_window.lift() # brings window back to front
                self.goal_entry.focus_set()
                pass
        except:  # runs if the entered value produces an error & allows user to retry
            tkinter.messagebox.showerror("Error", "Please enter a number in the box.")
            self.goalset_window.lift()  # brings window to the front after error message is closed
            self.goal_entry.focus_set()
            if DEBUG:
                print("There was an error entering the goal amount.")
                print("Most likely the amount entered wasn't a number or the box was empty.")


    # runs if the savings goal is reached (can be added to)
    def goalreached(self):
        self.save_bar["value"] = 99.9  # if the widget reaches 100% it resets so this shows the bar as full if the
                                       # goal is reached/exceeded without resetting
        if DEBUG:
            print("The Savings Goal has been reached!!!")


#######################################################################################################################

# this runs first in the program to check if there is already an amount in the piggy bank
def initialize_bal():
    try:  # tries to read teh file if it exists already
        test = open("smart_bank_balance.txt", "r")  # reads file if it exists
        total_bal = int(test.readline())  # saves teh value as the initial total balance
        test.close()  # closes the file
        if DISPLAY:  # updates the LCD display if that's turned on
            lcd.text("Total: ${:0.2f}".format(total_bal), 1)
        if DEBUG:
            print("The total file was found.")
            print(f"Total: ${total_bal}")
        return total_bal # returns the value it read

    except:  # if the file doesn't exist (ie first time using the program)
        total_bal = 0  # total balance begins at 0
        if DISPLAY:  # displays the total on LCD
            lcd.text("Total: ${:0.2f}".format(total_bal), 1)
        if DEBUG:
            print("No total file found.")
            print(f"Total: ${total_bal}")
        return total_bal  # returns the total balance


# checks if the goal has already been manually set
def initialize_goal():
    try:  # tries to read the file if it exists already
        test2 = open("smart_bank_goal.txt", "r")  # reads file if it exists
        orig_goal = int(test2.readline())  # saves the value as the initial savings goal
        test2.close()  # closes the file
        if DEBUG:
            print("The goal file was found.")
            print(f"Goal: ${orig_goal}")
        return orig_goal # returns the value it read
    except:  # if the file doesn't exist (ie first time using the program)
        orig_goal = 5  # the default goal is $5 (can be changed)
        if DEBUG:
            print("No goal file found.")
            print(f"Goal: ${orig_goal}")
        return orig_goal  # returns the default savings goal

# executes at the end of the program when the user hits save
def save_changes(total, goal):
    if os.path.exists("smart_bank_balance.txt"):  # if the file already exists, it deletes it
        os.remove("smart_bank_balance.txt")  # in order to avoid duplicates or old data
    if os.path.exists("smart_bank_goal.txt"):  # if the file already exists, it deletes it
        os.remove("smart_bank_goal.txt")
    save_amount = open("smart_bank_balance.txt", "w")  # creates and writes in the file
    save_amount.write(str(total))  # writes the total in the file
    save_amount.close()  # closes the file

    save_goal = open("smart_bank_goal.txt", "w")  # creates and writes in the file
    save_goal.write(str(goal))  # writes the total in the file
    save_goal.close()  # closes the file
    if DEBUG:
        print("Total Balance Saved." + "\nSavings Goal Saved.")
    quit()  # ends the program


####### MAIN #######
# set to debug mode if necessary
DEBUG = False

# initializes the total balance
total_bal = initialize_bal()
init_goal = initialize_goal()

# creates the main GUI window
window1 = Tk()
window1.title("Smart Piggy Bank")  # set window title
window1.geometry("1500x800+65+55")  # set position of the window for raspberry pi
t = GUI(window1, total_bal, init_goal)  # create object in GUI class
t.setupGUI()  # begin the setup process

window1.mainloop()
