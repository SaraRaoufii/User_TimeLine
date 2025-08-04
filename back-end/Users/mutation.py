import graphene
import graphql_jwt
from graphql_jwt.shortcuts import get_token
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
        current_user = info.context.user
        print("Authenticated:", current_user.is_authenticated)
        if not current_user.is_authenticated:
            raise Exception("You should login")
        
        # if not current_user.is_staff:
        #     raise Exception("You do not have access")
        
        if current_user.role !="admin":
            raise Exception("You do not have access")
        
        target_user = Users(username=username, password=password, first_name=first_name, last_name=last_name, phone=phone , email=email, address=address, role=role)
        target_user.set_password(password)
        target_user.save()
        send_create(current_user,target_user)
        return CreateUser(user=target_user)
    

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
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception("You should login")
        
        changes = {}
        try:
            target_user = Users.objects.get(pk=id)
            if username is not None and target_user.username!=username:
                changes["username"] = {"old_val": target_user.username , "new_val": username}
                target_user.username = username

            if password is not None and not target_user.check_password(password):
                changes["password"] = {"old_val": "********", "new_val": "********"}
                target_user.set_password(password)


            if first_name is not None and target_user.first_name!=first_name:
                changes["first_name"] = {"old_val": target_user.first_name , "new_val": first_name}
                target_user.first_name = first_name

            if last_name is not None and target_user.last_name!=last_name:
                changes["last_name"] = {"old_val": target_user.last_name , "new_val": last_name}
                target_user.last_name = last_name

            if phone is not None and target_user.phone!=phone:
                changes["phone"] = {"old_val": target_user.phone , "new_val": phone}
                target_user.phone = phone

            if email is not None and target_user.email!=email:
                changes["email"] = {"old_val": target_user.email , "new_val": email}
                target_user.email = email

            if address is not None and target_user.address!=address:
                changes["address"] = {"old_val": target_user.address , "new_val": address}
                target_user.address = address
            
            if role is not None and target_user.role!=role:
                changes["role"] = {"old_val": target_user.role , "new_val": role}
                target_user.role = role

            target_user.save()
            send_edit(current_user,target_user,"SUCCESS", changes=changes)
            return UpdateUser(user=target_user)
    
        except Exception as e:
            send_edit(current_user,target_user, "FAILED" ,changes=changes)
            raise Exception(f"Update User Failed:{str(e)}")

"""
class for delete user with id
"""
class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    ok = graphene.Boolean()

    def mutate(self , info, id):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception("You should login")
        
        try:
            target_user = Users.objects.get(pk=id)
        except:
            raise Exception("target user not found")
        
        if current_user.id==target_user.id:
            target_user.delete()
            send_delete(target_user)
            return DeleteUser(ok=True)
        
        if current_user.role!="admin":
            raise Exception("You do noy have access")
        
        if target_user.role=="admin":
            raise Exception("You con not delete admin users")
        
        target_user.delete()
        send_delete(current_user, target_user)
        return DeleteUser(ok=True)

class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    user_id = graphene.ID()
    tocken = graphene.String()
    def mutate(self, info , username, password):
        user = authenticate(username=username , password=password)
        if user is None:
            return LoginUser(success=False, message= "Your informaitions are false" , user_id=None)
        else:
            send_login(user)
            tocken=get_token(user)
            print(user)
            return LoginUser(success=True, message= "You login successfull" , user_id=user.id, tocken=tocken)

class LogoutUser(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info):
        user = info.context.user
        request = info.context

        if not user.is_authenticated:
            return LogoutUser(success=False, message="Invalid or missing token.")

        send_logout(user)

        logout(request)

        return LogoutUser

class AuthMutation(graphene.ObjectType):
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()



class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()



def send_edit(actoruser , targetuser, action_s , changes):
    description = f"changes profile of user: {targetuser}\n"
    for key,val in changes.items():
        description += f"_{key}: old value {val['old_val']} changes to new value{val['new_val']} \n"
       
        
    Logs.objects.create(
        target_user=targetuser,
        actor_user=actoruser,
        action_type="UPDATE_PROFILE",
        action_status=action_s,
        description=description,
    )

def send_delete(actoruser, targetuser):
    Logs.objects.create(
        actor_user=actoruser,
        target_user=targetuser,
        action_type="DELETE",
        description=f"delete {targetuser} ",
    )
        
def send_create(actoruser, targetuser ):
    Logs.objects.create(
        actor_user=actoruser,
        target_user=targetuser,
        action_type="CREATE",
        description=f"create {targetuser}",
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