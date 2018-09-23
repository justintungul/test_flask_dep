from flask import redirect, render_template, session, flash
from the_wall.models.post import Post

post = Post()

class Posts:
    def createMessage(self):
        newId = post.insertMessage()
        if newId:
            flash(f'You posted a new message!', 'success')
            return redirect('/wall')
        else:
            flash(f'Unable to post a new message!', 'error')
            return redirect('/wall')

    def createComment(self):
        newId = post.insertComment()
        if newId:
            flash(f'You posted a new message!', 'success')
            return redirect('/wall')
        else:
            flash(f'Unable to post a new message!', 'error')
            return redirect('/wall')
            
    def deleteMessage(self, id, created_at):
        res = post.deleteMessageById(id, created_at)
        if res:
            flash(f'Message has a been deleted!', 'success')
            return redirect('/wall')
        else:
            flash(f'Unable to delete message with comments!', 'error')
            return redirect('/wall')
            
    def deleteComment(self, id, created_at):
        res = post.deleteCommentById(id, created_at)
        if res:
            flash(f'Comment has a been deleted!', 'success')
            return redirect('/wall')
        else:
            flash(f'Unable to delete comment!', 'error')
            return redirect('/wall')

