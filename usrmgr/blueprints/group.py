from flask import Blueprint, jsonify, request

from usrmgr.models import Group, User

groups = Blueprint('groups', __name__, url_prefix='/api/v0')


def fetch_group(groupid):
    return Group.query.filter_by(groupid=groupid).first()


def fetch_user(userid):
    return User.query.filter_by(userid=userid).first()


@groups.route('/groups/<string:groupid>', methods=('POST',))
def add_group(groupid):
    group = fetch_group(groupid)
    if group:
        return jsonify(
            {'error': 'Group {} already exists.'.format(groupid,)}), 409

    group = Group(groupid)
    group.save()

    return jsonify({'results': group.as_dict()}), 201


@groups.route('/groups/<string:groupid>', methods=('DELETE',))
def delete_group(groupid):
    group = fetch_group(groupid)
    if not group:
        return jsonify(
            {'error': 'Group {} does not exist.'.format(groupid,)}), 404

    group.delete()
    return jsonify({'result': 'success'}), 200


@groups.route('/groups/<string:groupid>', methods=('PUT',))
def modify_group(groupid):
    group = fetch_group(groupid)
    if not group:
        return jsonify(
            {'error': 'Group {} does not exist.'.format(groupid,)}), 404

    new_groupid = request.data.get('groupid')
    if new_groupid:
        group.groupid = new_groupid

    group.save()
    return jsonify({'results': group.as_dict()}), 200


@groups.route('/groups', methods=('GET',))
def list_groups():
    groups = Group.get_all()
    return jsonify({'results': [group.as_dict() for group in groups]}), 200


@groups.route('/groups/<string:groupid>', methods=('GET',))
def list_group(groupid):
    group = fetch_group(groupid)
    if not group:
        return jsonify(
            {'error': 'Group {} does not exist.'.format(groupid,)}), 404

    return jsonify({'results': group.as_dict()}), 200
