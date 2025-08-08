import graphene
from graphene_django import DjangoObjectType
from Log.models import Logs
# from django_filters import FilterSet

class LogsType(DjangoObjectType):
    typename = graphene.String()
    formatted_time = graphene.String()
    formatted_description = graphene.String()

    def resolve_typename(self , info):
        return "Logs"

    def resolve_formatted_time(self, info):
        return self.action_time.strftime("%H:%M | %d %b %Y")  

    def resolve_formatted_description(self, info):
        return self.description

    class Meta:
        model = Logs
        fields = "__all__"
