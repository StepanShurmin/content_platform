from content.models import Likes, Dislikes, Publication


def toggle_like(like):
    if like.is_active:
        like.is_active = False
        like.save()
    else:
        like.is_active = True
        like.save()


def toggle_dislike(dislike):
    if dislike.is_active:
        dislike.is_active = False
        dislike.save()
    else:
        dislike.is_active = True
        dislike.save()


def create_like(user, post):
    Likes.objects.create(user=user, publication=post, is_active=True)


def create_dislikes(user, post):
    Dislikes.objects.create(user=user, publication=post, is_active=True)
