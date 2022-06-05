from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields

app = Flask(__name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/documentation', authorizations=authorizations)

app.register_blueprint(blueprint)

collection_language = api.model(
    'Language', {'language': fields.String('The Language')})

languages = []


@api.route('/language')
class Language(Resource):

    @api.marshal_with(collection_language, envelope='results')
    @api.doc(security='apikey')
    def get(self):
        return languages

    @api.expect(collection_language)
    def post(self):
        if any(row['language'] == api.payload['language'] for row in languages):
            return {'result': 'The resource already exists'}, 409

        payload = api.payload
        payload['id'] = len(languages) + 1
        languages.append(payload)
        return {'result': 'language added'}, 201


if __name__ == "__main__":
    app.run(debug=True)
