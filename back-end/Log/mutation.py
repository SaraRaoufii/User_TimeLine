import graphene
from Log.models import Logs
    
class DeleteLogs(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    ok = graphene.Boolean()
    def mutate(self, info , id):
        try:
            log = Logs.objects.get(pk=id)
            if log.is_protected:
                raise Exception("This log can not delete")
            user=log.user
            send_delete(user,log)
            log.delete()
            return DeleteLogs(ok=True)
        
        except Logs.DoesNotExist:
            raise Exception("log does not exist")


class DeleteAllLogs(graphene.Mutation):
    class Arguments:
        pass

    delete_all = graphene.Boolean()
    def mutate(self, info ):
        Logs.objects.filter(is_protected=False).delete()
        send_delete_all()
        return DeleteAllLogs(delete_all=True)
    


class LogMutation(graphene.ObjectType):
    delete_log = DeleteLogs.Field()
    delete_all_log = DeleteAllLogs.Field()

def send_delete(user,log):
    Logs.objects.create(
        user=user,
        action_type="DELETE_LOG",
        description=f"delete log {log.id}: {log}",
        is_protected=True,
    )

def send_delete_all():
    Logs.objects.create(
        action_type="DELETE_ALL_LOGS",
        description=f"delete all logs",
        is_protected=True,
    )