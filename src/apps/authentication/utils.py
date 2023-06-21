import random
import string

from django.contrib.auth import get_user_model
from django.utils.text import slugify

from .api.tokens import JWTAccessToken


def slugify_instance_name(instance, new_slug=None):
    """
    Create a unique slug value
    -----
    Checking slug existence by apply recursion
    """

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    # Check if the new slug is existed
    klass = instance.__class__
    qs = klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = f"{slug}-{random.randint(300_000, 500_000)}"
        return slugify_instance_name(instance, slug)

    instance.slug = slug

    return instance


def generate_random_number(length=6) -> str:
    """generates a string of random digits encoded as string.

    Args:
        length (int, optional): The number of digits to return. Defaults to 6.

    Returns:
        str: A string of decimal digits
    """
    rand = random.SystemRandom()

    if hasattr(rand, "choices"):
        digits = rand.choices(string.digits, k=length)
    else:
        digits = (rand.choice(string.digits) for i in range(length))

    return "".join(digits)


def get_user_from_access_token(access_token_str):
    access_token_obj = JWTAccessToken(access_token_str, verify=True)
    user_id = access_token_obj["user_id"]
    user = get_user_model().objects.get(id=user_id)
    return user
