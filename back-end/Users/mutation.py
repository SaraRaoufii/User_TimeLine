import graphene
import graphql_jwt
from graphql_jwt.shortcuts import get_token
from Users.models import Users,DeletedUserSnapshot
from Users.type import UserType
from Log.models import Logs
from Log_Auth.models import Auth_Logs
from graphql_jwt.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import F
import re
from django.core.exceptions import ValidationError
import json
import datetime


def validate_phone(phone):
    if phone and not re.fullmatch(r'^\d{11}$', phone):
        raise ValidationError("Phone number must be exactly 11 digits.")


def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r'[@$!%*?&]', password):
        raise ValidationError("Password must contain at least one special character (@$!%*?&).")


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        phone = graphene.String()
        email = graphene.String()
        address = graphene.String()
        isActive = graphene.Boolean()
        role = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, username, password, first_name, last_name, phone=None, email=None, address=None, isActive=True, role=None):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception(json.dumps({"non_field_error": "You should login"}))
        if current_user.role.upper() != "ADMIN":
            raise Exception(json.dumps({"non_field_error": "You do not have access"}))

        role = role.upper() if role else "USER"
        if role not in ["ADMIN", "USER"]:
            raise Exception(json.dumps({"role": "Invalid role, must be 'ADMIN' or 'USER'"}))

        try:
            if Users.objects.filter(username=username).exists():
                raise Exception(json.dumps({"username": "Username already exists."}))
            if email and Users.objects.filter(email=email).exists():
                raise Exception(json.dumps({"email": "Email already exists."}))

            validate_password(password)
            if phone:
                validate_phone(phone)

            target_user = Users.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                address=address,
                role=role,
                is_active=isActive
            )
        except ValidationError as e:
            error_message = str(e)
            if "Phone" in error_message or "phone" in error_message:
                raise Exception(json.dumps({"phone": [error_message]}))
            elif "Password" in error_message or "password" in error_message:
                raise Exception(json.dumps({"password": [error_message]}))
            else:
                raise Exception(json.dumps({"non_field_error": [error_message]}))

        send_create(current_user, target_user)
        return CreateUser(user=target_user)


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
        isActive = graphene.Boolean()
        role = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, id, username=None, password=None, first_name=None, last_name=None,
               phone=None, email=None, address=None, role=None, isActive=None):

        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception(json.dumps({"non_field_error": "You should login"}))
        if not current_user.is_active:
            raise Exception(json.dumps({"non_field_error": "User is not active"}))

        changes = {}
        target_user = None
        try:
            target_user = Users.objects.get(pk=id)
            if Users.objects.filter(username=username).exists() and target_user.username!=username:
                raise Exception(json.dumps({"username": "Username already exists."}))
            if target_user.role.upper() == "ADMIN" and target_user.id!=current_user.id:
                raise Exception(json.dumps({"non_field_error": "You cannot edit admin users"}))
            if email and Users.objects.filter(email=email).exists() and target_user.email!= email:
                raise Exception(json.dumps({"email": "Email already exists."}))


            if username and target_user.username != username:
                changes["username"] = {"old_val": target_user.username, "new_val": username}
                target_user.username = username

            if password and not target_user.check_password(password):
                validate_password(password)
                changes["password"] = {"old_val": "********", "new_val": "********"}
                target_user.set_password(password)

            if first_name and target_user.first_name != first_name:
                changes["first_name"] = {"old_val": target_user.first_name, "new_val": first_name}
                target_user.first_name = first_name

            if last_name and target_user.last_name != last_name:
                changes["last_name"] = {"old_val": target_user.last_name, "new_val": last_name}
                target_user.last_name = last_name

            if phone and target_user.phone != phone:
                validate_phone(phone)
                changes["phone"] = {"old_val": target_user.phone, "new_val": phone}
                target_user.phone = phone

            if email and target_user.email != email:
                changes["email"] = {"old_val": target_user.email, "new_val": email}
                target_user.email = email

            if address and target_user.address != address:
                changes["address"] = {"old_val": target_user.address, "new_val": address}
                target_user.address = address

            if isActive is not None and target_user.is_active != isActive:
                changes["is_active"] = {"old_val": target_user.is_active, "new_val": isActive}
                target_user.is_active = isActive

            if role:
                role_upper = role.upper()
                if role_upper not in ["ADMIN", "USER"]:
                    raise Exception(json.dumps({"role": "Invalid role, must be 'ADMIN' or 'USER'"}))
                if target_user.role != role_upper:
                    if current_user.role.upper() != "ADMIN":
                        raise Exception(json.dumps({"role": "Only admin can change roles"}))
                    changes["role"] = {"old_val": target_user.role, "new_val": role_upper}
                    target_user.role = role_upper

            target_user.save()
            send_edit(current_user, target_user, "SUCCESS", changes=changes)
            return UpdateUser(user=target_user)

        except ValidationError as e:
            error_message = str(e)
            if "Phone" in error_message or "phone" in error_message:
                raise Exception(json.dumps({"phone": error_message}))
            elif "Password" in error_message or "password" in error_message:
                raise Exception(json.dumps({"password": error_message}))
            else:
                raise Exception(json.dumps({"non_field_error": error_message}))


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    ok = graphene.Boolean()

    def mutate(self, info, id):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception(json.dumps({"non_field_error": "You should login"}))
        
        try:
            target_user = Users.objects.get(pk=id)
        except Users.DoesNotExist:
            raise Exception(json.dumps({"non_field_error": "Target user not found"}))
        
        target_username = target_user.username
        current_username = current_user.username

        if current_user.id == target_user.id:
            send_self_delete(current_username)
            target_user.delete()
            return DeleteUser(ok=True)

        if current_user.role.upper() != "ADMIN":
            raise Exception(json.dumps({"non_field_error": "You do not have access"}))

        if target_user.role.upper() == "ADMIN" and current_user.role.upper() == "ADMIN":
            raise Exception(json.dumps({"non_field_error": "You cannot delete admin users"}))
        
        user_snapshot = {
            "username": target_user.username,
            "email": target_user.email,
            "phone": target_user.phone,
            "first_name": target_user.first_name,
            "last_name": target_user.last_name,
            "address": target_user.address,
            "role": target_user.role,
            "is_active": target_user.is_active,
            "created_at": target_user.created_at.isoformat(),  
            "updated_at": target_user.updated_at.isoformat(),
        }

        user_logs = list(Logs.objects.filter(target_user=target_user).values())
        for log in user_logs:
            for key, value in log.items():
                if isinstance(value, (datetime.date, datetime.datetime)):
                    log[key] = value.isoformat()

 
        DeletedUserSnapshot.objects.create(
            user_data=user_snapshot,
            logs=user_logs
        )

        send_delete(current_user, user_snapshot)
        target_user.delete()
        return DeleteUser(ok=True)



class ObtainJSONWebToken(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, username, password):
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            raise Exception(json.dumps({"non_field_error": "Invalid username or password."}))


        if user.is_locked:
            raise Exception(json.dumps({"non_field_error": "Account is locked."}))

        if not user.check_password(password):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.is_locked = True
                send_lock(user)
            user.save(update_fields=["failed_login_attempts", "is_locked"])

            if not user.is_locked:
                send_login_failed(user)

            raise Exception(json.dumps({"non_field_error": "Invalid username or password."}))

        if not user.is_active:
            raise Exception(json.dumps({"non_field_error": "Account is deactivated."}))

        user.login_num = F('login_num') + 1
        user.save(update_fields=["login_num", "failed_login_attempts"])
        user.refresh_from_db()
        
        send_login(user)

        token = get_token(user)
        return cls(user=user, token=token)


class RevokeToken(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        refresh_token = graphene.String(required=True)

    @login_required
    def mutate(self, info, refresh_token):
        user = info.context.user
        if not user.is_active or user.is_locked:
            return RevokeToken(success=False, message="Account inactive or locked.")
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
        
        if not user.is_active or user.is_locked:
            return LogoutUser(success=False, message="Account inactive or locked.")

        send_logout(user)
        return LogoutUser(success=True, message="Logged out successfully")

class ResetLockedUser(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        user_id = graphene.ID(required=True)

    def mutate(self, info, user_id):
        current_user = info.context.user

        if not current_user.is_authenticated:
            return ResetLockedUser(success=False, message="You should login")
        
        if not current_user.is_active or current_user.is_locked:
            return ResetLockedUser(success=False, message="Admin account inactive or locked.")

        if current_user.role.upper() != "ADMIN":
            return ResetLockedUser(success=False, message="Only admin can reset locked accounts")
        

        try:
            target_user = Users.objects.get(pk=user_id)
            if not target_user.is_locked:
                return ResetLockedUser(success=False, message=f"User {target_user.username} is not locked.")

        except Users.DoesNotExist:
            return ResetLockedUser(success=False, message="Target user not found")

        target_user.failed_login_attempts = 0
        target_user.is_locked = False
        target_user.save(update_fields=["failed_login_attempts", "is_locked"])
        send_resetlock(current_user,target_user)

        return ResetLockedUser(success=True, message=f"User {target_user.username} unlocked successfully")


class AuthMutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    logout_user = LogoutUser.Field()
    revoke_token = RevokeToken.Field()
    reset_locked_user = ResetLockedUser.Field()


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    reset_lock = ResetLockedUser.Field()


def send_edit(actoruser, targetuser, action_s, changes):
    if actoruser.is_locked or not actoruser.is_active:
        raise Exception(json.dumps({"non_field_error": "Action not allowed: account locked or inactive"}))

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

def send_delete(actoruser, targetuser_snapshot):
    if actoruser.is_locked or not actoruser.is_active:
        raise Exception(json.dumps({"non_field_error": "Action not allowed: account locked or inactive"}))

    Logs.objects.create(
        actor_user=actoruser,
        target_user=None,  
        action_type="DELETE_USER",
        action_title="Delete user",
        category="Management",
        description=json.dumps({
            "message": f"Deleted user {targetuser_snapshot['username']}",
            "user_snapshot": targetuser_snapshot  
        })
    )


def send_self_delete(username):
    Logs.objects.create(
        actor_user=None,
        target_user=None,
        action_type="DELETE_USER",
        action_title="Account Self-Deletion",
        category="Account",
        description=json.dumps({
            "message": f"Account for user '{username}' was deleted by the user themselves.",
        })
    )

def send_create(actoruser, targetuser):
    if actoruser.is_locked or not actoruser.is_active:
        raise Exception(json.dumps({"non_field_error": "Action not allowed: account locked or inactive"}))

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
    user.failed_login_attempts=0
    user.save(update_fields=["failed_login_attempts"])
 
    Auth_Logs.objects.create(
        user=user,
        action_type="Login",
        action_title="Login user",
        description=f"Login {user.username}"
    )

def send_login_failed(user):
        user.save(update_fields=["failed_login_attempts"])

        Auth_Logs.objects.create(
        user=user,
        action_type="LOGIN_FAILED",
        action_title="Login failed",
        description=f"Failed login attempt {user.failed_login_attempts} for user {user.username}"
    )

def send_logout(user):
    if not user.is_active or user.is_locked:
        raise Exception(json.dumps({"non_field_error": "Cannot logout: account inactive or locked."}))
    
    Auth_Logs.objects.create(
        user=user,
        action_type="Logout",
        action_title="Logout user",
        description=f"Logout {user.username}"
    )

def send_resetlock(actoruser, targetuser):
    Logs.objects.create(
        actor_user=actoruser,
        target_user=targetuser,
        action_type="RESET_LOCK",
        action_title="Reset Locked Account",
        category="Management",
        description=json.dumps({
            "message": f"Admin {actoruser.username} reset locked account {targetuser.username}"
        })
    )

def send_lock(user):
    Auth_Logs.objects.create(
        user=user,
        action_type="LOCK_USER",
        action_title="Account locked",
        description=f"User {user.username} account was locked due to failed login attempts"
    )
