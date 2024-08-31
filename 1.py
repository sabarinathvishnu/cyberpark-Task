import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class ShoppingListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping List App")


        self.categories = ["Electronics"]


        self.items = self.load_list()


        self.create_widgets()
        self.update_listbox()

    def create_widgets(self):

        self.item_entry = tk.Entry(self.root, width=50)
        self.item_entry.pack(pady=10)


        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(self.root, text="Remove Item", command=self.remove_item)
        self.remove_button.pack(pady=5)

        self.clear_button = tk.Button(self.root, text="Clear List", command=self.clear_list)
        self.clear_button.pack(pady=5)

        self.edit_button = tk.Button(self.root, text="Edit Item", command=self.edit_item)
        self.edit_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save List", command=self.save_list)
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(self.root, text="Load List", command=self.load_list)
        self.load_button.pack(pady=5)

        self.listbox = tk.Listbox(self.root, width=50, height=10)
        self.listbox.pack(pady=10)

        self.category_var = tk.StringVar(self.root)
        self.category_var.set(self.categories[0])  # Set default value
        self.category_menu = tk.OptionMenu(self.root, self.category_var, *self.categories)
        self.category_menu.pack(pady=5)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.items:
            display_text = f"{item['name']} - {item['category']}"
            self.listbox.insert(tk.END, display_text)

    def add_item(self):
        item_name = self.item_entry.get().strip()
        if item_name:
            category = self.category_var.get()
            self.items.append({'name': item_name, 'category': category})
            self.item_entry.delete(0, tk.END)
            self.update_listbox()
            self.show_message("Item added successfully!")
        else:
            self.show_message("Error: Item cannot be empty.")

    def remove_item(self):
        try:
            selected_index = self.listbox.curselection()[0]
            del self.items[selected_index]
            self.update_listbox()
            self.show_message("Item removed successfully!")
        except IndexError:
            self.show_message("Error: No item selected.")

    def clear_list(self):
        self.items.clear()
        self.update_listbox()
        self.show_message("List cleared!")

    def edit_item(self):
        try:
            selected_index = self.listbox.curselection()[0]
            current_item = self.items[selected_index]
            new_name = simpledialog.askstring("Edit Item", "Enter new item name:", initialvalue=current_item['name'])
            if new_name:
                new_category = simpledialog.askstring("Edit Item", "Enter new category:", initialvalue=current_item['category'])
                if new_category:
                    self.items[selected_index] = {'name': new_name, 'category': new_category}
                    self.update_listbox()
                    self.show_message("Item updated successfully!")
        except IndexError:
            self.show_message("Error: No item selected.")

    def save_list(self):
        with open("shopping_list.json", "w") as file:
            json.dump(self.items, file)
        self.show_message("List saved successfully!")

    def load_list(self):
        try:
            with open("shopping_list.json", "r") as file:
                items = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            items = []
        return items

    def show_message(self, message):
        messagebox.showinfo("Info", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingListApp(root)
    root.mainloop()
