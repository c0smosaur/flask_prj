from flask import render_template, request, Blueprint, session
import sqlite3
import pandas as pd

def get_db(db_name):
    return sqlite3.connect(db_name)

def exe_sql(conn, command: str):
    try: 
        conn.execute(command)
        conn.commit()

        if command.split()[0].lower() == 'select':
            df = pd.read_sql(command, conn, index_col=None)
            df_html = df.to_html()
            return df_html, 1
        else:
            return None, 1
    except:
        return None, 0

# --------------------------------------------------------------------------------

# bp = Flask(__name__)
bp = Blueprint("app_data",__name__,url_prefix="/sql")

@bp.route('/')
def index():
    if session['login']:
        return render_template("data.html")
    else:
        return render_template('login.html', message="You need to login first.")

# @bp.route('/command', methods=['POST'])
# def command():
#     return "TEST" + request.form.get('first_test')

# @bp.route('/data')
# def data_pg():
#     return render_template('data.html')

@bp.route('/dbsql', methods=["POST"])
def sql_test():
    if request.method=="POST":
        db_name = request.form.get('db_name')
        sql_command = request.form.get('sql')

        conn = get_db(db_name)

        output, status = exe_sql(conn, sql_command)

        if status==1:
            # 처리됨
            return render_template('data.html', label="Success") + output

        else:
            # 처리 안됨
            return render_template('data.html', label="Error", output=None)
    
    return db_name + sql_command



# Q: 그럼 만약에 내가 새 창으로 결과를 띄우고 싶다면? 아예 새로운 html을 만들어줘야 하나? 
# A: 새로운 html파일을 쓰거나, 단순히 output만 return으로 넘기는 방법이 있다