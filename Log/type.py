import graphene
from graphene_django import DjangoObjectType
from Log.models import Logs
from django_filters import FilterSet
from graphene import relay




class LogFilter(FilterSet):
    class Meta:
        model = Logs
        fields ={
             'action_type' : ['exact',],
             'action_status' : ['exact',],
             'user' : ['exact',],
             'id':['exact'],
        }
   

class LogsType(DjangoObjectType):
    typename = graphene.String()
    def resolve_typename(self , info):
        return "Logs"
    class Meta:
        model = Logs
        interfaces = (relay.Node, )
        fields = "__all__"
        filterset_class = LogFilter