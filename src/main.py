import tkinter as tk
import json
import random

class Sensei_Zedle():
    # --- GUI ---
    window = None
    grid_frame = None
    grid = None
    submit_button = None
    listbox = None
    search_var = None
    guess_form = None
    restart_button = None
    
    # --- Constants ---
    names = None
    categories = None
    categories_num = None
    full_data = None
    max_tries = None
    
    # --- Can change, related to game ---
    answer_data = None
    current_guess = None    # number

    # --- Can change, related to current guess ---
    guessed_name = None
    guessed_data = None
    similiarity = None

    def __init__(self, max_tries):
        self.grid = []
        self.current_guess = 0
        self.max_tries = max_tries

    def window_setup(self):
        self.window.geometry("780x780")
        self.window.title("Sensei-Zedle")

    def update_entry_text(self, entry, text):
        entry.config(state='normal')
        entry.delete(0, tk.END)
        entry.insert(0, text)
        entry.config(state='readonly')

    def update_guess_entry(self, entry, text, similiarity):
        self.update_entry_text(entry, text)
        if similiarity == 0:
            entry.config(readonlybackground="#FF0000", fg="#FFFFFF")
        elif similiarity == 0.5:
            entry.config(readonlybackground="#FFFF00", fg="#000000")
        elif similiarity == 1:
            entry.config(readonlybackground="#00FF00", fg="#000000")
        else:
            raise Exception("Similiarity is not acceptable value")
        return

    def listbox_select(self, event):
        selected = self.listbox.curselection()
        if selected:
            value = self.listbox.get(selected[0])
            self.search_var.set(value)

    def update_listbox(self, *args):
        search_term = self.search_var.get().lower()
        self.listbox.delete(0, tk.END)
        for item in self.names:
            if search_term in item.lower():
                self.listbox.insert(tk.END, item)

    def setup_grid(self):
        for row in range(self.max_tries + 1):
            row_entries = []
            for col in range(self.categories_num):
                e = tk.Entry(self.grid_frame, state='readonly', width=10, justify="center")
                e.grid(row=row, column=col, padx=2, pady=2)
                row_entries.append(e)
            self.grid.append(row_entries)

    def style_categories(self):
        categories_row = self.grid[0]       # first row in the grid is for categories
        for cat in categories_row:
            cat.config(readonlybackground="#000000", fg="#ffffff")

    def fill_grid_categories(self):
        categories_row = self.grid[0]       # first row in the grid is for categories
        for idx, category in enumerate(self.categories):
            self.update_entry_text(categories_row[idx], category)
        self.style_categories()

    def get_categories(self, path):
        with open(path) as file:
            self.categories = json.load(file)
        if self.categories is None:
            raise Exception("Can't get categories from data/categories")
        self.categories_num = len(self.categories)
        
    def get_data(self, path):
        with open(path) as file:
            self.full_data = json.load(file)
        self.names = [entry['Name'] for entry in self.full_data]

    def create_gui(self):
        self.window = tk.Tk()
        self.window_setup()
        self.grid_frame = tk.Frame(self.window)

        self.listbox = tk.Listbox(self.window, width=30, height=10)
        self.listbox.bind("<<ListboxSelect>>", self.listbox_select)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_listbox)

        self.guess_form = tk.Entry(self.window, textvariable=self.search_var, width=30)

        self.setup_grid()
        self.fill_grid_categories()

        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit_guess)

        self.restart_button = tk.Button(self.window, text="Restart", command=self.restart_game)

        self.guess_form.pack(pady=5)
        self.submit_button.pack(pady=5)
        self.listbox.pack(pady=10)
        self.grid_frame.pack(pady=10)
        self.restart_button.pack(pady=10)

        self.update_listbox()

    def choose_answer(self):
        self.answer_data = random.choice(self.full_data)

    def get_guess_data(self):
        self.guessed_data = None
        for item in self.full_data:
            self.guessed_data = item if item["Name"] == self.guessed_name else self.guessed_data
        if self.guessed_data is None:
            raise Exception("Guess does not exist in data_list, make_guess func")

    def display_guess(self):
        grid_row = self.grid[self.current_guess]
        for idx, category in enumerate(self.categories):
            self.update_guess_entry(grid_row[idx], self.guessed_data[category], self.similiarity[idx])

    def make_guess(self):
        self.current_guess += 1
        self.get_guess_data()
        self.similiarity = [0] * self.categories_num
        for idx, category in enumerate(self.categories):
            if self.guessed_data[category] in self.answer_data[category] or self.answer_data[category] in self.guessed_data[category]:
                self.similiarity[idx] = 0.5
            if self.guessed_data[category] == self.answer_data[category]:
                self.similiarity[idx] = 1
        self.display_guess()
        self.check_if_finished()
        self.guessed_name = None
        self.guessed_data = None
        self.similiarity = None
        
    def submit_guess(self):
        self.guessed_name = self.search_var.get().strip()
        if self.guessed_name not in self.names:
            return                          # Player cannot guess name that is not in database
        self.search_var.set("")
        self.make_guess()

    def check_if_finished(self):
        if sum(self.similiarity) == self.categories_num:
            self.stop_game()

    def reset_entry(self, entry):
        self.update_entry_text(entry, "")
        entry.config(readonlybackground="#FFFFFF", fg="#000000")

    def reset_grid(self):
        for row in self.grid[1:]:
            for entry in row:
                self.reset_entry(entry)

    def stop_game(self):
        print("Game stopped")
        self.submit_button.config(state="disabled")

    def restart_game(self):
        self.submit_button.config(state="active")
        self.reset_grid()
        self.choose_answer()
        self.current_guess = 0

    def start_game(self):
        self.get_categories('src/data/categories.json')
        self.get_data('src/data/sensei_ze.json')
        self.create_gui()
        self.restart_game()
        
        self.window.mainloop()

x = Sensei_Zedle(max_tries = 5)
x.start_game()
    
