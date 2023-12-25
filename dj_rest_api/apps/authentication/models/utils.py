import random
import string


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
