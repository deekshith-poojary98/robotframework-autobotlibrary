*** Settings ***
Library    ..\\src\\PyRoboGUI.py    fail_safe=True    pause_duration=5


*** Test Cases ***
Tc1
    VAR    @{list_of_buttons}    Yes     No
    Take Screenshot    filepath=region_screenshot.png    region=(0, 0, 800, 600)


