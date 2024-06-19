import tkinter
import psycopg2
import customtkinter as ctk

# connect to database
conn = psycopg2.connect(host='xxxx', dbname='xxxx', user='xxxx',
                        password='xxxx', port=0000)

cur = conn.cursor()

# set up the customtkinter window
width = 900
height = 600
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
root = ctk.CTk()

root.geometry(f"{width}x{height}")
root.title("Window")

# creating the frames
main_menu = ctk.CTkFrame(master=root,
                         width=width,
                         height=height)
main_menu.grid(row=0, column=0)

edit_menu = ctk.CTkFrame(master=root,
                         width=width,
                         height=height)
edit_menu.grid(row=0, column=0)

add_menu = ctk.CTkFrame(master=root,
                        width=width,
                        height=height)
add_menu.grid(row=0, column=0)

delete_menu = ctk.CTkFrame(master=root,
                           width=width,
                           height=height)
delete_menu.grid(row=0, column=0)

search_menu = ctk.CTkFrame(master=root,
                           width=width,
                           height=height)
search_menu.grid(row=0, column=0)


def display_worker_labels():
    cur.execute("""SELECT * FROM worker;""")
    current_x = 400
    current_y = 150
    for w in cur:
        worker_label = ctk.CTkLabel(
            master=root,
            fg_color="#2FA572",
            text=f" ID = {w[0]} | Name: {w[1]} | Age: {w[2]} | Height: {w[3]}cm ",
            font=("Arial", 20),
            text_color="white"
        )
        worker_label.place(x=current_x, y=current_y)
        current_y += 30


def display_worker_buttons(frame, button_function):
    cur.execute("""SELECT * FROM worker;""")
    current_x = 400
    current_y = 150
    for w in cur:
        button_worker = ctk.CTkButton(
            frame,
            text=f" ID = {w[0]} | Name: {w[1]} | Age: {w[2]} | Height: {w[3]}cm ",
            font=("Cosmic Sans", 20),
            command=lambda worker=w: button_function(*worker)
        )
        button_worker.place(x=current_x, y=current_y)
        current_y += 30


def delete_worker(id, name, age, height):
    cur.execute(f"""DELETE FROM worker WHERE id = {id}""")
    for widget in delete_menu.winfo_children():
        widget.destroy()
    for widget in edit_menu.winfo_children():
        widget.destroy()

    create_edit_inputs()
    create_delete_menu_frame()


def create_edit_inputs():
    global name_input
    global age_input
    global height_input
    global current_id
    global button_submit_changes
    name_input = ctk.CTkEntry(edit_menu, width=120)
    name_input.place(x=100, y=125)
    age_input = ctk.CTkEntry(edit_menu, width=120)
    age_input.place(x=80, y=165)
    height_input = ctk.CTkEntry(edit_menu, width=120)
    height_input.place(x=105, y=205)
    current_id = None

    button_submit_changes = ctk.CTkButton(
        edit_menu,
        text="Submit changes",
        state=tkinter.DISABLED,
        corner_radius=8,
        height=35,
        width=140,
        font=("Cosmic Sans", 23),
        command=change_worker
    )
    button_submit_changes.place(x=30, y=300)


def change_worker():
    curr_name = name_input.get()
    curr_age = age_input.get()
    curr_height = height_input.get()
    cur.execute("""
        UPDATE worker 
        SET name = %s, age = %s, height = %s
        WHERE id = %s;
        """, (curr_name, curr_age, curr_height, current_id))

    for widget in edit_menu.winfo_children():
        widget.destroy()
    create_edit_inputs()
    create_edit_menu_frame()


create_edit_inputs()


def edit_worker(id, name, age, height):
    global current_id
    current_id = id
    name_input.delete(0, 'end')
    name_input.insert(0, name)
    age_input.delete(0, 'end')
    age_input.insert(0, age)
    height_input.delete(0, 'end')
    height_input.insert(0, height)
    button_submit_changes.configure(state=ctk.NORMAL)


def get_id_equal():
    id_dialog = ctk.CTkInputDialog(text="id =  ", title="id")
    input_id = id_dialog.get_input()
    cur.execute(f"""SELECT * FROM worker WHERE id = {input_id};""")

    create_search_menu_frame(cur)


def get_name_equal():
    name_dialog = ctk.CTkInputDialog(text="name =  ", title="name")
    input_name = name_dialog.get_input()
    cur.execute("SELECT * FROM worker WHERE name = %s;", (input_name,))

    create_search_menu_frame(cur)


def get_age_equal():
    age_dialog = ctk.CTkInputDialog(text="age =  ", title="age")
    input_age = age_dialog.get_input()
    cur.execute("SELECT * FROM worker WHERE age = %s;", (input_age,))

    create_search_menu_frame(cur)


def get_age_more():
    age_dialog = ctk.CTkInputDialog(text="age >  ", title="age")
    input_age = age_dialog.get_input()
    cur.execute("SELECT * FROM worker WHERE age > %s;", (input_age,))

    create_search_menu_frame(cur)


def get_age_less():
    age_dialog = ctk.CTkInputDialog(text="age <  ", title="age")
    input_age = age_dialog.get_input()
    cur.execute("SELECT * FROM worker WHERE age < %s;", (input_age,))

    create_search_menu_frame(cur)


def get_height_equal():
    height_dialog = ctk.CTkInputDialog(text="height =  ", title="height")
    input_height = height_dialog.get_input()
    cur.execute("SELECT * FROM worker WHERE height = %s;", (input_height,))

    create_search_menu_frame(cur)


def get_height_more():
    height_dialog = ctk.CTkInputDialog(text="height >  ", title="height")
    input_height = height_dialog.get_input()
    cur.execute("SELECT * FROM worker WHERE height > %s;", (input_height,))

    create_search_menu_frame(cur)


def get_height_less():
    height_dialog = ctk.CTkInputDialog(text="height <  ", title="height")
    input_height = height_dialog.get_input()
    cur.execute("SELECT * FROM worker WHERE height < %s;", (input_height,))

    create_search_menu_frame(cur)


def search_bar():
    search_dialog = ctk.CTkInputDialog(text="Search", title="SearchBar")
    input_query = search_dialog.get_input()
    query = "SELECT * FROM worker WHERE name LIKE %s"
    cur.execute(query, ('%' + input_query + '%',))

    create_search_menu_frame(cur)


def create_search_menu_frame(search_result):
    search_menu.tkraise()

    button1_menu = ctk.CTkButton(
        search_menu,
        text="Go back",
        corner_radius=8,
        height=45,
        width=180,
        font=("Cosmic Sans", 23),
        command=create_main_menu_frame
    )
    button1_menu.place(x=30, y=15)

    current_x = 250
    current_y = 150
    for w in search_result:
        worker_label = ctk.CTkLabel(
            master=root,
            fg_color="#2FA572",
            text=f" ID = {w[0]} | Name: {w[1]} | Age: {w[2]} | Height: {w[3]}cm ",
            font=("Arial", 20),
            text_color="white"
        )
        worker_label.place(x=current_x, y=current_y)
        current_y += 30


def create_main_buttons(frame_name):
    button1_menu = ctk.CTkButton(
        frame_name,
        text="Home",
        corner_radius=8,
        height=45,
        width=180,
        font=("Cosmic Sans", 23),
        command=create_main_menu_frame
    )
    button1_menu.place(x=30, y=15)

    # edit worker button
    button2_menu = ctk.CTkButton(
        frame_name,
        text="Edit",
        corner_radius=8,
        height=45,
        width=180,
        font=("Cosmic Sans", 23),
        command=create_edit_menu_frame
    )
    button2_menu.place(x=255, y=15)

    # add worker button
    button3_menu = ctk.CTkButton(
        frame_name,
        text="Add",
        corner_radius=8,
        height=45,
        width=180,
        font=("Cosmic Sans", 23),
        command=create_add_menu_frame
    )
    button3_menu.place(x=480, y=15)

    # delete worker button
    button4_menu = ctk.CTkButton(
        frame_name,
        text="Delete",
        corner_radius=8,
        height=45,
        width=180,
        font=("Cosmic Sans", 23),
        command=create_delete_menu_frame
    )
    button4_menu.place(x=700, y=15)


def create_main_menu_frame():
    main_menu.tkraise()
    create_main_buttons(main_menu)

    # creating the label for 'search by'
    search_by_label = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text=" Search by: ",
        font=("Arial", 22),
        text_color="white"
    )
    search_by_label.place(x=50, y=125)

    # creating the buttons for search
    button_id_equal = ctk.CTkButton(
        main_menu,
        text=" ID = ",
        corner_radius=8,
        height=25,
        width=90,
        font=("Cosmic Sans", 20),
        command=get_id_equal
    )
    button_id_equal.place(x=60, y=170)

    button_name_equal = ctk.CTkButton(
        main_menu,
        text="Name = ",
        corner_radius=8,
        height=25,
        width=90,
        font=("Cosmic Sans", 20),
        command=get_name_equal
    )
    button_name_equal.place(x=60, y=210)

    button_age_equal = ctk.CTkButton(
        main_menu,
        text="Age = ",
        corner_radius=8,
        height=25,
        width=90,
        font=("Cosmic Sans", 20),
        command=get_age_equal
    )
    button_age_equal.place(x=60, y=250)

    button_age_more = ctk.CTkButton(
        main_menu,
        text="Age > ",
        corner_radius=8,
        height=25,
        width=90,
        font=("Cosmic Sans", 20),
        command=get_age_more
    )
    button_age_more.place(x=60, y=290)

    button_age_less = ctk.CTkButton(
        main_menu,
        text="Age < ",
        corner_radius=8,
        height=25,
        width=90,
        font=("Cosmic Sans", 20),
        command=get_age_less
    )
    button_age_less.place(x=60, y=330)

    button_height_equal = ctk.CTkButton(
        main_menu,
        text="Height = ",
        corner_radius=8,
        height=25,
        width=90,
        font=("Cosmic Sans", 20),
        command=get_height_equal
    )
    button_height_equal.place(x=60, y=370)

    button_height_more = ctk.CTkButton(
        main_menu,
        text="Height > ",
        corner_radius=8,
        height=25,
        width=90,
        font=("Cosmic Sans", 20),
        command=get_height_more
    )
    button_height_more.place(x=60, y=410)

    button_height_less = ctk.CTkButton(
        main_menu,
        text="Height < ",
        corner_radius=8,
        height=25,
        width=90,
        font=("Cosmic Sans", 20),
        command=get_height_less
    )
    button_height_less.place(x=60, y=450)

    button_search = ctk.CTkButton(
        main_menu,
        text="Search for ",
        corner_radius=8,
        height=25,
        width=90,
        font=("Cosmic Sans", 20),
        command=search_bar
    )
    button_search.place(x=60, y=490)

    list_of_workers_label = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text=" List of workers ",
        font=("Arial", 25),
        text_color="white"
    )
    list_of_workers_label.place(x=520, y=105)

    display_worker_labels()


def create_edit_menu_frame():
    edit_menu.tkraise()
    create_main_buttons(edit_menu)

    list_of_workers_label_two = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text=" List of workers ",
        font=("Arial", 25),
        text_color="white"
    )
    list_of_workers_label_two.place(x=520, y=105)

    name_label = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text="  Name: ",
        font=("Arial", 22),
        text_color="white"
    )
    name_label.place(x=15, y=125)

    # name_input = ctk.CTkEntry(root, width=120)
    # name_input.place(x=100, y=125)

    age_label = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text="  Age: ",
        font=("Arial", 22),
        text_color="white"
    )
    age_label.place(x=15, y=165)

    height_label = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text="  Height: ",
        font=("Arial", 22),
        text_color="white"
    )
    height_label.place(x=15, y=205)

    display_worker_buttons(edit_menu, edit_worker)


def create_add_menu_frame():
    add_menu.tkraise()
    create_main_buttons(add_menu)

    id_label = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text="  Enter ID: ",
        font=("Arial", 22),
        text_color="white"
    )
    id_label.place(x=15, y=125)

    id_input = ctk.CTkEntry(root, width=120)
    id_input.place(x=125, y=125)

    name_label = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text="  Enter Name: ",
        font=("Arial", 22),
        text_color="white"
    )
    name_label.place(x=15, y=165)

    name_input = ctk.CTkEntry(root, width=120)
    name_input.place(x=160, y=165)

    age_label = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text="  Enter Age: ",
        font=("Arial", 22),
        text_color="white"
    )
    age_label.place(x=15, y=205)

    age_input = ctk.CTkEntry(root, width=120)
    age_input.place(x=140, y=205)

    height_label = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text="  Enter Height: ",
        font=("Arial", 22),
        text_color="white"
    )
    height_label.place(x=15, y=245)

    height_input = ctk.CTkEntry(root, width=120)
    height_input.place(x=165, y=245)

    list_of_workers_label_two = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text=" List of workers ",
        font=("Arial", 25),
        text_color="white"
    )
    list_of_workers_label_two.place(x=520, y=105)

    display_worker_labels()

    def add_worker():
        worker_id = id_input.get()
        worker_name = name_input.get()
        worker_age = age_input.get()
        worker_height = height_input.get()

        id_input.delete(0, 'end')
        name_input.delete(0, 'end')
        age_input.delete(0, 'end')
        height_input.delete(0, 'end')

        if worker_id and worker_name and worker_age and worker_height:
            cur.execute(
                """INSERT INTO worker (id, name, age, height) VALUES (%s, %s, %s, %s)""",
                (worker_id, worker_name, worker_age, worker_height)
            )

        display_worker_labels()

    button_add_worker = ctk.CTkButton(
        add_menu,
        text="Add worker",
        corner_radius=8,
        height=45,
        width=180,
        font=("Cosmic Sans", 23),
        command=add_worker
    )
    button_add_worker.place(x=30, y=320)


def create_delete_menu_frame():
    delete_menu.tkraise()
    create_main_buttons(delete_menu)

    list_of_workers_label_two = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text=" List of workers ",
        font=("Arial", 25),
        text_color="white"
    )
    list_of_workers_label_two.place(x=520, y=105)

    list_of_workers_label_two = ctk.CTkLabel(
        master=root,
        fg_color="#2B2B2B",
        text=" Click to delete ",
        font=("Arial", 30),
        text_color="white"
    )
    list_of_workers_label_two.place(x=70, y=160)

    display_worker_buttons(delete_menu, delete_worker)


create_main_menu_frame()


root.mainloop()

conn.commit()

cur.close()
conn.close()
