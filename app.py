from flask import Flask, jsonify, request
from flask_restful import Api
import requests
import re
from services.GetHtmlContent import WebContent
from services.ExtractLinks import Extract

app = Flask(__name__)
api = Api(app)

api.add_resource(WebContent, '/api/gethtmlcontent', endpoint='gethtmlcontent')
api.add_resource(Extract, '/api/extractlinks', endpoint='extractlinks')

if __name__ == '__main__':
    app.run(port=5000, debug=True)