from django.db import models
import random
import string


class Utilities:
    @staticmethod
    def generate_code(length):
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

        return code
