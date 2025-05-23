import os
import time
import pyautogui
import tkinter as tk
import pygetwindow as gw
from tkinter import filedialog, messagebox


# pip install pygetwindow pyautogui pillow 




# Adjust to auto-screenshot CERTA Test Fixture terminal output
def get_window_region(app_title):
    """Returns (left, top, width, height) of the app window."""
    windows = gw.getWindowsWithTitle(app_title)
    if windows:
        win = windows[0]
        #if win.isMinimized:
        #    win.restore()
        #win.activate()
        #time.sleep(0.1)
        return (win.left, win.top, win.width, win.height)
    else:
        raise Exception(f"No window found with title containing: '{app_title}'")

def take_android_screenshot(output_path):
    temp_path = "/sdcard/temp_screenshot.png"
    os.system(f"adb shell screencap -p {temp_path}")
    os.system(f"adb pull {temp_path} {output_path}")
    os.system(f"adb shell rm {temp_path}")

def take_pc_screenshot(output_path, region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(output_path)

def capture(test_case, test_step, output_dir):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    android_file = f"{test_case}-Tablet_Screenshot_{test_step}a.png"
    pc_file = f"{test_case}-CERTA_Terminal_{test_step}b.png"
    android_path = os.path.join(output_dir, android_file)
    pc_path = os.path.join(output_dir, pc_file)

    try:
        take_android_screenshot(android_path)
        region = get_window_region("CERTA Test Fixture")
        take_pc_screenshot(pc_path, region)
        messagebox.showinfo("Success", f"Captured and saved:\n{android_file}\n{pc_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to capture screenshots: {e}")

# GUI
def main():
    root = tk.Tk()
    root.title("Screenshot Capture Tool")


    tk.Label(root, text="Test Case Number:").grid(row=0, column=0, sticky="e")
    test_case_var = tk.IntVar(value=1)
    tk.Entry(root, textvariable=test_case_var, width=5).grid(row=0, column=1)
    tk.Button(root, text="+", command=lambda: test_case_var.set(test_case_var.get() + 1)).grid(row=0, column=2)
    tk.Button(root, text="-", command=lambda: test_case_var.set(test_case_var.get() - 1)).grid(row=0, column=3)



    tk.Label(root, text="Test Step Number:").grid(row=1, column=0, sticky="e")
    test_step_var = tk.IntVar(value="1")
    tk.Entry(root, textvariable=test_step_var).grid(row=1, column=1)
    tk.Button(root, text="+", command=lambda: test_step_var.set(test_step_var.get() + 1)).grid(row=1, column=2)
    tk.Button(root, text="-", command=lambda: test_step_var.set(test_step_var.get() - 1)).grid(row=1, column=3)



    tk.Label(root, text="Output Directory:").grid(row=2, column=0, sticky="e")
    output_dir_var = tk.StringVar()
    tk.Entry(root, textvariable=output_dir_var, width=30).grid(row=2, column=1)
    tk.Button(root, text="Browse", command=lambda: output_dir_var.set(filedialog.askdirectory())).grid(row=2, column=2)

    def on_capture():
        if not output_dir_var.get():
            messagebox.showwarning("Warning", "Please select an output directory.")
            return
        capture(test_case_var.get(), test_step_var.get(), output_dir_var.get())
        test_step_var.set(test_step_var.get() + 1)

    tk.Button(root, text="Capture Screenshots", command=on_capture, bg="lightgreen").grid(row=3, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
