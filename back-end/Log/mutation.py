import graphene
from Log.models import Logs
    
class DeleteLogs(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    ok = graphene.Boolean()
    def mutate(self, info , id):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception("You should login")

        if current_user.role !="admin":
            raise Exception("You do not have access")
        
        try:
            log = Logs.objects.get(pk=id)
            if log.is_protected:
                raise Exception("This log can not delete")
            send_delete(current_user,log)
            log.delete()
            return DeleteLogs(ok=True)
        
        except Logs.DoesNotExist:
            raise Exception("log does not exist")


class DeleteAllLogs(graphene.Mutation):
    class Arguments:
        pass

    delete_all = graphene.Boolean()
    def mutate(self, info ):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception("You should login")

        if current_user.role !="admin":
            raise Exception("You do not have access")
        
        Logs.objects.filter(is_protected=False).delete()
        send_delete_all(current_user)
        return DeleteAllLogs(delete_all=True)
    


class LogMutation(graphene.ObjectType):
    delete_log = DeleteLogs.Field()
    delete_all_log = DeleteAllLogs.Field()

def send_delete(user,log):
    Logs.objects.create(
        actor_user=user,
        action_title="Delete log",
        action_type="DELETE_LOG",
        description=f"delete log {log.id}: {log}",
        is_protected=True,
    )

def send_delete_all(user):
    Logs.objects.create(
        actor_user=user, 
        action_title="Delete all logs",
        action_type="DELETE_ALL_LOGS",
        description=f"delete all logs",
        is_protected=True,
    )