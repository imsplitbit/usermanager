import json

from flask import Blueprint, request, jsonify

from usrmgr.models import User, Group


users = Blueprint('users', __name__, url_prefix='/api/v0')


def fetch_user(userid):
    return User.query.filter_by(userid=userid).first()


def fetch_group(groupid):
    return Group.query.filter_by(groupid=groupid).first()


@users.route('/users/<string:userid>', methods=('POST',))
def add_user(userid):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    groupids = request.data.get('groups')

    if groupids and isinstance(groupids, basestring):
        try:
            groupids = json.loads(groupids)
            if not isinstance(groupids, list):
                return jsonify(
                    {'error': 'groups must be a json marshalled' +
                              'list of groupids, got: {}'.format(
                                  type(groupids))}), 400
        except Exception:
            return jsonify(
                {'error': 'groups must be a json marshalled' +
                          'list of groupids.'}), 400
    else:
        return jsonify(
            {'error': 'Wrong data type for groups, got {}'.format(
                type(groupids))}), 400

    user = fetch_user(userid)
    if user:
        return jsonify(
            {'error': 'User {} already exists.'.format(userid,)}), 409

    group_objs = []
    for groupid in groupids:
        print "groupid {}".format(groupid)
        group = fetch_group(groupid)
        print "Group {}".format(group)
        if group is None:
            print "making group"
            group = Group(groupid)
            print "group made"
            group.save()
            print "group saved"

        print "group appending"
        group_objs.append(group)
        print "group appended"

    user = User(userid)
    user.first_name = first_name
    user.last_name = last_name
    print "setting group memberships"
    user.group_memberships = group_objs
    print "group memberships set"
    user.save()
    print "saved user"
    print "showing json"
    print json.dumps({'results': user.as_dict()})
    print "json shown"
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
