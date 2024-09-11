import pyautogui
import pyperclip
import time
import keyboard  # To detect the Pause key state

paused = False  # Variable to track the pause state

while True:
    # Get text from the clipboard
    text = pyperclip.paste()
    
    # Prompt the user for the time needed, defaulting to 2 seconds
    time_needed = pyautogui.prompt(
        f"Type the text: {text}"
    )

    # If the user presses "Cancel", skip the rest of the loop
    if time_needed is None:
        continue
    
    # If the user inputs -1 or 'q', exit the program
    if time_needed == '-1' or time_needed.lower() == 'q':
        break
    
    # If the user inputs nothing, use the default time of 1 second
    if time_needed.strip() == "":
        time_needed = 1
    else:
        try:
            # Attempt to convert the input to a float value
            time_needed = float(time_needed)
        except ValueError:
            # Handle non-numeric inputs gracefully
            pyautogui.alert("Invalid input. Please enter a number or 'q' to exit.")
            continue

    # Wait for the specified time before typing
    time.sleep(time_needed)

    for char in text:
        # Check if the Pause key is pressed
        if keyboard.is_pressed('pause'):
            paused = not paused  # Toggle the pause state
            state = "paused" if paused else "resumed"
            pyautogui.alert(f"Typing has been {state}. Press Pause key to toggle again.")
            time.sleep(0.5)  # Small delay to avoid rapid toggling
            
        # If paused, wait until unpaused
        while paused:
            if keyboard.is_pressed('pause'):
                paused = not paused
                pyautogui.alert(f"Typing resumed. Press Pause key to toggle again.")
                time.sleep(0.5)  # Delay to avoid immediate re-pause

        # Type each character with the specified interval
        pyautogui.write(char, interval=0.08)

    # Wait for half a second before pressing Enter
    time.sleep(0.5)
    
    # Press 'Ctrl + Enter' after typing
    pyautogui.hotkey('ctrl', 'enter')
