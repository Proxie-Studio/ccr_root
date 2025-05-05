import tkinter as tk
from tkinter import ttk
import serial
import time
import serial.tools.list_ports

class TrafficLightSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Light Simulation")
        self.root.geometry("1000x650")  # Window size

        # Grid Configuration with adjusted weights for equidistance
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=0)  # For COM port and Logic/BLE column
        root.grid_columnconfigure(2, weight=1)  # For Output
        root.grid_rowconfigure(0, weight=2)
        root.grid_rowconfigure(1, weight=1)

        # Consistent padding for equidistance
        padding_x = 20
        padding_y = (20, 10)

        # Frame for Input 1 (Vertical Traffic Light)
        frame1 = tk.Frame(root)
        frame1.grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky="n")
        
        tk.Label(frame1, text="Input 1", font=("Arial", 12, "bold")).pack()
        
        self.canvas1 = tk.Canvas(frame1, width=200, height=350, bg='white', bd=2, relief=tk.GROOVE)
        self.canvas1.pack()
        
        self.canvas1.create_rectangle(50, 40, 150, 290, fill='black', outline='gray')
        self.red_light1 = self.canvas1.create_oval(75, 50, 125, 100, fill='gray')
        self.yellow_light1 = self.canvas1.create_oval(75, 130, 125, 180, fill='gray')
        self.green_light1 = self.canvas1.create_oval(75, 210, 125, 260, fill='gray')

        # Frame for Output (Vertical Traffic Light with Red and Green only)
        frame4 = tk.Frame(root)
        frame4.grid(row=0, column=2, padx=padding_x, pady=padding_y, sticky="n")
        
        tk.Label(frame4, text="Output", font=("Arial", 12, "bold")).pack()
        
        self.canvas4 = tk.Canvas(frame4, width=200, height=250, bg='white', bd=2, relief=tk.GROOVE)
        self.canvas4.pack()
        
        self.canvas4.create_rectangle(50, 40, 150, 210, fill='black', outline='gray')
        self.red_light4 = self.canvas4.create_oval(75, 50, 125, 100, fill='gray')
        self.green_light4 = self.canvas4.create_oval(75, 150, 125, 200, fill='gray')

        # Frame for Input 2 (Horizontal Traffic Light)
        frame2 = tk.Frame(root)
        frame2.grid(row=1, column=0, padx=padding_x, pady=padding_y, sticky="n")
        
        tk.Label(frame2, text="Input 2", font=("Arial", 12, "bold")).pack()
        
        self.canvas2 = tk.Canvas(frame2, width=250, height=150, bg='white', bd=2, relief=tk.GROOVE)
        self.canvas2.pack()
        
        self.canvas2.create_rectangle(50, 40, 200, 110, fill='black', outline='gray')
        self.red_light2 = self.canvas2.create_oval(70, 50, 120, 100, fill='gray')
        self.green_light2 = self.canvas2.create_oval(130, 50, 180, 100, fill='gray')

        # Frame for Input 3 (Horizontal Traffic Light)
        frame3 = tk.Frame(root)
        frame3.grid(row=1, column=2, padx=padding_x, pady=padding_y, sticky="n")
        
        tk.Label(frame3, text="Input 3", font=("Arial", 12, "bold")).pack()
        
        self.canvas3 = tk.Canvas(frame3, width=250, height=150, bg='white', bd=2, relief=tk.GROOVE)
        self.canvas3.pack()
        
        self.canvas3.create_rectangle(50, 40, 200, 110, fill='black', outline='gray')
        self.red_light3 = self.canvas3.create_oval(70, 50, 120, 100, fill='gray')
        self.green_light3 = self.canvas3.create_oval(130, 50, 180, 100, fill='gray')

        # COM Port Selection Frame for Input 1
        com_frame = ttk.LabelFrame(root, text="COM Port Selection for Input 1", padding=(5, 2))
        com_frame.grid(row=0, column=1, padx=padding_x, pady=(10, 2), sticky="n")

        self.com_label = ttk.Label(com_frame, text="Select COM Port:")
        self.com_label.pack(fill="x", pady=(0, 2))

        self.com_ports = self.get_available_ports()
        self.com_var = tk.StringVar()
        self.com_dropdown = ttk.Combobox(com_frame, textvariable=self.com_var, values=self.com_ports)
        self.com_dropdown.pack(fill="x", pady=(0, 2))

        self.connect_button = ttk.Button(com_frame, text="Connect", command=self.connect_serial)
        self.connect_button.pack(fill="x")

        self.disconnect_button = ttk.Button(com_frame, text="Disconnect", command=self.disconnect_serial, state=tk.DISABLED)
        self.disconnect_button.pack(fill="x", pady=(2, 0))

        # COM Selection Port for Output
        com_frame4 = ttk.LabelFrame(root, text="COM Selection Port for Output", padding=(5, 2))
        com_frame4.grid(row=0, column=1, padx=padding_x, pady=(130, 2), sticky="n")

        self.com_label4 = ttk.Label(com_frame4, text="Select COM Port:")
        self.com_label4.pack(fill="x", pady=(0, 2))

        self.com_ports4 = self.get_available_ports()
        self.com_var4 = tk.StringVar()
        self.com_dropdown4 = ttk.Combobox(com_frame4, textvariable=self.com_var4, values=self.com_ports4)
        self.com_dropdown4.pack(fill="x", pady=(0, 2))

        self.connect_button4 = ttk.Button(com_frame4, text="Connect", command=self.connect_serial4)
        self.connect_button4.pack(fill="x")

        self.disconnect_button4 = ttk.Button(com_frame4, text="Disconnect", command=self.disconnect_serial4, state=tk.DISABLED)
        self.disconnect_button4.pack(fill="x", pady=(2, 0))

        # COM Selection Port for BLE
        com_frame_ble = ttk.LabelFrame(root, text="COM Selection Port for BLE", padding=(5, 2))
        com_frame_ble.grid(row=0, column=1, padx=padding_x, pady=(250, 2), sticky="n")

        self.com_label_ble = ttk.Label(com_frame_ble, text="Select COM Port:")
        self.com_label_ble.pack(fill="x", pady=(0, 2))

        self.com_ports_ble = self.get_available_ports()
        self.com_var_ble = tk.StringVar()
        self.com_dropdown_ble = ttk.Combobox(com_frame_ble, textvariable=self.com_var_ble, values=self.com_ports_ble)
        self.com_dropdown_ble.pack(fill="x", pady=(0, 2))

        self.connect_button_ble = ttk.Button(com_frame_ble, text="Connect", command=self.connect_serial_ble)
        self.connect_button_ble.pack(fill="x")

        self.disconnect_button_ble = ttk.Button(com_frame_ble, text="Disconnect", command=self.disconnect_serial_ble, state=tk.DISABLED)
        self.disconnect_button_ble.pack(fill="x", pady=(2, 0))

        # Logic Selection Frame
        logic_frame = ttk.LabelFrame(root, text="Logic Selection", padding=(5, 2))
        logic_frame.grid(row=0, column=1, padx=padding_x, pady=(370, 2), sticky="n")

        self.logic_label = ttk.Label(logic_frame, text="Select Logic:")
        self.logic_label.pack(fill="x", pady=(0, 2))

        self.logic_options = ["TW1", "TW2", "TW3"]
        self.logic_var = tk.StringVar()
        self.logic_dropdown = ttk.Combobox(logic_frame, textvariable=self.logic_var, values=self.logic_options)
        self.logic_dropdown.pack(fill="x", pady=(0, 2))
        self.logic_dropdown.bind("<<ComboboxSelected>>", self.apply_logic)

        # ESP32 connections
        self.esp32 = None  # For Input 1
        self.esp32_output = None  # For Output
        self.esp32_ble = None  # For BLE

        # States for Input 1, Input 2, Input 3, and Output
        self.input1_state = 'gray'
        self.input2_state = 'red'
        self.input3_state = 'red'
        self.output_state = 'gray'

        # Bind click events for Input 2 and Input 3 only (Output is no longer interactive)
        self.canvas2.tag_bind(self.red_light2, '<Button-1>', lambda e: self.toggle_light(2, 'red'))
        self.canvas2.tag_bind(self.green_light2, '<Button-1>', lambda e: self.toggle_light(2, 'green'))
        self.canvas3.tag_bind(self.red_light3, '<Button-1>', lambda e: self.toggle_light(3, 'red'))
        self.canvas3.tag_bind(self.green_light3, '<Button-1>', lambda e: self.toggle_light(3, 'green'))

        # Initial light states
        self.set_light(1, 'gray')
        self.set_light(2, 'red')
        self.set_light(3, 'red')
        self.set_light(4, 'gray')

        # Start real-time updates
        self.update_lights()

    def get_available_ports(self):
        """Return a list of available COM ports."""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports if ports else ["No ports available"]
    
    def connect_serial(self):
        """Connect to the ESP32 via the selected COM port for Input 1."""
        try:
            com_port = self.com_var.get()
            if com_port != "No ports available":
                self.esp32 = serial.Serial(com_port, 115200, timeout=0.1)
                time.sleep(2)
                self.connect_button.config(state=tk.DISABLED)
                self.disconnect_button.config(state=tk.NORMAL)
            else:
                print("No valid COM port selected for Input 1")
        except Exception as e:
            print("Error connecting to ESP32 for Input 1:", e)
            self.esp32 = None
    
    def disconnect_serial(self):
        """Disconnect from the ESP32 for Input 1."""
        if self.esp32:
            self.esp32.close()
            self.esp32 = None
            print("Disconnected from Input 1")
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)

    def connect_serial4(self):
        """Connect to the ESP32 via the selected COM port for Output."""
        try:
            com_port = self.com_var4.get()
            if com_port != "No ports available":
                self.esp32_output = serial.Serial(com_port, 9600, timeout=0.1)
                time.sleep(2)  # Wait for the connection to stabilize
                self.connect_button4.config(state=tk.DISABLED)
                self.disconnect_button4.config(state=tk.NORMAL)
                # Send the current Output state to the ESP32
                self.send_output_command(self.output_state)
                print(f"Connected to ESP32 for Output on {com_port}")
            else:
                print("No valid COM port selected for Output")
        except Exception as e:
            print("Error connecting to ESP32 for Output:", e)
            self.esp32_output = None
    
    def disconnect_serial4(self):
        """Disconnect from the ESP32 for Output."""
        if self.esp32_output:
            # Send 'o' to turn off the lights before disconnecting
            try:
                self.esp32_output.write(b'o')
                print("Sent 'o' to turn off Output lights before disconnecting")
            except Exception as e:
                print("Error sending 'o' command on disconnect:", e)
            self.esp32_output.close()
            self.esp32_output = None
            print("Disconnected from Output")
            self.connect_button4.config(state=tk.NORMAL)
            self.disconnect_button4.config(state=tk.DISABLED)

    def connect_serial_ble(self):
        """Connect to the BLE device via the selected COM port."""
        try:
            com_port = self.com_var_ble.get()
            if com_port != "No ports available":
                self.esp32_ble = serial.Serial(com_port, 115200, timeout=0.1)
                time.sleep(2)
                self.connect_button_ble.config(state=tk.DISABLED)
                self.disconnect_button_ble.config(state=tk.NORMAL)
                # Send the current Output state to the BLE device
                self.send_ble_command(self.output_state)
                print(f"Connected to BLE device on {com_port}")
            else:
                print("No valid COM port selected for BLE")
        except Exception as e:
            print("Error connecting to BLE:", e)
            self.esp32_ble = None
    
    def disconnect_serial_ble(self):
        """Disconnect from the BLE device."""
        if self.esp32_ble:
            # Send '0' to the BLE device before disconnecting
            try:
                self.esp32_ble.write(b'0')
                print("Sent '0' to BLE device before disconnecting")
            except Exception as e:
                print("Error sending '0' to BLE on disconnect:", e)
            self.esp32_ble.close()
            self.esp32_ble = None
            print("Disconnected from BLE")
            self.connect_button_ble.config(state=tk.NORMAL)
            self.disconnect_button_ble.config(state=tk.DISABLED)

    def send_output_command(self, color):
        """Send the output command to the ESP32 with retry logic."""
        if not self.esp32_output:
            print("ESP32 for Output is not connected")
            return False

        max_retries = 3
        for attempt in range(max_retries):
            try:
                if color == 'red':
                    self.esp32_output.write(b'r')
                    print("Sent 'r' to ESP32 for Output (red)")
                elif color == 'green':
                    self.esp32_output.write(b'g')
                    print("Sent 'g' to ESP32 for Output (green)")
                else:
                    self.esp32_output.write(b'o')
                    print("Sent 'o' to ESP32 for Output (off)")
                return True
            except Exception as e:
                print(f"Error sending command to ESP32 (attempt {attempt + 1}/{max_retries}):", e)
                if attempt < max_retries - 1:
                    time.sleep(0.5)  # Wait before retrying
        print("Failed to send command to ESP32 after retries")
        return False

    def send_ble_command(self, color):
        """Send the BLE command (1 for red, 0 for green/gray) with retry logic."""
        if not self.esp32_ble:
            print("BLE device is not connected")
            return False

        max_retries = 3
        for attempt in range(max_retries):
            try:
                if color == 'red':
                    self.esp32_ble.write(b'1')
                    print("Sent '1' to BLE device (Output is red)")
                else:  # green or gray
                    self.esp32_ble.write(b'0')
                    print("Sent '0' to BLE device (Output is green/gray)")
                return True
            except Exception as e:
                print(f"Error sending command to BLE device (attempt {attempt + 1}/{max_retries}):", e)
                if attempt < max_retries - 1:
                    time.sleep(0.5)  # Wait before retrying
        print("Failed to send command to BLE device after retries")
        return False

    def set_light(self, input_num, color):
        """Set the light color for specified input."""
        if input_num == 1:
            self.canvas1.itemconfig(self.red_light1, fill='gray')
            self.canvas1.itemconfig(self.yellow_light1, fill='gray')
            self.canvas1.itemconfig(self.green_light1, fill='gray')
            if color == 'red':
                self.canvas1.itemconfig(self.red_light1, fill='red')
            elif color == 'yellow':
                self.canvas1.itemconfig(self.yellow_light1, fill='yellow')
            elif color == 'green':
                self.canvas1.itemconfig(self.green_light1, fill='green')
            self.input1_state = color
            self.apply_logic(None)
        elif input_num == 2:
            self.canvas2.itemconfig(self.red_light2, fill='gray')
            self.canvas2.itemconfig(self.green_light2, fill='gray')
            if color == 'red':
                self.canvas2.itemconfig(self.red_light2, fill='red')
            elif color == 'green':
                self.canvas2.itemconfig(self.green_light2, fill='green')
            self.input2_state = color
            self.apply_logic(None)
        elif input_num == 3:
            self.canvas3.itemconfig(self.red_light3, fill='gray')
            self.canvas3.itemconfig(self.green_light3, fill='gray')
            if color == 'red':
                self.canvas3.itemconfig(self.red_light3, fill='red')
            elif color == 'green':
                self.canvas3.itemconfig(self.green_light3, fill='green')
            self.input3_state = color
            self.apply_logic(None)
        elif input_num == 4:
            self.canvas4.itemconfig(self.red_light4, fill='gray')
            self.canvas4.itemconfig(self.green_light4, fill='gray')
            if color == 'red':
                self.canvas4.itemconfig(self.red_light4, fill='red')
            elif color == 'green':
                self.canvas4.itemconfig(self.green_light4, fill='green')
            self.output_state = color
            # Send the command to the ESP32 to control the actual lights
            self.send_output_command(color)
            # Send the signal to the BLE device
            self.send_ble_command(color)

    def toggle_light(self, input_num, color):
        """Toggle the light state when clicked for Inputs 2 and 3."""
        if input_num == 2:
            self.input2_state = color
            self.set_light(2, color)
        elif input_num == 3:
            self.input3_state = color
            self.set_light(3, color)

    def apply_logic(self, event):
        """Apply logic based on the selected logic option."""
        logic = self.logic_var.get()
        if not logic:
            return

        # Count the number of inputs that are red
        red_count = 0
        if self.input1_state == 'red':
            red_count += 1
        if self.input2_state == 'red':
            red_count += 1
        if self.input3_state == 'red':
            red_count += 1

        if logic == "TW1":
            # If at least one input is red, output is red; else green
            if red_count >= 1:
                self.set_light(4, 'red')
            else:
                self.set_light(4, 'green')
        elif logic == "TW2":
            # If at least two inputs are red, output is red; else green
            if red_count >= 2:
                self.set_light(4, 'red')
            else:
                self.set_light(4, 'green')
        elif logic == "TW3":
            # If all three inputs are red, output is red; else green
            if red_count == 3:
                self.set_light(4, 'red')
            else:
                self.set_light(4, 'green')

    def update_lights(self):
        """Update lights based on ESP32 input for Input 1 and Output."""
        if self.esp32:
            try:
                if self.esp32.in_waiting > 0:
                    data = self.esp32.readline().decode('utf-8').strip()
                    if data in ['red', 'yellow', 'green']:
                        self.set_light(1, data)
            except Exception as e:
                print("Error reading from ESP32 for Input 1:", e)

        if self.esp32_output:
            try:
                if self.esp32_output.in_waiting > 0:
                    data = self.esp32_output.readline().decode('utf-8').strip()
                    if data in ['red', 'green']:
                        self.set_light(4, data)
            except Exception as e:
                print("Error reading from ESP32 for Output:", e)

        if self.esp32_ble:
            try:
                if self.esp32_ble.in_waiting > 0:
                    data = self.esp32_ble.readline().decode('utf-8').strip()
                    print(f"Received from BLE: {data}")
            except Exception as e:
                print("Error reading from BLE:", e)
        
        self.root.after(50, self.update_lights)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficLightSimulation(root)
    root.mainloop()