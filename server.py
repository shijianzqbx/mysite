#coding=utf-8
import web
import db
import json
# 这是一个元组
urls = (
    '/login','Login',
    '/','Index',
    '/new','New',
    '/view/(\d+)','View',
    '/edit/(\d+)', 'Edit',
    '/delete/(\d+)', 'Delete',
    '/logout','Logout'
)

app = web.application(urls, globals())
render = web.template.render('templates')
loginform = web.form.Form(
                      web.form.Textbox('username'),
                      web.form.Password('password'),
                      web.form.Button('login')
                      )

def notfound():
    return web.notfound(u"页面不存在")

app.notfound = notfound

class Login:
    def GET(self):
        return render.login()

    def POST(self):
        i = web.input()
        user = db.get_user(i.username,i.password)
        if user:
            web.setcookie('username',i.username)
            web.redirect('/')
        else:
            return render.login(loginform)

class Index():
    def GET(self):
        username = web.cookies().get('username')
        if username:
            articles = db.get_articles()
            return render.index(articles)
        else:
            web.redirect('/login')


class New():
    articleform = web.form.Form(
                         web.form.Textbox('title',
                         web.form.notnull,
                         size=30,
                         description=u'文章标题:'),
                         web.form.Textarea('content',
                         web.form.notnull,
                         rows=30,
                         cols=80,
                         description=u'文章内容:'),
                         web.form.Button(u'提交'),
                         )
    def GET(self):
        return render.new()

    def POST(self):
        i = web.input()
        db.add_article(i.title, i.content)
        return json.dumps({'state':1})


class View():
    def GET(self,id):
        article = db.get_article(id)
        return render.view(article)

class Edit():
    def GET(self,id):
        article = db.get_article(id)
        return render.edit(article)

    def POST(self,id):
        i = web.input()
        db.update_article(id,i.title,i.content)
        return json.dumps({'state':1})
        #web.redirect('/view/{id}'.format(id=id))

class Delete():
    def GET(self,id):
        db.delete_article(id)
        web.seeother('/')

class Logout():
    def GET(self):
        web.setcookie('username', '', expires=-1)
        web.seeother('/login')

if  __name__ == '__main__':
    app = web.application(urls, globals(),True)
    app.run()
