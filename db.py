import sqlite3
con = sqlite3.connect("tutorial.db")
cur = con.cursor()

global_event_id = 0

# cur.execute("""CREATE TABLE users 
#     (
#     user_id INTEGER,
#     name TEXT,
#     quetion_number INTEGER,
#     event_id INTEGER
#     )""")

# cur.execute("""CREATE TABLE events 
#     (
#     event_id INTEGER,
#     name_of_event TEXT,
#     category TEXT,
#     place TEXT,
#     time TEXT,
#     who TEXT,
#     description TEXT,
#     status TEXT,
#     user_id INTEGER
#     )""")

def add_user(user_id):
    if len(list(cur.execute(f"SELECT quetion_number FROM users WHERE user_id = {user_id}"))) == 0:
        cur.execute(f"""
        INSERT INTO users VALUES ({user_id}, 'name', -1, -1)
        """)
        con.commit()


def get_events(user_id):
    add_user(user_id)
    return list(cur.execute(f"SELECT name_of_event, place, category, who, time, description FROM events WHERE user_id = {user_id} AND status = 'active'"))


def get_all_events():
    return list(cur.execute(f"SELECT name_of_event, place, category, who, time, description FROM events WHERE status = 'active'"))

def add_event(user_id):
    add_user(user_id)
    global global_event_id
    cur.execute(f"""
    INSERT INTO events VALUES ({global_event_id}, '', '', '', '', '', '', 'inactive', {user_id})
    """)
    con.commit()
    global_event_id += 1
    return global_event_id - 1

def upd_event(event_id, key, value):
    cur.execute(f"""UPDATE events 
    SET {key} = '{value}' 
    WHERE event_id = {event_id}""")
    con.commit()

def upd_cur_event(user_id, event_id):
    add_user(user_id)
    cur.execute(f"""UPDATE users 
    SET event_id = {event_id}
    WHERE user_id = {user_id}""")

    cur.execute(f"""UPDATE users 
    SET quetion_number = 0
    WHERE user_id = {user_id}""")
    con.commit()

def get_quetion_number(user_id):
    add_user(user_id)
    res = int(list(cur.execute(f"SELECT quetion_number FROM users WHERE user_id = {user_id}"))[0][0])
    cur.execute(f"""UPDATE users 
    SET quetion_number = quetion_number + 1
    WHERE user_id = {user_id}""")
    con.commit()
    return res

def get_event_id(user_id):
    add_user(user_id)
    res = int(list(cur.execute(f"SELECT event_id FROM users WHERE user_id = {user_id}"))[0][0])
    return res
