import graphene
from Users.query import UserQuery
from Users.mutation import UserMutation,AuthMutation
from Log.mutation import LogMutation
from Log.query import LogsQuery
from Log_Auth.query import AuthLogsQuery




class Mutation(UserMutation, LogMutation, AuthMutation,  graphene.ObjectType):
    pass

class Query(UserQuery, LogsQuery, AuthLogsQuery ,graphene.ObjectType):
    pass
    
    
schema = graphene.Schema(query=Query , mutation=Mutation)