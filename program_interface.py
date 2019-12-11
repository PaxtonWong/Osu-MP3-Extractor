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
        self.destroy_window_protocol()
    
    def _start_screen(self):
        input_label = tk.Label(self.window, font = (mainfont, 14), text = "Osu! Beatmap Directory",padx = 10, pady = 10)
        output_label = tk.Label(self.window, font = (mainfont, 14), text = "Output Folder",padx = 10, pady = 10)
        input_label.grid(row = 0, column = 0)
        output_label.grid(row = 1, column = 0)
        
        self.input_dir_bar = tk.Entry(self.window, bd = 5)
        self.input_dir_bar.grid(row = 0, column = 1)
        self.output_dir_bar = tk.Entry(self.window, bd = 5)
        self.output_dir_bar.grid(row = 1, column = 1)

        start_button = tk.Button(self.window, text = "Next", command = self.directory_check, font = (mainfont, 14))
        start_button.grid(row = 2, column = 1)


    def search_screen(self):
        self._clear_screen()
        self.window.title("Osu! MP3 Extractor: Song Search")
        
        search_bar_label = tk.Label(self.window, font = (mainfont, 14), text = "Enter Search Term:")
        search_bar_label.grid(row = 0, column = 0)
        
        self.search_bar = tk.Entry(self.window, bd = 5)
        self.search_bar.grid(row = 0, column = 1)
        
        search_button = tk.Button(self.window, text = "Search", command = self._results_screen)
        search_button.grid(row = 1, column = 1)


        
    def _results_screen(self):
        self.window.title("Osu! MP3 Extractor: Search Results")
        search_term = self.search_bar.get()
        self._clear_screen()
        #retrieve search results into self.search_instance.search_objects
        self.search_instance.get_search_results(search_term)
        
        num_results = len(self.search_instance.search_objects)
        results_label = tk.Label(self.window, text = "{} Result(s):".format(num_results), font = (mainfont, 12))
        results_label.pack(side = "left")
        self.result_bar = tk.Text(self.window, wrap = "none")
        scroll_bar = tk.Scrollbar(orient = "vertical", command = self.result_bar.yview)
        self.result_bar.configure(yscrollcommand = scroll_bar.set)
        scroll_bar.pack(side = "right", fill = "y")
        self.result_bar.pack(fill = "both", expand = True)
        self._render_search_results()
        
    def _render_search_results(self):
        for i in range(len(self.search_instance.search_objects)):
            res = tk.Button(self.window, text = self.search_instance.search_objects[i].song_string(),
                            command = self.search_instance.search_objects[i].toggle_selected, font = (mainfont, 11))
            self.result_bar.window_create("end", window = res)
            self.result_bar.insert("end", '\n')
        self.result_bar.configure(state = "disabled")
        
    def _clear_screen(self):
        for widget in self.window.grid_slaves():
            widget.destroy()

        
    def directory_check(self):
        input_dir = self.input_dir_bar.get()
        output_dir = self.output_dir_bar.get()
        if not os.path.isdir(input_dir):
            messagebox.showinfo("Error","Please enter in your full Osu! beatmap directory path - ie. ...\osu!\Songs")
            return   
        self.search_instance = search_functions.SearchInstance(self.conn, self.db_cur, input_dir, output_dir)
        self.search_screen()

    def _quit_message(self):
        if messagebox.askokcancel("Quit", "Close Osu! MP3 Extractor application?"):
            self.window.destroy()
            if self.conn:
                print("database closed")
                self.conn.close()

    def destroy_window_protocol(self):
        self.window.protocol("WM_DELETE_WINDOW", self._quit_message)
        self.window.mainloop()
        
        


