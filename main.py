import pyautogui
import pyperclip
import time

while True:
    # Get text from the clipboard
    text = pyperclip.paste()

    # Prompt the user for the time needed, defaulting to 2 seconds
    time_needed = pyautogui.prompt(
        """
        How much time (in seconds) do you need for:
        1. Switching to the editor you want to simulate typing
        2. Placing the cursor at the starting position
        
        Press OK to use the default time of 2 seconds.
        Type -1 to exit.
    """
    )

    # If the user presses "Cancel", time_needed will be None, so exit the program
    if time_needed is None:
        break

    # If the user inputs nothing, use the default time
    if time_needed.strip() == "":
        time_needed = 2
    else:
        try:
            time_needed = int(time_needed)
        except ValueError:
            # Handle non-integer inputs gracefully
            pyautogui.alert("Invalid input. Please enter a number or -1 to exit.")
            continue

    # If the user inputs -1, exit the program
    if time_needed == -1:
        break

    # Wait for the specified time before typing
    time.sleep(time_needed)

    # Type the clipboard content with a typing interval of 0.14 seconds
    pyautogui.write(text, interval=0.14)
