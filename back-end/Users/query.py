import graphene
from Users.models import Users
from .type import UserType, UserCountsType

class UserCountsType(graphene.ObjectType):
    total_users = graphene.Int()
    admin_count = graphene.Int()

class UserQuery(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.ID(required=True))
    me = graphene.Field(UserType)
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))
    user_counts = graphene.Field(UserCountsType)

    def resolve_all_users(root, info):
        return Users.objects.all()
    
    def resolve_user_by_id(self, info , id):
        try:
            return Users.objects.get(id=id)
        except Users.DoesNotExist:
            return None
        
    def resolve_user_by_username(self, info , username):
        try:
            return Users.objects.get(username=username)
        except Users.DoesNotExist:
            return None
        
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            return None
        return user
    
    def resolve_user_counts(root, info):
        total = Users.objects.count()
        admins = Users.objects.filter(role='admin').count() 
        return UserCountsType(total_users=total, admin_count=admins)
        
    