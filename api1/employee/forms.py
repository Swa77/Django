from django import forms
from .models import Jobprofile
# write your validations here and include this in admin.py
class Employeeform(forms.ModelForm):
    class Meta:
        model=Jobprofile

        fields=[

            'name',
            'company',
            'logo'
        ]

    def  clean(self,*args,**kwargs):
        data = self.cleaned_data
        name=data.get('name',None)

        if name=="":
            name=None
        if name is None:
            raise forms.ValidationError("Name cannot be empty!")

        return super().clean(*args,**kwargs)
