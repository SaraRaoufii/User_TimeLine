from .models import Auth_Logs
from graphene_django import DjangoObjectType
import graphene
class AuthLogsType(DjangoObjectType):
    typename = graphene.String()
    def resolve_typename(self , info):
        return "Logs"
    class Meta:
        model = Auth_Logs
        fields = "__all__"
