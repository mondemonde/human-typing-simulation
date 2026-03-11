import pyautogui
import pyperclip
import time
import keyboard  # To detect the Pause key state
import tkinter as tk
from tkinter import simpledialog
import win32gui
import win32con

paused = False  # Variable to track the pause state

while True:
    # Get text from the clipboard
    text = pyperclip.paste()

    # Create root window
    root = tk.Tk()
    root.withdraw()

    # Function to handle dialog
    def show_dialog(parent):
        dialog = tk.Toplevel(parent)
        dialog.title("Input")
        dialog.overrideredirect(False)
        dialog.attributes("-topmost", True)

        # Get screen width and calculate position
        screen_width = root.winfo_screenwidth()
        x_position = (
            screen_width - 600
        )  # Position 300px from right edge (300px dialog width + 300px)
        dialog.geometry(f"300x500+{x_position}+300")  # 300px width, 500px height

        result = [
            None
        ]  # Use list to store result since nonlocal isn't needed for lists

        # Create input field at the very top
        entry_label = tk.Label(dialog, text="Type the delay (seconds):")
        entry_label.pack(pady=20)
        entry = tk.Entry(dialog)
        entry.pack(pady=20)

        # Button frame below input
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=20)

        def on_ok():
            # Find and activate Firefox window
            def find_firefox_window(hwnd, _):
                if "Mozilla Firefox" in win32gui.GetWindowText(hwnd):
                    win32gui.ShowWindow(
                        hwnd, win32con.SW_RESTORE
                    )  # Restore if minimized
                    win32gui.SetForegroundWindow(hwnd)  # Bring to front
                    return False  # Stop enumeration
                return True

            # Try to find and activate Firefox window
            win32gui.EnumWindows(find_firefox_window, None)

            # Store the result and close dialog
            result[0] = entry.get()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        tk.Button(button_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Refresh", command=on_cancel).pack(side=tk.LEFT)

        # Display copied text below buttons
        text_frame = tk.Frame(dialog)
        text_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        text_label = tk.Label(text_frame, text="Copied Text:", anchor="w")
        text_label.pack(fill=tk.X, padx=10)

        text_display = tk.Text(text_frame, wrap=tk.WORD, height=10)
        text_display.insert("1.0", text)
        text_display.config(state="disabled")  # Make it read-only
        text_display.pack(fill=tk.BOTH, expand=True, padx=10)

        # Center the dialog contents
        dialog.update_idletasks()
        dialog.geometry(f"300x500+{x_position}+300")  # 300px width, 500px height

        # Focus the entry field
        entry.focus_set()

        # Wait for dialog
        dialog.wait_window()
        return result[0]

    # Show dialog and get result
    time_needed = show_dialog(root)
    root.destroy()

    # If the user presses "Cancel", skip the rest of the loop
    if time_needed is None:
        continue

    # If the user inputs -1 or 'q', exit the program
    if time_needed == "-1" or time_needed.lower() == "q":
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
            pyautogui.alert("Invalid input. Please enter a number or 'q' to exit.")  # type: ignore
            continue

    # Wait for the specified time before typing
    time.sleep(time_needed)
    char_count: int = 1
    isNewLine: bool = False
    for char in text:
        char_count += 1
        if char_count % 15 == 0:
            time.sleep(0.5)
        # Check if the Pause key is pressed
        if keyboard.is_pressed("pause"):
            paused = not paused  # Toggle the pause state
            state = "paused" if paused else "resumed"
            pyautogui.alert(  # type: ignore
                f"Typing has been {state}. Press Pause key to toggle again."
            )
            time.sleep(0.5)  # Small delay to avoid rapid toggling

        # If paused, wait until unpaused
        while paused:
            if keyboard.is_pressed("pause"):
                paused = not paused
                pyautogui.alert(f"Typing resumed. Press Pause key to toggle again.")  # type: ignore
                time.sleep(0.5)  # Delay to avoid immediate re-pause

        # Check if the current character is a newline
        if char == "\n":
            print("Newline detected!")  # Handle newlines here, if needed
            # If you don't want to type the newline, you can skip or replace it
            pyautogui.press(
                "enter",
            )  # Simulate Enter key instead of newline
            time.sleep(0.5)  # Delay to avoid immediate re-pause
            pyautogui.press("home")  # Simulate Enter key instead of newline
            continue
        elif char == "\r":
            # Handle carriage returns here, if needed
            # If you don't want to type the carriage return, you can skip or replace it
            # pyautogui.press('return')  # Simulate Return key instead of carriage return

            isNewLine = True
            continue

        # elif char == ' ' and isNewLine:
        #     # Handle carriage returns here, if needed
        #     # If you don't want to type the carriage return, you can skip or replace it
        #     #pyautogui.press('return')  # Simulate Return key instead of carriage return
        #     continue

        else:
            # Type each character with the specified interval
            pyautogui.write(char, interval=0.005)
            isNewLine = False

    # Wait for half a second before pressing Enter
    # time.sleep(0.3)

    # Press 'Ctrl + Enter' after typing
    pyautogui.hotkey("ctrl", "enter")
