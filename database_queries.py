import database_updater as du
import search_functions as sf
import sqlite3

def get_not_downloaded(conn, db_cur, input_dir, output_dir):
    du.update_existing_song_list(conn, db_cur, input_dir)
    du.clear_deleted_downloads(conn, db_cur, output_dir)
    db_cur.execute('''SELECT * FROM songlist
                    LEFT JOIN downloaded ON songlist.id = downloaded.id
                    WHERE downloaded.id IS NULL;''')
    
    return db_cur.fetchall()

def display_songlist(db_cur):
    #Debugging function
    db_cur.execute("SELECT * FROM songlist;")
    songlist = db_cur.fetchall()
    for song in songlist:
        print(song)

def display_downloaded(db_cur):
    #Debugging function
    db_cur.execute("SELECT * FROM downloaded;")
    downloaded = db_cur.fetchall()
    for download in downloaded:
        print(download)

