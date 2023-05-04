#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter
import ipdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Home(Resource):
    def get(self):
        return {"newsletter": "it's a beautiful 108 out in Austin today"}


class NewsLetters(Resource):
    def get(self):
        newsletters = [newsletter.to_dict()
                       for newsletter in Newsletter.query.all()]

        return newsletters

    def post(self):
        # title, body
        newsletter = Newsletter(
            title=request.form["title"],
            body=request.form["body"]
        )

        db.session.add(newsletter)
        db.session.commit()

        return make_response(
            newsletter.to_dict(),
            201
        )


class NewsletterById(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter(Newsletter.id == id).first()

        if newsletter:
            return newsletter.to_dict()
        else:
            return make_response({"error": "Newsletter doesn't exist"}, 422)


api.add_resource(Home, "/")
api.add_resource(NewsLetters, "/newsletters")
api.add_resource(NewsletterById, "/newsletters/<int:id>")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
