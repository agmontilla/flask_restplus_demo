from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

collection_language = api.model(
    'Language', {'language': fields.String('The Language')})

languages = []


@api.route('/language')
class Language(Resource):
    def get(self):
        return languages

    @api.expect(collection_language)
    def post(self):
        if api.payload in languages:
            return {'result': 'The resource already exists'}, 409

        languages.append(api.payload)
        return {'result': 'language added'}, 201


if __name__ == "__main__":
    app.run(debug=True)
