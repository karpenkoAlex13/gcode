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


def create_object(element):
    prts = element.Parameters()
    parameters = ()
    count = 0
    while count != prts[0]:
        count += 1
        frame = tk.Frame(master=fr_his_prts)
        frame.pack()
        parameters += (frame,)
        lb = tk.Label(master=frame, text="x:")
        lb.grid(row=0, column=0, padx=1, pady=2)
        en = tk.Entry(master=frame, width=10)
        en.grid(row=0, column=1, padx=1, pady=2)
        lb = tk.Label(master=frame, text="y:")
        lb.grid(row=0, column=2, padx=1, pady=2)
        en = tk.Entry(master=frame, width=10)
        en.grid(row=0, column=3, padx=1, pady=2)
    if prts[1] is None:
        bt = tk.Button(master=fr_his_prts, text="+coord")
        bt.pack()
        parameters += (bt,)
        prts = prts[1:]
    # Create coord parameters
    for parameter in prts[1:]:
        frame = tk.Frame(master=fr_his_prts)
        frame.pack()
        parameters += (frame,)
        lb = tk.Label(master=frame, text=parameter[0] + ":")
        lb.grid(row=0, column=0, padx=1, pady=2)
        en = tk.Entry(master=frame, width=10)
        en.grid(row=0, column=1, padx=1, pady=2)
    # Create constants parameters
    global hierarchy_widgets, active_object
    if active_object is not None:
        active_object.config(bg="white")
    lb = tk.Label(master=fr_hierarchy, text=element.str(), fg="gray", bg="blue")
    lb.grid(row=len(hierarchy_widgets), column=0)
    lb.bind("<Button-1>", lambda event: actions.open_object(element, lb))
    active_object = lb
    hierarchy_widgets.append(lb)
    # update hierarchy
    return parameters


def open_object(new_prts, old_prts, picture):
    for widget in old_prts:
        widget.pack_forget()
    for widget in new_prts:
        widget.pack()
    if picture is not None:
        global active_object
        if active_object is not None:
            active_object.config(bg="white")
        active_object = picture
        active_object.config(bg="blue")


def create_objects_list(objects):
    global objects_list   # ??
    for element in objects:
        objects_list.append(tk.Button(master=fr21, text=element.str(), command=lambda: actions.create_object(element)))


def open_objects_list():
    fr_hierarchy.pack_forget()
    button_new_object["text"] = 'create obj \u25B2'
    button_new_object.config(fg='blue')
    for element in objects_list:
        element.pack()


def close_objects_list():
    for element in objects_list:
        element.pack_forget()
    button_new_object["text"] = 'create obj \u25BC'
    button_new_object.config(fg='black')
    fr_hierarchy.pack()


def create_point(coord, postpone=False):
    global point
    if point is not None:
        can.delete(point)
    if postpone:
        return
    point = can.create_oval(coord[0]-4, coord[1]-4, coord[0]+4, coord[1]+4, fill="blue")


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
can.bind("<Button-1>", lambda event: actions.cleek((event.x, event.y)))
can.bind("<Return>", lambda event: actions.set_coordinares())
fr22 = tk.Frame(master=fr2, bg='green')
fr22.pack(side=tk.LEFT)


button_new_object = tk.Button(master=fr21, text='create obj \u25BC', command=actions.choice_object)
button_new_object.pack()
fr_hierarchy = tk.Frame(master=fr21)
fr_hierarchy.pack()

fr_his_prts = tk.Frame(master=fr22)
fr_his_prts.pack()
lab_his_parameter = tk.Label(master=fr_his_prts, text="My parameter:", fg="grey")
lab_his_parameter.pack()

lab = tk.Label(master=fr1, text='mm/pix: ')
lab.grid(row=0, column=0)
ent1 = tk.Entry(master=fr1, width=10, bg='blue')
ent1.grid(row=0, column=1)
#    self.photo = ImageTk.PhotoImage(Image.open("mouse.jpeg"))
#    image = can.create_image(0, 0, anchor='nw', image=self.photo)
