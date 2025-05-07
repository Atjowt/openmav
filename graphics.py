import openmav
import tkinter as tk
import threading

class WindowCentering:
    @staticmethod
    def center_window(root):
        root.update_idletasks()
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        root.geometry(f"+{x_position}+{y_position}")

class StartScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OpenMav API Start Screen")
        self.widgets_to_remove = []
        self.process = None  # Store OpenMav process

        # Responsive scaling based on screen resolution
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.scale_factor = min(self.screen_width / 1920, self.screen_height / 1080)
        self.scaled_font_size = max(12, int(16 * self.scale_factor))  # Ensure font isn't too small

        self.create_start_screen()

    def create_start_screen(self):
        self.root.grid_columnconfigure(0, weight=1)  # Ensure column expands

        # Welcome Label
        welcome_label = tk.Label(self.root, text="Welcome to OpenMav API!", font=("Helvetica", self.scaled_font_size))
        welcome_label.grid(row=0, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(welcome_label)

        # Start Button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_openmav, font=("Helvetica", self.scaled_font_size))
        self.start_button.grid(row=1, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(self.start_button)

        # Quit Button
        quit_button = tk.Button(self.root, text="Quit Application", command=self.quit_application, font=("Helvetica", self.scaled_font_size))
        quit_button.grid(row=2, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(quit_button)

     # OpenMav and disable the Start button while running
    def start_openmav(self):
        if self.process and self.process.poll() is None:
            print("OpenMav is already running.")
            return
        
        self.start_button.config(state="disabled") 
        self.process = openmav.launch()  # Store the process reference

        # If OpenMav was successfully launched, monitor it
        if self.process:
            thread = threading.Thread(target=self.monitor_openmav, daemon=True)
            thread.start()
        else:
            print("Failed to start OpenMav.")
            self.start_button.config(state="normal")  # Re-enable if launch fails

    # Monitor OpenMav process and re-enable Start button when it exits. Called in a separate thread
    def monitor_openmav(self):
        self.process.wait()  # Wait for OpenMav to close, pausing the thread
        self.root.after(100, self.enable_start_button)  # Re-enable Start button from the main thread

    # Re-enable the Start button when OpenMav exits
    def enable_start_button(self):
        self.start_button.config(state="normal")

    # Exit application and ensure OpenMav is closed
    def quit_application(self):
        # If OpenMav is running, terminate it
        if self.process and self.process.poll() is None:
            self.process.terminate()  
        self.root.destroy() # Close the application

    def run(self):
        self.root.update()  # Ensures the window is fully loaded before centering
        WindowCentering.center_window(self.root)
        self.root.mainloop()

# Run the start screen
if __name__ == "__main__":
    start_screen = StartScreen()
    start_screen.run()
