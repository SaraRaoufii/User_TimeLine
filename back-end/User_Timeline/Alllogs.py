import graphene
from django.db.models import Value, CharField
from Log_Auth.models import Auth_Logs
from Log.models import Logs
from Users.type import UserType
from django.db.models import Value, CharField, Q
import json
from graphene.types.generic import GenericScalar

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
    old_values = graphene.JSONString()
    new_values = graphene.JSONString()
    is_protected = graphene.Boolean()
    

class CombinedLogsQuery(graphene.ObjectType):
    all_logs_combined = graphene.List(
        CombinedLogType,
        page=graphene.Int(default_value=1),
        limit=graphene.Int(default_value=10),
        username=graphene.List(graphene.String),
        start_time=graphene.DateTime(),
        end_time=graphene.DateTime(),
        action_title=graphene.List(graphene.String),
        category=graphene.String(),
        old_values=GenericScalar(),
        new_values=GenericScalar(),
        search=graphene.String(),
        order_by=graphene.String(default_value="-action_time")
    )

    def resolve_all_logs_combined(root, info, page=1,search=None, limit=10, username=None, start_time=None, end_time=None, action_title=None, old_values=None, new_values=None, category=None, order_by="-action_time" ):
        auth_qs = Auth_Logs.objects.annotate(
            category_value=Value('Authentication', output_field=CharField())
        )
        logs_qs = Logs.objects.annotate(
            category_value=Value('Management', output_field=CharField())
        )
        
        if search:
            auth_qs =auth_qs.filter(
                Q(user__username__icontains=search)|
                Q(action_title__icontains=search)|
                Q(category_value__icontains=search)
            )
            logs_qs =logs_qs.filter(
                Q(actor_user__username__icontains=search)|
                Q(action_title__icontains=search)|
                Q(category_value__icontains=search)|
                Q(description__icontains=search)|
                Q(target_user__username__icontains =search)
            )


        if username and isinstance(username, list) and len(username) > 0:
            auth_qs = auth_qs.filter(user__username__in=username)
            logs_qs = logs_qs.filter(Q(actor_user__username__in=username) | Q(target_user__username__in=username))

        if start_time and end_time:
            auth_qs = auth_qs.filter(action_time__range=[start_time, end_time])
            logs_qs = logs_qs.filter(action_time__range=[start_time, end_time])
        elif start_time:
            auth_qs = auth_qs.filter(action_time__gte=start_time)
            logs_qs = logs_qs.filter(action_time__gte=start_time)
        elif end_time:
            auth_qs = auth_qs.filter(action_time__lte=end_time)
            logs_qs = logs_qs.filter(action_time__lte=end_time)

        if action_title and isinstance(action_title, list) and len(action_title) > 0:
            q = Q()
            for val in action_title:
                q |= Q(action_title__iexact=val) | Q(action_type__iexact=val)
            logs_qs = logs_qs.filter(q)
            auth_qs = auth_qs.filter(q)  
            
        if old_values or new_values:
            auth_qs = Auth_Logs.objects.none()

        if old_values:
            if isinstance(old_values, str):
                try:
                    old_values_dict = json.loads(old_values)
                except json.JSONDecodeError:
                    old_values_dict = {}
            elif isinstance(old_values, dict):
                old_values_dict = old_values
            else:
                old_values_dict = {}

            filtered_ids = []
            for log in logs_qs:
                try:
                    desc = json.loads(log.description)
                except json.JSONDecodeError:
                    continue
                fields_changed = desc.get("fields_changed", {})
                match = True
                for key, val in old_values_dict.items():
                    if key not in fields_changed or str(fields_changed[key].get("old_val")) != str(val):
                        match = False
                        break
                if match:
                    filtered_ids.append(log.id)
            logs_qs = logs_qs.filter(id__in=filtered_ids)

        if new_values:
            if isinstance(new_values, str):
                try:
                    new_values_dict = json.loads(new_values)
                except json.JSONDecodeError:
                    new_values_dict = {}
            elif isinstance(new_values, dict):
                new_values_dict = new_values
            else:
                new_values_dict = {}

            filtered_ids = []
            for log in logs_qs:
                try:
                    desc = json.loads(log.description)
                except json.JSONDecodeError:
                    continue
                fields_changed = desc.get("fields_changed", {})
                match = True
                for key, val in new_values_dict.items():
                    if key not in fields_changed or str(fields_changed[key].get("new_val")) != str(val):
                        match = False
                        break
                if match:
                    filtered_ids.append(log.id)
            logs_qs = logs_qs.filter(id__in=filtered_ids)
        
        
        if category:
            if category.lower() in ["authentication logs", "authentication"]:
                logs_qs = Logs.objects.none()
            elif category.lower() in ["management logs", "management"]:
                auth_qs = Auth_Logs.objects.none()
  
        combined = list(auth_qs) + list(logs_qs)
        reverse = True if order_by.startswith('-') else False
        sort_field = order_by.lstrip('-')
        combined.sort(key=lambda x: getattr(x, sort_field, None), reverse=reverse)

        
        offset = (page - 1) * limit
        paginated = combined[offset:offset + limit]

        result = []
        for item in paginated:
            result.append(
                CombinedLogType(
                    log_id=getattr(item, 'id', None),
                    action_type=getattr(item, 'action_type', None),
                    action_time=getattr(item, 'action_time', None),
                    action_title=getattr(item, 'action_title', None),
                    description=getattr(item, 'description', None),
                    user=getattr(item, 'user', None),
                    actor_user=getattr(item, 'actor_user', None),
                    target_user=getattr(item, 'target_user', None),
                    category=getattr(item, 'category_value', None),
                    old_values=getattr(item, 'old_values', None),
                    new_values=getattr(item, 'new_values', None)
                )
            )
        return result
