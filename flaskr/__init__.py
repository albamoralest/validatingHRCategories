import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flaskr import auth, evaluation
from datetime import datetime

def create_app(test_config=None):
    # create and configure the app, instance of Flask
    #_name_is the name of the current Python module
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    
    app.register_blueprint(auth.bp)

    app.register_blueprint(evaluation.bp)
    app.add_url_rule('/', endpoint='index')

    Bootstrap(app)
    #2019-08-11T12:02:05.000Z
    @app.template_filter('datetimeformat')
    #def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    def datetimeformat(value, format='%Y-%m-%d'):
        if value is "" or value is None:
            return value
        else:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').strftime(format)
    
    return app