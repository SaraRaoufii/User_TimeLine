from .type import LogsType
import graphene
from Log.models import Logs
from graphene_django.filter import DjangoFilterConnectionField
import json
from django.db.models import Q
from graphene.types.generic import GenericScalar



class LogsQuery(graphene.ObjectType):
    logs = graphene.List(
        LogsType,
        page=graphene.Int(),
        limit=graphene.Int(),
        username=graphene.List(graphene.String),
        start_time=graphene.DateTime(),
        end_time=graphene.DateTime(),
        action_title=graphene.List(graphene.String),
        old_values = GenericScalar(),
        new_values = GenericScalar(),
        search=graphene.String(),
        order_by=graphene.String(default_value="-action_time")
    )

    def resolve_logs(root, info ,search=None, page=1, limit=20 , username=None, start_time=None, end_time=None, action_title=None, old_values=None, new_values=None, order_by="-action_time"):
        offset = (page-1)*limit
        
        logs_qs = Logs.objects.all()
        if search:
            logs_qs =logs_qs.filter(
                Q(actor_user__username__icontains=search)|
                Q(action_title__icontains=search)|
                Q(description__icontains=search)|
                Q(target_user__username__icontains =search)
            )
        if username and isinstance(username, list) and len(username) > 0:
            logs_qs = logs_qs.filter(Q(actor_user__username__in=username) | Q(target_user__username__in=username))

        if start_time and end_time:
            logs_qs = logs_qs.filter(action_time__range=[start_time, end_time])
        elif start_time:
            logs_qs = logs_qs.filter(action_time__gte=start_time)
        elif end_time:
            logs_qs = logs_qs.filter(action_time__lte=end_time)

        if action_title and isinstance(action_title, list) and len(action_title) > 0:
            q = Q()
            for val in action_title:
                val_lower = val.lower()
                q |= Q(action_title__iexact=val_lower) | Q(action_type__iexact=val_lower)
            logs_qs = logs_qs.filter(q)
                
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
        
        logs_qs = logs_qs.order_by(order_by)
        logs_page = logs_qs[offset:offset + limit]

        return logs_page
   
