from flask_restful import abort, reqparse

list_parser = reqparse.RequestParser()
list_parser.add_argument('draw', type=int, help='Used for DataTables, ignore it')
list_parser.add_argument('start', type=int, default=0)
list_parser.add_argument('length', type=int, default=10)


def abort_if_not_found(obj):
    if not obj:
        abort(404, message=f"Entity with this id does not exist.")
