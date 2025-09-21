from .models import Logs

def search_logs(self , action_type=None, action_status=None, action_time=None):
    queryset = Logs.objects.all()
    if action_type:
        queryset = queryset.filter(action_type=action_type)
    if action_status:
        queryset = queryset.filter(action_status=action_status)
    if action_time:
        queryset = queryset.filter(action_time=action_time)