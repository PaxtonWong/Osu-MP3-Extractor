import database_updater as du
import database_queries as dq
import search_functions as sf
import sqlite3
import string
def do_search(song_base, db_cur, songs_dir, output_dir):
    instance = sf.SearchInstance(song_base, db_cur, songs_dir, output_dir)
    search_for = input()
    results = instance.get_search_results(search_for)
    for result in results:
        print(result.song_string())

if __name__ == '__main__':
    songs_dir = input()
    output_dir = input()
    song_base, db_cur = du.connect_db("song_extract.db")
    if song_base:

        while 1:
            user_input = input()
            if user_input == "cr new db":
                du.create_new_database(song_base, db_cur, songs_dir)
            elif user_input == "upd sl":
                du.update_existing_song_list(song_base, db_cur, songs_dir)
            elif user_input == "clr del dwnl":
                du.clear_deleted_downloads(song_base, db_cur, output_dir)
            elif user_input == "extr all":
                du.extract_all_songs(song_base, db_cur, songs_dir, output_dir)
            elif user_input == "search":
                do_search(song_base, db_cur, songs_dir, output_dir)
            elif user_input == "quit":
                break
            elif user_input == "display songlist":
                du.display_songlist(db_cur)
            elif user_input == "display downloaded":
                du.display_downloaded(db_cur)
            elif user_input == "display non-downloaded":
                temp1 = dq.get_not_downloaded(song_base, db_cur, songs_dir, output_dir)
                for entry in temp1:
                    print(entry[0])
            else:
                print("Invalid Command")
        if song_base:
            song_base.close()
    
