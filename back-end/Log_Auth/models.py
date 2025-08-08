from django.db import models
from Users.models import Users

from django.db import models
from Users.models import Users

class Auth_Logs(models.Model):
    Actions_Types = [
        ("Login" , "Log_in"),
        ("Logout" , "Log_out"),
    ]
    Action_Status= [
        ("SUCCESS","Success"),
        ("FAILED", "Failed"),
    ]
    user = models.ForeignKey(Users, on_delete=models.CASCADE , related_name='auth_logs', null=True, blank=True)
    action_type = models.CharField(choices=Actions_Types , max_length=20)
    action_time = models.DateTimeField(auto_now_add=True)
    action_status = models.CharField(choices=Action_Status , default="SUCCESS" , max_length=10)
    description = models.TextField(blank=True , null=True)
    action_title = models.CharField(max_length=255 , blank=True , null=True)
    is_protected = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"{self.action_type} by {self.actor_user} on {self.action_time}"

        