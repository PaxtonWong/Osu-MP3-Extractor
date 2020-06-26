import tkinter as tk
from tkinter import messagebox
import search_functions
import os
from functools import partial
import database_queries as dq
import database_updater as du
mainfont = "Arial"
class Window:
    
    #Initialization with DB, search instance created within.
    def __init__(self, conn, db_cur):
        self.conn = conn
        self.db_cur = db_cur
        self.window = tk.Tk()
        self.window.geometry("400x300")
        self.window.title("Osu! MP3 Extractor: Enter Directory")
        self.result_list_buttons = []
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
        self._clear_screen1()
        self._clear_buttons()
        self.window.title("Osu! MP3 Extractor: Song Search")
        
        search_bar_label = tk.Label(self.window, font = (mainfont, 14), text = "Enter Search Terms:")
        search_bar_label.grid(row = 0, column = 0)
        
        songname_label = tk.Label(self.window, font = (mainfont, 12), text = "Song Name:")
        songname_label.grid(row = 1, column = 0)
        
        author_label = tk.Label(self.window, font = (mainfont, 12), text = "Author:")
        author_label.grid(row = 2, column = 0)
        
        self.search_bar = tk.Entry(self.window, bd = 5)
        self.search_bar.grid(row = 1, column = 1)
        
        self.author_bar = tk.Entry(self.window, bd = 5)
        self.author_bar.grid(row = 2, column = 1)
        
        search_button = tk.Button(self.window, text = "Search", command = self._results_screen)
        search_button.grid(row = 3, column = 1)
        

        
    def _results_screen(self):
        search_term = self.search_bar.get()
        search_author = self.author_bar.get()
        if search_term == "" and search_author == "":
            return
        self.window.title("Osu! MP3 Extractor: Search Results")
        self._clear_buttons()
        self._clear_screen1()
        #retrieve search results into self.search_instance.search_objects
        self.search_instance.get_search_results(search_term, search_author)
        #print(len(self.search_instance.search_objects))
        self.results_label = tk.Label(self.window, text = "{} Result(s):".format(len(self.search_instance.search_objects)), font = (mainfont, 12))
        self.results_label.pack(side = "top")
        extract_button = tk.Button(self.window, text = "Extract Selected", command = self.extract_button_command, font = (mainfont, 12))
        extract_button.pack(side = "bottom")
        back_button = tk.Button(self.window, text = "Back", command = self.search_screen, font = (mainfont, 12))
        back_button.pack(side = "left")
        self.result_bar = tk.Text(self.window, wrap = "none")
        scroll_bar = tk.Scrollbar(orient = "vertical", command = self.result_bar.yview)
        self.result_bar.configure(yscrollcommand = scroll_bar.set)
        scroll_bar.pack(side = "right", fill = "y")
        self.result_bar.pack(fill = "both", expand = True)
        self._render_search_results()

        
    def _render_search_results(self):
        #Reach into self.search_instance to toggle selected SearchObject instances.
        self.result_bar.configure(state = "normal")
        for i in range(len(self.search_instance.search_objects)):
            self.result_list_buttons.append(tk.Button(self.window, text = self.search_instance.search_objects[i].song_string(),
                            command = partial(self._toggle_search_result,i), font = (mainfont, 11), bg = "Gray"))
            self.result_bar.window_create("end", window = self.result_list_buttons[i])
            self.result_bar.insert("end", '\n')
        self.result_bar.configure(state = "disabled")
        
    def extract_button_command(self):
        self.search_instance.extract_selected()
        self._clear_buttons()
        self.result_bar.configure(state = "normal")
        self.result_bar.delete('1.0',tk.END)
        self.results_label.configure(text = "{} Results(s)".format(len(self.search_instance.search_objects)))
        self._render_search_results()

    def _toggle_search_result(self, index):
        #Pass in the corresponding list index of the search result in self.search_instance.search_objects
        #to toggle the search result and change the button color at once. Set button command to this function.
        self.search_instance.search_objects[index].toggle_selected()
        if self.search_instance.search_objects[index].is_selected():
            self.result_list_buttons[index].configure(bg="blue")
        else:
            self.result_list_buttons[index].configure(bg="Gray")
         
        
    def _clear_screen1(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def _clear_buttons(self):
        for button in self.result_list_buttons:
            button.destroy()
        self.result_list_buttons = []

    def directory_check(self):
        input_dir = self.input_dir_bar.get()
        output_dir = self.output_dir_bar.get()
        if not os.path.isdir(input_dir):
            messagebox.showinfo("Error","Please enter in your full Osu! beatmap directory path - ie. ...\osu!\Songs")
            return   
        self.search_instance = search_functions.SearchInstance(self.conn, self.db_cur, input_dir, output_dir)
        if self._new_profile_check(input_dir, output_dir):
            self.search_screen()

    def _quit_message(self):
        if messagebox.askokcancel("Quit", "Close Osu! MP3  application?"):
            self.window.destroy()
            if self.conn:
                print("database closed")
                self.conn.close()

    def destroy_window_protocol(self):
        self.window.protocol("WM_DELETE_WINDOW", self._quit_message)
        self.window.mainloop()
        
    def _new_profile_check(self, input_dir, output_dir):
        if dq.is_new_profile(self.db_cur):
            print("creating new profile")
            messagebox.showinfo("New Profile Detected","Please wait, Osu! MP3 Retriever is updating your song list.")
            du.update_existing_song_list(self.conn, self.db_cur, input_dir)
            #dq.display_songlist(self.db_cur)
        print("# of songs indexed: ",dq.get_songlist_count(self.db_cur))
        return True
        
    
        
        
        


    

