from common import mysql


class User(mysql.Model):
    __table__ = 'users'
    __primary_key__ = dict(
        id = '',
    )
    __fields__ = dict(
        email = '',
        passwd = '',
        admin = 0,
        name = '',
        image = '',
        created_at = '',
    )

class Blog(mysql.Model):
    __table__ = 'blogs'
    __primary_key__ = dict(
        id = '',
    )
    __fields__ = dict(
        user_id = '',
        user_name = '',
        summary = '',
        name = '',
        user_image = '',
        content = '',
        created_at = '',
    )

class Comment(mysql.Model):
    __table__ = 'comments'
    __primary_key__ = dict(
        id = '',
    )
    __fields__ = dict(
        blog_id = '',
        user_id = '',
        user_name = '',
        user_image = '',
        content = '',
        created_at = '',
    )