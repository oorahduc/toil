from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sqlite3
import re
from .style import *

DATABASE = str(Path.home()) + "/.toil/toil.db"


def init_db():
    return sqlite3.connect(DATABASE)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def load_factory():
    con = init_db()
    con.row_factory = dict_factory
    cur = con.cursor().execute('SELECT * FROM tasks ORDER by created')
    return cur.fetchall()


def construct_task(task_params):
    tags = re.findall(r'@\w+', " ".join(task_params))
    task_name = " ".join(filter(lambda x: x[0] != '@', task_params))
    return tags, task_name


def get_id(args):
    return re.findall(r'@(\d+)', args[0])


def save_task(task, tags):
    taskname = task
    con = init_db()
    cur = con.cursor()
    try:
        try:
            cur.execute("insert into tasks (name) values (?)", (taskname,))
            task_id = cur.lastrowid
        except Exception as e:
            raise e
        try:
            for tag in tags:
                cur.execute("insert into task_attributes (taskid, tag) values (?, ?)", (task_id, tag))
        except Exception as e:
            raise e
        con.commit()
        con.close()
    except Exception as e:
        raise e


def check_task(task_id):
    con = init_db()
    cur = con.cursor()
    try:
        task = cur.execute("select * from tasks where id=(?)", (task_id[0],)).fetchone()
        cur.execute("update tasks set state='done' where id=(?)", (task_id[0],))
        print("Checked " + green("\U00002714 ") + task[1])
        con.commit()
        con.close()
    except Exception as e:
        raise e


def uncheck_task(task_id):
    con = init_db()
    cur = con.cursor()
    try:
        task = cur.execute("select * from tasks where id=(?)", (task_id[0],)).fetchone()
        cur.execute("update tasks set state='pending' where id=(?)", (task_id[0],))
        print("Unchecked " + white("\U0000274F ") + task[1])
        con.commit()
        con.close()
    except Exception as e:
        raise e


def get_tags():
    con = init_db()
    cur = con.cursor()
    try:
        tags = cur.execute("select distinct tag from task_attributes").fetchall()
        con.close()
        return list(tags)
    except Exception as e:
        raise e


def get_tasks_by_tag(tag):
    con = init_db()
    cur = con.cursor()
    try:
        tasks = cur.execute("select * from tasks where id IN (select taskid from task_attributes where tag=(?))",
                            (tag[0],)).fetchall()
        con.close()
        return list(tasks)
    except Exception as e:
        raise e


def display_tasks(tasks):
    for task in tasks:
        if task[4] == "done":
            task_state = supergreen("\U00002714")
        else:
            task_state = "\U0000274F"
        if task[3] == 1:
            starred = gold("\U0000272E ")
        else:
            starred = ""

        now = datetime.utcnow()
        created = datetime.strptime(task[5], '%Y-%m-%d %H:%M:%S')
        age = relativedelta(now, created)
        print(f"    {'{0}.'.format(task[0]):<{3}} " + task_state + f" {starred:<{2}}{task[1]:<{40}}" + white(
            str(age.days) + "d"))
    print("")


def count_tasks():
    con = init_db()
    cur = con.cursor()
    try:
        all = cur.execute("select count(*) from tasks").fetchone()
        pending = cur.execute("select count(*) from tasks where state='pending'").fetchone()
        starred = cur.execute("select count(*) from tasks where starred=1").fetchone()
        con.close()
        return [int(all[0]), int(pending[0]), int(starred[0])]
    except Exception as e:
        raise e


def star_task(task_id):
    con = init_db()
    cur = con.cursor()
    try:
        task = cur.execute("select * from tasks where id=(?)", (task_id[0],)).fetchone()
        cur.execute("update tasks set starred=1 where id=(?)", (task_id[0],))
        print("Starred " + gold("\U0000272E ") + task[1])
        con.commit()
        con.close()
    except Exception as e:
        raise e


def unstar_task(task_id):
    con = init_db()
    cur = con.cursor()
    try:
        task = cur.execute("select * from tasks where id=(?)", (task_id[0],)).fetchone()
        cur.execute("update tasks set starred=0 where id=(?)", (task_id[0],))
        print("Starred " + white("\U0000274F ") + task[1])
        con.commit()
        con.close()
    except Exception as e:
        raise e


def delete_task(task_id):
    con = init_db()
    cur = con.cursor()
    try:
        task = cur.execute("select * from tasks where id=(?)", (task_id[0],)).fetchone()
        cur.execute("delete from tasks where id=(?)", (task_id[0],))
        print("Deleted " + task[1])
        con.commit()
        con.close()
    except Exception as e:
        raise e
