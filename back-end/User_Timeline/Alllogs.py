import graphene
from django.db.models import Value, CharField
from Log_Auth.models import Auth_Logs
from Log.models import Logs
from Users.type import UserType

class CombinedLogType(graphene.ObjectType):
    log_id = graphene.ID()
    action_type = graphene.String()
    action_time = graphene.DateTime()
    action_title = graphene.String()
    description = graphene.String()
    user = graphene.Field(UserType)
    actor_user = graphene.Field(UserType)
    target_user = graphene.Field(UserType)
    category = graphene.String()

class CombinedLogsQuery(graphene.ObjectType):
    all_logs_combined = graphene.List(
        CombinedLogType,
        page=graphene.Int(default_value=1),
        limit=graphene.Int(default_value=10),
    )

    def resolve_all_logs_combined(root, info, page=1, limit=10):
        auth_qs = Auth_Logs.objects.annotate(
            category_value=Value('Authentication', output_field=CharField())
        )

        logs_qs = Logs.objects.annotate(
            category_value=Value('Management', output_field=CharField())
        )

        combined = list(auth_qs) + list(logs_qs)
        combined.sort(key=lambda x: x.action_time, reverse=True)

        offset = (page - 1) * limit
        paginated = combined[offset:offset + limit]

        result = []
        for item in paginated:
            result.append(
                CombinedLogType(
                    log_id=item.id,
                    action_type=getattr(item, 'action_type', None),
                    action_time=getattr(item, 'action_time', None),
                    action_title=getattr(item, 'action_title', None),
                    description=getattr(item, 'description', None),
                    user=getattr(item, 'user', None),
                    actor_user=getattr(item, 'actor_user', None),
                    target_user=getattr(item, 'target_user', None),
                    category=getattr(item, 'category_value', None)
                )
            )
        return result
