# apps/profiles/infrastructure/mapper.py
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.infrastructure.models.profile_model import ProfileModel


def model_to_entity(model: ProfileModel) -> ProfileEntity:
    """
    Converts a Django ProfileModel into a domain ProfileEntity.
    """
    return ProfileEntity(
        user_id=model.user.id,
        description=getattr(model, "description", None),
        background_color=getattr(model, "background_color", None),
        profile_pic_url=getattr(model, "profile_pic_url", None),
        profile_header_img_url=getattr(model, "profile_header_img_url", None),
        bg_img=getattr(model, "bg_img", None),
        profile_theme_music_url=getattr(model, "profile_theme_music_url", ""),
        is_online_msg=getattr(model, "is_online_msg", None),
        is_offline_msg=getattr(model, "is_offline_msg", None),
        upload_count=getattr(model, "upload_count", 0),
        followers_count=getattr(model, "followers_count", 0),
        following_count=getattr(model, "following_count", 0),
        friends_count=getattr(model, "friends_count", 0),
        likes_given=getattr(model, "likes_given", 0),
        dislikes_given=getattr(model, "dislikes_given", 0),
        posts_uploaded=getattr(model, "posts_uploaded", 0),
        comments_posted=getattr(model, "comments_posted", 0),
        last_updated=getattr(model, "last_updated", None),
    )


def entity_to_model(entity: ProfileEntity, model: ProfileModel = None) -> ProfileModel:
    """
    Converts a domain ProfileEntity into a Django ProfileModel.
    If a model is passed, it updates the fields; otherwise creates a new instance.
    """
    if model is None:
        model = ProfileModel()
    
    # user relationship
    from apps.users.models import UserModel
    model.user_id = entity.user_id

    model.description = entity.description
    model.background_color = entity.background_color
    model.profile_pic_url = entity.profile_pic_url
    model.profile_header_img_url = entity.profile_header_img_url
    model.bg_img = entity.bg_img
    model.profile_theme_music_url = entity.profile_theme_music_url
    model.is_online_msg = entity.is_online_msg
    model.is_offline_msg = entity.is_offline_msg
    model.upload_count = entity.upload_count
    model.followers_count = entity.followers_count
    model.following_count = entity.following_count
    model.friends_count = entity.friends_count
    model.likes_given = entity.likes_given
    model.dislikes_given = entity.dislikes_given
    model.posts_uploaded = entity.posts_uploaded
    model.comments_posted = entity.comments_posted
    model.last_updated = entity.last_updated

    return model
