import web

urls = ('pythonanywhere.com/HenryChinask1', 'hello')

app = web.application(urls, globals())

class Hello:
    def GET(self, name):
        if not name:
            name = 'World'
        return 'Hello' + name + '!'

if __name__ == '__main__':
    app.run()