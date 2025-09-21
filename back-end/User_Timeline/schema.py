import graphene
from Users.query import UserQuery
from Users.mutation import UserMutation,AuthMutation
from Log.mutation import LogMutation
from Log.query import LogsQuery
from Log_Auth.query import AuthLogsQuery
from .Alllogs import CombinedLogsQuery



class Mutation(UserMutation, LogMutation, AuthMutation,  graphene.ObjectType):
    pass

class Query(UserQuery, LogsQuery, AuthLogsQuery, CombinedLogsQuery ,graphene.ObjectType):
    pass
    
    
schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=True)
