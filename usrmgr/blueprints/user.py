from flask import Blueprint, request, jsonify

from usrmgr.models import User


users = Blueprint('users', __name__)


@users.route('/users', methods=('POST',))
def add_user():
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    userid = request.data.get('userid')

    user = User.query.filter_by(userid=userid).first()
    if user:
        return jsonify(
            {'error': 'User {} already exists.'.format(userid,)}), 409

    user = User(userid)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return jsonify({'results': user.as_dict()}), 201
