import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from AS7341_measurement import Sensor

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.measure = False
        self.LED_enabled = False
        self.sensor = Sensor()
        self.sensor.configure()
        self.canvas = FigureCanvasTkAgg(self.sensor.fig, master=self)
    
    def measure_spectrum(self):
        self.sensor.ax.clear()
        self.canvas.get_tk_widget().pack(pady=4)
        self.sensor.single_measurement()
        self.sensor.plot_graph(show_graph=False)
        self.canvas.draw()
    
    def LED_status_change(self):
        if self.LED_enabled:
            self.sensor.AS7341_EnableLED(False)
            self.led_btn.configure(text='Turn on LEDs')
        else:
            self.sensor.AS7341_EnableLED(True)
            self.led_btn.configure(text='Turn off LEDs')    
        self.LED_enabled = not self.LED_enabled
    
    def create_window(self):
        self.attributes('-zoomed', True)
        self.title('VIS-NIR spectrum measurement using AS7341 by K. Mistewicz')
        self.measure_btn = tk.Button(self, text='Measure', width=10, bg='lightblue', command=lambda:self.measure_spectrum())
        self.measure_btn.pack(pady=4)
        self.led_btn = tk.Button(self, text='Turn on LEDs', width=10, bg='lightblue', command=lambda:self.LED_status_change())
        self.led_btn.pack(pady=4)
        self.mainloop()


if __name__ == '__main__':
    app = Application()
    app.create_window()
