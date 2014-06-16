import web

render = web.template.render('templates/')

urls = (
	'/(.*)', 'index'
)

#db = web.database(dbn='mysql', user='root', pw='root', db='surfstat')# host='localhost', port='8889')

class index:
	def GET(self, name):
		return render.index(name)
		
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
	
