#coding=utf-8
import sqlite3

dbname = 'blog.db'
conn = sqlite3.connect(dbname,check_same_thread = False)


def create_article():
    sql = '''
    create table article(
    id     INTEGER  PRIMARY KEY autoincrement NOT NULL,
    title char(50) NOT NULL,
    content   text NOT NULL,
    createtime   TIMESTAMP default (datetime('now', 'localtime'))
    );
    '''
    conn.execute(sql)

def create_user():
    sql = '''
    create table user(
    id     INTEGER  PRIMARY KEY autoincrement NOT NULL,
    name   char(50) NOT NULL,
    password char(50) NOT NULL
    );
    '''
    conn.execute(sql)

#清空表
def clear_tables(table):
    sql = "delete from {table}".format(table=table)
    conn.execute(sql)
    conn.commit()

def clear():
    clear_tables('user')
    clear_tables('article')

#测试写入博客
def test_article():
    sql = u"insert into article(title,content)values('测试','测试内容')"
    conn.execute(sql)
    conn.commit()

#加一个用户
def add_user(name,password):
    sql = u"insert into user(name,password)values('{name}','{password}')".format(name=name,password=password)
    conn.execute(sql)
    conn.commit()

#创建表
def create_tables():
    create_article()
    create_user()


def get_user(name,password):
    conn.row_factory = sqlite3.Row
    sql = u"select * from user where name = '{name}' and password = '{password}' ".format(name=name,password=password)
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    if len(datas) > 0:
        return datas[0]
    else:
        return None

def add_article(title,content):
    sql = u"insert into article(title,content)values('{title}','{content}')".format(title=title,content=content)
    conn.execute(sql)
    conn.commit()

def get_articles():
    conn.row_factory = sqlite3.Row
    sql = u"select * from article "
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    return datas

def get_article(id):
    conn.row_factory = sqlite3.Row
    sql = u"select * from article where id = {id}".format(id=id)
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    return datas[0]

def update_article(id,title,content):
    sql = u"update article set title='{title}',content='{content}' where id = {id}"
    sql = sql.format(title=title,content=content,id=id)
    conn.execute(sql)
    conn.commit()

def delete_article(id):
    sql = 'delete from article where id = {id}'.format(id = id)
    conn.execute(sql)
    conn.commit()

if __name__ == '__main__':
    print(get_article(15))
