from django.forms.models import ModelForm
from .models import User, Supplier, Bill

class Userform(ModelForm):
    class Meta:
        fields = "__all__"
        model = User


class Suppform(ModelForm):
    class Meta:
        fields = "__all__"
        model = Supplier


class Billform(ModelForm):
    class Meta:
        fields = "__all__"
        model = Bill
