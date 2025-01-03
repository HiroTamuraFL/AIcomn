from django import forms
from .models import Messages
 
class UploadForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['image']