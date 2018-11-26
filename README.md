# Code Gakko App Backend

This is the codebase for the backend portion of the Code Gakko App. It comprises
of a database-facing RESTful API that interfaces with the Code Gakko game and frontend client

## Setting up MongoDB

Ensure Python 2.7 (with virualenv) is installed. (Anaconda2 works)

### Windows
1. Refer to [this](https://stackoverflow.com/questions/2404742/how-to-install-mongodb-on-windows) to install MongoDB for Windows
2. Follow the instructions so that you can run `$ mongod` to start the database
3. In a separate terminal window/tab, run `$ mongo`. This starts a Mongo shell that connects to the database that you just started
4. In the shell, you need to type the following commands:

  * `> use codegakko-sample`
  * `> db.createUser({user: "YOUR_USERNAME", pwd: "YOUR_PWD", roles: [ "readWrite", "dbAdmin" ]})`
  * Check that the user is created with `db.auth("YOUR_USERNAME", "YOUR_PWD")`

5. Now that you've created a database and an account for that database, you need to store the account credentials as an environment variable.
6. To set your environment variables, open a command prompt and type

  * `setx MONGODB_USER "YOUR_USERNAME"`
  * `setx MONGODB_PWD "YOUR_PWD"`

Now the code-gakko-app-backend app can connect to the database.

### Mac OS X / Ubuntu

1. Install [Homebrew](http://brew.sh/)
2. `$ brew install mongodb --with-openssl`
3. At this point you should be able to run the commands `mongod` and `mongo`
4. `$ mongod` This starts the database
5. In a separate terminal window/tab, run `$ mongo`. This starts a Mongo shell that connects to the database that you just started
6. In the shell, you need to type the following commands:

  * `> use codegakko-sample`
  * `> db.createUser({user: "YOUR_USERNAME", pwd: "YOUR_PWD", roles: [ "readWrite", "dbAdmin" ]})`
  * Check that the user is created with `db.auth("YOUR_USERNAME", "YOUR_PWD")`

Now that you've created a database and an account for that database, you need to store the account credentials as an environment variable.

In your `~/.bash_profile` file, add the following lines:

  * `MONGODB_USER=YOUR_USERNAME`
  * `MONGODB_PWD=YOUR_PWD`
  
For Ubuntu:

  * `export MONGODB_USER=YOUR_USERNAME`
  * `export MONGODB_PWD=YOUR_PWD`

Restart your bash shell. Now the code-gakko-app-backend app can connect to the database.

## Installation

1. Clone the repository
2. cd code-gakko-app-backend
3. Make sure your unset your `PYTHONPATH` variable if you have one: `unset PYTHONPATH`
4. Create a virtualenv with the name codegakko: `virtualenv codegakko`
5. Activate virtualenv:  
  * For UNIX systems: `source codegakko/bin/activate`  
  * For Windows: `codegakko\Scripts\activate`
6. Install the packages: `pip install -r requirements.txt`
7. If you are missing any packages in the next step, pip install them manually.

If you add any packages, make sure you add them to `requirements.txt` using
`pip freeze > requirements.txt`

## Running the App

1. Make sure MongoDB is running
2. Activate virtualenv: `source codegakko/bin/actvate`
3. Run the app: `python app.py`


## App structure

* app
  * controllers *interfaces models and views*
  * models *definition of MongoDB schema*
  * views *API routes split by class objet*
  * templates

## Backend Testing

Windows
1. Set a Terminal Environment Variable to point to your Test Mongo DB Instance set GAKKO_BLOCKS_CONFIG=F:\mycode\code-gakko-app-backend\app\config_test.cfg
2. Setup a Mongo DB Test Instance as defined in your config_test.cfg
3. Install pytest via 'pip install pytest'
4. Go to your backend folder and start test scripts via 'pytest -s'
