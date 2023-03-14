from django import forms

from accounts.validators import allow_only_images_validator
from .models import Consultation, ConsultationItem, Fee, Service




class ConsultationItemForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ConsultationItemForm, self). __init__(*args, **kwargs)
        self.fields["category"].widget.attrs.update(
            {
             'type': 'select',
             'class' : 'form-control',
             'placeholder' : '' 
            }
        )
        self.fields["type"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : '' 
            }
        )
        self.fields["fee"].widget.attrs.update(
            {
             'type': 'select',
             'class' : 'form-control',
            'placeholder' : 'specialty e.g cat'
             
            }
        )
        self.fields["description"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
            'placeholder' : 'add more details...'
             
            }
        )
        # self.fields["is_available"].widget.attrs.update(
        #     {
        #      'type': 'checkbox',
        #      'class' : 'form-control',
        #     'placeholder' : ''
             
        #     }
        # )
   
    class Meta:
        model = ConsultationItem
        fields = ['category', 'type', 'fee', 'description', 'is_available']