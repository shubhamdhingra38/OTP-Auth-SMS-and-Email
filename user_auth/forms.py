from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyUser


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False


    class Meta:
        model = MyUser
        fields = ['username', 'name', 'email', 'phone_num']