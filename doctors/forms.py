from django import forms
from .models import Doctor, AnimalSpecialty #OpeningHour
#from accounts.validators import allow_only_images_validator



class DoctorForm(forms.ModelForm):
    
    SPECIALTY_CHOICE = (
        ('cat', 'Cat'),
        ('cattle', 'Cattle'),
        ('dog', 'Dog'),
        ('goat', 'Goat'),
        ('horse', 'Horse'),
        ('poultry', 'Poultry'),
        ('sheep', 'Sheep'),
    )
    
    #vcn_number = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), )
    vcn_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    state_of_practice = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # specialty = forms.MultipleChoiceField( choices=SPECIALTY_CHOICE, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}))
    
    
    
    def __init__(self, *args, **kwargs):
        super(DoctorForm, self). __init__(*args, **kwargs)
        self.fields["vcn_number"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : 'VCN Number' 
            }
        )
        self.fields["state_of_practice"].widget.attrs.update(
            {
             'type': 'multiple',
             'class' : 'form-control',
             'placeholder' : 'state of practice e.g Niger' 
            }
        )
        # self.fields["specialty"].widget.attrs.update(
        #     {
        #      'type': 'choice',
        #      'class' : 'form-control',
        #      'placeholder' : 'specialty' 
        #     }
        # )
        
    class Meta:
        
        model = Doctor
        fields = ['vcn_number', 'state_of_practice',]

			
	
		








# class OpeningHourForm(forms.ModelForm):
#     class Meta:
#         model = OpeningHour
#         fields = ['day', 'from_hour', 'to_hour', 'is_closed']