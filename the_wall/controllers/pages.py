from flask import redirect, render_template, session
from the_wall.models.post import Post

post = Post()

class Pages:
    def index(self):
        return render_template('index.html')

    def wall(self):
        msgs = post.getAllPosts() 
        return render_template('wall.html', messages = msgs)

