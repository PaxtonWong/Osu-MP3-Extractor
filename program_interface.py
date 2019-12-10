import tkinter as tk
from tkinter import messagebox
import search_functions
import os
mainfont = "Arial"
class Window:
    
    #Initialization with DB, search instance created within.
    def __init__(self, conn, db_cur):
        self.conn = conn
        self.db_cur = db_cur
        self.window = tk.Tk()
        self.window.geometry("400x300")
        self.window.title("Osu! MP3 Extractor: Enter Directory")
        self._start_screen()
    
    def _start_screen(self):
        self.input_label = tk.Label(self.window, font = (mainfont, 14), text = "Osu! Beatmap Directory",padx = 10, pady = 10)
        self.output_label = tk.Label(self.window, font = (mainfont, 14), text = "Output Folder",padx = 10, pady = 10)
        self.input_label.grid(row = 0, column = 0)
        self.output_label.grid(row = 1, column = 0)
        
        self.input_dir_bar = tk.Entry(self.window, bd = 5)
        self.input_dir_bar.grid(row = 0, column = 1)
        self.output_dir_bar = tk.Entry(self.window, bd = 5)
        self.output_dir_bar.grid(row = 1, column = 1)

        self.start_button = tk.Button(self.window, text = "Next", command = self.directory_check, font = (mainfont, 14))
        self.start_button.grid(row = 2, column = 1)


    def search_screen(self):
        self._hide_start_screen()
        self.window.title("Osu! MP3 Extractor: Song Search")
        
        self.search_bar_label = tk.Label(self.window, font = (mainfont, 14), text = "Enter Search Term:")
        self.search_bar_label.grid(row = 0, column = 0)
        
        self.search_bar = tk.Entry(self.window, bd = 5)
        self.search_bar.grid(row = 0, column = 1)
        
        self.search_button = tk.Button(self.window, text = "Search", command = self._results_screen)
        self.search_button.grid(row = 1, column = 1)

        
    def _results_screen(self):
        self.window.title("Osu! MP3 Extractor: Search Results")
        search_term = self.search_bar.get()
        #retrieve search results using self.search_instance.get_search_results(search_term)
        #results = self.search_instance.get_search_results(search_term)

    def _hide_start_screen(self):
        #Hides start screen widgets but saves their state.
        for widget in self.window.grid_slaves():
            widget.destroy()

        
    def directory_check(self):
        input_dir = self.input_dir_bar.get()
        output_dir = self.output_dir_bar.get()
        if not os.path.isdir(input_dir):
            messagebox.showinfo("Error","Please enter in your full Osu! beatmap directory path - ie. ...\osu!\Songs")
            return   
        #self.search_instance = search_functions.SearchInstance(self.conn, self.db_cur, input_dir, output_dir)
        self.search_screen()
        


