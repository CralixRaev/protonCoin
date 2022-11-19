from flask_restful import fields

default_list_fields = {
    'recordsTotal': fields.Integer(),
    'recordsFiltered': fields.Integer(),
    # 'data': fields.List(fields.Nested()),
}


basis_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
}

criteria_fields = {
    'id': fields.Integer(),
    'basis': fields.Nested(basis_fields),
    'name': fields.String(),
    'cost': fields.Integer(),
    'is_user_achievable': fields.Boolean(),
}

achievement_fields = {
    'id': fields.Integer(),
    # 'user': fields.Nested(user_fields),
    'criteria': fields.Nested(criteria_fields),
    'achievement_file': fields.String(),
    'comment': fields.String(),
}

