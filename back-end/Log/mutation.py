import graphene
import json
from Log.models import Logs

class DeleteLogs(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception(json.dumps({"non_field_error": "You should login"}))

        if current_user.role.upper() != "ADMIN":
            raise Exception(json.dumps({"non_field_error": "You do not have access"}))

        try:
            log = Logs.objects.get(pk=id)
        except Logs.DoesNotExist:
            raise Exception(json.dumps({"non_field_error": "Log does not exist"}))

        if log.is_protected:
            raise Exception(json.dumps({"non_field_error": "This log is protected and cannot be deleted"}))


        send_delete(current_user, log)
        log.delete()
        return DeleteLogs(ok=True, message=f"1 log (ID: {id}) deleted successfully")



class DeleteAllLogs(graphene.Mutation):
    delete_all = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception(json.dumps({"non_field_error": "You should login"}))

        if current_user.role.upper() != "ADMIN":
            raise Exception(json.dumps({"non_field_error": "You do not have access"}))

        logs_to_delete = Logs.objects.filter(is_protected=False)
        count = logs_to_delete.count()

        if count == 0:
            if Logs.objects.exists(): 
                return DeleteAllLogs(
                    delete_all=False,
                    message="No logs available for deletion. Only protected logs remain."
                )
            else: 
                return DeleteAllLogs(
                    delete_all=False,
                    message="No logs exist in the system."
                )

        logs_to_delete.delete()
        send_delete_all(current_user , count)
        return DeleteAllLogs(
                delete_all=True,
                message=f"Success: {count} logs deleted successfully"
            )



class LogMutation(graphene.ObjectType):
    delete_log = DeleteLogs.Field()
    delete_all_log = DeleteAllLogs.Field()


def send_delete(user, log):
    Logs.objects.create(
        actor_user=user,
        action_title="Delete log",
        action_type="DELETE_LOG",
        description=json.dumps({
            "message": f"Deleted 1 log (ID: {log.id}) successfully",
            "count": 1,
            "log_id": log.id
        }),
        is_protected=True,
    )


def send_delete_all(user, count):
    Logs.objects.create(
        actor_user=user,
        action_title="Delete all logs",
        action_type="DELETE_ALL_LOGS",
        description=json.dumps({
            "message": f"Deleted {count} non-protected logs",
            "count": count
        }),
        is_protected=True,
    )
