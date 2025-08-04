from django.db import models
from Users.models import Users

class Logs(models.Model):
    Actions_Types = [
        ("CREATE", "Create"),
        ("READ", "Read"),
        ("UPDATE_PROFILE" , "Update_profile"),
        ("DELETE" , "Delete"),
        ("DELETE_ALL_LOGS" , "Delete_All_Logs"),
        ("DELETE_LOGS" , "Delete_log"),
    ]
    Action_Status= [
        ("SUCCESS","Success"),
        ("FAILED", "Failed"),
    ]
    actor_user = models.ForeignKey(Users, on_delete=models.CASCADE , related_name='action_performed', null=True, blank=True)
    target_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="action_recieve", null=True , blank=True)
    action_type = models.CharField(choices=Actions_Types , max_length=20)
    action_time = models.DateTimeField(auto_now_add=True)
    action_status = models.CharField(choices=Action_Status , default="SUCCESS" , max_length=10)
    description = models.TextField(blank=True , null=True)
    is_protected = models.BooleanField(default=False)
    



    def __str__(self) -> str:
        return f"{self.action_type} by {self.user} in {self.action_time}"
    