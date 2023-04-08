import tkinter as tk
from tkinter import ttk
import PySimpleGUI as psgui
import customtkinter
import json
from

MAIN_COLOR = "#212121"
SEC_COLOR = "#373737"
THIRD_COLOR = "#A4A4A4"
FOURTH_COLOR = "#828282"
FONT_COLOR = "#242424"

with open('data.json', 'r') as data_file:
    try:
        data = json.load(data_file)
        if data == {}:
            data = {
                "Connections": [],
                "Queries": []
            }
            with open('data.json', 'w+') as _:
                json.dump(data, _)
    except:
        data = {
            "Connections": [],
            "Queries": []
        }
        with open('data.json', 'w+') as _:
            json.dump(data, _)


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Query Explainer")
        self.geometry("1200x800")

        # Main container that will hold the frames
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # Dictionary to store the frames
        self.frames = {}

        # Add frames to the dictionary
        for F in (Page1, Page2, Page3):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Page1)

    def show_frame(self, frame_class):
        self.frames[frame_class].destroy()
        self.frames[frame_class] = frame_class(self.container, self)
        self.frames[frame_class].grid(row=0, column=0)
        frame = self.frames[frame_class]
        frame.tkraise()


class Page1(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        # create the left container
        left_container = tk.Frame(self, width=300, height=800, bg=SEC_COLOR)
        left_container.pack(side="left", fill="both", expand=True)
        left_container.pack_propagate(0)

        # create the right container
        right_container = tk.Frame(self, width=900, height=800, bg=MAIN_COLOR)
        right_container.pack(side="right", fill="both", expand=True)
        right_container.pack_propagate(0)

        # add a label to the left container
        history_label = tk.Label(left_container, text="Your\nDatabases", bg=SEC_COLOR, font=("Arial", 32, "bold"),
                                 fg="white")
        history_label.pack(pady=10)

        # create a scrollable listbox widget
        history_listbox = tk.Listbox(left_container, bg=SEC_COLOR, font=("Arial", 20), fg=FONT_COLOR,
                                     selectmode="single", highlightthickness=0, borderwidth=0)
        history_listbox.pack(side="left", fill="both", expand=True)

        # create a scrollbar widget and link it to the listbox
        scrollbar = ttk.Scrollbar(left_container, orient="vertical", command=history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        history_listbox.configure(yscrollcommand=scrollbar.set)

        # reading the history
        with open('data.json', 'r') as f:
            d = json.load(f)
            connections = d['Connections']
            if len(connections) != 0:
                for i in range(len(connections)):
                    history_listbox.insert("end", f"{connections[i]['IP']}")
                    if i % 2 == 0:
                        history_listbox.itemconfig(i, {'bg': THIRD_COLOR})
                    else:
                        history_listbox.itemconfig(i, {'bg': FOURTH_COLOR})

        # create a function to handle clicks on the listbox items
        def handle_click(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                ip = event.widget.get(index)
                x = None
                with open('data.json', 'r') as _:
                    x = json.load(_)
                for t in x["Connections"]:
                    if t["IP"] == ip:

                        entries = get_entries()
                        for i in range(5):
                            entries[i].delete(0, tk.END)
                            entries[i].insert(0, t[list(t.keys())[i]])

        # bind the handle_click function to the listbox
        history_listbox.bind("<<ListboxSelect>>", handle_click)

        # create the right inner container
        right_inner_container = tk.Frame(right_container, width=600, height=800, bg=MAIN_COLOR)
        right_inner_container.pack(anchor="center")
        right_inner_container.pack_propagate(0)

        # add a label to the right container
        input_label = tk.Label(right_inner_container, text="Query Explainer", font=("Arial", 54, "bold"),
                               bg=MAIN_COLOR, fg="white")
        input_label.pack(pady=(30, 70))

        # create the right inner container
        right_inner2_container = tk.Frame(right_inner_container, width=600, bg=MAIN_COLOR,
                                          highlightbackground=SEC_COLOR, highlightthickness=2)
        right_inner2_container.pack(anchor="center")

        # add a label to the right container
        input_label = tk.Label(right_inner2_container, text="Enter the Connection Details:", font=("Arial", 28, "bold"),
                               bg=MAIN_COLOR, fg="white")
        input_label.pack(pady=(10, 30))

        # create the input rows
        rows = []
        label_names = ['Host IP', "Port Number", "Database Name", 'Username', "Password"]
        for i in range(5):
            row = tk.Frame(right_inner2_container, bg=MAIN_COLOR)
            row.pack(fill="x", padx=20, pady=5)

            label = tk.Label(row, text=f"{label_names[i] + ':'}", font=("Arial", 28, "bold"), bg=MAIN_COLOR, fg="white",
                             width=15, anchor="w")
            label.pack(side="left")

            entry = customtkinter.CTkEntry(master=row,
                                           width=300,
                                           height=45,
                                           text_color="white",
                                           font=("Arial", 28, "normal"),
                                           border_width=2,
                                           corner_radius=10)
            entry.pack(anchor=tk.E, side="right", fill="x", expand=True)

            rows.append((label, entry))

        # add a submit button
        submit_button = customtkinter.CTkButton(master=right_inner2_container,
                                                fg_color=SEC_COLOR,
                                                text="Submit",
                                                font=("Arial", 28, "bold"),
                                                hover_color=FOURTH_COLOR,
                                                text_color="white",
                                                command=lambda: submit_page1(controller))
        submit_button.pack(pady=10)

        # center the input rows within the right container
        for row in rows:
            row[0].pack_configure(anchor="center")
            row[1].pack_configure(anchor="center")

        def submit_page1(c):
            successful = True
            entries = get_entries()
            connection = {
                "IP": entries[0].get(),
                "Port": entries[1].get(),
                "Database": entries[2].get(),
                "Username": entries[3].get(),
                "Password": entries[4].get(),
            }
            print(connection)
            dat = None
            with open('data.json', 'r') as fil:
                dat = json.load(fil)
                if connection["IP"] in [x["IP"] for x in dat["Connections"]]:
                    successful = False
                else:
                    dat["Connections"].append(connection)

            with open('data.json', 'w+') as fil:
                json.dump(dat, fil)

            if successful:
                c.show_frame(Page2)
            else:
                print("Error")

        def get_entries():
            entries = [
                self.children['!frame2'].children['!frame'].children['!frame'].children['!frame'].children['!ctkentry']]
            for i in range(2, 6):
                entries.append(
                    self.children['!frame2'].children['!frame'].children['!frame'].children['!frame' + str(i)].children[
                        '!ctkentry'])
            return entries


class Page2(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # create the left container
        left_container = tk.Frame(self, width=300, height=800, bg=SEC_COLOR)
        left_container.pack(side="left", fill="both", expand=True)
        left_container.pack_propagate(0)

        # create the right container
        right_container = tk.Frame(self, width=900, height=800, bg=MAIN_COLOR)
        right_container.pack(side="right", fill="both", expand=True)
        right_container.pack_propagate(0)

        # add a label to the left container
        history_label = tk.Label(left_container, text="Previous\nQueries", bg=SEC_COLOR, font=("Arial", 32, "bold"),
                                 fg="white")
        history_label.pack(pady=10)

        # create a scrollable listbox widget
        history_listbox = tk.Listbox(left_container, bg=SEC_COLOR, font=("Arial", 20), fg=FONT_COLOR,
                                     selectmode="single", highlightthickness=0, borderwidth=0)
        history_listbox.pack(side="left", fill="both", expand=True)

        # create a scrollbar widget and link it to the listbox
        scrollbar = ttk.Scrollbar(left_container, orient="vertical", command=history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        history_listbox.configure(yscrollcommand=scrollbar.set)

        # add some items to the listbox
        for i in range(10):
            history_listbox.insert("end", f"Item {i + 1}")
            if i % 2 == 0:
                history_listbox.itemconfig(i, {'bg': THIRD_COLOR})
            else:
                history_listbox.itemconfig(i, {'bg': FOURTH_COLOR})

        # create a function to handle clicks on the listbox items
        def handle_click(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                value = event.widget.get(index)
                print(f"You clicked on item {index + 1}: {value}")

        # bind the handle_click function to the listbox
        history_listbox.bind("<<ListboxSelect>>", handle_click)

        # create the right inner container
        right_inner_container = tk.Frame(right_container, width=800, height=800, bg=MAIN_COLOR)
        right_inner_container.pack(anchor="center")
        right_inner_container.pack_propagate(0)

        # add a label to the right container
        input_label = tk.Label(right_inner_container, text="Enter the SQL Queries:", font=("Arial", 28, "bold"),
                               bg=MAIN_COLOR, fg="white")
        input_label.pack(pady=20)

        row = tk.Frame(right_inner_container, bg=MAIN_COLOR, width=650, height=50)
        row.pack(anchor="center", pady=20)
        row.pack_propagate(0)

        label = tk.Label(row, text="Query Name: ", font=("Arial", 28, "bold"), bg=MAIN_COLOR, fg="white", anchor="w")
        label.pack(side="left", fill="both", anchor="center")

        entry = customtkinter.CTkEntry(master=row,
                                       height=45,
                                       width=3000,
                                       text_color="white",
                                       font=("Arial", 28, "normal"),
                                       border_width=2,
                                       corner_radius=10)
        entry.pack(anchor=tk.E, side="right", expand=True)

        query1_container = tk.Frame(right_inner_container, width=800, height=300, bg=MAIN_COLOR)
        query1_container.pack(anchor="w")

        query1_label = tk.Label(query1_container, text="Query 1:", font=("Arial", 24, "bold"),
                                bg=MAIN_COLOR, fg="white")
        query1_label.pack(side="left", anchor="center", padx=(0, 20))

        query1_inner_container = tk.Frame(query1_container, width=800, height=245, bg=MAIN_COLOR,
                                          highlightbackground=FOURTH_COLOR, highlightthickness=2)
        query1_inner_container.pack(anchor="w")
        query1_inner_container.pack_propagate(0)
        query1_textbox = customtkinter.CTkTextbox(query1_inner_container,
                                                  width=800, height=245,
                                                  fg_color=MAIN_COLOR,
                                                  font=("Courier", 16, "normal"))
        query1_textbox.pack()

        query2_container = tk.Frame(right_inner_container, width=800, height=300, bg=MAIN_COLOR)
        query2_container.pack(anchor="w", pady=(30, 0))

        query2_label = tk.Label(query2_container, text="Query 2:", font=("Arial", 24, "bold"),
                                bg=MAIN_COLOR, fg="white")
        query2_label.pack(side="left", anchor="center", padx=(0, 20))

        query2_inner_container = tk.Frame(query2_container, width=800, height=245, bg=MAIN_COLOR,
                                          highlightbackground=FOURTH_COLOR, highlightthickness=2)
        query2_inner_container.pack(anchor="w")
        query2_inner_container.pack_propagate(0)

        query2_textbox = customtkinter.CTkTextbox(query2_inner_container,
                                                  fg_color=MAIN_COLOR,
                                                  width=800, height=245,
                                                  font=("Courier", 16, "normal"))
        query2_textbox.pack()

        database_back_button = customtkinter.CTkButton(master=right_inner_container,
                                                       fg_color=SEC_COLOR,
                                                       text="Back to Connection",
                                                       font=("Arial", 28, "bold"),
                                                       hover_color=FOURTH_COLOR,
                                                       text_color="white",
                                                       command=lambda: controller.show_frame(Page1))
        database_back_button.pack(side="left", anchor="s", pady=(0, 35))

        submit_button = customtkinter.CTkButton(master=right_inner_container,
                                                fg_color=SEC_COLOR,
                                                text="Execute",
                                                font=("Arial", 28, "bold"),
                                                hover_color=FOURTH_COLOR,
                                                text_color="white",
                                                command=lambda: controller.show_frame(Page3))
        submit_button.pack(side="right", anchor="s", pady=(0, 35))


class Page3(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        container = tk.Frame(self, width=1200, height=800, bg=MAIN_COLOR)
        container.pack(side="left", fill="both", expand=True)
        container.pack_propagate(0)

        first_inner_container = tk.Frame(container, width=1100, height=420, bg=MAIN_COLOR)
        first_inner_container.pack(anchor="center", pady=(0, 20))
        first_inner_container.pack_propagate(0)

        input_label = tk.Label(first_inner_container, text="Query Comparison:", font=("Arial", 28, "bold"),
                               bg=MAIN_COLOR, fg="white")
        input_label.pack(pady=20)

        trees_container = tk.Frame(first_inner_container, bg=MAIN_COLOR, width=1100, height=600,
                                   highlightbackground="white", highlightthickness=2)
        trees_container.pack(pady=0)
        trees_container.pack_propagate(0)

        q1_container = tk.Frame(trees_container, bg="green", width=1100 / 2, height=600)
        q1_container.pack(side="left")
        q1_container.pack_propagate(0)

        q2_container = tk.Frame(trees_container, bg="yellow", width=1100 / 2, height=600)
        q2_container.pack(side="right")
        q2_container.pack_propagate(0)

        q1_label = tk.Label(q1_container, text="Query 1:", font=("Arial", 28, "bold"), borderwidth=5,
                            bg=MAIN_COLOR, fg="white", width=100)
        q1_label.pack(side="top")

        q2_label = tk.Label(q2_container, text="Query 2:", font=("Arial", 28, "bold"), borderwidth=5,
                            bg=MAIN_COLOR, fg="white", width=100)
        q2_label.pack(side="top")

        differance_message = tk.Label(container, text="Explanation of the Query Comparison:",
                                      font=("Arial", 28, "bold"), bg=MAIN_COLOR, fg="white")
        differance_message.pack(anchor="w", padx=50)

        message_container = tk.Frame(container, bg=MAIN_COLOR, highlightthickness=2, highlightbackground="white")
        message_container.pack(padx=50, fill="both")

        comparison_message = customtkinter.CTkTextbox(message_container, fg_color=MAIN_COLOR)
        comparison_message.configure(state="disabled")
        comparison_message.pack(fill="both")

        database_back_button = customtkinter.CTkButton(master=container,
                                                       fg_color=SEC_COLOR,
                                                       text="Enter Another Queries",
                                                       font=("Arial", 28, "bold"),
                                                       hover_color=FOURTH_COLOR,
                                                       text_color="white",
                                                       command=lambda: controller.show_frame(Page2))
        database_back_button.pack(side="left", anchor="s", padx=(50, 0), pady=(0, 30))

        submit_button = customtkinter.CTkButton(master=container,
                                                fg_color=SEC_COLOR,
                                                text="Go to Connection",
                                                font=("Arial", 28, "bold"),
                                                hover_color=FOURTH_COLOR,
                                                text_color="white",
                                                command=lambda: controller.show_frame(Page1))
        submit_button.pack(side="right", anchor="s", padx=(0, 50), pady=(0, 30))


if __name__ == "__main__":
    app = MainApplication()
    app.show_frame(Page1)
    app.mainloop()
