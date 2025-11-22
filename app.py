from flask import Flask, render_template, request, redirect , url_for
from datetime import datetime
import psycopg2 
import threading
import webview

def db_conn():
    conn = psycopg2.connect(database='Flask_Todo',host ='localhost',user='Tshepang',password ='Testingtesting',port='5432')
    return conn

app=Flask(__name__)

@app.route('/')
def index():
    conn=db_conn()
    cur = conn.cursor()
    cur.execute(''' SELECT * FROM todo_list 
                 ORDER BY is_done ASC, created_at DESC
                ''')
    rows= cur.fetchall()
    cur.close()
    conn.close()

    #Grouping them by date 
    grouped ={}
    for row in rows:
        date_key = row[3].date()
        grouped.setdefault(date_key, []).append(row)
    grouped_list = sorted(grouped.items(), key=lambda x: x[0], reverse=True)

    return render_template('index.html',grouped=grouped_list)

@app.route('/create',methods=['POST','GET'])
def create():
    conn = db_conn()
    cur = conn.cursor()
    if request.method =='POST':
        title =request.form['todo_action']
        description = request.form['todo_description']
        duration =request.form['todo_duration']
        created_at = datetime.utcnow().date()
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

@app.route('/toggle_done',methods =['POST','GET'])
def toggle_done():
    if request.method == 'POST':
        id = request.form['id']
        print(f'✅Record with id:{id} has been marked as done/undone')

        conn = db_conn()
        cur=conn.cursor()
        try:
            #The line SET is_done = Not is_done flips the value each time you click it 
            cur.execute('''
                        UPDATE todo_list 
                        SET is_done = NOT is_done 
                        WHERE id =%s;
                        ''',(id,))
            conn.commit()
            print(f'✅ Record is marked as done or undone')
        except Exception as e:
            print(f"❌ unable to toggle as done/undone:{e}")
        finally:
            cur.close()
            conn.close()
    
    return redirect(url_for('index'))


def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__== '__main__':
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

   # Open PyWebView window
    webview.create_window('Flask Todo App', 'http://127.0.0.1:5000', width=1000, height=700)
    webview.start()