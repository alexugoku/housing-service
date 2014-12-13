from django.forms import (
    Form, CharField, Textarea, PasswordInput, ChoiceField, DateField,
    ImageField,
)
from django.forms import ModelForm
from accommodations.models import Student, Dorm


class UserLogin(Form):
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)


class UserProfileForm(Form):
    first_name = CharField(max_length=100, required=False)
    last_name = CharField(max_length=100, required=False)
    # gender = ChoiceField(choices=UserProfile.GENDERS, required=False)
    date_of_birth = DateField(required=False)
    avatar = ImageField(required=False)


class ApplicationForm(ModelForm):
    class Meta:
        model = Student


class DormForm(ModelForm):
    class Meta:
        model = Dorm