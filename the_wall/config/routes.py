from the_wall import app
from the_wall.controllers.pages import Pages
from the_wall.controllers.users import Users
from the_wall.controllers.posts import Posts

pages = Pages()
users = Users()
posts = Posts()

@app.route('/')
def index():
    return pages.index()

@app.route('/wall')
def wall():
    return pages.wall()

@app.route('/login', methods=['POST'])
def login():
    return users.login()

@app.route('/register', methods=['POST'])
def register():
    return users.register()

@app.route('/logout')
def logout():
    return users.logout()

@app.route('/new/message', methods=['POST'])
def new_message():
    return posts.createMessage()

@app.route('/new/comment', methods=['POST'])
def new_comment():
    return posts.createComment()

@app.route('/delete/message/<id>/<created_at>')
def delete_message(id, created_at):
    return posts.deleteMessage(id, created_at)

@app.route('/delete/comment/<id>/<created_at>')
def delete_comment(id, created_at):
    return posts.deleteComment(id, created_at)