import graphene
from .type import AuthLogsType
from .models import Auth_Logs
from django.db.models import Q
class AuthLogsQuery(graphene.ObjectType):
    auth_logs = graphene.List(
        AuthLogsType,
        page=graphene.Int(),
        limit=graphene.Int(),
        username=graphene.List(graphene.String),
        action_title=graphene.List(graphene.String),
        start_time=graphene.DateTime(),
        end_time=graphene.DateTime(),
        search=graphene.String(),
        order_by=graphene.String(default_value="-action_time")
    )

    def resolve_auth_logs(root, info,search=None, page=1, limit=20, username=None , action_title=None, start_time=None, end_time=None, order_by="-action_time"):
        offset = (page - 1) * limit
        queryset = Auth_Logs.objects.all()
        if search:
           queryset =queryset.filter(
                Q(user__username__icontains=search)|
                Q(action_title__icontains=search)
            )
        if username and isinstance(username, list) and len(username) > 0:
            queryset = queryset.filter(user__username__in=username)
        if action_title and isinstance(action_title, list) and len(action_title) > 0:
            queryset = queryset.filter(action_title__in=action_title)
          
        if start_time and end_time:
            queryset = queryset.filter(action_time__range=[start_time, end_time])
        elif start_time:
            queryset = queryset.filter(action_time__gte=start_time)
        elif end_time:
            queryset = queryset.filter(action_time__lte=end_time)

        queryset = queryset.order_by(order_by)
        return queryset[offset:offset + limit]
