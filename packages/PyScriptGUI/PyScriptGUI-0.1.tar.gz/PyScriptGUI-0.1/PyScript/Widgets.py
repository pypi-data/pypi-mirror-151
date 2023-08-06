"""All the classes in PyScript."""

from tkinter import Tk
from tkinter import Label as Lbl

# Window
class Window:
    def __init__(self, title: str = "PyScript GUI", geometry: tuple = (500, 500), resizable: tuple = (True, True),
                 place: tuple = (400, 400)):

        self.win = Tk()
        self.title_ = title
        self.geometry_ = geometry
        self.resizable_ = resizable
        self.place1 = str(place[0])
        self.place2 = str(place[1])
        self.place_ = "+" + self.place1 + "+" + self.place2

        self.win.title(self.title_)
        self.win.resizable(self.resizable_[1], self.resizable_[0])
        self.geo_str = self._geo_tuple_to_str()
        self.win.geometry(self.geo_str + self.place_)

    def run(self):
        self.win.mainloop()

    def _geo_tuple_to_str(self):
        result = ""
        if len(self.geometry_) >= 3:
            from PyScript.Exceptions.UnexpectedValueError import UnexpectedValueError
            raise UnexpectedValueError("More than 2 Values Found in Geometry Parameter.")
        else:
            result += str(self.geometry_[0])
            result += "x"
            result += str(self.geometry_[1])
        return result

    def geometry(self, param: tuple):
        self.geometry_ = param
        self.geo_str = self._geo_tuple_to_str()
        self.win.geometry(self.geo_str)

    def geo(self, param: tuple):
        self.geometry(param)

    def resizable(self, height: bool, width: bool):
        self.win.resizable(width, height)
        self.resizable_ = (width, height)

    def place(self, x: int, y: int):
        self.win.geometry(self.win.geometry.join("+", x, "+", y))

    def center(self):
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        coordinate_x = int(screen_width/2 - self.geometry_[0]/2)
        coordinate_y = int(screen_height/2 - self.geometry_[1]/2)
        self.win.geometry(f"{self.geometry_[0]}x{self.geometry_[1]}+{coordinate_x}+{coordinate_y}")


# Label
class Label:
    def __init__(self, text: str, font: tuple = ("Arial", 12), bg: str = "white", fg: str = "black"):

        self.lbl = Lbl()
        self.text_ = text
        self.font_ = font
        self.bg_ = bg
        self.fg_ = fg

        self.lbl.config(text=self.text_, font=self.font_, bg=self.bg_, fg=self.fg_)

    def grid(self, row: int, column: int, columnspan: int = 1, rowspan: int = 1, sticky: str = "NSEW"):
        self.lbl.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, sticky=sticky)

    def pack(self):
        self.lbl.pack()

    def place(self, x: int, y: int):
        self.lbl.place(x=x, y=y)

    def config(self, text: str = None, font: tuple = None, bg: str = None, fg: str = None):
        if text is not None:
            self.text_ = text
            self.lbl.config(text=self.text_)

        if font is not None:
            self.font_ = font
            self.lbl.config(font=self.font_)

        if bg is not None:
            self.bg_ = bg
            self.lbl.config(bg=self.bg_)

        if fg is not None:
            self.fg_ = fg
            self.lbl.config(fg=self.fg_)
            