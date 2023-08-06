import enum
class CKey():
    """A class representing various buttons that may not correspond to
    letters. This includes modifier keys and function keys.

    The actual values for these items differ between platforms. Some platforms
    may have additional buttons, but these are guaranteed to be present
    everywhere.

    this is a modifyed version of the one from the keyboard modual. It has removed keys for capatibilty
    
    """
    

    #: The Backspace key.
    class backspace():
        name = "backspace"
    #: A down arrow key.
    class down():
        name = "down"
    #: The Enter or Return key.
    class enter():
        name = "enter"
    #: The Esc key.
    class esc():
        name = "esc"
    #: A left arrow key.
    class left():
        name = "left"
    #: A right arrow key.
    class right():
        name = "right"
    #: The Space key.
    class space():
        name = "space"

    #: The Tab key.
    class tab():
        name = "tab"

    #: An up arrow key.
    class up():
        name = "up"



