from .type import AuthLogsType
import graphene
from .models import Auth_Logs
from graphene_django.filter import DjangoFilterConnectionField


class AuthLogsQuery(graphene.ObjectType):
    all_auth_logs = graphene.List(AuthLogsType)
    auth_logs_by_id = graphene.Field(AuthLogsType , id=graphene.ID(required=True))
    

    def resolve_all_auth_logs(root , info):
        return Auth_Logs.objects.all()
    
    def resolve_auth_logs_by_id(self, info , id):
        try:
            return Auth_Logs.objects.get(id=id)
        except Auth_Logs.DoesNotExist:
            return None

