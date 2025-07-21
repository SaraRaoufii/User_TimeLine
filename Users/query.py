import graphene
from Users.models import Users
from .type import UserType

class UserQuery(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.ID(required=True))

    def resolve_all_users(root, info):
        return Users.objects.all()
    def resolve_user_by_id(self, info , id):
        try:
            return Users.objects.get(id=id)
        except Users.DoesNotExist:
            return None
        
    