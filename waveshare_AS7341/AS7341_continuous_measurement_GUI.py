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
    
    def continuous_measurement(self):
        self.measure_spectrum()
        if self.measure:
            self.after(500, self.continuous_measurement)
    
    def start_stop(self):
        self.measure = not self.measure
        print('btn pressed'+str(self.measure))
        if self.measure:
            self.start_stop_btn.configure(text='STOP')
            self.continuous_measurement()
        else:
            self.start_stop_btn.configure(text='START')
        
    def measure_spectrum(self):
        self.sensor.ax.clear()
        self.canvas.get_tk_widget().pack(pady=4)
        self.sensor.single_measurement()
        self.sensor.plot_graph(show_graph=False)
        self.canvas.draw()
        self.update()
    
    def LED_status_change(self):
        if self.LED_enabled:
            self.sensor.AS7341_EnableLED(False)
            self.led_btn.configure(text='Turn on LEDs')
        else:
            self.sensor.AS7341_EnableLED(True)
            self.led_btn.configure(text='Turn off LEDs')    
        self.LED_enabled = not self.LED_enabled
    
    def save_data(self):
        self.sensor.write_data_to_file('measured_data.txt')
    
    def create_window(self):
        self.attributes('-zoomed', True)
        self.title('VIS-NIR spectrum measurement using AS7341 by K. Mistewicz')
        self.start_stop_btn = tk.Button(self, text='START', width=10, bg='lightblue', command=lambda:self.start_stop())
        self.start_stop_btn.pack(pady=4)
        self.led_btn = tk.Button(self, text='Turn on LEDs', width=10, bg='lightblue', command=lambda:self.LED_status_change())
        self.led_btn.pack(pady=4)
        self.save_btn = tk.Button(self, text='Save data', width=10, bg='lightblue', command=lambda:self.save_data())
        self.save_btn.pack(pady=4)
        self.mainloop()


if __name__ == '__main__':
    app = Application()
    app.create_window()
