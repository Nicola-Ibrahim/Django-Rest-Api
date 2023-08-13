import graphene
from django import forms
from graphene_django.forms.mutation import DjangoModelFormMutation

from ..models import models
from .types import UserType


class UserForm(forms.ModelForm):
    """
    using Model Form class to handle mutation in graphene is the best way
    """

    class Meta:
        model = models.User
        fields = [
            "email",
            "password",
            "first_name",
        ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     if self.instance:
    #         self.fields["email"].disabled = True

    def clean_email(self):
        instance = getattr(self, "instance", None)
        print(instance is None)
        if instance:
            return instance.email

        return self.cleaned_data["email"]


class MutationUser(DjangoModelFormMutation):
    """**_Summary:_**
    this mutation is for adding and updating companies in database
    """

    user = graphene.Field(UserType)

    class Meta:
        form_class = UserForm
        model_operations = ["create", "update"]
