import os
import database_updater as du
import database_queries as dq

class SearchObject:
    selected = False
    info = 0
    song_label = ""
    #Instantiated for each search bar result
    def __init__(self, row_tuple):
        self.info = row_tuple
        self.song_label = "{} {} - {}".format(row_tuple[0], row_tuple[1], row_tuple[2])
    
    def toggle_selected(self):
        if self.selected == False:
            self.selected = True
            return
        self.selected = False

    def get_song_id(self):
        return self.info[0]

    def get_song_tuple(self):
        return self.info
    
    def is_selected(self):
        return self.selected
        
    def song_string(self):
        #For use with the GUI interface
        return self.song_label

        
    
class SearchInstance:
    conn = 0
    db_cur = 0
    input_dir = ""
    output_dir = ""
    
    #A list of SearchObject instances
    search_objects = []
    
    def __init__(self, conn, db_cur, input_dir, output_dir):
        #Process everything available for download
        self.conn = conn
        self.db_cur = db_cur
        self.input_dir = input_dir
        self.output_dir = output_dir
        #self.update_search_state(conn, db_cur, input_dir, output_dir)
    
    def get_search_results(self, search_term):
        #Search out of non-downloaded songs (not through database)
        self.search_objects = []
        results = dq.get_search_results(self.conn, self.db_cur, self.input_dir, self.output_dir, search_term)
        #print(len(results))
        for result in results:
            if os.path.isdir(os.path.join(self.input_dir,"{} {} - {}".format(result[0], result[1], result[2]))):
                self.search_objects.append(SearchObject(result))
            
    def extract_selected(self):
        remaining_search_objects = []
        print(self.output_dir)
        for so in self.search_objects:
            if so.is_selected():
                du._extract_song(so.get_song_tuple(), self.conn, self.db_cur, self.input_dir, self.output_dir)
            else:
                try:
                    #Re-initialize a new SearchObject to prevent referencing issues
                    remaining_search_objects.append(SearchObject(so.get_song_tuple()))
                except:
                    print("SearchObject incorrectly initialized")
        #Make sure to commit as the _extract_song() function does not for performance's sake
        self.conn.commit()
        #self.update_search_state(self.conn, self.db_cur, self.input_dir, self.output_dir)
        self.search_objects = remaining_search_objects

    def update_search_state(self, conn, db_cur, input_dir, output_dir):
        self.search_objects = []
        try:
            not_downloaded = dq.get_not_downloaded(conn, db_cur, input_dir, output_dir)
            for tupl in not_downloaded:
                self.search_objects.append(SearchObject(tupl))
        except:
            raise Exception("Data Retrieval Issue")
        
    def view_search_results(self):
        return self.search_objects
        
        
                
            
    



    
