from graphene_django import DjangoObjectType
from Users.models import Users

class UserType(DjangoObjectType):
    class Meta:
        model = Users
        fields = "__all__"