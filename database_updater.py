import os
import sqlite3
import re
import shutil

def _parse_name(folder_name):
    #Seperate the segments of the song's folder name.
    song_id = ""
    author = ""
    song_name = ""
    index = 0
    length = len(folder_name)
    while 1: 
        if not folder_name[index] == ' ':
            song_id += folder_name[index]
            index += 1
        else:
            break
        
    while 1:
        if not folder_name[index] == '-':
            author += folder_name[index]
            index += 1
        else:
            author = str(author[1:len(author)-1])
            break
        
    song_name = (folder_name[index:length])[2:length]
    return song_id, author, song_name

def _insert_song_entry(conn, db_cur, folder_name, songs_dir):
    #No commit here because of performance. Intended for repeated calls.
    #Checks within the song folder for the mp3 file and stores directory location.
    file_name_checker = re.compile("[0-9]+ .+ - .+")
    if file_name_checker.match(folder_name):
        _, author, song_name = _parse_name(folder_name)
        file_list = os.listdir(os.path.join(songs_dir, folder_name))    
        cur_mp3 = ""   
        
        #Try statement in order to account for bad .osu file names

        song_id = _get_unique_id(songs_dir, folder_name)
        print(song_id)
     
        for file_name in file_list:
            _, ext = os.path.splitext(file_name)
            if ext == ".mp3":
                cur_mp3 = file_name
                break
        if len(cur_mp3) != 0:
            #check to make sure that an mp3 actually exists
            try:
                db_cur.execute('''INSERT INTO songlist(id, author, songname, filename) 
                VALUES (?,?,?,?);''',(int(song_id), author, song_name, cur_mp3))
            except:
                print(folder_name)
                conn.rollback()

                    
def _extract_song(row, conn, db_cur, input_dir, output_dir):
    file_loc = os.path.join("{} {} - {}".format(row[0],row[1],row[2]),row[3])
    file_loc = os.path.join(input_dir, file_loc)
    output_loc = os.path.join(output_dir, "{} {} - {}.mp3".format(row[0],row[1],row[2]))
        
    if os.path.isfile(file_loc):
        if not os.path.isfile(output_loc):
            shutil.copyfile(file_loc, output_loc)
            try:
                db_cur.execute('''INSERT INTO downloaded(id) VALUES (?)''',(row[0],))
                return 1
            except:
                conn.rollback()
    else:
        #give user a message that original song folder was deleted
        try:
            db_cur.execute('''DELETE FROM songlist WHERE songlist.id = ?''', row[0])
        except:
            conn.rollback()
    return 0

        
def create_new_database(conn, db_cur, songs_dir):
    dir_list = os.listdir(songs_dir)
    for folder_name in dir_list:
        _insert_song_entry(conn, db_cur, folder_name, songs_dir)
    conn.commit()
    

def update_existing_song_list(conn, db_cur, songs_dir):
    dir_list = os.listdir(songs_dir)
    db_cur.execute('''SELECT MAX(timestamp) FROM timestamps;''')
    latest_timestamp = db_cur.fetchone()[0]
    if latest_timestamp == None:
        latest_timestamp = 0
    update_list = []
    new_timestamp = 0
    for folder_name in dir_list:
        timestamp = os.path.getmtime(os.path.join(songs_dir,folder_name))        
        if timestamp > latest_timestamp:
            update_list.append(folder_name)
        if timestamp > new_timestamp:
            new_timestamp = timestamp
            
    for folder_name in update_list:
        #May need to somehow prevent inserting of duplicate row, if existing folder was modified.
        _insert_song_entry(conn, db_cur, folder_name, songs_dir)
    try:
        db_cur.execute('''INSERT INTO timestamps(timestamp) VALUES (?)''',(new_timestamp,))
    except:
        print("Timestamp insert failed")
        conn.rollback()
    conn.commit()
       

def clear_deleted_downloads(conn, db_cur, downloaded_dir):
    dir_list = os.listdir(downloaded_dir)
    db_cur.execute('''SELECT songlist.id, songlist.author, songlist.songname
                    FROM songlist
                    INNER JOIN downloaded ON songlist.id = downloaded.id;''')
    rows = db_cur.fetchall()
    delete_list = []
    for row in rows:
        if not os.path.isfile(os.path.join(downloaded_dir,"{} {} - {}.mp3".format(row[0], row[1], row[2]))):
            delete_list.append((row[0],))
    db_cur.executemany('''DELETE FROM downloaded WHERE downloaded.id = ?''', delete_list)
    conn.commit()
        
def extract_all_songs(conn, db_cur, input_dir, output_dir):
    #extraction should only occur using table entries from songlist.
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    try:
        db_cur.execute('''SELECT * FROM songlist;''')
        rows = db_cur.fetchall()
    except:
        print("Error extracting songs.\n")
        return
    extracted = 0
    for row in rows:
        extracted += _extract_song(row, conn, db_cur, input_dir, output_dir)
                
    conn.commit()
    print("Songs extracted: {}\n".format(extracted))

def _get_unique_id(input_dir, current_folder_name):
    #Get the beatmap id from the .OSU file to acquire primary key
    full_path = os.path.join(input_dir, current_folder_name)
    file_list = os.listdir(full_path)
    osu_file = ""
    beatmap_id = 0
    
    for file_name in file_list:
        _, ext = os.path.splitext(file_name)
        if ext == ".osu":
            osu_file = file_name   
            break   
    osu_file = os.path.join(full_path,osu_file)
    if not os.path.isfile(osu_file):
        print(osu_file)
        
    with open(osu_file, encoding = "UTF-8") as osf:
        buffer = osf.read(1600)
        split_text = re.split("\n|:",buffer)
        
        for ind in range(len(split_text)):
            if split_text[ind] == "BeatmapID":
                return int(split_text[ind+1])
            
    return beatmap_id
    

def connect_db(db_name):
    #Connect to the database File and return the connection.
    try:
        song_base = sqlite3.connect(db_name)
        db_cur = song_base.cursor()
        db_cur.execute('''CREATE TABLE IF NOT EXISTS
                   songlist(
                   id INTEGER NOT NULL,
                   author TEXT,
                   songname TEXT,
                   filename TEXT,
                   PRIMARY KEY (id));''')
        db_cur.execute('''CREATE TABLE IF NOT EXISTS
                    downloaded(
                    id INTEGER PRIMARY KEY NOT NULL,
                    FOREIGN KEY (id) REFERENCES songlist (id)
                    );''')
        db_cur.execute('''CREATE TABLE IF NOT EXISTS
                    timestamps(
                    timestamp REAL
                    );''')
    except:
        print("Couldn't Connect to Database. Closing...\n")
        song_base.rollback()
        return None
    else:
        song_base.commit()
        return song_base, db_cur





    
    
    
    
