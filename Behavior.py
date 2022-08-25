import Pattern
def pass_f(*args): pass


class Behavior:
    def __init__(self):
        self.coordinate = ()
        self.active_object: Pattern.Geometry or None = None
        self.use_coord = pass_f
        self.ratio = 1

    def create_code(self):
        Window.write_code(Pattern.create_code(self.ratio))

    def create_object(self, element):
        Window.choice_object()
        obj = element()
        if obj.get_parameters()[1]:
            obj.widgets, obj.crds_widgets, obj.plus_coord, obj.minus_coord, picture = Window.create_object(obj)
        else:
            obj.widgets, obj.crds_widgets, picture = Window.create_object(obj)
        obj.points, obj.elements = (), ()
        self.open_object(obj, picture)
        Pattern.our_objects.append(self.active_object)  # ??

    def open_object(self, element, picture):
        if self.active_object == element:
            return
        elif self.active_object is None:
            widgets = ()
        else:
            widgets = self.active_object.widgets
            Window.can_del_elements(self.active_object.points)
        self.active_object = element
        self.active_object.points = ()
        for point in element.coordinates:
            self.active_object.points += (Window.can_create_definition_points(point), )
        Window.open_object(element.widgets, widgets, picture)
        if not element.coordinates_received() and self.use_coord != self.set_coordinates:
            self.use_coord = self.set_coordinates

    def destroy_object(self):
        Window.can_del_elements(self.active_object.points + self.active_object.elements)
        Window.delete_object(self.active_object.widgets)
        Pattern.our_objects.remove(self.active_object)
        self.active_object = None

    def new_coord(self, widget, crds_widget):
        self.active_object.widgets += (widget,)
        self.active_object.crds_widgets += (crds_widget,)
        self.active_object.additional_coord += 1
        if self.use_coord != self.set_coordinates:
            self.use_coord = self.set_coordinates

    def del_coord(self):
        if not self.active_object.additional_coord:
            return
        if self.active_object.coordinates_received():
            del self.active_object.coordinates[-1]
        self.active_object.additional_coord -= 1
        self.active_object.crds_widgets = self.active_object.crds_widgets[:-1]
        widget = self.active_object.widgets[-1]
        self.active_object.widgets = self.active_object.widgets[:-1]
        # if self.active_object.coordinates_received():
        #    self.use_coord = pass_f
        return widget

    def get_coordinates(self, coord=None):
        if coord is None:
            self.coordinate = None
        else:
            self.coordinate = coord

    def set_coordinates(self, number=None, coord=None):
        amount = len(self.active_object.coordinates)
        if number is None or number == amount:
            if self.coordinate is None and coord is None:
                return
            if self.active_object.coordinates_received():
                try:
                    self.active_object.plus_coord()
                except AttributeError:
                    self.use_coord = pass_f
                    return
            if coord is None:
                coord = self.coordinate
                Window.next_coord(amount, coord, self.active_object.crds_widgets)
            self.active_object.coordinates.append(coord)
        elif number < amount:
            self.active_object.coordinates[number] = coord
        else:
            return
        Window.can_del_elements(self.active_object.points + self.active_object.elements)
        self.active_object.points = ()
        for coord in self.active_object.coordinates:
            self.active_object.points += (Window.can_create_definition_points(coord),)

        if self.active_object.id_object():
            self.active_object.elements = ()
            if isinstance(self.active_object, Pattern.Circle):
                self.active_object.elements += (Window.can_create_circle(self.active_object.get_coordinates()), )
            else:
                self.active_object.elements += (Window.can_create_lines(self.active_object.get_coordinates()), )


import Window


def run():
    Window.run()


Window.create_objects_list(Pattern.objects)
