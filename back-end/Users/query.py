import graphene
from Users.models import Users
from .type import UserType

class UserQuery(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.ID(required=True))
    me = graphene.Field(UserType)

    def resolve_all_users(root, info):
        return Users.objects.all()
    def resolve_user_by_id(self, info , id):
        try:
            return Users.objects.get(id=id)
        except Users.DoesNotExist:
            return None
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            return None
        return user
        
    