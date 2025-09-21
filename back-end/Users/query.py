import graphene
from Users.models import Users
from .type import UserType, UserCountsType
from django.db.models import Q

class UserCountsType(graphene.ObjectType):
    total_users = graphene.Int()
    admin_count = graphene.Int()

class UserQuery(graphene.ObjectType):
    all_users = graphene.List(UserType,
                            login_num=graphene.Int(),
                            is_active=graphene.Boolean(),
                            page=graphene.Int(default_value=1),
                            limit=graphene.Int(default_value=10),
                            start_date=graphene.DateTime(),
                            end_date=graphene.DateTime(),
                            search=graphene.String(),
                            order_by=graphene.String(default_value="-created_at")
                              )
    user_by_id = graphene.Field(UserType, id=graphene.ID(required=True))
    me = graphene.Field(UserType)
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))
    user_counts = graphene.Field(UserCountsType)

    def resolve_all_users(root, info ,search=None, page=1, limit=10, login_num=None , is_active= None ,start_date=None, end_date=None, order_by="-created_at"):
        UsersList = Users.objects.all()
        offset = (page - 1) * limit
        if search:
            q = (
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(address__icontains=search) |
                Q(role__icontains=search)
            )

            search_lower = search.lower()
            if search_lower == "active":
                q |= Q(is_active=True)
            elif search_lower == "inactive":
                q |= Q(is_active=False)

            UsersList = UsersList.filter(q)
        if login_num:
            UsersList = UsersList.filter(login_num=login_num)
        if is_active is not None:
            UsersList = UsersList.filter(is_active=is_active)
                    
        if start_date and end_date:
            UsersList = UsersList.filter(created_at__range=[start_date, end_date])
        elif start_date:
            UsersList = UsersList.filter(created_at__gte=start_date)
        elif end_date:
            UsersList = UsersList.filter(created_at__lte=end_date)

        UsersList = UsersList.order_by(order_by)
        return UsersList[offset: offset+limit]
    
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
        admins = Users.objects.filter(role='ADMIN').count()
        return UserCountsType(total_users=total, admin_count=admins)
        
    