from app import db


class User(db.Model):
    """This class represents the users table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    userid = db.Column(db.String(32))
    groups = db.Column(db.String(255))
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


class Group(db.Model):
    """This class represents the groups table"""
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
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


class UserGroup(db.Model):
    """This class represents the usergroups table"""
    __tablename__ = 'usergroups'

    id = db.Column(db.Integer, primary_key=True)
    groupid = db.Column(db.Integer)
    userid = db.Column(db.Integer)

    def __init__(self, groupid, userid):
        self.groupid = groupid
        self.userid = userid

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return UserGroup.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<UserGroup: {}:{}>'.format(self.groupid, self.userid)
