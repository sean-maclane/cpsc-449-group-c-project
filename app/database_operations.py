
def initialize():
    pass

def init_db():
    db = get_data()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def close_db(e=None):
    """
    close_db checks if a connection was created by checking if g.db was set.
    If the connection exists, it is closed. Further down you will tell your
    application about the close_db function in the application factory so that
    it is called after each request.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def get_data():
    """
    g is a special object that is unique for each request. It is used to store
    data that might be accessed by multiple functions during the request. The
    connection is stored and reused instead of creating a new connection if
    get_data is called a second time in the same request.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = make_dicts
    return g.db


def query_db():
    pass

def db_transaction():
    pass





# initiate db with
# $FLASK_APP=post_api.py
# $flask init
@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('data.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# close db connection
@app.teardown_appcontext
def close_db(e=None):
    if e is not None:
        print(f'Closing db: {e}')
    db = g.pop('db', None)
    if db is not None:
        db.close()
