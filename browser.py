from tkinter import *
import webview




def ejecutar():

    # define an instance of tkinter
    root = Tk()
      
    #  size of the window where we show our website
    root.geometry("800x450")

    webview.create_window('Reporte', 'http://127.0.0.1:8050/')






    webview.start()


if __name__ == '__main__':
    ejecutar()