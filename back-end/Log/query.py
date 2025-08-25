from .type import LogsType
import graphene
from Log.models import Logs
from graphene_django.filter import DjangoFilterConnectionField


class LogsQuery(graphene.ObjectType):
    logs = graphene.List(
        LogsType,
        page=graphene.Int(),
        limit=graphene.Int()
    )

    def resolve_logs(root, info , page=1, limit=50):
        offset = (page-1)*limit
        return Logs.objects.all()[offset:offset+limit]
