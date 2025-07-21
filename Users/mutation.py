import graphene
from Users.models import Users
from Users.type import UserType
from Log.models import Logs


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        phone = graphene.String()
        email = graphene.String()
        address = graphene.String()
        is_active = graphene.Boolean()


    user = graphene.Field(UserType)
    def mutate(self, info, username, password, first_name, last_name, phone, email, address):
        user = Users(username=username, password=password, first_name=first_name, last_name=last_name, phone=phone , email=email, address=address)
        user.save()
        send_create(user)
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        username = graphene.String()
        password = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        phone = graphene.String()
        email = graphene.String()
        address = graphene.String()
        is_active = graphene.Boolean()
         
    user = graphene.Field(UserType)
    def mutate(self, info , id, username=None, password=None, first_name=None, last_name=None, phone=None, email=None, address=None):
        try:
            user = Users.objects.get(pk=id)
            changes = {}
            if username is not None and user.username!=username:
                changes["username"] = {"old_val": user.username , "new_val": username}
                user.username = username

            if password is not None and user.password!=password:
                changes["password"] = {"old_val": user.password , "new_val": password}
                user.password = password

            if first_name is not None and user.first_name!=first_name:
                changes["first_name"] = {"old_val": user.first_name , "new_val": first_name}
                user.first_name = first_name

            if last_name is not None and user.last_name!=last_name:
                changes["last_name"] = {"old_val": user.last_name , "new_val": last_name}
                user.last_name = last_name

            if phone is not None and user.phone!=phone:
                changes["phone"] = {"old_val": user.phone , "new_val": phone}
                user.phone = phone

            if email is not None and user.email!=email:
                changes["email"] = {"old_val": user.email , "new_val": email}
                user.email = email

            if address is not None and user.address!=address:
                changes["address"] = {"old_val": user.address , "new_val": address}
                user.address = address
            
            user.save()
            send_edit(user,"SUCCESS", changes=changes)
            return UpdateUser(user=user)
    
        except Exception as e:
            send_edit(user, "FAILED" ,changes=changes)
            raise Exception(f"Update User Failed:{str(e)}")

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    ok = graphene.Boolean()
    def mutate(self , info, id):
        user = Users.objects.get(pk=id)
        user.delete()
        send_delete(user)
        return DeleteUser(ok=True)
        
class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()



def send_edit(user , action_s , changes):
    description = f"changes profile of user: {user}\n"
    for key,val in changes.items():
        description += f"_{key}: old value {val['old_val']} changes to new value{val['new_val']} \n"
       
        
    Logs.objects.create(
        user=user,
        action_type="UPDATE_PROFILE",
        action_status=action_s,
        description=description,
    )

def send_delete(user):
    Logs.objects.create(
        user=None,
        action_type="DELETE",
        description=f"delete {user} ",
    )
        
def send_create(user):
    Logs.objects.create(
        user=user,
        action_type="CREATE",
        description=f"create {user}",
    )
    
        