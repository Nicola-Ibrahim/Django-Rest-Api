import random
import string

from django.utils.text import slugify


def slugify_instance_name(instance, field_name, new_slug=None):
    """
    Generate a slug for an instance based on a specified field.

    This function takes an instance of a Django model and a field name,
    and generates a slug for the instance based on the value of the specified field.
    It ensures that the generated slug is unique within the model's queryset.

    Args:
        instance (django.db.models.Model): The instance of the model.
        field_name (str): The name of the field to be used for generating the slug.
        new_slug (str, optional): A new slug to be used. Defaults to None.

    Returns:
        django.db.models.Model: The instance with the slug attribute updated.

    Example:
        Assuming you have an instance of some model 'MyModel':

        ```python
        my_instance = MyModel.objects.get(id=1)
        updated_instance = slugify_instance_name(my_instance, 'name')
        ```

        This will generate a slug based on the 'name' field of 'my_instance' and update
        the 'slug' attribute of the instance.

    Note:
        The generated slug will be unique within the queryset of the model, ensuring
        that there are no conflicts with existing slugs.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        value = getattr(instance, field_name)
        slug = slugify(value)

    # Check if the new slug exists in the model's queryset
    klass = instance.__class__
    qs = klass.objects.filter(slug=slug).exclude(id=instance.id)

    # If it exists, append a random number to make it unique
    if qs.exists():
        slug = f"{slug}-{random.randint(300_000, 500_000)}"
        return slugify_instance_name(instance, field_name, slug)

    instance.slug = slug
    return instance


def generate_random_number(length: int = 6) -> str:
    """
    Generate a random number with the specified length.

    This function generates a random number with the specified length using the
    `random.choices` method from the `random` module.

    Args:
        length (int, optional): The length of the random number. Defaults to 6.

    Returns:
        str: A string containing the generated random number.

    Example:
        ```python
        random_number = generate_random_number()
        ```

        This will generate a random number with the default length of 6.

    Note:
        The function uses `random.choices` to select digits from the string of
        decimal digits (0-9) to form the random number.
    """
    digits = random.choices(string.digits, k=length)

    return "".join(digits)
