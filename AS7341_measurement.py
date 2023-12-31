import time
import sys
import os
import logging
from waveshare_AS7341 import AS7341
import matplotlib.pyplot as plt
import pandas as pd


class Sensor(AS7341.AS7341):
    def __init__(self):
        super().__init__()
        self.measured_values = [] # The data measured by the light sensor
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
    
    def configure(self, LEDs_enabled=False):
        logging.basicConfig(level=logging.INFO)
        self.measureMode = 0
        self.AS7341_ATIME_config(100)
        self.AS7341_ASTEP_config(999)
        self.AS7341_AGAIN_config(6)
        self.AS7341_EnableLED(LEDs_enabled) #The LEDs enabling/disabling
        self.AS7341_ControlLed(True,10)
    
    def single_measurement(self):
        self.measured_values = []
        self.AS7341_startMeasure(0)
        self.AS7341_ReadSpectralDataOne()
        self.measured_values.append(self.channel1)
        self.measured_values.append(self.channel2)
        self.measured_values.append(self.channel3)
        self.measured_values.append(self.channel4)
        self.AS7341_startMeasure(1)
        self.AS7341_ReadSpectralDataTwo()
        self.measured_values.append(self.channel5)
        self.measured_values.append(self.channel6)
        self.measured_values.append(self.channel7)
        self.measured_values.append(self.channel8)
        self.measured_values.append(self.NIR)
        
    def print_measured_values(self):
        print('------------------------')
        print('channel 1 (405-425nm): ', self.measured_values[0])
        print('channel 2 (435-455nm): ', self.measured_values[1])
        print('channel 3 (470-490nm): ', self.measured_values[2])
        print('channel 4 (505-525nm): ', self.measured_values[3])
        print('channel 5 (545-565nm): ', self.measured_values[4])
        print('channel 6 (580-600nm): ', self.measured_values[5])
        print('channel 7 (620-640nm): ', self.measured_values[6])
        print('channel 8 (670-690nm): ', self.measured_values[7])
        print('channel NIR: ', self.measured_values[8])
        print('------------------------')        
        time.sleep(1)
    
    def write_data_to_file(self, filename):
        path = os.getcwd()
        file = open(path+'/'+filename, 'w')
        file.write('channel 1 (405-425nm): '+str(self.measured_values[0])+'\n')
        file.write('channel 2 (435-455nm): '+str(self.measured_values[1])+'\n')
        file.write('channel 3 (470-490nm): '+str(self.measured_values[2])+'\n')
        file.write('channel 4 (505-525nm): '+str(self.measured_values[3])+'\n')
        file.write('channel 5 (545-565nm): '+str(self.measured_values[4])+'\n')
        file.write('channel 6 (580-600nm): '+str(self.measured_values[5])+'\n')
        file.write('channel 7 (620-640nm): '+str(self.measured_values[6])+'\n')
        file.write('channel 8 (670-690nm): '+str(self.measured_values[7])+'\n')
        file.write('channel NIR: '+str(self.measured_values[8])+'\n')
        file.close()
    
    def plot_graph(self, show_graph=True):
        bars = ['410', '440', '470', '510', '550', '583', '620', '670', 'NIR']
        dictionary = {'bars': bars, 'values': self.measured_values}
        df = pd.DataFrame(dictionary)
        colors = ['#7e00db', '#0000ff', '#00a9ff', '#00ff00', '#a3ff00', '#fff600', '#ff7700', '#ff0000', 'black']
        # fig, ax = plt.subplots()
        # self.fig = plt.figure()
        self.ax.bar(df['bars'], df['values'], color=colors)
        plt.ylabel('light intensity, counts')
        plt.xlabel('wavelength, nm')
        if show_graph:
            self.fig.show()
        # return fig


if __name__ == '__main__':
    sensor = Sensor()
    sensor.configure()
    sensor.single_measurement()
    sensor.print_measured_values()
    sensor.write_data_to_file('data.txt')
    sensor.plot_graph()