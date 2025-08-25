import graphene
from .type import AuthLogsType
from .models import Auth_Logs

class AuthLogsQuery(graphene.ObjectType):
    auth_logs = graphene.List(
        AuthLogsType,
        page=graphene.Int(default_value=1),
        limit=graphene.Int(default_value=50)
    )

    def resolve_auth_logs(root, info, page=1, limit=50):
        offset = (page - 1) * limit
        queryset = Auth_Logs.objects.all().order_by('-action_time')
        return queryset[offset:offset + limit]
