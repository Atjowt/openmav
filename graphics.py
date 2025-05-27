import openmav
import tkinter as tk
import threading

# CONSTANTS
# Alter these to chnage the launch options and which variables are shown and able to be modified
LAUNCH_OPTIONS = openmav.LaunchOptions(
    aircraft=openmav.aircraft.F16_BLOCK_30,
    altitude=7000.0,
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
            "Latitude": "latitude",
            "Aileron": "aileron",
            "Elevator": "elevator",
            "Rudder": "rudder",
            "Pitch": "pitch",
            "Roll": "roll"
        }

CHANGEABLE_VARIABLES = {
            "Aileron": "aileron",
            "Elevator": "elevator",
            "Rudder": "rudder"
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
        self.remove_widgets()
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

                if attr_name in CHANGEABLE_VARIABLES.values():
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

        # Submit values button
        self.submit_button = tk.Button(self.root, text="Submit Values", command=self.submit_values, font=("Helvetica", self.scaled_font_size))
        self.submit_button.grid(row=len(TRACKED_VARIABLES)+2, column=1, columnspan=2, pady=10 * self.scale_factor)
        self.widgets_to_remove.append(self.submit_button)

        # Quit session button, closes the instance of the game running and reader and writer
        quit_session_btn = tk.Button(self.root, text="Quit session", command=self.quit_session, font=("Helvetica", self.scaled_font_size))
        quit_session_btn.grid(row=1, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(quit_session_btn)

        # Quit application button, closes the whole GUI
        quit_app_btn = tk.Button(self.root, text="Quit Application", command=self.quit_application, font=("Helvetica", self.scaled_font_size))
        quit_app_btn.grid(row=2, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(quit_app_btn)

        # Do a barrel roll, the user can't give data during this time or do other data altering functions
        self.barrel_roll_btn = tk.Button(self.root, text="Barrel roll", command=self.barrel_roll, font=("Helvetica", self.scaled_font_size))
        self.barrel_roll_btn.grid(row=3, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(self.barrel_roll_btn)

        # Do a barrel roll, the user can't give data during this time or do other data altering functions
        self.increase_altitude_btn = tk.Button(self.root, text="Increase altitude", command=self.increase_altitude, font=("Helvetica", self.scaled_font_size))
        self.increase_altitude_btn.grid(row=4, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(self.increase_altitude_btn)

        # Stabalizes the aircarft so the pitch is set to 0
        self.stabilize_pitch_btn = tk.Button(self.root, text="Stabalize pitch", command=self.stabilize_pitch, font=("Helvetica", self.scaled_font_size))
        self.stabilize_pitch_btn.grid(row=5, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(self.stabilize_pitch_btn)

        # Stabalizes the aircarft so the roll is set to 0
        self.stabilize_roll_btn = tk.Button(self.root, text="Stabalize roll", command=self.stabilize_roll, font=("Helvetica", self.scaled_font_size))
        self.stabilize_roll_btn.grid(row=6, column=0, padx=10 * self.scale_factor, pady=10 * self.scale_factor, sticky="nsew")
        self.widgets_to_remove.append(self.stabilize_roll_btn)

        threading.Thread(target=self.delayed_connect_and_update, daemon=True).start()


    # Waits for game to launch and then get fligth data
    def delayed_connect_and_update(self):
        try:
            # Open reader and writer
            self.reader = openmav.Reader()
            self.writer = openmav.Writer()

            # Set elevator to -0.05 to not lose altitude
            in_data = self.reader.read()
            out_data = openmav.OutData.from_indata(in_data)
            out_data.elevator = -0.05
            self.writer.write(out_data)

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


    # Valid data is taken and updates flightdata to user's choice
    # Invalid format of data is sorted out
    def submit_values(self):
        # Only include non-empty values and convert them to float
        values = {}
        for key, var in self.input_vars.items():
            val = var.get().strip()
            if val != "":
                try:
                    values[key] = float(val)
                except ValueError:
                    self.add_label("All fields must be numbers", len(TRACKED_VARIABLES)+3, 1, "red")

        # Get the current data
        in_data = self.reader.read()
        if not in_data:
            self.add_label("No data available", len(TRACKED_VARIABLES)+3, 1, "red")
            return

        out_data = openmav.OutData.from_indata(in_data)

        # Update only the variables that had input
        for attr, val in values.items():
            setattr(out_data, attr, val)

        # write back data
        self.writer.write(out_data)

        # Clear all input fields
        for var in self.input_vars.values():
            var.set("")

        # Add confirmation message
        self.add_label("Flightdata updated", len(TRACKED_VARIABLES)+3, 1, "green")

        
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

    
    # Increase the altitude to 7000
    def increase_altitude(self):
        self.add_label("Increasing altitude...", len(TRACKED_VARIABLES)+3, 1, "green")

        # Disable relevant controls
        self.disable_controls()

        # Initial values to stop turning
        in_data = self.reader.read()
        out_data = openmav.OutData.from_indata(in_data)
        out_data.elevator = -0.05
        out_data.aileron = 0.0
        out_data.rudder = 0.0
        out_data.throttle = 1.0
        self.writer.write(out_data)

        def perform_increase():
            try:
                target_altitude = 7000.0

                while True:
                    in_data = self.reader.read()
                    if not in_data:
                        self.add_label("No data available", len(TRACKED_VARIABLES)+3, 1, "red")
                        break

                    current_altitude = in_data.altitude
                    if current_altitude > target_altitude:
                        break

                    out_data = openmav.OutData.from_indata(in_data)
                    out_data.elevator = -0.25 if current_altitude < target_altitude else 0.0
                    out_data.aileron = 0.0
                    out_data.rudder = 0.0
                    

                    self.writer.write(out_data)

                self.add_label("Altitude set to 7000 ft", len(TRACKED_VARIABLES)+3, 1, "green")

                # Stabilize flight after reaching altitude
                self.stabilize_pitch()


            except Exception as e:
                self.add_label(f"Error: {e}", len(TRACKED_VARIABLES)+3, 1, "red")

            # Decrease throttle
            in_data = self.reader.read()
            out_data = openmav.OutData.from_indata(in_data)
            out_data.throttle = 0.5
            self.writer.write(out_data)

            # Re-enable buttons
            self.enable_controls()

        threading.Thread(target=perform_increase, daemon=True).start()

    # Do a barrel roll
    def barrel_roll(self):
        self.add_label("Doing barrel roll", len(TRACKED_VARIABLES)+3, 1, "green")

        # Disable relevant controls
        self.disable_controls()

        def perform_roll():
            try:
                in_data = self.reader.read()
                if not in_data:
                    self.add_label("No data available", len(TRACKED_VARIABLES)+3, 1, "red")
                    return

                out_data = openmav.OutData.from_indata(in_data)
                out_data.aileron = 0.8
                out_data.throttle *= 2.0
                self.writer.write(out_data)

                self.add_label("Barrelroll started!", len(TRACKED_VARIABLES)+4, 1, "green")

                threshold = 5.0
                initial_roll = in_data.roll

                while True:
                    in_data = self.reader.read()
                    if abs(in_data.roll - initial_roll) > 180.0 - threshold:
                        break

                self.add_label("Upside-down!", len(TRACKED_VARIABLES)+4, 1, "green")

                while True:
                    in_data = self.reader.read()
                    if abs(in_data.roll - initial_roll) < threshold:
                        break
                
                self.add_label("Barrel roll complete!", len(TRACKED_VARIABLES)+3, 1, "green")


                self.stabilize_roll()

            except Exception as e:
                self.add_label(f"Error during roll: {e}", len(TRACKED_VARIABLES)+3, 1, "red")
                self.add_label("", len(TRACKED_VARIABLES)+4, 1, "black")

            # Re-enable buttons
            self.enable_controls()

        threading.Thread(target=perform_roll, daemon=True).start()


    def stabilize_pitch(self):
        self.add_label("Stabilizing flight...", len(TRACKED_VARIABLES)+4, 1, "green")

        # Disable relevant controls
        self.disable_controls()

        def perform_stabilize_pitch():
            try:
                error_threshold = 1
                while True:
                    in_data = self.reader.read()
                    pitch = in_data.pitch
                    out_data = openmav.OutData.from_indata(in_data)

                    if abs(pitch) < error_threshold:
                        out_data.elevator = 0
                        self.writer.write(out_data)
                        break

                    elif pitch > 0:
                        new_elevator = (pitch * 0.01) * 7
                        out_data.elevator = max(min(0.3, new_elevator), 0.13)
                    else:
                        new_elevator = (pitch * 0.01) * 7
                        out_data.elevator = min(max(-0.3, new_elevator), -0.13)

                    self.writer.write(out_data)

                self.add_label("Flight stabilized", len(TRACKED_VARIABLES)+3, 1, "green")
                self.add_label("", len(TRACKED_VARIABLES)+4, 1, "black")

            except Exception as e:
                self.add_label(f"Pitch stabilization error: {e}", len(TRACKED_VARIABLES)+3, 1, "red")
                self.add_label("", len(TRACKED_VARIABLES)+4, 1, "black")

            # Re-enable buttons
            self.enable_controls()

        threading.Thread(target=perform_stabilize_pitch, daemon=True).start()


    def stabilize_roll(self):
        self.add_label("Stabilizing flight...", len(TRACKED_VARIABLES)+4, 1, "green")

        # Disable relevant controls
        self.disable_controls()

        def perform_stabilize_roll():
            try:
                error_threshold = 0.05
                while True:
                    in_data = self.reader.read()
                    roll = in_data.roll
                    out_data = openmav.OutData.from_indata(in_data)

                    if abs(roll) < error_threshold:
                        out_data.aileron = 0
                        self.writer.write(out_data)
                        break
                    
                    # Positive roll means tilitng to the right, should make aileron negative to start counter rotating
                    elif roll > 0:
                        new_aileron = (roll * (-0.01)) * 7
                        out_data.aileron = min(max(-0.8, new_aileron), -0.1)

                    # Negative roll means tilitng to the left, should make aileron positive to start counter rotating
                    else:
                        new_aileron = (roll * (-0.01)) * 7
                        out_data.aileron = max(min(0.8, new_aileron), 0.1)

                    self.writer.write(out_data)

                self.add_label("Flight stabilized", len(TRACKED_VARIABLES)+3, 1, "green")
                self.add_label("", len(TRACKED_VARIABLES)+4, 1, "black")

            except Exception as e:
                self.add_label(f"Roll stabilization error: {e}", len(TRACKED_VARIABLES)+3, 1, "red")
                self.add_label("", len(TRACKED_VARIABLES)+4, 1, "black")

            # Re-enable buttons
            self.enable_controls()

        threading.Thread(target=perform_stabilize_roll, daemon=True).start()


    # Helpers to manage control states
    def disable_controls(self):
        self.submit_button.config(state="disabled")
        self.barrel_roll_btn.config(state="disabled")
        self.increase_altitude_btn.config(state="disabled")
        self.stabilize_pitch_btn.config(state="disabled")
        self.stabilize_roll_btn.config(state="disabled")


    def enable_controls(self):
        self.submit_button.config(state="normal")
        self.barrel_roll_btn.config(state="normal")
        self.increase_altitude_btn.config(state="normal")
        self.stabilize_pitch_btn.config(state="normal")
        self.stabilize_roll_btn.config(state="normal")

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
