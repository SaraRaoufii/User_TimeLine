from .type import LogsType
import graphene
from Log.models import Logs
from graphene_django.filter import DjangoFilterConnectionField


class LogsQuery(graphene.ObjectType):
    all_logs = graphene.List(LogsType)
    logs_by_id = graphene.Field(LogsType , id=graphene.ID(required=True))

    def resolve_all_logs(root , info):
        return Logs.objects.all()
    
    def resolve_logs_by_id(self, info , id):
        try:
            return Logs.objects.get(id=id)
        except Logs.DoesNotExist:
            return None

