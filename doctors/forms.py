from django import forms
from .models import Doctor, AnimalSpecialty, OpeningHour, BankAccount
#from accounts.validators import allow_only_images_validator

class DateInput(forms.DateInput):
    input_type = 'date'

class DoctorForm(forms.ModelForm):
    
   
    vcn_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    state_of_practice = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialty = forms.SelectMultiple(choices=AnimalSpecialty.objects.all())
    induction_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',"type": "date", 'readonly': 'readonly'}), required=False)
   
    def __init__(self, *args, **kwargs):
        super(DoctorForm, self). __init__(*args, **kwargs)
        self.fields["specialty"].required = False
        self.fields["vcn_number"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : 'vcn number' 
            }
        )
        self.fields["state_of_practice"].widget.attrs.update(
            {
             'type': 'multiple',
             'class' : 'form-control',
             'placeholder' : 'state of practice e.g Niger'
            
            }
        )
        self.fields["specialty"].widget.attrs.update(
            {
             'type': 'multiple',
             'class' : 'form-control',
            'placeholder' : 'specialty e.g cat',
              'required': 'false'
            }
        )
        self.fields["induction_date"].widget.attrs.update(
            {
             'type': 'date',
             'class' : 'form-control',
            'placeholder' : ' date of induction'
             
            }
        )
       
    class Meta:
        
        model = Doctor
        fields = ['vcn_number', 'state_of_practice','specialty', 'induction_date']
        widgets = {

			
            'vcn_number': forms.TimeInput(attrs={'class': 'form-control'}),
            'state_of_practice': forms.TimeInput(attrs={'class': 'form-control'}),
            'specialty': forms.SelectMultiple(attrs={'class': 'form-control'}),
			'induction_date': forms.DateInput(attrs={'class': 'form-control', "type": "date"}),	
            'my_date_field': DateInput()
		}
		



class BankAccountForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(BankAccountForm, self). __init__(*args, **kwargs)
        self.fields["bank_name"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : '1239860905' 
            }
        )
        self.fields["account_number"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : '' 
            }
        )
        self.fields["account_name"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
            'placeholder' : 'John Doe'
             
            }
        )
     
    class Meta:
        model = BankAccount
        fields = ['bank_name', 'account_number', 'account_name']

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_offline']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'from_hour': forms.Select(attrs={'class': 'form-control'}),
            'to_hour': forms.Select(attrs={'class': 'form-control'}),
           
        }




 # specialty= forms.ModelMultipleChoiceField(queryset=AnimalSpecialty.objects.all(), widget=forms.CheckboxSelectMultiple())
 # specialty = forms.MultipleChoiceField( choices=SPECIALTY_CHOICE, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}))
#vcn_number = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), )
    