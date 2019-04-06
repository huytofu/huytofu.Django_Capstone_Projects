from django.forms import ModelForm
from . import models
from groups.models import Group

class FilterPostForm(ModelForm):
    class Meta():
        model = models.Post
        fields = ('title','message','group')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(members__in=[user])
