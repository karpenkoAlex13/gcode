import Pattern


class Behavior:
    def __init__(self):
        self.objects_list_closed = True
        self.coordinate = None
        self.active_object = None

    def create_object(self, element):
        self.objects_list_closed = True
        Window.close_objects_list()
        obj = element()
        obj.widgets = Window.create_object(obj)
        self.open_object(obj, None)
        Pattern.our_objects.append(self.active_object)  # ??

    def open_object(self, element, picture):
        if self.active_object == element:
            return
        elif self.active_object is None:
            widgets = ()
        else:
            widgets = self.active_object.widgets
        self.active_object = element
        Window.open_object(element.widgets, widgets, picture)

    def cleek(self, coord):
        Window.can.focus_set()
        if self.coordinate is None or self.coordinate != coord:
            Window.create_point(coord)
            self.coordinate = coord
        else:
            Window.create_point(coord, True)
            self.coordinate = None

    def set_coordinares(self):
        if self.active_object is not None and self.coordinate is not None:
            self.active_object.append_coordinates(self.coordinate)

    def choice_object(self):
        if self.objects_list_closed:
            Window.open_objects_list()
        else:
            Window.close_objects_list()
        self.objects_list_closed = not self.objects_list_closed


import Window


def run():
    Window.run()


Window.create_objects_list(Pattern.objects)
