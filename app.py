import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect , url_for
from datetime import datetime,timezone
import psycopg2 

load_dotenv()

def db_conn():
    return psycopg2.connect(
        database = os.getenv("DB_NAME"),
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        port =os.getenv("DB_PORT")
    )

app=Flask(__name__)

@app.route('/')
def index():
    conn=db_conn()
    cur = conn.cursor()
    
    # Get a list of incomplete tasks 
    cur.execute(''' SELECT * FROM todo_list 
                 WHERE is_done = FALSE 
                 ORDER BY created_at DESC
                ''')
    active_rows= cur.fetchall()

    #Get a list of completed tasks
    cur.execute('''
        SELECT * FROM todo_list
        WHERE is_done = TRUE
        ORDER BY created_at DESC
        ''')
    completed_row= cur.fetchall()

    cur.close()
    conn.close()

    #Grouping active tasks by date 
    grouped_active ={}#Create a dictionary
    for row in active_rows:
        date_key = row[3].date()
        grouped_active.setdefault(date_key, []).append(row)

    grouped_active = sorted(grouped_active.items(), key=lambda x: x[0], reverse=True)

    #Grouping completed tasks by date
    grouped_done= {}
    for row in completed_row:
        date_key= row[3].date()
        grouped_done.setdefault(date_key,[]).append(row)

    grouped_done = sorted(grouped_done.items(), key=lambda x: x[0], reverse=True)

    return render_template('index.html',grouped_active=grouped_active , grouped_done=grouped_done)

@app.route('/create',methods=['POST','GET'])
def create():
    conn = db_conn()
    cur = conn.cursor()
    if request.method =='POST':
        title =request.form['todo_action']
        description = request.form['todo_description']
        duration =request.form['todo_duration']
        created_at = datetime.now(timezone.utc)
        cur.execute('''
        INSERT INTO todo_list (title,description,created_at,duration)
        VALUES(%s,%s,%s,%s)
        ''',(title,description,created_at,duration))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index'))
    
@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        id = request.form['id']
        print(f"🟢 Deleting record with ID: {id}")

        conn = db_conn()
        cur = conn.cursor()
        try:
            cur.execute('''DELETE FROM todo_list WHERE id = %s''', (id,))
            conn.commit()
            print('✅ Record deleted successfully')
        except Exception as e:
            print(f'❌ Error deleting record: {e}')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('index'))

@app.route('/toggle_done', methods=['POST'])
def toggle_done():
    # Only allow POST for toggling
    id_raw = request.form.get('id')
    try:
        id = int(id_raw)
    except (TypeError, ValueError):
        print(f"❌ toggle_done got invalid id: {id_raw}")
        return redirect(url_for('index'))

    print(f'✅ Toggling done state for id: {id}')

    conn = db_conn()
    cur = conn.cursor()
    try:
        cur.execute('''
            UPDATE todo_list
            SET is_done = NOT is_done
            WHERE id = %s
        ''', (id,))
        conn.commit()
        print(f'✅ Rows updated: {cur.rowcount}')
    except Exception as e:
        print(f"❌ unable to toggle as done/undone: {e}")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('index'))

if __name__== '__main__':
    app.run()
  