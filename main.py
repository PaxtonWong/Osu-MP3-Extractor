import database_updater as du
import search_functions as sf
import program_interface as pi

def do_search(song_base, db_cur, songs_dir, output_dir):
    instance = sf.SearchInstance(song_base, db_cur, songs_dir, output_dir)
    search_for = input()
    results = instance.get_search_results(search_for)
    for result in results:
        print(result.song_string())

if __name__ == '__main__':
    db_name = "song_extract.db"
    song_base, db_cur = du.connect_db(db_name)
    if song_base:
        app_window = pi.Window(song_base, db_cur)
        
##        while 1:
##            user_input = input()
##            if user_input == "cr new db":
##                du.create_new_database(song_base, db_cur, songs_dir)
##            elif user_input == "upd sl":
##                du.update_existing_song_list(song_base, db_cur, songs_dir)
##            elif user_input == "clr del dwnl":
##                du.clear_deleted_downloads(song_base, db_cur, output_dir)
##            elif user_input == "extr all":
##                du.extract_all_songs(song_base, db_cur, songs_dir, output_dir)
##            elif user_input == "search":
##                do_search(song_base, db_cur, songs_dir, output_dir)
##            elif user_input == "quit":
##                break
##            elif user_input == "display songlist":
##                du.display_songlist(db_cur)
##            elif user_input == "display downloaded":
##                du.display_downloaded(db_cur)
##            elif user_input == "display non-downloaded":
##                temp1 = dq.get_not_downloaded(song_base, db_cur, songs_dir, output_dir)
##                for entry in temp1:
##                    print(entry[0])
##            else:
##                print("Invalid Command")

    
