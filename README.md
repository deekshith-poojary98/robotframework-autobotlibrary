# AutoBotLibrary
AutoBotLibrary is a Python library designed to integrate with Robot Framework to enable seamless GUI automation. It builds upon [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/index.html) to provide a comprehensive set of utilities for mouse control, keyboard interactions, dialog handling, and image-based UI automation.  

## Features
- **Mouse control**: movement, clicks, dragging, and scrolling.
- **Keyboard control**: typing, pressing keys, and key combinations.
- **Dialog box handling**: alerts, confirmations, prompts, and password inputs.
- **Screen handling**: resolution retrieval, screenshots, and image-based element location.
- **Robot Framework** integration for test automation.

## Documentation
You can find the keyword documentation [here](https://deekshith-poojary98.github.io/robotframework-autobotlibrary/).

## Installation
```bash
pip install robotframework-autobotlibrary
```

## Importing the Library
In your Robot Framework test suite:

```robot
*** Settings ***
Library    AutoBotLibrary
```

In Python:
```py
from AutoBotLibrary import AutoBotLibrary
```

## Example Usage in Robot Framework
```robot
*** Test Cases ***
Mouse and Keyboard Automation
    # Move the mouse to coordinates (100, 200) over 1 second
    Move Mouse To    100    200    move_duration=1
    
    # Click at (100, 200)
    Click    x_cord=100    y_cord=200
    
    # Type the text "Hello, World!"
    Type Text    text=Hello, World!

Image-Based Automation
    # Find the location of an image on the screen
    ${location}=    Find On Screen    image_path=button.png
    
    # Wait until the image appears
    ${center}=    Wait Until Image Appears    image_path=button.png

Dialog Handling
    # Display an alert box
    ${response}=    Alert Box    alert_message=Task Complete!
    
    # Show a confirmation box
    VAR    @{list_of_buttons}    Yes     No
    ${confirmation}=    Confirm Box    confirm_message=Proceed?    button_labels=${list_of_buttons}
```

## Example Usage in Python
```py
from AutoBotLibrary import AutoBotLibrary

robot = AutoBotLibrary()

# Move the mouse to (200, 300)
robot.move_mouse_to(200, 300, move_duration=0.5)

# Take a screenshot
screenshot_path = robot.take_screenshot(filepath="screenshot.png")
print(f"Screenshot saved at: {screenshot_path}")

# Display a confirmation dialog box
response = robot.confirm_box(confirm_message="Do you want to continue?", button_labels=["Yes", "No"])
print(f"User selected: {response}")

# Wait until an image appears on the screen
location = robot.wait_until_image_appears("button.png", timeout=15)
print(f"Button found at: {location}")
```

## Available Methods
### Mouse Control
- `get_screen_resolution()`: Get the screen's width and height.
- `get_mouse_position()`: Get the current position of the mouse.
- `move_mouse_to(x, y, duration, motion)`: Move the mouse to a specific position.
- `click(x, y, click_count, delay, button)`: Perform mouse clicks.
- `drag_to(x, y, button, motion, duration)`: Drag the mouse to a specific position.

### Keyboard Control
- `type_text(text, delay)`: Type text with a specified delay between keystrokes.
- `press_key(keys, count, delay)`: Press a key or combination of keys.
- `press_and_hold_key(key)`: Press and hold a key.
- `release_key(key)`: Release a key.

- ### Dialog Handling
- `alert_box(message, title, button)`: Display an alert dialog box.
- `confirm_box(message, title, buttons)`: Display a confirmation dialog.
- `prompt_box(message, title, default)`: Display a prompt box for user input.
- `password_box(message, title, default, mask)`: Display a password input box.

### Image-Based Automation
- `find_on_screen(image_path, confidence, region, gray_scale)`: Locate an image on the screen.
- `find_image_center(image_path, confidence, region, gray_scale)`: Find the center of an image on the screen.
- `wait_until_image_appears(image_path, confidence, region, gray_scale, timeout)`: Wait for an image to appear on the screen.

- ### Screen Capture
- `take_screenshot(filepath, region)`: Capture a screenshot of the screen or a specific region.

## Contributions
Contributions, issues, and feature requests are welcome! Feel free to open a pull request or issue on the GitHub repository.

## License
This project is licensed under the [BSD-3-Clause License](https://github.com/deekshith-poojary98/robotframework-autobotlibrary?tab=License-1-ov-file).
