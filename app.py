from app import app

if app.config['ENVIRONMENT'] == 'prod':
	app.run(debug=True,host="0.0.0.0")
elif app.config['ENVIRONMENT'] == 'dev':
	app.run(debug=True)
