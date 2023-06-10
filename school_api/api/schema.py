import graphene
import uuid
from graphene_django import DjangoObjectType
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, user_id=graphene.UUID())

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, user_id):
        return User.objects.get(pk=user_id)


class UserInput(graphene.InputObjectType):
    id = graphene.UUID()
    type = graphene.String(description="User type (student, teacher, coordinator)")
    name = graphene.String()
    last_name = graphene.String()
    username = graphene.String()
    pass_hash = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user_data=None):
        user_instance = User(
            id=uuid.uuid4(),
            type=user_data.type,
            name=user_data.name,
            last_name=user_data.last_name,
            username=user_data.username,
            pass_hash=user_data.pass_hash
        )
        user_instance.save()
        return CreateUser(user=user_instance)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user_data=None):
        user_instance = User.objects.get(pk=user_data.id)

        if user_instance:
            user_instance.type = user_data.type
            user_instance.name = user_data.name
            user_instance.last_name = user_data.last_name
            user_instance.username = user_data.username
            user_instance.pass_hash = user_data.pass_hash
            user_instance.save()

            return UpdateUser(user=user_instance)
        return UpdateUser(user=None)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.UUID()

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id):
        user_instance = User.objects.get(pk=id)
        user_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

