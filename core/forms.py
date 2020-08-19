from django import forms
from.models import Contestimg

class ContestimgForm(forms.ModelForm): 
    class Meta:  
        model = Contestimg
        fields = ['image_title','image','contest']