import tkinter as tk
# from PIL import Image, ImageTk
from Behavior import Behavior

actions = Behavior()


def run():
    root.mainloop()


objects_list = []
point = None
hierarchy_widgets = []
active_object = None
objects_list_closed = True


def create_object(element):
    prts = element.get_parameters()
    parameters = ()
    coordinates = ()
    count = 0

    def get_coordinates(str_x, str_y, number):
        x, y = str_x.get(), str_y.get()
        try:
            x = int(x)
        except ValueError:
            try:
                x = float(x)
            except ValueError:
                str_x.delete(0, tk.END)
                return
        try:
            y = int(y)
        except ValueError:
            try:
                y = float(y)
            except ValueError:
                str_y.delete(0, tk.END)
                return
        actions.set_coordinates(number, (x, y))

    while count != prts[0]:
        if not count:
            frame = tk.Frame(master=fr_his_prts, bg="yellow")
        else:
            frame = tk.Frame(master=fr_his_prts)
        frame.pack()
        parameters += (frame,)
        lb = tk.Label(master=frame, text="x:")
        lb.grid(row=0, column=0, padx=1, pady=2)
        entry_x = tk.Entry(master=frame, width=10)
        entry_x.grid(row=0, column=1, padx=1, pady=2)
        lb = tk.Label(master=frame, text="y:")
        lb.grid(row=0, column=2, padx=1, pady=2)
        entry_y = tk.Entry(master=frame, width=10)
        entry_y.grid(row=0, column=3, padx=1, pady=2)
        entry_x.bind("<Return>", lambda event, en_x=entry_x, en_y=entry_y, n=count: get_coordinates(en_x, en_y, n))
        entry_y.bind("<Return>", lambda event, en_x=entry_x, en_y=entry_y, n=count: get_coordinates(en_x, en_y, n))
        coordinates += ((entry_x, entry_y),)
        count += 1
    if prts[1]:
        frame = tk.Frame(master=fr_his_prts)
        frame.pack()
        parameters += (frame,)

        def plus_coord():
            nonlocal count
            now_frame = tk.Frame(master=fr_his_prts)
            now_frame.pack()
            label = tk.Label(master=now_frame, text="x:")
            label.grid(row=0, column=0, padx=1, pady=2)
            enx = tk.Entry(master=now_frame, width=10)
            enx.grid(row=0, column=1, padx=1, pady=2)
            label = tk.Label(master=now_frame, text="y:")
            label.grid(row=0, column=2, padx=1, pady=2)
            eny = tk.Entry(master=now_frame, width=10)
            eny.grid(row=0, column=3, padx=1, pady=2)
            enx.bind("<Return>", lambda event, en_x=enx, en_y=eny, n=count: get_coordinates(en_x, en_y, n))
            eny.bind("<Return>", lambda event, en_x=enx, en_y=eny, n=count: get_coordinates(en_x, en_y, n))
            actions.new_coord(now_frame, (enx, eny))
            count += 1

        def minus_coord():
            widget = actions.del_coord()
            if widget is not None:
                nonlocal count
                count -= 1
                widget.destroy()

        bt = tk.Button(master=frame, text="+coord", command=plus_coord)
        bt.grid(row=0, column=0)
        bt = tk.Button(master=frame, text="-coord", command=minus_coord)
        bt.grid(row=0, column=1)

    # Create coord parameters

    def get_const(key, widgets):
        text = widgets[1].get()
        try:
            text = int(text)
        except ValueError:
            try:
                text = float(text)
            except ValueError:
                widgets[1].delete(0, tk.END)
                if element.consts[key] is not None:
                    widgets[1].insert(0, element.consts[key])
                return
        if key in element.consts:
            del element.consts[key]
        element.consts[key] = text
        if widgets[0] is not None:
            widgets[0].config(fg="black")
            widgets[1].bind("<Return>", lambda event, key_=key, w_=(None, widgets[1]): get_const(key_, w_))

    for parameter in prts[2]:
        frame = tk.Frame(master=fr_his_prts)
        frame.pack()
        parameters += (frame,)
        lb = tk.Label(master=frame, text=parameter + ":", fg="gray")
        lb.grid(row=0, column=0, padx=1, pady=2)
        entry = tk.Entry(master=frame, width=10)
        entry.grid(row=0, column=1, padx=1, pady=2)
        entry.bind("<Return>", lambda event, key=parameter, widgets=(lb, entry): get_const(key, widgets))
    # Create constants parameters
    global hierarchy_widgets
    lb = tk.Label(master=fr_hierarchy, text=element.str(), fg="gray")
    lb.grid(row=len(hierarchy_widgets), column=0)

    def open_():
        actions.open_object(element, lb)
        lb.focus_set()

    lb.bind("<Button-1>", lambda event: open_())
    lb.bind("<BackSpace>", lambda event: actions.destroy_object())
    hierarchy_widgets.append(lb)
    # update hierarchy
    if prts[1]:
        return parameters, coordinates, plus_coord, minus_coord, lb
    else:
        return parameters, coordinates, lb


def next_coord(index, coord, entry_widgets):
    for i in range(2):
        entry_widgets[index][i].delete(0, tk.END)
        entry_widgets[index][i].insert(0, str(coord[i]))


def open_object(new_prts, old_prts, picture):
    for widget in old_prts:
        widget.pack_forget()
    for widget in new_prts:
        widget.pack()
    global active_object
    if active_object is not None:
        active_object.config(bg="white")
    picture.focus_set()
    root.update()
    active_object = picture
    active_object.config(bg="blue")
    entry_for_name.delete(0, tk.END)
    entry_for_name.insert(0, active_object["text"])


def delete_object(widgets):
    for widget in widgets:
        widget.destroy()
    global active_object
    active_object.destroy()
    active_object = None


def create_objects_list(objects):
    for element in objects:
        objects_list.append(tk.Button(master=fr21, text=element.str(),
                                      command=lambda obj=element: actions.create_object(obj)))


root = tk.Tk()
fr1 = tk.Frame(bg='gray')
fr1.pack(fill=tk.X)
fr2 = tk.Frame()
fr2.pack(fill=tk.BOTH, expand=True)
fr3 = tk.Frame(bg='blue')
fr3.pack(fill=tk.BOTH, expand=True)
fr21 = tk.Frame(master=fr2, bg='green')
fr21.pack(fill=tk.Y, side=tk.LEFT)
can = tk.Canvas(master=fr2, width=1000, height=600, bg='black')
can.pack(side=tk.LEFT)  # fill=tk.BOTH, side=tk.LEFT, expand=True)
can.bind("<Button-1>", lambda event: can_point((event.x, event.y)))
can.bind("<Return>", lambda event: actions.use_coord())
can.bind("<Double-Button-1>", lambda event: can_point())


def can_point(coord=None):
    global point
    if point is not None:
        can.delete(point)
    if coord is not None:
        point = can.create_oval(coord[0] - 3, coord[1] - 3, coord[0] + 3, coord[1] + 3, fill="blue")
        actions.get_coordinates(coord)
        can.focus_set()
    else:
        actions.get_coordinates()
        point = None


def can_create_definition_points(coord): return can.create_oval(coord[0] - 4, coord[1] - 4, coord[0] + 4, coord[1] + 4,
                                                                fill="yellow")


def can_del_elements(elements):
    for element in elements:
        can.delete(element)


def can_create_lines(coordinates):
    lines = ()
    for crds in coordinates:
        lines += (can.create_line(crds, fill="blue"),)
    return lines


def can_create_circle(args): return (can.create_arc(args[:4], start=args[4], extent=args[5]
                                                    , outline="blue", style=tk.ARC),)


fr22 = tk.Frame(master=fr2, bg='black')
fr22.pack(side=tk.LEFT)


def choice_object():
    global objects_list_closed
    if objects_list_closed:
        fr_hierarchy.pack_forget()
        button_new_object["text"] = 'create obj \u25B2'
        button_new_object.config(fg='blue')
        for element in objects_list:
            element.pack()
    else:
        for element in objects_list:
            element.pack_forget()
        button_new_object["text"] = 'create obj \u25BC'
        button_new_object.config(fg='black')
        fr_hierarchy.pack()
    objects_list_closed = not objects_list_closed


button_new_object = tk.Button(master=fr21, text='create obj \u25BC', command=choice_object)
button_new_object.pack()
fr_hierarchy = tk.Frame(master=fr21)
fr_hierarchy.pack()

fr_object_name = tk.Frame(master=fr22)
fr_object_name.pack()
name = tk.Label(master=fr_object_name, text="Name: ", font=("Comic Sans MS", 16, "bold"))
name.grid(row=0, column=0, pady=1)
entry_for_name = tk.Entry(master=fr_object_name)
entry_for_name.grid(row=0, column=1, pady=1)


def set_name(del_focus=False):
    if del_focus:
        root.focus_set()
    text = entry_for_name.get()
    if active_object is not None and text:
        active_object["text"] = text


entry_for_name.bind("<Return>", lambda event: set_name(True))
entry_for_name.bind("<FocusOut>", lambda event: set_name())
fr_his_prts = tk.Frame(master=fr22)
fr_his_prts.pack()
lab_his_parameter = tk.Label(master=fr_his_prts, text="My parameter:", fg="grey")
lab_his_parameter.pack()
lab = tk.Label(master=fr1, text='mm/pix: ')
lab.grid(row=0, column=0)


def mm_in_pix():
    text = ent1.get()
    print(text)
    try:
        number = float(text)
        actions.ratio = number
    except ValueError:
        ent1.delete(0, tk.END)
        ent1.insert(0, actions.ratio)


ent1 = tk.Entry(master=fr1, width=10, bg='blue')
ent1.insert(0, 1)
ent1.grid(row=0, column=1)
ent1.bind("<Return>", lambda event: mm_in_pix())
but = tk.Button(master=fr1, text="create Gcode", command=actions.create_code)
but.grid(row=0, column=2)
text_space = tk.Text(master=fr3, height=10)
text_space.pack()


def write_code(text):
    text_space.insert(1.0, text)

#    self.photo = ImageTk.PhotoImage(Image.open("mouse.jpeg"))
#    image = can.create_image(0, 0, anchor='nw', image=self.photo)
