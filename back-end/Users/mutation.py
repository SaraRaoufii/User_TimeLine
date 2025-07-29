import graphene
import graphql_jwt
from Users.models import Users
from Users.type import UserType
from Log.models import Logs
from Log_Auth.models import Auth_Logs
from django.contrib.auth import authenticate, logout

"""
class for creat new user with username, firstname, ...
"""
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
        role = graphene.String()


    user = graphene.Field(UserType)
    def mutate(self, info, username, password, first_name, last_name, phone, email, address , role):
        user = Users(username=username, password=password, first_name=first_name, last_name=last_name, phone=phone , email=email, address=address, role=role)
        user.set_password(password)
        user.save()
        send_create(user)
        return CreateUser(user=user)
    

"""
class for update informatiom of user with id
"""
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
        role = graphene.String()
         
    user = graphene.Field(UserType)
    def mutate(self, info , id, username=None, password=None, first_name=None, last_name=None, phone=None, email=None, 
    address=None , role=None):
        changes = {}
        try:
            user = Users.objects.get(pk=id)
            if username is not None and user.username!=username:
                changes["username"] = {"old_val": user.username , "new_val": username}
                user.username = username

            if password is not None and not user.check_password(password):
                changes["password"] = {"old_val": "********", "new_val": "********"}
                user.set_password(password)


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
            
            if role is not None and user.role!=role:
                changes["role"] = {"old_val": user.role , "new_val": role}
                user.role = role

            user.save()
            send_edit(user,"SUCCESS", changes=changes)
            return UpdateUser(user=user)
    
        except Exception as e:
            send_edit(user, "FAILED" ,changes=changes)
            raise Exception(f"Update User Failed:{str(e)}")

"""
class for delete user with id
"""
class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    ok = graphene.Boolean()
    def mutate(self , info, id):
        user = Users.objects.get(pk=id)
        user.delete()
        send_delete(user)
        return DeleteUser(ok=True)

class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    user_id = graphene.ID()
    def mutate(self, info , username, password):
        user = authenticate(username=username , password=password)
        if user is None:
            return LoginUser(success=False, message= "Your informaitions are false" , user_id=None)
        else:
            send_login(user)
            print(user)
            return LoginUser(success=True, message= "You login successfull" , user_id=user.id)

class LogoutUser(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    def mutate(self, info):
        user = info.context.user
        request = info.context

        if user.is_authenticated:
            send_logout(user)
            logout(request)
            return LogoutUser(success=True, message="User logged out successfully.")
        else:
            return LogoutUser(success=False, message="User is not authenticated.")
            

class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()



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
        user=user,
        action_type="DELETE",
        description=f"delete {user} ",
    )
        
def send_create(user):
    Logs.objects.create(
        user=user,
        action_type="CREATE",
        description=f"create {user}",
    )

def send_login(user):
    Auth_Logs.objects.create(
        user=user,
        action_type="Login",
        description=f"Login {user}"
    )

def send_logout(user):
    Auth_Logs.objects.create(
        user=user,
        action_type="Logout",
        description=f"Logout {user}"
    )