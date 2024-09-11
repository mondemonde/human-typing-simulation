import pyautogui
import pyperclip
import time
import win32con
import win32gui

def always_on_top(hwnd):
    """Sets the specified window to always be on top."""
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)

while True:
    # Get text from the clipboard
    text = pyperclip.paste()
    
  
    # Prompt the user for the time needed, defaulting to 2 seconds
    time_needed = pyautogui.prompt(
        f"Type the text: {text}"
    )

    # If the user presses "Cancel", time_needed will be None, so exit the program
    if time_needed is None:
        continue
     # If the user inputs -1 or 'q', exit the program
    if time_needed == -1 or time_needed.lower() == 'q':
        break
    

   
    # If the user inputs nothing, use the default time
    if time_needed.strip() == "":
        time_needed = 1
    else:
        try:
            time_needed = 1 #int(time_needed)
        except ValueError:
            # Handle non-integer inputs gracefully
            pyautogui.alert("Invalid input. Please enter a number or 'q' to exit.")
            continue

    

    # Wait for the specified time before typing
    time.sleep(time_needed)
    
    

    # Type the clipboard content with a typing interval of 0.14 seconds
    pyautogui.write(text, interval=0.2)
    
    time.sleep(0.5)
    # Press 'Enter' after typing
     # Press 'Ctrl + Enter' after typing
    pyautogui.hotkey('ctrl', 'enter')
    
      # Get the handle of the active window
    #hwnd = win32gui.GetForegroundWindow()

    # Set the active window to always be on top
    #always_on_top(hwnd)


    