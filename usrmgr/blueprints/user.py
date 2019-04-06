from flask import Blueprint, request, jsonify

from usrmgr.models import User


users = Blueprint('users', __name__, url_prefix='/api/v0')


def fetch_user(userid):
    return User.query.filter_by(userid=userid).first()


@users.route('/users/<string:userid>', methods=('POST',))
def add_user(userid):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    user = fetch_user(userid)
    if user:
        return jsonify(
            {'error': 'User {} already exists.'.format(userid,)}), 409

    user = User(userid)
    user.first_name = first_name
    user.last_name = last_name

    user.save()

    return jsonify({'results': user.as_dict()}), 201


@users.route('/users', methods=('GET',))
def list_users():
    users = User.get_all()
    return jsonify(
        {'results': [user.as_dict() for user in users]}), 200


@users.route('/users/<string:userid>', methods=('GET',))
def list_user(userid):
    user = fetch_user(userid)
    if not user:
        return jsonify(
            {'error': 'User {} does not exist'.format(userid,)}), 404

    return jsonify({'results': user.as_dict()}), 200


@users.route('/users/<string:userid>', methods=('PUT',))
def modify_user(userid):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    new_userid = request.data.get('userid')

    user = fetch_user(userid)
    if not user:
        return jsonify(
            {'error': 'User {} does not exist'.format(userid,)}), 404

    if new_userid:
        user.userid = new_userid
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()

    return jsonify({'results': user.as_dict()}), 200


@users.route('/users/<string:userid>', methods=('DELETE',))
def delete_user(userid):
    user = fetch_user(userid)
    if not user:
        return jsonify(
            {'error': 'User {} does not exist'.format(userid,)}), 404

    user.delete()
    return jsonify({}), 200
