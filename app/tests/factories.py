import factory

from app.models import Post, User


def user_factory(session):
    class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        """Фабрика Пользователя."""

        username = factory.Faker("word")
        email = factory.Faker("email")
        hashed_password = "123"

        class Meta:
            model = User
            sqlalchemy_session = session

    return UserFactory


def post_factory(session):
    class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
        """Фабрика Публикации."""

        user = factory.SubFactory(user_factory(session))
        text = factory.Faker("sentence")

        class Meta:
            model = Post
            sqlalchemy_session = session

    return PostFactory
