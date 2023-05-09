# Programmer: Jacob Tupper
# Prjoect: Recipe Book
# Date: 5/6/23

# Importing tkinter adn sqlite
import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkinter import *
import sqlite3 as lite
import sys

# Creating the Mainwindow Class
class Mainwindow:

    # Initializing
    def __init__(self):

        # Connecting to the Database
        conn = lite.connect('Recipe Database.db')

        cur = conn.cursor()

        # Creating Main window
        self.mainwindow = tkinter.Tk()

        self.mainwindow.title('Recipes')

        # Creating Frames
        self.top_rightframe = tkinter.Frame(self.mainwindow)
        self.top_leftframe = tkinter.Frame(self.mainwindow)
        self.midframe = tkinter.Frame(self.mainwindow)
        self.bottomframe = tkinter.Frame(self.mainwindow)
        self.bbottomframe = tkinter.Frame(self.mainwindow)

        # Creating Label
        self.selectionlabel = tkinter.Label(self.top_leftframe, text='Select a Recipe:')

        # Creating buttons for the main window
        self.accountbutton = tkinter.Button(self.top_rightframe, text='Account', command=self.account)
        self.rp_select_button = tkinter.Button(self.bbottomframe, text='Get Recipe', command=self.rp_select_info)
        self.rp_update_button = tkinter.Button(self.bbottomframe, text='Update Recipe', command=self.rp_update)
        self.rp_create_button = tkinter.Button(self.bbottomframe, text='Create Recipe', command=self.rp_create)
        self.rp_delete_button = tkinter.Button(self.bbottomframe, text='Remove Recipe', command=self.rp_remove_confirm)

        # Creating a Try and except with creating the Treeview
        try:
            self.recipe_treeview = ttk.Treeview(self.midframe)

            # Creating Columns
            self.recipe_treeview['columns'] = ('RCID', 'RCName', 'DESC')

            self.recipe_treeview.column('#0', width=0, anchor=tkinter.CENTER)
            self.recipe_treeview.column('RCID', anchor=tkinter.CENTER, width=80)
            self.recipe_treeview.column('RCName', anchor=tkinter.CENTER, width=250)
            self.recipe_treeview.column('DESC', anchor=tkinter.CENTER, width=400)

            # Creating Headings
            self.recipe_treeview.heading('#0', text='', anchor=tkinter.CENTER)

            self.recipe_treeview.heading('RCID', text='Recipe ID', anchor=tkinter.CENTER)
            self.recipe_treeview.heading('RCName', text='Recipe', anchor=tkinter.CENTER)
            self.recipe_treeview.heading('DESC', text='Brief Description', anchor=tkinter.CENTER)

            # creating Labels and Entries for Recipe Information
            self.recipe_label = tkinter.Label(self.bottomframe, text='Recipe')
            self.recipe_label.grid(row=0, column=2, padx=8)

            self.recipe_ID_label = tkinter.Label(self.bottomframe, text='Recipe ID')
            self.recipe_ID_label.grid(row=0, column=1, padx=8)

            self.recipe_entry = tkinter.Entry(self.bottomframe, width=30)
            self.recipe_entry.grid(row=1, column=2, padx=8)

            self.recipe_ID_entry = tkinter.Entry(self.bottomframe, width=5)
            self.recipe_ID_entry.grid(row=1, column=1, padx=8)

            # Populating the treeview
            cur.execute("SELECT RecipeID, RecipeName, Description FROM Recipe ORDER BY RecipeID")
            rows = cur.fetchall()

            for row in rows:
                print(row)  # print all records in the database
                self.recipe_treeview.insert("", tkinter.END, values=row)

        # Except Statement
        except:
            tkinter.messagebox.showerror('DateBase Error', 'DateBase Failed to Load Recipes')
        # Closing the Connection
        finally:
            conn.close()

        # Packing the tree view
        self.recipe_treeview.pack()

        # Packing Label
        self.selectionlabel.pack()

        # Packing Buttons
        self.accountbutton.pack()
        self.rp_select_button.pack(side='left', padx=10, pady=10)
        self.rp_update_button.pack(side='left', padx=10, pady=10)
        self.rp_create_button.pack(side='left', padx=10, pady=10)
        self.rp_delete_button.pack(side='left', padx=5, pady=10)
        self.recipe_treeview.bind("<ButtonRelease-1>", self.select_recipe)
        # Packing Frames
        self.top_rightframe.pack(anchor='ne')
        self.top_leftframe.pack(anchor='n')
        self.midframe.pack()
        self.bottomframe.pack()
        self.bbottomframe.pack()

        # Creating mainloop
        tkinter.mainloop()

    # Defining select recipe
    def select_recipe(self, event):

        # Creating a try and except statement
        try:

            self.recipe_ID_entry.delete(0, END)
            self.recipe_entry.delete(0, END)
            # Focusing on the information on the treeview
            selected = self.recipe_treeview.focus()

            # setting items to a variable
            values = self.recipe_treeview.item(selected, 'values')

            # Inserting values into entries
            self.recipe_ID_entry.insert(0, values[0])
            self.recipe_entry.insert(0, values[1])

        # exception for not selecting recipe
        except IndexError:
            tkinter.messagebox.showerror('Empty Box', 'User Forgot To Click On A Recipe')

    # Defining select information
    def rp_select_info(self):

        # connecting to database
        conn = lite.connect('Recipe Database.db')

        cur = conn.cursor()

        # Creating recipe window
        self.recipe_window = tkinter.Tk()

        # Setting the geometry for the recipe window
        self.recipe_window.geometry('450x400')

        self.recipe_window.title('Recipe')

        # Creating Frames
        self.rp_return_frame = tkinter.Frame(self.recipe_window)
        self.rp_title_frame = tkinter.Frame(self.recipe_window)
        self.recipe_instructions_frame = tkinter.Frame(self.recipe_window)
        self.ingredients_frame = tkinter.Frame(self.recipe_window)

        # Creating Button
        self.rp_return_button = tkinter.Button(self.rp_return_frame, text='Return',
                                               command=self.rp_return_to_mainwindow)

        # Creating a Try and Except statement
        try:

            # Getting the Recipe Name from Database
            cur.execute('SELECT RecipeName FROM Recipe'
                        ' WHERE RecipeID = :OID OR RecipeName = :RN',
                        {'OID': self.recipe_ID_entry.get(),
                         'RN': self.recipe_entry.get()})

            # Setting the retrieved Recipe Name to a Variable
            title = cur.fetchone()

            # Creating Recipe name Label
            self.rp_title = tkinter.Label(self.rp_title_frame, text=title, font=40, pady=10)

            # Getting Recipe Instructions from database
            cur.execute('SELECT Instructions FROM Recipe'
                        ' WHERE RecipeName = :RN',
                        {'RN': self.recipe_entry.get()})

            # Setting the retrieved Recipe Instructions to a Variable
            instruction = cur.fetchone()

            # Creating Recipe Instruction Label
            self.recipe_instru_label = tkinter.Label(self.recipe_instructions_frame, text=instruction, wraplength=400,
                                                     highlightbackground='black', highlightthickness=2)

            # Getting Recipe Ingredients from database
            cur.execute('SELECT UofM FROM Ingrdients JOIN Recipe R on Ingrdients.IGID = R.IGID WHERE R.IGID = :OID '
                        'OR RecipeName = :RN',
                        {'OID': self.recipe_ID_entry.get(),
                         'RN': self.recipe_entry.get()})

            # Setting the retrieved Recipe Ingredients to a Variable
            ingredients = cur.fetchone()

            # Creating Recipe ingredients Label
            self.ingredients_label = tkinter.Label(self.ingredients_frame, text=ingredients, wraplength=400, pady=20)

            # Creating an if statement in case the User did not enter anything into entry boxes
            if not self.recipe_entry.get():
                tkinter.messagebox.showerror('Empty Entry Box', 'User Did Not Select Recipe. '
                                                                'Make Sure That Entries are filled.')
                self.recipe_window.destroy()

        # Exception statement incase user does not enter information
        except lite.ProgrammingError:
            tkinter.messagebox.showerror('Empty Entry Box', 'User Did Not Select Recipe.')
            self.recipe_window.destroy()
        # Closing the Database
        finally:
            conn.close()

        # Packing Buttons
        self.rp_return_button.pack()

        # Packing Labels
        self.rp_title.pack()
        self.recipe_instru_label.pack()
        self.ingredients_label.pack()

        # Packing Frames
        self.rp_return_frame.pack(anchor='ne')
        self.rp_title_frame.pack()
        self.recipe_instructions_frame.pack()
        self.ingredients_frame.pack()

        # Destroying the main window
        self.mainwindow.destroy()

    # Defining updating
    def rp_update(self):

        # Connecting to the Database
        conn = lite.connect('Recipe Database.db')

        cur = conn.cursor()

        # Creating Try and except
        try:
            # Creating update window
            self.rp_update_window = tkinter.Tk()

            self.rp_update_window.geometry('290x300')

            self.rp_update_window.title('Update Recipe')

            # Creating Frames
            self.ru_topframe = tkinter.Frame(self.rp_update_window)
            self.ru_bottomframe = tkinter.Frame(self.rp_update_window)
            self.ru_return_frame = tkinter.Frame(self.rp_update_window)

            # Creating Buttons
            self.ru_return_button = tkinter.Button(self.ru_return_frame, text='Return', command=self.ru_return_to_mainwindow)
            self.ru_update_button = tkinter.Button(self.ru_bottomframe, text='Save Changes', command=self.ru_update)

            # Creating Labels and Entries
            self.ru_recipe_id_label = tkinter.Label(self.ru_topframe, text='Recipe ID:')
            self.ru_recipe_id_label.grid(row=0, column=0, pady=5)

            self.ru_recipe_id_entry = tkinter.Entry(self.ru_topframe, width=3)
            self.ru_recipe_id_entry.grid(row=0,column=2, pady=5)

            self.ru_recipe_name_label = tkinter.Label(self.ru_topframe, text='Recipe:')
            self.ru_recipe_name_label.grid(row=1, column=0, pady=5)

            self.ru_recipe_name_entry = tkinter.Entry(self.ru_topframe, width=30)
            self.ru_recipe_name_entry.grid(row=1, column=2, pady=5)

            self.ru_recipe_DCR_label = tkinter.Label(self.ru_topframe, text='Brief Description:')
            self.ru_recipe_DCR_label.grid(row=2, column=0, pady=5)

            self.ru_recipe_DCR_entry = tkinter.Entry(self.ru_topframe)
            self.ru_recipe_DCR_entry.grid(row=2, column=2, pady=5)

            self.ru_recipe_INST_label = tkinter.Label(self.ru_topframe, text='Instructions:')
            self.ru_recipe_INST_label.grid(row=3, column=0, pady=5)

            self.ru_recipe_INST_entry = tkinter.Entry(self.ru_topframe)
            self.ru_recipe_INST_entry.grid(row=3, column=2, pady=5)

            self.ru_recipe_IG_label = tkinter.Label(self.ru_topframe, text='Ingredients:')
            self.ru_recipe_IG_label.grid(row=4, column=0, pady=5)

            self.ru_recipe_IG_entry = tkinter.Entry(self.ru_topframe)
            self.ru_recipe_IG_entry.grid(row=4, column=2, pady=5)

            # Populating Entry boxes
            cur.execute('SELECT * FROM Recipe'
                        ' WHERE RecipeID = ?', self.recipe_ID_entry.get())

            recipe_name = cur.fetchall()

            for record in recipe_name:
                self.ru_recipe_id_entry.insert(0, record[0])
                self.ru_recipe_name_entry.insert(0, record[2])
                self.ru_recipe_DCR_entry.insert(0, record[3])
                self.ru_recipe_INST_entry.insert(0, record[4])

            cur.execute('SELECT * FROM Ingrdients WHERE IGID = ?',
                        self.recipe_ID_entry.get())

            ing = cur.fetchall()

            for IG in ing:
                self.ru_recipe_IG_entry.insert(0, IG[1])

            # Packing Buttons
            self.ru_return_button.pack()
            self.ru_update_button.pack(pady=10)

            # Packing Frames
            self.ru_return_frame.pack(anchor='ne', pady=10)
            self.ru_topframe.pack()
            self.ru_bottomframe.pack()

            # Destroying main window
            self.mainwindow.destroy()

        # Except statement
        except lite.ProgrammingError:
            tkinter.messagebox.showerror('Empty Entry Box', 'User Did Not Select Recipe.')
            self.rp_update_window.destroy()

        # Closing connection to database
        finally:
            conn.close()

    # defining ru_update
    def ru_update(self):

        # Connecting to database
        conn = lite.connect('Recipe Database.db')

        cur = conn.cursor()

        # Updating Recipe Table
        cur.execute('''UPDATE Recipe SET 
                    RecipeName = :Recipe_name,
                    Description = :DESC,
                    Instructions = :INST
                    WHERE RecipeID = :OID''',
                    {'Recipe_name': self.ru_recipe_name_entry.get(),
                     'DESC': self.ru_recipe_DCR_entry.get(),
                     'INST': self.ru_recipe_INST_entry.get(),
                     'OID': self.ru_recipe_id_entry.get()})

        # Updating Ingrdients table
        cur.execute('''UPDATE Ingrdients SET
                    UofM = :UM
                    WHERE IGID = :OID''',
                    {'UM': self.ru_recipe_IG_entry.get(),
                     'OID': self.ru_recipe_id_entry.get()})

        # Commiting and closing database
        conn.commit()

        conn.close()

        # Calling the conformation function
        self.ru_confirm_window()

    # DEfining ru_confirm
    def ru_confirm_window(self):

        # Creating update conformation
        self.ru_cm_window = tkinter.Tk()

        self.ru_cm_window.title('Updating Recipe')

        # Creating frames
        self.cm_upper_frame = tkinter.Frame(self.ru_cm_window)
        self.cm_lower_frame = tkinter.Frame(self.ru_cm_window)

        # Creating label
        self.cm_label = tkinter.Label(self.cm_upper_frame, text='Your changes has been saved.')

        # Creating Button
        self.cm_button = tkinter.Button(self.cm_lower_frame, text='OK', command=self.cm_return_to_mainwindow)

        # Packing label
        self.cm_label.pack()

        # Packing Button
        self.cm_button.pack()

        # Packing Frames
        self.cm_upper_frame.pack()
        self.cm_lower_frame.pack()

        # Destroying the Update window
        self.rp_update_window.destroy()

    # Defining ru_return
    def ru_return_to_mainwindow(self):

        # Declaring if the Update window is open close it
        if self.rp_update_window != 0:
            self.rp_update_window.destroy()

        # Calling Main Window class
        Mainwindow()

    # Defining cm_return
    def cm_return_to_mainwindow(self):
        # Declaring if the confirm window is open close it
        if self.ru_cm_window != 0:
            self.ru_cm_window.destroy()
        Mainwindow()

    # Defining rp_create
    def rp_create(self):

        # Creating Connection to database
        conn = lite.connect('Recipe Database.db')

        cur = conn.cursor()

        # Creating recipe ID
        ID = 1

        # Collecting all records
        records = cur.execute('SELECT * FROM Recipe')

        # Making a four loop and adding 1 to ID
        for record in records:
            ID += 1

        # Creating window
        self.rp_createwindow = tkinter.Tk()

        self.rp_createwindow.geometry('290x300')

        self.rp_createwindow.title('Create Recipe')

        # Creating frames
        self.ct_return_frame = tkinter.Frame(self.rp_createwindow)
        self.ct_upper_frame = tkinter.Frame(self.rp_createwindow)
        self.ct_lower_frame = tkinter.Frame(self.rp_createwindow)

        # Creating Buttons
        self.ct_return_button = tkinter.Button(self.ct_return_frame, text='Return', command=self.ct_return_to_mainwindow)
        self.ct_confirm_button = tkinter.Button(self.ct_lower_frame, text='Save New Recipe', command=self.ct_cm)

        # Creating Labels and Entries
        self.ct_recipe_ID_label = tkinter.Label(self.ct_upper_frame, text='Recipe ID:')
        self.ct_recipe_ID_label.grid(row=0, column=0, pady=5)

        self.ct_recipe_ID_entry = tkinter.Entry(self.ct_upper_frame)
        self.ct_recipe_ID_entry.grid(row=0, column=2, pady=5)

        self.ct_recipe_name_label = tkinter.Label(self.ct_upper_frame, text='Enter New Recipe Title:')
        self.ct_recipe_name_label.grid(row=1, column=0, pady=5)

        self.ct_recipe_name_entry = tkinter.Entry(self.ct_upper_frame)
        self.ct_recipe_name_entry.grid(row=1, column=2, pady=5)

        self.ct_recipe_DESC_label = tkinter.Label(self.ct_upper_frame, text='Brief Description:')
        self.ct_recipe_DESC_label.grid(row=2, column=0, pady=5)

        self.ct_recipe_DESC_entry = tkinter.Entry(self.ct_upper_frame)
        self.ct_recipe_DESC_entry.grid(row=2, column=2, pady=5)

        self.ct_recipe_INST_label = tkinter.Label(self.ct_upper_frame, text='Enter Recipe Instructions:')
        self.ct_recipe_INST_label.grid(row=3, column=0, pady=5)

        self.ct_recipe_INST_entry = tkinter.Entry(self.ct_upper_frame)
        self.ct_recipe_INST_entry.grid(row=3, column=2, pady=5)

        self.ct_recipe_IG_label = tkinter.Label(self.ct_upper_frame, text='Enter Ingredients:')
        self.ct_recipe_IG_label.grid(row=4, column=0, pady=5)

        self.ct_recipe_IG_entry = tkinter.Entry(self.ct_upper_frame)
        self.ct_recipe_IG_entry.grid(row=4, column=2, pady=5)

        # Setting recipe ID
        self.ct_recipe_ID_entry.insert(0, ID)

        # packing Buttons
        self.ct_return_button.pack()
        self.ct_confirm_button.pack()

        # Packing frames
        self.ct_return_frame.pack(anchor='ne', pady=10)
        self.ct_upper_frame.pack()
        self.ct_lower_frame.pack()

        # Destroying main window
        self.mainwindow.destroy()

    # Defining ct_cm
    def ct_cm(self):

        # connecting to the Database
        conn = lite.connect('Recipe Database.db')

        cur = conn.cursor()

        # setting ID variable
        ID = 1

        records = cur.execute('SELECT * FROM Recipe')

        for record in records:
            ID += 1


        # Creating try and except function
        try:

            # Inserting New information into database
            cur.execute('INSERT INTO Recipe VALUES (:ID, :AID, :Recipe_Name, :DESC, :INST, :IGID)',
                        {'ID': ID,
                         'AID': 1,
                         'Recipe_Name': self.ct_recipe_name_entry.get(),
                         'DESC': self.ct_recipe_DESC_entry.get(),
                         'INST': self.ct_recipe_INST_entry.get(),
                         'IGID': ID})

            cur.execute('INSERT INTO Ingrdients VALUES (:ID, :UM)',
                        {'ID': ID,
                         'UM': self.ct_recipe_IG_entry.get()})

            # Calling a function
            self.ct_cm_return_to_mainwindow()
            conn.commit()

        # Telling the user that they typed in a similar Recipe
        except lite.IntegrityError:
            tkinter.messagebox.showerror('Same Entry ERROR', 'You Have Entered a Field that is Similar to another Recipe.'
                                                             'Change the Recipe Name.')

        # Closing Connection
        finally:
            conn.close()

    # Defining ct_return
    def ct_return_to_mainwindow(self):

        # making sure that the window is open then close it
        if self.rp_createwindow != 0:
            self.rp_createwindow.destroy()

        # Calling class
        Mainwindow()

    # Defining cr_cm_return
    def ct_cm_return_to_mainwindow(self):

        # Creating creation window
        self.ct_cm_window = tkinter.Tk()

        # Creating frames
        self.ct_cm_upper_frame = tkinter.Frame(self.ct_cm_window)
        self.ct_cm_lower_frame = tkinter.Frame(self.ct_cm_window)

        # Creating label
        self.ct_cm_label = tkinter.Label(self.ct_cm_upper_frame, text='Your New Recipe Has Been Saved.')

        # Creating Button
        self.ct_cm_button = tkinter.Button(self.ct_cm_lower_frame, text='OK', command=self.cm_return2_to_mainwindow)

        # Packing label
        self.ct_cm_label.pack()

        # PAcking Button
        self.ct_cm_button.pack()

        # Packing Frames
        self.ct_cm_upper_frame.pack()
        self.ct_cm_lower_frame.pack()

        # Destroying the create window
        self.rp_createwindow.destroy()

    # Defining cm_return2
    def cm_return2_to_mainwindow(self):

        # IF the window is open then close it
        if self.ct_cm_window != 0:
            self.ct_cm_window.destroy()

       # Calling main window
        Mainwindow()

    # Defining rp_remove
    def rp_remove(self):
        conn = lite.connect('Recipe Database.db')

        cur = conn.cursor()

        try:
            cur.execute('DELETE FROM RECIPE WHERE RecipeID = :ID',
                        {'ID': self.recipe_ID_entry.get()})

            cur.execute('DELETE FROM Ingrdients WHERE IGID = :OID',
                        {'OID': self.recipe_ID_entry.get()})

            conn.commit()

            self.mainwindow.destroy()
            self.rp_remove_cm_window.destroy()

            Mainwindow()
        except lite.OperationalError:
            tkinter.messagebox.showerror('Empty Entry Box', 'User Did Not Select Recipe.')
            self.rp_remove_cm_window.destroy()
        finally:
            conn.close()

    # Defining rp_remove_confirm
    def rp_remove_confirm(self):

        # Creating remove window
        self.rp_remove_cm_window = tkinter.Tk()

        self.rp_remove_cm_window.title('Remove Recipe')

        # Creating frames
        self.rm_cm_upper_frame = tkinter.Frame(self.rp_remove_cm_window, padx=10)
        self.rm_cm_lower_frame = tkinter.Frame(self.rp_remove_cm_window)

        # Setting a name variable
        remove_recipe_name = self.recipe_entry.get()

        # Creating a label
        self.rm_cm_label = tkinter.Label(self.rm_cm_upper_frame,
                                         text=f'''You Sure That You Want To Remove {remove_recipe_name}
        From Your Recipe Book?''')

        # Creating buttons
        self.rm_cm_button = tkinter.Button(self.rm_cm_lower_frame, text='Yes', command=self.rp_remove)
        self.rm_no_button = tkinter.Button(self.rm_cm_lower_frame, text='No', command=self.rp_remove_cm_window.destroy)

        # Packing label
        self.rm_cm_label.pack()

        # Packing Buttons
        self.rm_cm_button.pack(side='left', padx=5, pady=5, ipadx=10)
        self.rm_no_button.pack(side='left', padx=5, pady=5, ipadx=10)

        # Packing Frames
        self.rm_cm_upper_frame.pack()
        self.rm_cm_lower_frame.pack()

    # Defining rp_return
    def rp_return_to_mainwindow(self):

        # Checking if window is open
        if self.recipe_window != 0:
            self.recipe_window.destroy()

        # Calling main window
        Mainwindow()

    # Defining account
    def account(self):

        # Connecting to database
        conn = lite.connect('Recipe Database.db')

        cur = conn.cursor()

        # Creating window
        self.accountwindow = tkinter.Tk()

        self.accountwindow.title('Account Information')

        # Creating Frames
        self.ac_topframe = tkinter.Frame(self.accountwindow)
        self.ac_midframe = tkinter.Frame(self.accountwindow)
        self.ac_bottomframe = tkinter.Frame(self.accountwindow)
        self.ac_bbottomframe = tkinter.Frame(self.accountwindow)
        self.ac_bbbottomframe = tkinter.Frame(self.accountwindow)

        # Creating Buttons
        self.returnbutton = tkinter.Button(self.ac_topframe, text='Return', command=self.return_to_mainwindow)
        self.ac_select_button = tkinter.Button(self.ac_bbbottomframe, text='Select', command=self.select_ac_info)
        self.ac_update_button = tkinter.Button(self.ac_bbbottomframe, text='Update Account', command=self.update_ac_info)
        self.pw_ac_update_button = tkinter.Button(self.ac_bbbottomframe, text='Update Password', command=self.pw_confirm)

        # Creating TreeView
        self.ac_info = ttk.Treeview(self.ac_midframe)
        self.ac_info['columns'] = ('User ID', 'User First Name', 'PW')

        self.ac_info.column('#0', width=0, anchor=tkinter.CENTER)
        self.ac_info.column('User ID', anchor=tkinter.CENTER, width=40)
        self.ac_info.column('User First Name', anchor=tkinter.CENTER, width=100)
        self.ac_info.column('PW', anchor=tkinter.CENTER, width=100)

        self.ac_info.heading('#0', text='', anchor=tkinter.CENTER)

        self.ac_info.heading('User ID', text='ID', anchor=tkinter.CENTER)
        self.ac_info.heading('User First Name', text='First Name', anchor=tkinter.CENTER)
        self.ac_info.heading('PW', text='Password', anchor=tkinter.CENTER)

        # Creating Labels and Entries
        self.ac_id_label = tkinter.Label(self.ac_bottomframe, text='ID')
        self.ac_id_label.grid(row=0, column=1, padx=60)

        self.firstnamelabel = tkinter.Label(self.ac_bottomframe, text='First Name')
        self.firstnamelabel.grid(row=0, column=2, padx=30)

        self.passwordlabel = tkinter.Label(self.ac_bottomframe, text='Password')
        self.passwordlabel.grid(row=0, column=3, padx=30)

        self.ID_entry = tkinter.Entry(self.ac_bbottomframe)
        self.ID_entry.grid(row=1, column=1)

        self.firstname_entry = tkinter.Entry(self.ac_bbottomframe)
        self.firstname_entry.grid(row=1, column=2)

        self.password_entry = tkinter.Entry(self.ac_bbottomframe)
        self.password_entry.grid(row=1, column=3)

        # Populating TreeView
        cur.execute("SELECT * FROM account")
        rows = cur.fetchall()

        for row in rows:
            print(row)
            self.ac_info.insert("", tkinter.END, values=row)

        # Packing Buttons
        self.returnbutton.pack()
        self.ac_select_button.pack(side='left', padx=10)
        self.ac_update_button.pack(side='left', padx=10)
        self.pw_ac_update_button.pack(side='left', padx=10)

        # Packing Treeview
        self.ac_info.pack()

        # Packing Frames
        self.ac_topframe.pack(anchor='ne')
        self.ac_midframe.pack()
        self.ac_bottomframe.pack()
        self.ac_bbottomframe.pack()
        self.ac_bbbottomframe.pack()

        # Closing connection
        conn.close()

        # Closing Mainwindow
        self.mainwindow.destroy()

    # Defining select_ac
    def select_ac_info(self):

        # Create focus variable
        selected = self.ac_info.focus()

        # creating items variable
        values = self.ac_info.item(selected, 'values')

        # Inserting information into entries
        self.ID_entry.insert(0, values[0])
        self.firstname_entry.insert(0, values[1])
        self.password_entry.insert(0, values[2])

    # defining update_ac
    def update_ac_info(self):

        # Connecting to Database
        conn = lite.connect('Recipe Database.db')

        cur = conn.cursor()

        # Creating focus and item variables
        selected = self.ac_info.focus()
        values = self.ac_info.item(selected, 'values')

        # Collecting items
        self.ac_info.item(selected, text='', values=(self.ID_entry.getint(values[0]), self.firstname_entry.get(),
                                                     self.password_entry.get()))

        # Updating Account
        cur.execute("""UPDATE Account SET 
        UserName = :Username
        where OID = :OID""",
        {'Username': self.firstname_entry.get(),
            'OID': self.ID_entry.get()})

        # Commiting and closing database
        conn.commit()
        conn.close()

        # Clearing Entries
        self.ID_entry.delete(0, tkinter.END)
        self.firstname_entry.delete(0, tkinter.END)
        self.password_entry.delete(0, tkinter.END)

    # Defining return
    def return_to_mainwindow(self):

        # MAking sure window is open then close it
        if self.accountwindow != 0:
            self.accountwindow.destroy()

        # calling main window
        Mainwindow()

    # def pw_confirm
    def pw_confirm(self):

        # Creating Window
        self.confirmation = tkinter.Tk()

        # Creating Frame
        self.cn_upper_frame = tkinter.Frame(self.confirmation)
        self.cn_bottom_frame = tkinter.Frame(self.confirmation)

        # Creating Labels
        self.CN_label = tkinter.Label(self.cn_upper_frame, text='Do you want to update your password?')

        # Creating Button
        self.CN_button = tkinter.Button(self.cn_bottom_frame, text='Confirm', command=self.pw_update)

        # Packing Label
        self.CN_label.pack()

        # PAcking Button
        self.CN_button.pack()

        # Packing Frames
        self.cn_upper_frame.pack()
        self.cn_bottom_frame.pack()

    # def pw_update
    def pw_update(self):

        # Connecting to database
        conn = lite.connect('Recipe Database.db')

        cur = conn.cursor()

        # Creating Focus and Item Variables
        selected = self.ac_info.focus()
        values = self.ac_info.item(selected, 'values')

        # Getting items
        self.ac_info.item(selected, text='', values=(self.ID_entry.getint(values[0]), self.firstname_entry.get(),
                                                     self.password_entry.get()))

        # Updateing the Password
        cur.execute("""UPDATE Account SET
        Password = :PW
        WHERE OID = :OID""",
        {'PW': self.password_entry.get(),
         'OID': self.ID_entry.get()})


        # Commiting and closing database
        conn.commit()
        conn.close()

        # Emptying entries
        self.ID_entry.delete(0, tkinter.END)
        self.firstname_entry.delete(0, tkinter.END)
        self.password_entry.delete(0, tkinter.END)

# Calling main Function
if __name__ == '__main__':
    run = Mainwindow()