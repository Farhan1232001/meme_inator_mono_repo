from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'apps.posts'
    label = 'posts' # This allows you to use "posts.PostModel"