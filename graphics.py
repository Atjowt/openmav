import openmav
import tkinter as tk
import threading

# CONSTANTS, can be changed
LAUNCH_OPTIONS = openmav.LaunchOptions(
    aircraft=openmav.aircraft.F16_BLOCK_30,
    altitude=5000.0,
    heading=180.0,
    speed=400.0,
    throttle=0.5,
    engine_running=True,
    input=openmav.SocketOptions(port=5400, rate=30),
    output=openmav.SocketOptions(port=5500, rate=30),
)
LAUNCH_OPTIONS.args = ['--state=cruise', '--httpd=5000']

TRACKED_VARIABLES = {
            "Speed": "speed",
            "Altitude": "altitude",
            "Longitude": "longitude",
            "Latitude": "latitude"
        }

# Ensure ok screen positioning
class WindowCentering:
    @staticmethod
    def center_window(root):
        root.update_idletasks()
        w, h = root.winfo_width(), root.winfo_height()
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        root.geometry(f"+{x}+{y}")


# Class for the GUI
class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.widgets_to_remove = []
        self.process = None
        self.reader = None
        self.writer = None

        self.current_value_vars = {} 
        self.input_vars = {}         

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.scale_factor = min(self.screen_width / 1920, self.screen_height / 1080)
        self.scaled_font_size = max(12, int(16 * self.scale_factor))

        self.create_start_screen()

    # The screen that is shown when strting the application
    def create_start_screen(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.add_label("Welcome to OpenMav API!", 0, 0, "black")

        self.start_button = tk.Button(self.root, text="Start", command=self.create_waiting_screen, font=("Helvetica", self.scaled_font_size))
        self.start_button.grid(row=1, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(self.start_button)

        quit_button = tk.Button(self.root, text="Quit Application", command=self.quit_application, font=("Helvetica", self.scaled_font_size))
        quit_button.grid(row=2, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(quit_button)

    # The screen while waiting for the game to start on users end
    def create_waiting_screen(self):
        self.remove_widgets()
        self.root.grid_columnconfigure(0, weight=1)
        self.add_label("When game is done booting, click connect!", 0, 0, "black")

        connect_btn = tk.Button(self.root, text="Connect", command=self.create_running_screen, font=("Helvetica", self.scaled_font_size))
        connect_btn.grid(row=1, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(connect_btn)

        quit_session_btn = tk.Button(self.root, text="Quit session", command=self.quit_session, font=("Helvetica", self.scaled_font_size))
        quit_session_btn.grid(row=2, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(quit_session_btn)

        quit_button = tk.Button(self.root, text="Quit Application", command=self.quit_application, font=("Helvetica", self.scaled_font_size))
        quit_button.grid(row=3, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(quit_button)

        # Starts the game
        self.start_openmav()

    # The screen that is shown after launching the game
    def create_running_screen(self):
        self.current_value_vars.clear()
        self.root.grid_columnconfigure(0, weight=1)

        self.add_label("Game is running!", 0, 0, "black", colspan=10)

        labels = [("Variable names", 1), ("Set value", 2), ("Current value", 3)]
        for text, col in labels:
            self.add_label(text, 1, col, "black")

        for i, (label_text, attr_name) in enumerate(TRACKED_VARIABLES.items(), start=2):
            label = tk.Label(self.root, text=f"{label_text}:", font=("Helvetica", self.scaled_font_size))
            label.grid(row=i, column=1, sticky="w", padx=20 * self.scale_factor, pady=2 * self.scale_factor)
            self.widgets_to_remove.append(label)

            input_var = tk.StringVar()
            entry = tk.Entry(self.root, textvariable=input_var, font=("Helvetica", self.scaled_font_size))
            entry.grid(row=i, column=2, sticky="ew", padx=10 * self.scale_factor, pady=2 * self.scale_factor)
            self.widgets_to_remove.append(entry)
            self.input_vars[attr_name] = input_var

            current_var = tk.StringVar(value="N/A")
            current_label = tk.Label(self.root, textvariable=current_var, font=("Helvetica", self.scaled_font_size))
            current_label.grid(row=i, column=3, sticky="w", padx=10 * self.scale_factor, pady=2 * self.scale_factor)
            self.widgets_to_remove.append(current_label)
            self.current_value_vars[attr_name] = current_var

        submit_button = tk.Button(self.root, text="Submit Values", command=self.submit_values, font=("Helvetica", self.scaled_font_size))
        submit_button.grid(row=len(TRACKED_VARIABLES)+2, column=1, columnspan=2, pady=10 * self.scale_factor)
        self.widgets_to_remove.append(submit_button)

        quit_session_btn = tk.Button(self.root, text="Quit session", command=self.quit_session, font=("Helvetica", self.scaled_font_size))
        quit_session_btn.grid(row=1, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(quit_session_btn)

        quit_app_btn = tk.Button(self.root, text="Quit Application", command=self.quit_application, font=("Helvetica", self.scaled_font_size))
        quit_app_btn.grid(row=2, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(quit_app_btn)

        threading.Thread(target=self.delayed_connect_and_update, daemon=True).start()

    # Waits for game to launch and then get fligth data
    def delayed_connect_and_update(self):
        try:
            # Open reader and writer
            self.reader = openmav.Reader()
            self.writer = openmav.Writer()

            while True:
                in_data = self.reader.read()
                if in_data:
                    # For all tracked variables
                    for attr in TRACKED_VARIABLES.values():
                        value = getattr(in_data, attr, "N/A")
                        if attr in self.current_value_vars:
                             # Round off if int or float
                            if isinstance(value, (int, float)):
                                display_value = f"{value:.2f}"
                            else:
                                display_value = str(value)
                            self.current_value_vars[attr].set(display_value)
        except ConnectionRefusedError:
            self.remove_widgets()
            self.add_label("Failed to get a connection", 3, 0, "black")
            self.create_start_screen()

    # Checks that all data is ints and updates flightdata to users choice
    def submit_values(self):
        try:
            # Check that all values are convertable to floats
            values = {key: float(var.get()) for key, var in self.input_vars.items()}

            # Get the current data
            in_data = self.reader.read()
            if not in_data:
                self.add_label("Ingen data tillgänglig", len(TRACKED_VARIABLES)+3, 1, "red")
                return

            out_data = openmav.OutData.from_indata(in_data)

            # For all tracked variables, set the new data given by user
            for attr, val in values.items():
                setattr(out_data, attr, val)

            # write back data
            self.writer.write(out_data)

            # Remove all data in fields
            for var in self.input_vars.values():
                var.set("")

            # Add confirmation message
            self.add_label("Flightdata updated", len(TRACKED_VARIABLES)+3, 1, "green")

        except ValueError:
            self.add_label("All fields must be numbers", len(TRACKED_VARIABLES)+3, 1, "red")

    # Launches the game as a separate thread
    def start_openmav(self):
        if self.process and self.process.poll() is None:
            print("OpenMav is already running.")
            return

        self.process = openmav.launch(options=LAUNCH_OPTIONS)

        if self.process:
            threading.Thread(target=self.monitor_openmav, daemon=True).start()
        else:
            self.remove_widgets()
            self.add_label("Failed to run game", 3, 0, "black")
            self.create_start_screen()

    # Monitor OpenMav process
    def monitor_openmav(self):
        self.process.wait()

    # Help function to create labels
    def add_label(self, message, row, col, color, colspan=1):
        label = tk.Label(self.root, text=message, font=("Helvetica", self.scaled_font_size), fg=color)
        label.grid(row=row, column=col, columnspan=colspan, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(label)

    def quit_application(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
        self.root.destroy()

    def quit_session(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
        self.remove_widgets()
        self.create_start_screen()

    def remove_widgets(self):
        for widget in self.widgets_to_remove:
            widget.destroy()
        self.widgets_to_remove.clear()

    def run(self):
        self.root.update()
        WindowCentering.center_window(self.root)
        self.root.mainloop()


# Runs program
if __name__ == "__main__":
    gui = GUI()
    gui.run()
