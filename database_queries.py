import database_updater as du


def get_not_downloaded(conn, db_cur, input_dir, output_dir):
    du.update_existing_song_list(conn, db_cur, input_dir)
    du.clear_deleted_downloads(conn, db_cur, output_dir)
    db_cur.execute('''SELECT * FROM songlist
                    LEFT JOIN downloaded ON (songlist.author = downloaded.author 
                    AND songlist.songname = downloaded.songname)
                    WHERE (downloaded.songname IS NULL OR downloaded.author is NULL);''')
    return db_cur.fetchall()

def get_search_results(conn, db_cur, input_dir, output_dir, songname:str = "", author:str = ""):
    du.update_existing_song_list(conn, db_cur, input_dir)
    du.clear_deleted_downloads(conn, db_cur, output_dir)
    print(songname, author)
    author_query = "AND songlist.author LIKE '%{}%'".format(author)
    songname_query = "AND songlist.songname LIKE '%{}%'".format(songname)
    if author == "":
        author_query = ""
    if songname == "":
        songname_query = ""
    db_cur.execute("""SELECT * FROM songlist
                    LEFT JOIN downloaded ON (songlist.author = downloaded.author 
                    AND songlist.songname = downloaded.songname)
                    WHERE ((downloaded.songname IS NULL OR downloaded.author is NULL)
                    {} {});""".format(songname_query,author_query))
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
        
def is_new_profile(db_cur):
    db_cur.execute("SELECT COUNT(id) FROM songlist")
    if db_cur.fetchone()[0] == 0:
        return True
    return False

def get_songlist_count(db_cur):
    db_cur.execute("SELECT COUNT(id) FROM songlist")
    return db_cur.fetchone()[0]
