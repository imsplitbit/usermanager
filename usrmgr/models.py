import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


db = SQLAlchemy()


association_table = db.Table(
    'usergroups', db.metadata,
    db.Column('uid', db.Integer, db.ForeignKey('users.id')),
    db.Column('gid', db.Integer, db.ForeignKey('groups.id'))
)


class User(db.Model):
    """This class represents the users table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    group_memberships = relationship(
        'Group', secondary=association_table, back_populates='member_users')
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    userid = db.Column(db.String(32))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, userid):
        """initialize with userid"""
        self.userid = userid

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<User: {}>'.format(self.userid)

    def as_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'userid': self.userid,
            'groups': [
                group.as_dict()['groupid'] for group in self.group_memberships
                ],
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }

    def json(self):
        return json.dumps(self.as_dict())


class Group(db.Model):
    """This class represents the groups table"""
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    member_users = relationship(
        'User', secondary=association_table,
        back_populates='group_memberships')
    groupid = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, groupid):
        """initialize with groupid"""
        self.groupid = groupid

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Group.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Group: {}>'.format(self.groupid)

    def as_dict(self):
        return {
            'groupid': self.groupid,
            'users': [user.as_dict() for user in self.member_users],
        }

    def json(self):
        return json.dumps(self.as_dict())
