'''
This file was adapted from the flask documentation for our project
'''

import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "project.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from project import db

    db.init_app(app)

    # apply the blueprints to the app
    from project import accounts, message, posts

    app.register_blueprint(accounts.bp)
    app.register_blueprint(message.bp)
    app.register_blueprint(posts.bp)

    # make url_for('index') == url_for('posts.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the posts blueprint a url_prefix, but for
    # the tutorial the posts will be the main index
    #app.add_url_rule("/", endpoint="index")

    return app
