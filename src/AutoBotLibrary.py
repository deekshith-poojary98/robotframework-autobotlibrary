# AutoBotLibrary
# Copyright (c) 2024, Deekshith Poojary
# This file is part of AutoBotLibrary, which uses PyAutoGUI.
# PyAutoGUI is licensed under the BSD-3-Clause License. See LICENSE file for details.

import os
import pyautogui as py
import time
from datetime import datetime
from robot.api.deco import keyword, not_keyword
from pyautogui import (KEY_NAMES,
                       easeInQuad,
                       easeOutQuad,
                       easeInOutQuad,
                       easeInBounce,
                       easeInElastic,
                       linear)
from typing import (Union,
                    Optional,
                    Dict,
                    List,
                    Any,
                    Tuple)

__version__ = "1.0.0"

class AutoBotLibraryError(Exception): ...


class InvalidMouseButtonError(AutoBotLibraryError):
    def __init__(self, button: str, allowed_buttons: List[str]):
        self.button = button
        self.allowed_buttons = "', '".join(allowed_buttons)
        self.message = f"Invalid button '{self.button}'. Please use '{self.allowed_buttons}'"
        super().__init__(self.message)


class InvalidKeyError(AutoBotLibraryError):
    def __init__(self, key: str):
        self.key = key
        self.message = f"Invalid key '{self.key}'. Please check here for valid keys https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys"
        super().__init__(self.message)


class ImageNotFoundError(AutoBotLibraryError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidMotionError(AutoBotLibraryError):
    def __init__(self, motion: str, allowed_motion: List[str]):
        self.motion = motion
        self.allowed_motion = allowed_motion
        self.message = f"Invalid motion '{self.motion}'. Please use any among these'{self.allowed_motion}'"
        super().__init__(self.message)


class AutoBotLibrary:
    """Robot Framework library wrapper for PyAutoGUI.

    ``AutoBotLibrary`` is a Robot Framework library for simulating various GUI interactions such as mouse movements, clicks, keyboard presses, and pop-up handling..
    This library is designed to help automate desktop applications by providing easy-to-use methods for basic GUI interactions, as well as image recognition capabilities.

    *Key Features*
    - *Mouse Actions*: Methods to control the mouse, including moving, clicking, and dragging.
    - *Keyboard Actions*: Methods to simulate individual key presses, combinations, and typing.
    - *Screen Interactions*: Functions to take screenshots, locate elements on screen, and scroll.
    - *Alert Handling*: Simple dialog boxes (alerts, confirmations, prompts) for gathering user input or displaying messages.
    - *Image Recognition*: Methods to locate images on the screen, find image centers, and wait for images to appear.

    *Note*: The keyboard functions do not work on Ubuntu when run in VirtualBox on Windows.

    *Example Usage*
    | ***** Settings *****
    | Library    AutoBotLibrary
    |
    | ***** Test Cases *****
    | Example Mouse Interaction
    |    Move Mouse To    x=100    y=200
    |    Click
    |
    | Example Keyboard Interaction
    |    Press Key    key=enter
    |    Type Text    Hello, Robot Framework!
    |
    | Example Dialog
    |    VAR    @{list_of_buttons}    Yes    No
    |    ${result}=    Confirm Box    Are you sure?    button_names=${list_of_buttons}
    |    Should Be Equal    ${result}    Yes
    |
    | Example Image Recognition
    |    ${location}=    Find On Screen    image_path=button.png
    |    Click    ${location["left"]}    ${location["top"]}
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    MOUSE_BUTTONS = ["left", "right", "middle"]
    MOUSE_MOTION = {
                    "ease_in_quad": easeInQuad,
                    "ease_out_quad": easeOutQuad,
                    "ease_in_out_quad": easeInOutQuad,
                    "ease_in_bounce": easeInBounce,
                    "ease_in_elastic": easeInElastic,
                    "linear": linear
                    }

    def __init__(self, fail_safe: bool = True, pause_duration: Union[int, float] = 0.5):
        """
        AutoBotLibrary can be imported with a few optional arguments.

        - ``fail_safe``: Determines whether the fail-safe feature in PyAutoGUI is enabled. If set to True, moving the mouse to the top-left corner (0,0) immediately stops any ongoing PyAutoGUI action.

        - ``pause_duration``: Specifies the amount of time (in seconds) to pause between each PyAutoGUI action. This delay is applied after every PyAutoGUI command, making the automation feel more natural and allowing time for the system to react between steps.
        """
        self.__argument_type_checker({"fail_safe": [fail_safe, bool],
                                      "pause_duration": [pause_duration, (int, float)]})
        py.FAILSAFE = fail_safe
        py.PAUSE = pause_duration


    @not_keyword
    def __argument_type_checker(self, arg_list: Dict[str, List[Any]]) -> None:
        for arg_name, value in arg_list.items():
            if isinstance(value[1], tuple):
                expected_type_names = "', or '".join(t.__name__ for t in value[1])
            else:
                expected_type_names = value[1].__name__

            if len(value) == 3:
                if value[0] is not None and not isinstance(value[0], value[1]):
                    raise TypeError(f"'{arg_name}' must be a '{expected_type_names}', got '{type(value[0]).__name__}'")
            else:
                if not isinstance(value[0], value[1]):
                    raise TypeError(f"'{arg_name}' must be a '{expected_type_names}', got '{type(value[0]).__name__}'")


    @keyword
    def get_screen_resolution(self) -> Dict[str, int]:
        """
        Retrieves the screen's resolution, returning the height and width in pixels.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Get Screen Resolution
        |   ${resolution}    Get Screen Resolution
        |   Log    Screen Height: ${resolution["height"]}, Width: ${resolution["width"]}
        """
        screen_res = py.size()
        return {"height": screen_res.height, "width": screen_res.width}


    @keyword
    def get_mouse_position(self):
        """
        Fetches the current position of the mouse cursor on the screen, returning the x and y coordinates.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Get Mouse Position
        |   ${position}    Get Mouse Position
        |   Log    Mouse X: ${position["x"]}, Y: ${position["y"]}
        """
        cur_pos = py.position()
        return {"x": cur_pos.x, "y": cur_pos.y}


    @keyword
    def coordinate_on_screen(self, x_cord: Union[int, float], y_cord: Union[int, float]) -> bool:
        """
        Checks if a given set of x and y coordinates is within the screen's boundaries.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Check Coordinate On Screen
        |   ${is_on_screen}    Coordinate On Screen    500    300
        |   Log    Is coordinate (500, 300) on screen: ${is_on_screen}
        """
        is_exists = py.onScreen(x=x_cord, y=y_cord)
        return is_exists


    @keyword
    def move_mouse_to(self, x_cord: Union[int, float],
                   y_cord: Union[int, float],
                   move_duration: Union[int, float] = 0,
                   move_motion: str = "linear"
                   ) -> None:
        """
        Moves the mouse pointer to a specified (x, y) screen coordinate.

        *Description*
        - ``x_cord``: The x-coordinate on the screen to which the mouse should be moved.
        - ``y_cord``: The y-coordinate on the screen to which the mouse should be moved.
        - ``move_duration``: The time in seconds it takes to move the mouse to the specified position. Defaults to 0, which moves the mouse instantly.
        - ``move_motion``: The motion effect to use for the `[https://pyautogui.readthedocs.io/en/latest/mouse.html#tween-easing-functions|mouse movement]`. Can be a string such as ``linear``, ``ease_in_out_quad``, etc. Defaults to ``linear``.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Moves the mouse to coordinates (500, 300) over a duration of 1.5 seconds using the default motion (linear)
        |   Move Mouse To    x_cord=500    y_cord=300    move_duration=1.5
        |
        |   # Moves the mouse to coordinates (200, 100) over a duration of 1 second using an ease-in-elastic motion effect
        |   Move Mouse To    x_cord=200    y_cord=100    move_duration=1    move_motion=ease_in_elastic
        """
        self.__argument_type_checker({
                        "x_cord": [x_cord, (int, float)],
                        "y_cord": [y_cord, (int, float)],
                        "move_duration": [move_duration, (int, float)],
                        "move_motion": [move_motion, str]
                        })

        if move_motion.lower() not in self.MOUSE_MOTION:
            raise InvalidMotionError(motion=move_motion, allowed_motion=list(self.MOUSE_MOTION.keys()))

        py.moveTo(x=x_cord, y=y_cord, duration=move_duration, tween=self.MOUSE_MOTION[move_motion.lower()])

    @keyword
    def move_mouse(self, x_offset: Union[int, float],
                   y_offset: Union[int, float],
                   move_duration: Union[int, float] = 0,
                   move_motion: str = "linear"
                   ) -> None:
        """
        Moves the mouse cursor to a point on the screen, relative to its current position.

        *Description*
        - ``x_offset``: The horizontal distance in pixels to move the mouse. Positive values move the cursor to the right, while negative values move it to the left.
        - ``y_offset``: The vertical distance in pixels to move the mouse. Positive values move the cursor down, while negative values move it up.
        - ``move_duration``: The time in seconds taken to move the mouse to the specified offset position. Defaults to 0 for instant movement.
        - ``move_motion``: The motion effect to use for the `[https://pyautogui.readthedocs.io/en/latest/mouse.html#tween-easing-functions|mouse movement]`. Can be a string such as ``linear``, ``ease_in_out_quad``, etc. Defaults to ``linear``.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Move the mouse cursor 100 pixels right and 50 pixels down
        |   Move Mouse    x_offset=100    y_offset=50
        |
        |   # Move the mouse cursor 200 pixels left with a duration of 1.5 seconds
        |   Move Mouse    x_offset=-200    move_duration=1.5
        """
        self.__argument_type_checker({
                        "x_offset": [x_offset, (int, float)],
                        "y_offset": [y_offset, (int, float)],
                        "move_duration": [move_duration, (int, float)],
                        "move_motion": [move_motion, str]
                        })

        if move_motion.lower() not in self.MOUSE_MOTION:
            raise InvalidMotionError(motion=move_motion, allowed_motion=list(self.MOUSE_MOTION.keys()))

        py.move(xOffset=x_offset, yOffset=y_offset, duration=move_duration, tween=self.MOUSE_MOTION[move_motion.lower()])


    @keyword
    def click(self, x_cord: Optional[Union[int, float]] = None,
            y_cord: Optional[Union[int, float]] = None,
            click_count: int = 1,
            click_delay: Union[int, float] = 0,
            button: str = 'left',
            move_motion: str = "linear",
            move_duration: Union[int, float] = 0,
            ) -> None:
        """
        Simulates a mouse click at a specified (x, y) coordinate or at the current mouse position if no coordinates are provided.

        *Description*
        - ``x_cord``: The x-coordinate for the click. If omitted, the click occurs at the current mouse position.
        - ``y_cord``: The y-coordinate for the click. If omitted, the click occurs at the current mouse position.
        - ``click_count``: The number of times to click (default is 1). Use a higher value to simulate multiple clicks.
        - ``click_delay``: The delay between clicks in seconds (default is 0). Specify a value to introduce a pause between consecutive clicks.
        - ``button``: Specifies the mouse button to use: ``left``, ``right``, or ``middle``. Defaults to ``left``.
        - ``move_motion``: The motion effect to use for the `[https://pyautogui.readthedocs.io/en/latest/mouse.html#tween-easing-functions|mouse movement]`. Can be a string such as ``linear``, ``ease_in_out_quad``, etc. Defaults to ``linear``.
        - ``move_duration``: The time in seconds it takes to move the mouse to the specified position. Defaults to 0, which moves the mouse instantly.

        *Note*:
        Double and Triple click can be simulated using this same keyword by setting ``click_count`` to 2 and 3 respectively.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Clicks the left mouse button at coordinates (200, 300) by moving to the coordinates in linear motion
        |   Click    x_cord=200    y_cord=300    button=left    move_motion=linear
        |
        |   # Right-clicks at the current mouse position
        |   Click    button=right
        |
        |   # Double-clicks at the current mouse position with a delay of 0.2 seconds between clicks
        |   Click    click_count=2    click_delay=0.2
        """
        self.__argument_type_checker({
                        "x_cord": [x_cord, (int, float), None],
                        "y_cord": [y_cord, (int, float), None],
                        "button": [button, str],
                        "click_count": [click_count, int],
                        "click_delay": [click_delay, (int, float)],
                        "move_motion": [move_motion, str],
                        "move_duration": [move_duration, (int, float)],
                        })
        if button not in self.MOUSE_BUTTONS:
            raise InvalidMouseButtonError(button=button, allowed_buttons=self.MOUSE_BUTTONS)

        if move_motion.lower() not in self.MOUSE_MOTION:
            raise InvalidMotionError(motion=move_motion, allowed_motion=list(self.MOUSE_MOTION.keys()))

        py.click(x=x_cord, y=y_cord, button=button, duration=move_duration, clicks=click_count, interval=click_delay, tween=self.MOUSE_MOTION[move_motion.lower()])


    @keyword
    def mouse_down(self, x_cord: Optional[Union[int, float]] = None,
            y_cord: Optional[Union[int, float]] = None,
            button: str = 'left',
            move_duration: Union[int, float] = 0,
            ) -> None:
        """
        Simulates a mouse press (down) at a specified (x, y) coordinate or at the current mouse position if no coordinates are provided.

        It moves the mouse to the specified (x, y) coordinates with the given duration, then simulates a mouse button press down.

        *Description*
        - ``x_cord``: The x-coordinate for the click. If omitted, the click occurs at the current mouse position.
        - ``y_cord``: The y-coordinate for the click. If omitted, the click occurs at the current mouse position.
        - ``click_count``: The number of times to click (default is 1). Use a higher value to simulate multiple clicks.
        - ``click_delay``: The delay between clicks in seconds (default is 0). Specify a value to introduce a pause between consecutive clicks.
        - ``button``: Specifies the mouse button to use: ``left``, ``right``, or ``middle``. Defaults to ``left``.
        - ``move_duration``: The time in seconds it takes to move the mouse to the specified position. Defaults to 0, which moves the mouse instantly.

        *Examples*:
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Presses the left mouse button at coordinates (200, 300) with duration of 10 seconds
        |   Mouse Down    x_cord=200    y_cord=300    button=left    move_duration=10
        |
        |   # Right-clicks at the current mouse position
        |   Mouse Down    button=right
        |
        |   # Presses the mouse button at the current mouse position with duration of 1 second
        |   Mouse Down    move_duration=1
        """
        self.__argument_type_checker({
                        "x_cord": [x_cord, (int, float), None],
                        "y_cord": [y_cord, (int, float), None],
                        "button": [button, str],
                        "move_duration": [move_duration, (int, float)],
                        })
        if button not in self.MOUSE_BUTTONS:
            raise InvalidMouseButtonError(button=button, allowed_buttons=self.MOUSE_BUTTONS)

        py.mouseDown(x=x_cord, y=y_cord, button=button, duration=move_duration)


    @keyword
    def mouse_up(self, x_cord: Optional[Union[int, float]] = None,
            y_cord: Optional[Union[int, float]] = None,
            button: str = 'left',
            move_duration: Union[int, float] = 0,
            ) -> None:
        """
        Simulates releasing a mouse button at a specified (x, y) coordinate or at the current mouse position if no coordinates are provided.

        *Description*
        - ``x_cord``: The x-coordinate for the click. If omitted, the click occurs at the current mouse position.
        - ``y_cord``: The y-coordinate for the click. If omitted, the click occurs at the current mouse position.
        - ``click_count``: The number of times to click (default is 1). Use a higher value to simulate multiple clicks.
        - ``click_delay``: The delay between clicks in seconds (default is 0). Specify a value to introduce a pause between consecutive clicks.
        - ``button``: Specifies the mouse button to use: ``left``, ``right``, or ``middle``. Defaults to ``left``.
        - ``move_duration``: The time in seconds it takes to move the mouse to the specified position. Defaults to 0, which moves the mouse instantly.

        *Examples*:
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Releases the left mouse button at coordinates (200, 300) with duration of 10 seconds
        |   Mouse Up    x_cord=200    y_cord=300    button=left    move_duration=10
        |
        |   # Releases the right mouse button at the current mouse position with instant movement
        |   Mouse Up    button=right
        |
        |   # Releases the mouse button at the current mouse position with duration of 1 second
        |   Mouse Up    move_duration=1
        """
        self.__argument_type_checker({
                        "x_cord": [x_cord, (int, float), None],
                        "y_cord": [y_cord, (int, float), None],
                        "button": [button, str],
                        "move_duration": [move_duration, (int, float)],
                        })
        if button not in self.MOUSE_BUTTONS:
            raise InvalidMouseButtonError(button=button, allowed_buttons=self.MOUSE_BUTTONS)

        py.mouseUp(x=x_cord, y=y_cord, button=button, duration=move_duration)


    @keyword
    def vertical_scroll(self, scroll_amount: Union[int, float],
                        x_cord: Optional[Union[int, float]] = None,
                        y_cord: Optional[Union[int, float]] = None) -> None:
        """
        Simulates a vertical scroll action on the screen at the specified coordinates.

        *Description*
        - ``scroll_amount``: The number of scroll units. A positive value scrolls up, while a negative value scrolls down.
        - ``x_cord``: The x-coordinate at which to perform the scroll. If omitted, the scroll action occurs at the current mouse position.
        - ``y_cord``: The y-coordinate at which to perform the scroll. If omitted, the scroll action occurs at the current mouse position.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Scrolls up by 10 units at the current mouse position
        |   Vertical Scroll    scroll_amount=10
        |
        |   # Scrolls down by 20 units at coordinates (300, 500)
        |   Vertical Scroll    scroll_amount=-20    x_cord=300    y_cord=500
        """
        self.__argument_type_checker({
                        "x_cord": [x_cord, (int, float), None],
                        "y_cord": [y_cord, (int, float), None],
                        "scroll_amount": [scroll_amount, (int, float)]
                        })
        py.scroll(clicks=scroll_amount, x=x_cord, y=y_cord)


    @keyword
    def horizontal_scroll(self, scroll_amount: Union[int, float],
                        x_cord: Optional[Union[int, float]] = None,
                        y_cord: Optional[Union[int, float]] = None) -> None:
        """
        Simulates a horizontal scroll action on the screen at the specified coordinates.

        *Description*
        - ``scroll_amount``: The number of scroll units. A positive value scrolls right, while a negative value scrolls left.
        - ``x_cord``: The x-coordinate at which to perform the scroll. If omitted, the scroll action occurs at the current mouse position.
        - ``y_cord``: The y-coordinate at which to perform the scroll. If omitted, the scroll action occurs at the current mouse position.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Scrolls right by 10 units at the current mouse position
        |   Horizontal Scroll    scroll_amount=10
        |
        |   # Scrolls left by 20 units at coordinates (300, 500)
        |   Horizontal Scroll    scroll_amount=-20    x_cord=300    y_cord=500
        """
        self.__argument_type_checker({
                        "x_cord": [x_cord, (int, float), None],
                        "y_cord": [y_cord, (int, float), None],
                        "scroll_amount": [scroll_amount, (int, float)]
                        })
        py.keyDown('shift')
        py.scroll(clicks=scroll_amount, x=x_cord, y=y_cord)
        py.keyUp('shift')


    @keyword
    def drag_to(self, x_cord: Optional[Union[int, float]] = None,
                y_cord: Optional[Union[int, float]] = None,
                button: str = 'left',
                move_motion: str = "linear",
                move_duration: Union[int, float] = 0) -> None:
        """
        Drags the mouse cursor to a specified (x, y) coordinate while holding down a specified mouse button.

        *Description*
        - ``x_cord``: The x-coordinate to drag the mouse to. If omitted, the cursor will drag horizontally based on the current x-position.
        - ``y_cord``: The y-coordinate to drag the mouse to. If omitted, the cursor will drag vertically based on the current y-position.
        - ``button``: Specifies which mouse button to hold down during the drag. Options are ``left``, ``right``, or ``middle``. Defaults to ``left``.
        - ``move_motion``: The motion effect to use for the `[https://pyautogui.readthedocs.io/en/latest/mouse.html#tween-easing-functions|mouse movement]`. Can be a string such as ``linear``, ``ease_in_out_quad``, etc. Defaults to ``linear``.
        - ``move_duration``: The time in seconds for the drag operation. If set to 0, the drag occurs instantly. Defaults to 0.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Drag to the coordinates (300, 400) using the left mouse button in a linear motion over 2 seconds
        |   Drag To    x_cord=300    y_cord=400    button=left    move_motion=linear    move_duration=2
        |
        |   # Drag to (150, 200) using the right mouse button with an ease-in-bounce motion over 1 second
        |   Drag To    x_cord=150    y_cord=200    button=right    move_motion=ease_in_bounce    move_duration=1
        """
        self.__argument_type_checker({
                        "x_cord": [x_cord, (int, float), None],
                        "y_cord": [y_cord, (int, float), None],
                        "button": [button, str],
                        "move_motion": [move_motion, str],
                        "move_duration": [move_duration, (int, float)],
                        })
        if button not in self.MOUSE_BUTTONS:
            raise InvalidMouseButtonError(button=button, allowed_buttons=self.MOUSE_BUTTONS)

        if move_motion.lower() not in self.MOUSE_MOTION:
            raise InvalidMotionError(motion=move_motion, allowed_motion=list(self.MOUSE_MOTION.keys()))

        py.dragTo(x=x_cord, y=y_cord, button=button, duration=move_duration, tween=self.MOUSE_MOTION[move_motion.lower()])


    @keyword
    def drag(self, x_offset: Optional[Union[int, float]] = None,
                y_offset: Optional[Union[int, float]] = None,
                button: str = 'left',
                move_motion: str = "linear",
                move_duration: Union[int, float] = 0) -> None:
        """
        Drags the mouse cursor by a specified offset relative to its current position, while holding down a specified mouse button.

        *Description*
        - ``x_offset``: The horizontal distance (in pixels) to drag the mouse from its current position. If omitted, the cursor will not move horizontally.
        - ``y_offset``: The vertical distance (in pixels) to drag the mouse from its current position. If omitted, the cursor will not move vertically.
        - ``button``: Specifies which mouse button to hold down during the drag. Options are ``left``, ``right``, or ``middle``. Defaults to ``left``.
        - ``move_motion``: The motion effect to use for the `[https://pyautogui.readthedocs.io/en/latest/mouse.html#tween-easing-functions|mouse movement]`. Can be a string such as ``linear``, ``ease_in_out_quad``, etc. Defaults to ``linear``.
        - ``move_duration``: The time in seconds for the drag operation. If set to 0, the drag occurs instantly. Defaults to 0.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Drag the mouse 100 pixels to the right and 50 pixels down using the left mouse button in a linear motion over 1 second
        |   Drag    x_offset=100    y_offset=50    button=left    move_motion=linear    move_duration=1
        |
        |   # Drag the mouse 50 pixels to the left using the right mouse button with an ease-out-quad motion over 2 seconds
        |   Drag    x_offset=-50    y_offset=0    button=right    move_motion=ease_out_quad    move_duration=2
        """
        self.__argument_type_checker({
                        "x_offset": [x_offset, (int, float), None],
                        "y_cord": [y_offset, (int, float), None],
                        "button": [button, str],
                        "move_motion": [move_motion, str],
                        "move_duration": [move_duration, (int, float)],
                        })
        if button not in self.MOUSE_BUTTONS:
            raise InvalidMouseButtonError(button=button, allowed_buttons=self.MOUSE_BUTTONS)

        if move_motion.lower() not in self.MOUSE_MOTION:
            raise InvalidMotionError(motion=move_motion, allowed_motion=list(self.MOUSE_MOTION.keys()))

        py.drag(xOffset=x_offset, yOffset=y_offset, button=button, duration=move_duration, tween=self.MOUSE_MOTION[move_motion.lower()])


    @keyword
    def type_text(self, text: str, delay: Union[int, float] = 0.1) -> None:
        """
        Types the specified text string, with an optional delay between characters.

        *Description*
        - ``text``: The text string that you want to type.
        - ``delay``: The delay in seconds between typing each character. You can set a custom delay, or leave it at the default of 0.1 seconds.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # This would type "Hello, world!" with a 0.2-second delay between each character
        |   Type Text    text=Hello, world!    delay=0.2
        """
        self.__argument_type_checker({
                        "text": [text, str],
                        "delay": [delay, (int, float)]
                        })
        py.write(text, interval=delay)


    @keyword
    def press_key(self, keys: Union[str, list], press_count: int = 1, press_delay: Union[int, float] = 0) -> None:
        """
        Simulates pressing a single keyboard key or list of keys a specified number of times, with an optional delay between each press.

        *Description*

        - ``keys``: The key to be pressed. It should be one of the `[https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys|valid key names]` (e.g., 'enter', 'a', 'shift', etc.).
        - ``press_count``: The number of times to press the key. Defaults to 1.
        - ``press_delay``: The delay (in seconds) between each key press. Defaults to 0 (no delay).

        *Note*: Use `[https://deekshith-poojary98.github.io/robotframework-autobotlibrary/#Press%20Keys | Press Keys]` keyword to stimulate pressing of multiple keys simultaneously.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Pressing 'enter' key 2 times with the delay of 5 seconds between each press
        |   Press Key    keys=enter  press_count=2   press_delay=5
        |
        |   # Pressing the list of keys one after the other
        |   VAR    @{list_of_keys}    A    B    C    enter
        |   Press Key    keys=${list_of_keys}
        """
        self.__argument_type_checker({
                        "keys": [keys, (str, list)],
                        "press_count": [press_count, int],
                        "press_delay": [press_delay, (int, float)]
                        })
        if isinstance(keys, str):
            keys = [keys]

        keys = [key.strip() for key in keys]
        for key in keys:
            if key.lower() not in KEY_NAMES:
                raise InvalidKeyError(key=key)

        py.press(keys=keys, presses=press_count, interval=press_delay)


    @keyword
    def press_keys(self, keys: Union[str, list]) -> None:
        """
        Simulates pressing one or more keys simultaneously on the keyboard.

        *Description*

        - ``keys``: The keys to be pressed. It should be one of the `[https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys|valid key names]` (e.g., 'enter', 'a', 'shift', etc.)

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Presses 'enter' key
        |   Press Keys    keys=enter
        |
        |   # Pressing the list of keys simultaneously
        |   VAR    @{list_of_keys}    ctrl    shift    c
        |   Press Keys    keys=${list_of_keys}
        """
        self.__argument_type_checker({"keys": [keys, (str, list)]})
        if isinstance(keys, str):
            keys = [keys]

        keys = [key.strip() for key in keys]
        for key in keys:
            if key.lower() not in KEY_NAMES:
                raise InvalidKeyError(key=key)
        py.hotkey(keys)

    @keyword
    def press_and_hold_key(self, key: str) -> None:
        """
        Simulates pressing a key down and holds it in the pressed state.

        *Description*

        - ``key``: The key to be pressed. It should be one of the `[https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys|valid key names]` (e.g., 'enter', 'a', 'shift', etc.).

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Pressing 'shift' key and holding it in the pressed state
        |   Press And Hold Key    key=shift
        """
        self.__argument_type_checker({"key": [key, str]})

        if key.strip().lower() not in KEY_NAMES:
            raise InvalidKeyError(key=key)
        py.keyDown(key=key.strip())


    @keyword
    def release_key(self, key: str) -> None:
        """
        Simulates releasing a key that was previously pressed down.

        *Description*

        - ``key``: The key to be pressed. It should be one of the `[https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys|valid key names]` (e.g., 'enter', 'a', 'shift', etc.).

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Releasing 'shift' key that was previously pressed down
        |   Release Key    key=shift
        """
        self.__argument_type_checker({"key": [key, str]})

        if key.strip().lower() not in KEY_NAMES:
            raise InvalidKeyError(key=key)
        py.keyUp(key=key.strip())


    @keyword
    def alert_box(self, alert_message: str = '',
                  alert_title: str = '',
                  button_label: str = ''
                  ) -> str:
        """
        Displays an alert box with a message and a button.

        *Description*

        - ``alert_message``: The message displayed in the alert box. Defaults to an empty string.
        - ``alert_title``: The title of the alert box. Defaults to an empty string.
        - ``button_label``: The label for the button in the alert box. Defaults to an empty string.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Display an alert box with a custom message and button
        |   ${clicked_button}    Alert Box    alert_message=Hello World!    alert_title=Greeting    button_label=OK
        """
        self.__argument_type_checker({
                        "alert_message": [alert_message, str],
                        "alert_title": [alert_title, str],
                        "button_label": [button_label, str]
                        })
        button_pressed = py.alert(text=alert_message, title=alert_title, button=button_label)
        return button_pressed


    @keyword
    def confirm_box(self, confirm_message: str = '',
                    confirm_title: str = '',
                    button_labels: list = ''
                    ) -> str:
        """
        Displays a confirmation dialog with custom message and buttons.

        *Description*

        - ``confirm_message``: The message displayed in the confirmation box. Defaults to an empty string.
        - ``confirm_title``: The title of the confirmation box. Defaults to an empty string.
        - ``button_labels``: A list of button labels displayed in the confirmation box.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Display a confirmation box with custom message and buttons
        |   VAR    @{list_of_buttons}    Yes    No
        |   ${clicked_button}    Confirm Box    confirm_message=Are you sure?    confirm_title=Confirmation    button_labels=${list_of_buttons}
        """
        self.__argument_type_checker({
                        "confirm_message": [confirm_message, str],
                        "confirm_title": [confirm_title, str],
                        "button_labels": [button_labels, list]
                        })
        button_pressed = py.confirm(text=confirm_message, title=confirm_title, buttons=button_labels)
        return button_pressed


    @keyword
    def prompt_box(self, prompt_message: str = '',
                   prompt_title: str = '',
                   default_text: str = ''
                   ) -> str:
        """
        Displays a prompt box to capture user input.

        *Description*

        - ``prompt_message``: The message displayed in the prompt box. Defaults to an empty string.
        - ``prompt_title``: The title of the prompt box. Defaults to an empty string.
        - ``default_text``: The default text shown in the input field. Defaults to an empty string.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Display a prompt box for user input with default text
        |   ${message}    Prompt Box    prompt_message=Enter your name    prompt_title=Name Input    default_text=John Doe
        """
        self.__argument_type_checker({
                        "prompt_message": [prompt_message, str],
                        "prompt_title": [prompt_title, str],
                        "default_text": [default_text, str]
                        })
        message = py.prompt(text=prompt_message, title=prompt_title, default=default_text)
        return message


    @keyword
    def password_box(self, password_message: str = '',
                     password_title: str = '',
                     default_text: str = '',
                     mask_text: str = "*"
                     ) -> str:
        """
        Displays a password input box with masked characters.

        *Description*

        - ``password_message``: The message displayed in the password box. Defaults to an empty string.
        - ``password_title``: The title of the password box. Defaults to an empty string.
        - ``default_text``: The default text shown in the input field. Defaults to an empty string.
        - ``mask_text``: The character used to mask input characters. Defaults to '*'.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Display a password box with a mask character
        |   ${password}    Password Box    password_message=Enter Password    password_title=Password Input    default_text=default_password    mask_text=#
        """
        self.__argument_type_checker({
                        "prompt_message": [password_message, str],
                        "prompt_title": [password_title, str],
                        "default_text": [default_text, str],
                        "mask_text": [mask_text, str]
                        })
        password = py.password(text=password_message, title=password_title, default=default_text, mask=mask_text)
        return password


    @keyword
    def take_screenshot(self, filepath="screenshot_{}.png", region: Tuple[int, int, int, int] = None) -> str:
        """
        Takes a screenshot of the entire screen or a specified region and saves it to the specified path.

        *Description*

        - ``filepath``: The file path where the screenshot should be saved. If not specified, a default filename
        with a timestamp is used to save the screenshot.
        - ``region``: An optional tuple (x, y, width, height) specifying the screen region to capture.
        If omitted, captures the entire screen.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Takes a screenshot and saves it to the default location with a timestamp
        |   Take Screenshot
        |
        |   # Takes a screenshot and saves it to a custom file path
        |   Take Screenshot    filepath=custom_path/filename.png
        |
        |   # Takes a screenshot of a specific region and saves it
        |   Take Screenshot    filepath=region_screenshot.png    region=(0, 0, 800, 600)
        """
        self.__argument_type_checker({
                        "filepath": [filepath, str],
                        "region": [region, tuple, None]
                        })
        cur_time = datetime.now().strftime("%d%m%Y%H%M%S")
        path = filepath.format(cur_time)
        py.screenshot(imageFilename=path, region=region)
        absolute_path = os.path.abspath(path)

        return absolute_path

    @keyword
    def find_on_screen(self, image_path: str,
                       confidence: Union[int, float] = 0.9,
                       search_region: Tuple[int, int, int, int] = None,
                       gray_scale: bool =False
                       ) -> Union[Dict[str, Union[int, float]], None]:
        """
        Searches for a specified image on the screen and returns its bounding box coordinates if found.

        *Description*

        - ``image_path``: The path to the image file to be located on the screen.
        - ``confidence``: A confidence level for the image match (0 to 1). Higher values require a closer match. Defaults to 0.9.
        - ``search_region``: An optional tuple (x, y, width, height) defining the screen region to search in. If omitted, the entire screen is searched.
        - ``gray_scale``: A boolean indicating if the search should be done in grayscale, which can be faster. Defaults to False.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Finds an image on the entire screen with default confidence
        |   ${location}    Find On Screen    image_path=button.png
        |
        |   # Finds an image within a specific region with grayscale enabled
        |   ${location}    Find On Screen    image_path=icon.png    search_region=(100, 100, 500, 400)    gray_scale=True
        """
        self.__argument_type_checker({
                        "image_path": [image_path, str],
                        "search_region" : [search_region, tuple, None],
                        "confidence": [confidence, (int, float)],
                        "gray_scale": [gray_scale, bool]
                        })
        try:
            location = py.locateOnScreen(image=image_path, confidence=confidence, grayscale=gray_scale, region=search_region)

            if location:
                return {
                    "left": location.left,
                    "top": location.top,
                    "width": location.width,
                    "height": location.height
                    }
            else:
                return None
        except py.ImageNotFoundException:
            raise ImageNotFoundError(f"Image '{image_path}' not found on screen. Try adjusting the 'confidence' parameter")

    @keyword
    def find_image_center(self, image_path: str,
                       confidence: Union[int, float] = 0.9,
                       search_region: Tuple[int, int, int, int] = None,
                       gray_scale: bool =False
                       ) -> Union[Dict[str, Union[int, float]], None]:
        """
        Searches for an image on the screen and returns the coordinates of its center if found.

        *Description*

        - ``image_path``: The path to the image file to locate on the screen.
        - ``confidence``: The confidence level (0 to 1) for matching the image. Defaults to 0.9.
        - ``search_region``: A tuple specifying the search region `(x, y, width, height)`. If not provided, searches the full screen.
        - ``gray_scale``: Whether to search in grayscale mode. Useful for faster processing, especially with high-resolution images. Defaults to False.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Finds the center of an image on the entire screen with default confidence
        |   ${image_center}    Find Image Center    image_path=logo.png
        |
        |   # Finds the center of an image in a specific region with higher confidence
        |   ${image_center}    Find Image Center    image_path=icon.png    confidence=0.95    search_region=(50, 50, 800, 600)
        """
        self.__argument_type_checker({
                        "image_path": [image_path, str],
                        "search_region" : [search_region, tuple, None],
                        "confidence": [confidence, (int, float)],
                        "gray_scale": [gray_scale, bool]
                        })
        try:
            image_center = py.locateCenterOnScreen(image=image_path, confidence=confidence, grayscale=gray_scale, region=search_region)
            if image_center:
                return {"x": image_center.x, "y": image_center.y}
            else:
                return None
        except py.ImageNotFoundException:
            raise ImageNotFoundError(f"Image '{image_path}' not found on screen. Try adjusting the 'confidence' parameter")


    @keyword
    def wait_until_image_appears(self, image_path: str,
                       confidence: Union[int, float] = 0.9,
                       search_region: Tuple[int, int, int, int] = None,
                       gray_scale: bool =False,
                       timeout: Union[int, float] = 10
                       ) -> Dict[str, Union[int, float]]:
        """
        Waits until a specified image appears on the screen, within a given timeout.

        *Description*

        - ``image_path``: The file path to the target image to locate on the screen.
        - ``confidence``: The matching confidence threshold (0 to 1). A higher value requires a closer match. Defaults to 0.9.
        - ``search_region``: A tuple defining the specific screen region to search `(x, y, width, height)`. If omitted, searches the entire screen.
        - ``gray_scale``: Whether to perform the search in grayscale, often faster and may improve matching speed. Defaults to False.
        - ``timeout``: Maximum time in seconds to wait for the image to appear. Defaults to 10 seconds.

        *Examples*
        | ***** Settings *****
        | Library    AutoBotLibrary
        |
        | ***** Test Cases *****
        | Example
        |   # Waits up to 5 seconds for the image to appear on the entire screen
        |   Wait Until Image Appears    image_path=start_button.png    timeout=5
        |
        |   # Waits for the image within a specific region, with grayscale enabled
        |   Wait Until Image Appears    image_path=icon.png    search_region=(100, 100, 500, 400)    gray_scale=True
        """
        self.__argument_type_checker({
                        "image_path": [image_path, str],
                        "search_region" : [search_region, tuple, None],
                        "confidence": [confidence, (int, float)],
                        "gray_scale": [gray_scale, bool],
                        "timeout": [timeout, (int, float)]
                        })
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = py.locateOnScreen(image_path, confidence=confidence, grayscale=gray_scale, region=search_region)
                if location:
                    image_center = py.center(location)
                    return {"x": image_center.x, "y": image_center.y}
                time.sleep(0.5)
            except: ...
        raise ImageNotFoundError(message=f"Image '{image_path}' not found within {timeout} seconds.")

