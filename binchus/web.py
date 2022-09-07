from pathlib import Path
from .website import Website

_INDEX_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''
_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''

_USER_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {id}</title>
    </head>
    <body>
        <table>
            {thoughts}
        </table>
    </body>
</html>
'''
_THOUGHT_LINE_HTML = '''
<tr><td>{time_stamp}</td><td>{thought}</td></tr>
'''


website = Website()


def get_users(data_dir):
    data_dir_path = Path(data_dir)
    users = []
    for user_dir in data_dir_path.iterdir():
        users.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    return users


def run_webserver(address, data_dir):
    @website.route('/')
    def index():
        users = get_users(data_dir)
        index_html = _INDEX_HTML.format(users='\n'.join(users))
        return 200, index_html

    @website.route('/users/([0-9]+)')
    def user(user_id):
        user_dir_path = Path(data_dir) / user_id
        thoughts = []
        for thought_file in user_dir_path.iterdir():
            thoughts.append(_THOUGHT_LINE_HTML
                            .format(
                                    time_stamp=thought_file.name[0:10] + " "
                                    + thought_file.name[11:13] + ":"
                                    + thought_file.name[14:16] + ":"
                                    + thought_file.name[17:19],
                                    thought=thought_file.read_text())
                            )
        user_html = _USER_HTML.format(id=user_id, thoughts='\n'.join(thoughts))
        return 200, user_html

    ip, port = address
    website.run((ip, int(port)))
