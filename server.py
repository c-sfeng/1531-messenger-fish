"""Flask server"""
import sys
from flask_cors import CORS
from flask import Flask, send_from_directory
from server_files.exceptions.my_exceptions import default_handler
from server_files.data import database
from server_files.blueprints.admin import ADMIN_API
from server_files.blueprints.auth import AUTH_API
from server_files.blueprints.channel import CHANNEL_API
from server_files.blueprints.channels import CHANNELS_API
from server_files.blueprints.echo import ECHO_API
from server_files.blueprints.message import MESSAGE_API
from server_files.blueprints.search import SEARCH_API
from server_files.blueprints.standup import STANDUP_API
from server_files.blueprints.user import USER_API
from server_files.blueprints.users import USERS_API

APP = Flask(__name__,
            static_url_path='/static/',
            static_folder='server_files/static/')
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='coveremail001@gmail.com',
    MAIL_PASSWORD='abc4fj7klm'
)
APP.register_error_handler(Exception, default_handler)
CORS(APP)

# Register blueprints
APP.register_blueprint(ADMIN_API, url_prefix='/admin')
APP.register_blueprint(AUTH_API, url_prefix='/auth')
APP.register_blueprint(CHANNEL_API, url_prefix='/channel')
APP.register_blueprint(CHANNELS_API, url_prefix='/channels')
APP.register_blueprint(ECHO_API, url_prefix='/echo')
APP.register_blueprint(MESSAGE_API, url_prefix='/message')
APP.register_blueprint(SEARCH_API, url_prefix='/search')
APP.register_blueprint(STANDUP_API, url_prefix='/standup')
APP.register_blueprint(USER_API, url_prefix='/user')
APP.register_blueprint(USERS_API, url_prefix='/users')

@APP.route('/static/<path:path>')
def send_js(path):
    """Serves static image, with given path"""
    print(path)
    return send_from_directory(APP.static_folder, path)

if __name__ == '__main__':
    database.wipe_tokens()
    database.move_all_standup_to_unused()
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
