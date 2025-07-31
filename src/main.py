import tkinter as tk


def window_setup(window):
    window.geometry("780x780")
    window.title("Sensei-Zedle")


def update_listbox(search_var, data, listbox, *args):
    search_term = search_var.get().lower()
    listbox.delete(0, tk.END)
    for item in data:
        if search_term in item.lower():
            listbox.insert(tk.END, item)


def get_data():
    data = ['Apple', 'Banana', 'Grapes', 'Orange', 'Watermelon', 'Pineapple', 'Apple', 'Banana', 'Grapes', 'Orange', 'Watermelon', 'Pineapple', 'Apple', 'Banana', 'Grapes', 'Orange', 'Watermelon', 'Pineapple', 'Apple', 'Banana', 'Grapes', 'Orange', 'Watermelon', 'Pineapple']
    return data


def listbox_select(event, listbox, search_var):
    selected = listbox.curselection()
    if selected:
        value = listbox.get(selected[0])
        search_var.set(value)


def submit_guess(search_var, data, grid):
    print("Button clicked")
    new_item = search_var.get().strip()
    if new_item not in data:
        return
    print("Item in data")
    search_var.set("")
    return new_item

def setup_grid(frame, grid_list):
    for row in range(5):
        row_entries = []
        for col in range(5):
            e = tk.Entry(frame, state='readonly', width=10, justify="center")
            e.grid(row=row, column=col, padx=2, pady=2)
            row_entries.append(e)
        grid_list.append(row_entries)

def main():
    window = tk.Tk()
    window_setup(window)
    grid_frame = tk.Frame(window)

    data = get_data()
    grid_list = []
    

    listbox = tk.Listbox(window, width=30, height=10)
    listbox.bind("<<ListboxSelect>>", lambda event: listbox_select(event, listbox, search_var))
    
    search_var = tk.StringVar()
    search_var.trace_add("write", lambda *args: update_listbox(search_var, data, listbox, *args))
    
    guess_form = tk.Entry(window, textvariable=search_var, width=30)
    setup_grid(grid_frame, grid_list)

    submit_button = tk.Button(window, text="Submit", command=lambda:submit_guess(search_var, data, grid_list))


    guess_form.pack(pady=5)
    submit_button.pack(pady=5)
    listbox.pack(pady=10)
    grid_frame.pack(pady=10)

    
    update_listbox(search_var, data, listbox)
    window.mainloop()

if __name__ == "__main__":
    main()