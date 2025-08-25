import graphene
import graphql_jwt
from graphql_jwt.shortcuts import get_token
from Users.models import Users
from Users.type import UserType
from Log.models import Logs
from Log_Auth.models import Auth_Logs
import graphene
from graphql_jwt.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken

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
                if current_user.role != "admin":
                    raise Exception("Only admin can change roles")
                changes["role"] = {"old_val": target_user.role , "new_val": role}
                target_user.role = role

            target_user.save()
            send_edit(current_user,target_user,"SUCCESS", changes=changes)
            return UpdateUser(user=target_user)
    
        except Exception as e:
            send_edit(current_user, locals().get("target_user"), "FAILED", changes=changes)
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
            send_delete(current_user, target_user)
            target_user.delete()
            return DeleteUser(ok=True)
        
        if current_user.role!="admin":
            raise Exception("You do noy have access")
        
        if target_user.role=="admin":
            raise Exception("You con not delete admin users")
        
        send_delete(current_user, target_user)
        target_user.delete()
        return DeleteUser(ok=True)

class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        user = info.context.user
        if user.is_authenticated:
            send_login(user)
        return cls(user=info.context.user)

class RevokeToken(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        refresh_token = graphene.String(required=True)

    @login_required
    def mutate(self, info, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return RevokeToken(success=True, message="Token revoked successfully")
        except Exception as e:
            return RevokeToken(success=False, message=f"Failed to revoke token: {str(e)}")
        
class LogoutUser(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info):
        user = info.context.user

        if not user.is_authenticated:
            return LogoutUser(success=False, message="Invalid or missing token.")

        send_logout(user)
        return LogoutUser(success=True, message="Logged out successfully")


class AuthMutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    logout_user = LogoutUser.Field()
    revoke_token = RevokeToken.Field()



class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()



import json

def send_edit(actoruser, targetuser, action_s, changes):
    Logs.objects.create(
        actor_user=actoruser,
        target_user=targetuser,
        action_type="UPDATE_PROFILE",
        action_status=action_s,
        action_title="Edit user",
        category="Management",
        description=json.dumps({
            "message": f"Updated profile of user {targetuser.username}",
            "fields_changed": changes
        })
    )


def send_delete(actoruser, targetuser):
    Logs.objects.create(
        actor_user=actoruser,
        target_user=targetuser,
        action_type="DELETE",
        action_title="Delete user",
        category="Management",
        description=json.dumps({
            "message": f"Deleted user {targetuser.username}"
        })
    )

        
def send_create(actoruser, targetuser):
    Logs.objects.create(
        actor_user=actoruser,
        target_user=targetuser,
        action_type="CREATE",
        action_title="Create user",
        category="Management",
        description=json.dumps({
            "message": f"Created user {targetuser.username}"
        })
    )


def send_login(user):
    Auth_Logs.objects.create(
        user=user,
        action_type="Login",
        action_title="Login user",
        description=f"Login {user}"
    )

def send_logout(user):
    Auth_Logs.objects.create(
        user=user,
        action_type="Logout",
        action_title="Logout user",
        description=f"Logout {user}"
    )