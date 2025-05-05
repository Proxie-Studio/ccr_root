import tkinter as tk
from tkinter import ttk
import serial
import time
import serial.tools.list_ports

class TrafficLight:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Light Simulation")
        self.root.configure(bg="#f0f0f0")

        # Canvas
        self.canvas = tk.Canvas(root, width=200, height=300, bg='white', bd=2, relief=tk.GROOVE)
        self.canvas.grid(row=0, column=0, padx=20, pady=20, rowspan=3)

        # Traffic light frame
        self.canvas.create_rectangle(50, 50, 150, 250, fill='black', outline='gray')
        self.red_light = self.canvas.create_oval(75, 60, 125, 110, fill='gray')
        self.green_light = self.canvas.create_oval(75, 160, 125, 210, fill='gray')
        self.current_light = "red"
        self.update_light()

        # COM Port Selection Frame
        com_frame = ttk.LabelFrame(root, text="COM Port Selection", padding=(10, 5))
        com_frame.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        self.com_label = ttk.Label(com_frame, text="Select COM Port:")
        self.com_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.com_ports = self.get_available_ports()
        self.com_var = tk.StringVar()
        self.com_dropdown = ttk.Combobox(com_frame, textvariable=self.com_var, values=self.com_ports)
        self.com_dropdown.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        self.connect_button = ttk.Button(com_frame, text="Connect", command=self.connect_serial)
        self.connect_button.grid(row=2, column=0, sticky="ew")

        self.disconnect_button = ttk.Button(com_frame, text="Disconnect", command=self.disconnect_serial, state=tk.DISABLED)
        self.disconnect_button.grid(row=3, column=0, sticky="ew", pady=(5,0))

        self.arduino = None

        # Control Buttons Frame
        control_frame = ttk.LabelFrame(root, text="Control", padding=(10, 5))
        control_frame.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        control_frame.columnconfigure(0, weight=1)

        self.red_button = ttk.Button(control_frame, text="Red", command=self.turn_red, state=tk.DISABLED)
        self.red_button.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        self.green_button = ttk.Button(control_frame, text="Green", command=self.turn_green, state=tk.DISABLED)
        self.green_button.grid(row=1, column=0, sticky="ew")

        style = ttk.Style()
        style.configure("TButton", padding=5, font=('Arial', 10))
        style.configure("TLabelframe.Label", font=('Arial', 11, 'bold'))
        style.configure("TLabel", font=('Arial', 10))
        style.configure("TCombobox", font=('Arial', 10))

        self.canvas.tag_bind(self.red_light, "<Button-1>", lambda event: self.set_light("red"))
        self.canvas.tag_bind(self.green_light, "<Button-1>", lambda event: self.set_light("green"))

    def set_light(self, light_color):
        if self.arduino and self.arduino.is_open:
            if light_color == "red":
                self.turn_red()
            elif light_color == "green":
                self.turn_green()

    def get_available_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports

    def connect_serial(self):
        selected_port = self.com_var.get()
        if selected_port:
            try:
                self.arduino = serial.Serial(selected_port, 9600, timeout=1)
                time.sleep(2)
                self.red_button.config(state=tk.NORMAL)
                self.green_button.config(state=tk.NORMAL)
                self.connect_button.config(state=tk.DISABLED)
                self.com_dropdown.config(state=tk.DISABLED)
                self.disconnect_button.config(state=tk.NORMAL)
                print(f"Connected to {selected_port}")
            except serial.SerialException as e:
                print(f"Error connecting to {selected_port}: {e}")
        else:
            print("Please select a COM port.")

    def disconnect_serial(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            self.arduino = None
            self.red_button.config(state=tk.DISABLED)
            self.green_button.config(state=tk.DISABLED)
            self.connect_button.config(state=tk.NORMAL)
            self.com_dropdown.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)
            print("Disconnected.")

    def update_light(self):
        colors = {"red": ("red", "gray"),
                  "green": ("gray", "green")}

        self.canvas.itemconfig(self.red_light, fill=colors[self.current_light][0])
        self.canvas.itemconfig(self.green_light, fill=colors[self.current_light][1])

    def turn_red(self):
        self.current_light = "red"
        self.update_light()
        self.send_to_arduino('r')

    def turn_green(self):
        self.current_light = "green"
        self.update_light()
        self.send_to_arduino('g')

    def send_to_arduino(self, command):
        if self.arduino and self.arduino.is_open:
            self.arduino.write(command.encode())

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficLight(root)
    root.mainloop()
