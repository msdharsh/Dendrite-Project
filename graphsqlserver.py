from graphene import ObjectType, String, Schema, List, ID, Boolean
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask import Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/todo_db'
db = SQLAlchemy(app)

class TaskModel(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

class Task(SQLAlchemyObjectType):
    class Meta:
        model = TaskModel
        interfaces = (graphene.relay.Node, )

class Query(ObjectType):
    task = graphene.relay.Node.Field(Task)
    all_tasks = SQLAlchemyConnectionField(Task.connection)

schema = Schema(query=Query)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))