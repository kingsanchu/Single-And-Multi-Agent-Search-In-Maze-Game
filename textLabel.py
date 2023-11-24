from tkinter import *

class textLabel:
    """
    Creates a Text Label to display different results on the window.

    Attributes:
    - title (str): The title of the text label.
    - _value (int): The value displayed in the text label.
    - _parentMaze (object): The parent maze object.

    Methods:
    - __init__: Initializes the text label with provided parameters.
    - value: Gets the current value of the text label.
    - value.setter: Sets the value to be displayed in the text label.
    - drawLabel: Draws the text label on the canvas.
    """
   # This class is to create Text Label to show different results on the window.

    def __init__(self, parentMaze, title, value):
        """
        Initializes the text label with the given title and value.

        Args:
        - parentMaze (object): The parent maze object.
        - title (str): The title of the text label.
        - value (int): The initial value to display in the text label.
        """

        self.title = title
        self._value = value
        self._parentMaze = parentMaze
        # self._parentMaze._labels.append(self)
        self._var = None
        self.drawLabel()

    @property
    def value(self):
        """
        Gets the current value of the text label.

        Returns:
        - int: The value displayed in the text label.
        """
        return self._value

    @value.setter
    def value(self, v):
        """
        Sets the value to be displayed in the text label.

        Args:
        - v (int): The new value to be displayed in the text label.
        """
        self._value = v
        self._var.set(f'{self.title} : {v}')

    def drawLabel(self):
        """
        Draws the text label on the canvas.
        """
        self._var = StringVar()
        self.lab = Label(self._parentMaze._canvas, textvariable=self._var,
                         bg="white", fg="black", font=('Helvetica bold', 12), relief=RIDGE)
        self._var.set(f'{self.title} : {self.value}')
        self.lab.pack(expand=True, side=LEFT, anchor=NW)