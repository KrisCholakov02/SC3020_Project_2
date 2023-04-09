import json
import tkinter as tk
from tkinter import ttk

import customtkinter
import sqlvalidator

from explain import *

MAIN_COLOR = "#212121"
SEC_COLOR = "#373737"
THIRD_COLOR = "#A4A4A4"
FOURTH_COLOR = "#828282"
FONT_COLOR = "#242424"

CONNECTION = None
CONNECTION_NAME = None
QUERY1 = None
QUERY2 = None
QUERY1_TREE = None
QUERY2_TREE = None
COMP_RESULT = None

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
            "Queries": {}
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
                                     selectmode="single", highlightthickness=5, borderwidth=0,
                                     highlightcolor=SEC_COLOR, )
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
                    history_listbox.insert("end", "   " + f"{connections[i]['IP']}")
                    if i % 2 == 0:
                        history_listbox.itemconfig(i, {'bg': THIRD_COLOR})
                    else:
                        history_listbox.itemconfig(i, {'bg': FOURTH_COLOR})

        # create a function to handle clicks on the listbox items
        def handle_click(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                ip = event.widget.get(index)[3:]
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
                                           fg_color=SEC_COLOR,
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
            entries = get_entries()
            connection = {
                "IP": entries[0].get(),
                "Port": entries[1].get(),
                "Database": entries[2].get(),
                "Username": entries[3].get(),
                "Password": entries[4].get(),
            }
            with open('data.json', 'r') as fil:
                dat = json.load(fil)
                if not (connection["IP"] in [x["IP"] for x in dat["Connections"]]):
                    dat["Connections"].append(connection)
                    dat["Queries"][connection["IP"]] = []
                else:
                    for i in range(len(dat["Connections"])):
                        if dat["Connections"][i]["IP"] == connection["IP"]:
                            dat["Connections"][i] = connection
                            break

            with open('data.json', 'w+') as fil:
                json.dump(dat, fil)

            try:
                global CONNECTION
                CONNECTION = PostgresDB(connection["IP"], connection["Port"], connection["Database"],
                                        connection["Username"], connection["Password"])
                global CONNECTION_NAME
                CONNECTION_NAME = connection["IP"]
                print(CONNECTION_NAME)
                c.show_frame(Page2)
            except:
                connection_status_label = tk.Label(right_inner_container, text="Invalid Connection",
                                                   font=("Arial", 54, "bold"),
                                                   bg=MAIN_COLOR, fg="red")
                connection_status_label.pack(anchor="center", pady=(30, 70))
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

        # reading the history
        with open('data.json', 'r') as f:
            d = json.load(f)
            queries = d['Queries']
            if queries != {}:
                try:
                    current_queries = queries[CONNECTION_NAME]
                    for i in range(len(current_queries)):
                        history_listbox.insert("end", "   " + f"{current_queries[i][0]}")
                        if i % 2 == 0:
                            history_listbox.itemconfig(i, {'bg': THIRD_COLOR})
                        else:
                            history_listbox.itemconfig(i, {'bg': FOURTH_COLOR})
                except:
                    pass

        # create a function to handle clicks on the listbox items
        def handle_click(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                name = event.widget.get(index)[3:]
                x = None
                with open('data.json', 'r') as _:
                    x = json.load(_)
                for t in x["Queries"][CONNECTION_NAME]:
                    if t[0] == name:
                        entries = get_entries()
                        for a in range(3):
                            if a == 0:
                                entries[a].delete(0, tk.END)
                                entries[a].insert(0, t[a])
                            else:
                                entries[a].delete(1.0, tk.END)
                                entries[a].insert(1.0, t[a])

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
                                       fg_color=SEC_COLOR,
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
                                                command=lambda: submit_page2())
        submit_button.pack(side="right", anchor="s", pady=(0, 35))

        def submit_page2():
            entries = get_entries()
            query_cop = [
                entries[0].get(),
                entries[1].get(1.0, "end-1c"),
                entries[2].get(1.0, "end-1c"),
            ]
            with open('data.json', 'r') as fil:
                dat = json.load(fil)
                print(CONNECTION_NAME)
                if not (query_cop[0] in [x[0] for x in dat["Queries"][CONNECTION_NAME]]):
                    dat["Queries"][CONNECTION_NAME].append(query_cop)
                else:
                    for i in range(len(dat["Queries"][CONNECTION_NAME])):
                        if dat["Queries"][CONNECTION_NAME][i][0] == query_cop[0]:
                            dat["Queries"][CONNECTION_NAME][i] = query_cop
                            break

            with open('data.json', 'w+') as fil:
                json.dump(dat, fil)

            global QUERY1
            global QUERY2
            QUERY1 = entries[1].get(1.0, "end-1c").replace("\n", " ")
            QUERY2 = entries[2].get(1.0, "end-1c").replace("\n", " ")
            try:
                query_p1 = sqlvalidator.parse(QUERY1)
                query_p2 = sqlvalidator.parse(QUERY2)
                if query_p1.is_valid() and query_p2.is_valid():
                    try:
                        CONNECTION.explain_differences(QUERY1, QUERY2)
                        controller.show_frame(Page3)
                    except:
                        tk.messagebox.showerror("Error", "Not Queries for the Chosen Connection")
                else:
                    tk.messagebox.showerror("Error", "Invalid SQL Query")
            except Exception as e:
                tk.messagebox.showerror("Error", "Invalid SQL Query\n" + str(e))

        def get_entries():
            entries = [
                self.children['!frame2'].children['!frame'].children['!frame'].children['!ctkentry'],
                self.children['!frame2'].children['!frame'].children['!frame2'].children['!frame'].children[
                    '!ctktextbox'],
                self.children['!frame2'].children['!frame'].children['!frame3'].children['!frame'].children[
                    '!ctktextbox']
            ]
            return entries


class Page3(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        try:
            if CONNECTION is not None:
                global COMP_RESULT
                COMP_RESULT = CONNECTION.explain_differences(QUERY1, QUERY2)
                q1_tree = CONNECTION.qepTreeGenerator(QUERY1)
                q2_tree = CONNECTION.qepTreeGenerator(QUERY2)
                global QUERY1_TREE
                QUERY1_TREE = q1_tree
                global QUERY2_TREE
                QUERY2_TREE = q2_tree
        except Exception as e:
            tk.messagebox.showerror("Error", "Error in Query Comparison\n" + str(e))
            pass

        container = tk.Frame(self, width=1200, height=800, bg=MAIN_COLOR)
        container.pack(side="left", fill="both", expand=True)
        container.pack_propagate(0)

        first_inner_container = tk.Frame(container, width=1100, height=510, bg=MAIN_COLOR)
        first_inner_container.pack(anchor="center", pady=(0, 20))
        first_inner_container.pack_propagate(0)

        input_label = tk.Label(first_inner_container, text="Query Comparison:", font=("Arial", 28, "bold"),
                               bg=MAIN_COLOR, fg="white")
        input_label.pack(pady=20)

        trees_container = tk.Frame(first_inner_container, bg=MAIN_COLOR, width=1100, height=800,
                                   highlightbackground=THIRD_COLOR, highlightthickness=2, highlightcolor=THIRD_COLOR)
        trees_container.pack(pady=0)
        trees_container.pack_propagate(0)

        q1_container = tk.Frame(trees_container, bg=MAIN_COLOR, width=1100 / 2, height=1700, highlightthickness=1,
                                highlightcolor=THIRD_COLOR, highlightbackground=THIRD_COLOR)
        q1_container.pack(side="left")
        q1_container.pack_propagate(0)

        q2_container = tk.Frame(trees_container, bg=MAIN_COLOR, width=1100 / 2, height=1700, highlightthickness=1,
                                highlightcolor=THIRD_COLOR, highlightbackground=THIRD_COLOR)
        q2_container.pack(side="right")
        q2_container.pack_propagate(0)

        q1_label = tk.Label(q1_container, text="Query 1:", font=("Arial", 28, "bold"), borderwidth=5,
                            bg=MAIN_COLOR, fg="white", width=100)
        q1_label.pack(side="top")

        def get_tree_depth(tree):
            if tree is None:
                return 0
            if "children" not in list(tree.keys()):
                return 1
            else:
                if len(tree['children']) == 2:
                    return 1 + max(get_tree_depth(tree['children'][0]), get_tree_depth(tree['children'][1]))
                else:
                    return 1 + get_tree_depth(tree['children'][0])

        center_x = 1000
        rectangle_width = 100
        rectangle_height = 50
        levels_padding = 50
        notes_padding = 20

        def draw_node(canvas, x1, y1, text):
            rectangle = canvas.create_rectangle(x1, y1, x1 + rectangle_width, y1 + rectangle_height, fill="white",
                                                width=2,
                                                outline="black")
            rectangle_text = canvas.create_text((x1 + x1 + rectangle_width) / 2, (y1 + y1 + rectangle_height) / 2,
                                                text=text, font=("Arial", 12, "bold"),
                                                fill="black")
            canvas.itemconfig(rectangle)
            canvas.itemconfig(rectangle_text)

        def draw_tree(tree, canvas: tk.Canvas, x1=center_x - rectangle_width / 2, y1=levels_padding):
            current_node = tree['name']
            print(x1, y1)
            draw_node(canvas, x1, y1, current_node)
            if 'children' in list(tree.keys()):
                print("here")
                if len(tree['children']) == 1:
                    line1 = canvas.create_line(x1 + rectangle_width / 2, y1 + rectangle_height, x1 + rectangle_width / 2,
                                               y1 + levels_padding + rectangle_height, fill="black", width=2)
                    canvas.itemconfig(line1)
                    draw_tree(tree['children'][0], canvas, x1, y1 + levels_padding + rectangle_height)
                else:
                    if x1 == center_x - rectangle_width / 2:
                        b = 20
                    else:
                        b = 0
                    line1 = canvas.create_line(x1 + rectangle_width / 2, y1 + rectangle_height, x1 - b + 0.5 * rectangle_width - notes_padding * ((get_tree_depth(tree) - 3) ** 2) - ((get_tree_depth(tree) - 2) ** 2) * rectangle_width + rectangle_width / 2,
                                               y1 + levels_padding + rectangle_height, fill="black", width=2)
                    line2 = canvas.create_line(x1 + rectangle_width / 2, y1 + rectangle_height, x1 + b - 0.5 * rectangle_width + notes_padding * ((get_tree_depth(tree) - 3) ** 2) + ((get_tree_depth(tree) - 2) ** 2) * rectangle_width + rectangle_width / 2,
                                               y1 + levels_padding + rectangle_height, fill="black", width=2)
                    canvas.itemconfig(line1)
                    canvas.itemconfig(line2)

                    draw_tree(tree['children'][0], canvas, x1 - b + 0.5 * rectangle_width - notes_padding * ((get_tree_depth(tree) - 3) ** 2) - ((get_tree_depth(tree) - 2) ** 2) * rectangle_width, y1 + levels_padding + rectangle_height)
                    draw_tree(tree['children'][1], canvas, x1 + b - 0.5 * rectangle_width + notes_padding * ((get_tree_depth(tree) - 3) ** 2) + ((get_tree_depth(tree) - 2) ** 2) * rectangle_width, y1 + levels_padding + rectangle_height)

        q1_frame = tk.Frame(q1_container, bg="white", width=1100 / 2, height=280, highlightthickness=0, )
        q1_frame.pack()
        q1_frame.pack_propagate(0)

        q1_canvas = tk.Canvas(q1_frame, width=1100 / 2, height=280, bg="white", borderwidth=0, highlightthickness=0,
                              scrollregion=(0, 0, 2000, 2000))
        q1_scroll_y = tk.Scrollbar(q1_frame, orient="vertical", command=q1_canvas.yview)
        q1_scroll_x = tk.Scrollbar(q1_frame, orient="horizontal", command=q1_canvas.xview)

        q1_canvas.configure(yscrollcommand=q1_scroll_y.set, xscrollcommand=q1_scroll_x.set)

        q1_scroll_y.pack(side='right', fill='y')
        q1_scroll_x.pack(side='bottom', fill='x')
        q1_canvas.xview_moveto(0.365)
        q1_canvas.pack(side="left", fill="both", expand=True)
        if QUERY1_TREE is not None:
            draw_tree(QUERY1_TREE, q1_canvas)

        q2_label = tk.Label(q2_container, text="Query 2:", font=("Arial", 28, "bold"), borderwidth=5,
                            bg=MAIN_COLOR, fg="white", width=100)
        q2_label.pack(side="top")

        q2_frame = tk.Frame(q2_container, bg="white", width=1100 / 2, height=280, highlightthickness=0, )
        q2_frame.pack()
        q2_frame.pack_propagate(0)

        q2_canvas = tk.Canvas(q2_frame, width=1100 / 2, height=280, bg="white", borderwidth=0, highlightthickness=0,
                              scrollregion=(0, 0, 2000, 2000))
        q2_scroll_y = tk.Scrollbar(q2_frame, orient="vertical", command=q2_canvas.yview)
        q2_scroll_x = tk.Scrollbar(q2_frame, orient="horizontal", command=q2_canvas.xview)

        q2_canvas.configure(yscrollcommand=q2_scroll_y.set, xscrollcommand=q2_scroll_x.set)

        q2_scroll_y.pack(side='right', fill='y')
        q2_scroll_x.pack(side='bottom', fill='x')
        q2_canvas.xview_moveto(0.365)
        q2_canvas.pack(side="left", fill="both", expand=True)
        if QUERY2_TREE is not None:
            draw_tree(QUERY2_TREE, q2_canvas)

        q1_label2 = tk.Label(q1_container, text="QEP Structure", font=("Arial", 12), borderwidth=5,
                             bg=MAIN_COLOR, fg="white", width=100)
        q1_label2.pack(pady=0)

        q1_structure_textbox = customtkinter.CTkTextbox(q1_container, fg_color=MAIN_COLOR,
                                                        font=("Courier", 12, "normal"))
        if QUERY1_TREE is not None:
            q1_structure_textbox.insert(1.0, str(QUERY1_TREE))
        q1_structure_textbox.configure(state="disabled")
        q1_structure_textbox.pack(fill="both")

        q2_label2 = tk.Label(q2_container, text="QEP Structure", font=("Arial", 12), borderwidth=5,
                             bg=MAIN_COLOR, fg="white", width=100)
        q2_label2.pack(pady=0)

        q2_structure_textbox = customtkinter.CTkTextbox(q2_container, fg_color=MAIN_COLOR,
                                                        font=("Courier", 12, "normal"))
        if QUERY2_TREE is not None:
            q2_structure_textbox.insert(1.0, str(QUERY2_TREE))
        q2_structure_textbox.configure(state="disabled")
        q2_structure_textbox.pack(fill="both")

        differance_message = tk.Label(container, text="Explanation of the Query Comparison:",
                                      font=("Arial", 28, "bold"), bg=MAIN_COLOR, fg="white")
        differance_message.pack(anchor="w", padx=50)

        message_container = tk.Frame(container, bg=MAIN_COLOR, highlightthickness=2, highlightbackground="white",
                                     width=1100 / 3 * 2, height=200)
        message_container.pack(side='left', padx=(50, 0), anchor='n')
        message_container.pack_propagate(0)

        comparison_message = customtkinter.CTkTextbox(message_container, fg_color=MAIN_COLOR,
                                                      font=("Courier", 12, "normal"))
        comparison_message.insert(1.0, str(COMP_RESULT))
        comparison_message.configure(state="disabled")
        comparison_message.pack(fill="both")

        buttons_container = tk.Frame(container, bg=MAIN_COLOR, width=1100 / 3 * 1, height=200)
        buttons_container.pack(side='right', padx=(0, 50), anchor='n')
        buttons_container.pack_propagate(0)

        database_back_button = customtkinter.CTkButton(master=buttons_container,
                                                       fg_color=SEC_COLOR,
                                                       text="Enter Another Queries",
                                                       font=("Arial", 28, "bold"),
                                                       hover_color=FOURTH_COLOR,
                                                       text_color="white",
                                                       command=lambda: controller.show_frame(Page2))
        database_back_button.pack(side="top", anchor="center", pady=(30, 30))

        submit_button = customtkinter.CTkButton(master=buttons_container,
                                                fg_color=SEC_COLOR,
                                                text="Go to Connection",
                                                font=("Arial", 28, "bold"),
                                                hover_color=FOURTH_COLOR,
                                                text_color="white",
                                                command=lambda: controller.show_frame(Page1))
        submit_button.pack(side="bottom", anchor="center", pady=(0, 30))


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = MainApplication()
    app.show_frame(Page3)
    app.mainloop()
