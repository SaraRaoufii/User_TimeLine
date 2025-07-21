import graphene
from Users.query import UserQuery
from Users.mutation import UserMutation
from Log.mutation import LogMutation
from Log.query import LogsQuery
from graphene_django_extras import all_directives

class Mutation(UserMutation, LogMutation, graphene.ObjectType):
    pass

class Query(UserQuery, LogsQuery ,graphene.ObjectType):
    pass
    
    
schema = graphene.Schema(query=Query , mutation=Mutation , directives=all_directives)