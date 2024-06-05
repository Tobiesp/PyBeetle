import argparse
from flask import Flask
from webapp import DB, errPrint, SETTINGS
from webapp.settings import Settings


def create_app():
    app = Flask(__name__)

    global SETTINGS

    app.config['SECRET_KEY'] = SETTINGS.server.session_secret_key
    if SETTINGS.database.type == 'sqlite':
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{SETTINGS.database.file_path}"  #'sqlite:///db.sqlite'
    # TODO: Add the other databse connection string

    DB.init_app(app)

    # blueprint for auth routes in our app
    from webapp.auth_api import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from webapp.main_api import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


def process_args():
    parser = argparse.ArgumentParser(
                    prog='pyBeetle',
                    description='Server to store and track student event scores.')
    parser.add_argument('settings', '-s', '--settings', type=str, nargs=1, help='Settings consumed by the server. Must be in yaml form.')
    parser.add_argument('logging', '-l', '--logging', type=str, nargs=1, help='File used to configure logging for the server.')
    args = parser.parse_args()
    if args.settings == '':
        errPrint("Settings.yaml file must be supplied to the server")
        parser.print_help()
        exit(1)
    global SETTINGS
    SETTINGS = Settings(args.settings)

    # TODO: Process logging configs


def main():
    """Main function that starts the app"""
    process_args()
    app = create_app()
    app.run()


if __name__ == '__main__':
    main()
