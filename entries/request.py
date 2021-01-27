import sqlite3
import json
from models import Entry
from models import Mood


def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id,
            m.id m_id,
            m.label mood_label

        FROM entry e
        JOIN mood m
            ON e.mood_id =  m.id  
        """)

        # Initialize an empty list to hold all animal representations
        entries = []

        # Convert rows of data into a Python list
        # This fills the dataset list to be iterated over below
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            entry = Entry(row['id'], row['concept'], row['entry'],
                            row['date'], row['mood_id'])
                            
            mood = Mood(row['m_id'], row['mood_label'])

            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
        return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id           
        FROM entry e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory

        data = db_cursor.fetchone()

        # Create an entry instance from the current row from class
        # These data columns need match up exactly with parameters
        # in the class object. This is a Python object
        entry = Entry(data['id'], data['concept'], data['entry'],
                            data['date'], data['mood_id'])
        # The __dict__ converts it to a dictionary and then the 
        # json dumps converts is to json or a javascript object
        # to be sent to the client.
    return json.dumps(entry.__dict__)

def delete_entry(id):

    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entry
        WHERE id = ?
        """, (id, ))

def create_journal_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entry
            ( concept, entry, date, mood_id)
        VALUES
            ( ?, ?, ?, ?);   
        """, (new_entry['concept'], 
            new_entry['entry'], 
            new_entry['date'],
            new_entry['moodId']
            , ))

        id = db_cursor.lastrowid

        new_entry['id'] = id
    
    return json.dumps(new_entry)

def get_entries_by_search(search_term):

    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id,
            m.id m_id,
            m.label mood_label

        FROM entry e
        JOIN mood m
            ON e.mood_id =  m.id  
        WHERE e.entry LIKE ?
        """ , ("%" + search_term + "%", ))

        entries =[]
        dataset = db_cursor.fetchall()

        for row in dataset:
            
            # Instantiate an entry
            entry = Entry(row['id'], row['concept'], row['entry'],
                            row['date'], row['mood_id'])
            # Instantiate a mood          
            mood = Mood(row['m_id'], row['mood_label'])

            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    return json.dumps(entries)
        
        