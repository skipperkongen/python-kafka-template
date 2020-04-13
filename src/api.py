from flask import Blueprint
from flask_jwt_extended import jwt_required

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/dinmor/', methods=['GET'])
@jwt_required
def graphql():
    return "dinmor"
    view = GraphQLView.as_view(
        'graphql',
        schema=graphql_schema.schema,
        graphiql=True)
    return view()
