import factory
from django.contrib.auth.models import User
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from blog.models import Post, Comment


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
    
    title = factory.Faker("sentence", nb_words=4)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title)[:50])
    
    body = factory.Faker("text", max_nb_chars=1000)
    author = factory.SubFactory(UserFactory)
    tags = factory.Faker("words", nb=3)
    status = 1



class DraftPostFactory(PostFactory):
    status = 0  # Draft


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment
    
    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    content = factory.Faker("text", max_nb_chars=200)
    active = True


class InactiveCommentFactory(CommentFactory):
    active = False
