from graphene_django import DjangoObjectType
from Users.models import Users
import graphene

class UserType(DjangoObjectType):
    class Meta:
        model = Users
        fields = "__all__"

class UserCountsType(graphene.ObjectType):
    total_users = graphene.Int()
    admin_count = graphene.Int()