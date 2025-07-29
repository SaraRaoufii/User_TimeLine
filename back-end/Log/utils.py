from .models import Logs

def search_logs(self , user=None, action_type=None, action_status=None, is_protected=None):
    queryset = Logs.objects.all()
    if user:
        queryset = queryset.filter(user=user)
    if action_type:
        queryset = queryset.filter(action_type=action_type)
    if action_status:
        queryset = queryset.filter(action_status=action_status)
    if is_protected:
        queryset = queryset.filter(is_protected=is_protected)