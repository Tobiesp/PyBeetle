import argparse
import os
from flask import Flask
from webapp import DB, errPrint, SETTINGS
from flask_login import LoginManager
from webapp.models.user import User


def build_database(app: Flask):
    if SETTINGS.database.type == 'sqlite' and not os.access(SETTINGS.database.file_path, os.R_OK):
        with app.app_context():
            DB.create_all()


def create_database_connection_uri():
    if SETTINGS.database.type == 'sqlite':
        return f"sqlite:///{SETTINGS.database.file_path}"  #'sqlite:///db.sqlite'
    # TODO: Add the other databse connection string


def create_app():
    app = Flask(__name__)

    global SETTINGS

    app.config['APP'] = SETTINGS.server.app_name
    app.config['SECRET_KEY'] = SETTINGS.server.session_secret_key
    app.config['SESSION_COOKIE_NAME'] = 'pybeetle_session'
    app.config['PERMANENT_SESSION_LIFETIME'] = SETTINGS.server.session_timeout
    app.config['SQLALCHEMY_DATABASE_URI'] = create_database_connection_uri()

    return app


def setup_db_app(app: Flask):
    DB.init_app(app)
    build_database(app)


def setup_login_app(app: Flask):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

def setup_request_handlers(app: Flask):
    # blueprint for auth routes in our app
    from webapp.request_handlers.auth_api import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from webapp.request_handlers.main_api import main as main_blueprint
    app.register_blueprint(main_blueprint)


def process_args():
    parser = argparse.ArgumentParser(
                    prog='pyBeetle',
                    description='Server to store and track student event scores.')
    parser.add_argument('-s', '--settings', type=str, help='Settings consumed by the server. Must be in yaml form.')
    parser.add_argument('-l', '--logging', type=str, help='File used to configure logging for the server.')
    args = parser.parse_args()
    if args.settings == '':
        errPrint("Settings.yaml file must be supplied to the server")
        parser.print_help()
        exit(1)
    SETTINGS.load_settings(args.settings)

    # TODO: Process logging configs


def main():
    """Main function that starts the app"""
    process_args()
    app = create_app()
    setup_db_app(app)
    setup_login_app(app)
    setup_request_handlers(app)
    app.run()


if __name__ == '__main__':
    main()
