import time
from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView

from scema import schema
from init_database import init_db, init_data

app = Flask(__name__)
CORS(app)

init_db()
time.sleep(1)
init_data()

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == "__main__":
    app.run(debug=True)
