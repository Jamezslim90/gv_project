from django import forms
from .models import Doctor, AnimalSpecialty, OpeningHour, BankAccount
from .models import Meeting
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
        
class MeetingForm(forms.ModelForm):
    
     
    def __init__(self, *args, **kwargs):
        super(MeetingForm, self). __init__(*args, **kwargs)
        self.fields["customer_email"].widget.attrs.update(
            {
             'type': 'email',
             'class' : 'form-control',
            # 'placeholder' : 'client email',
              'required': 'false'
            }
        )
        self.fields["zoom_email"].widget.attrs.update(
            {
             'type': 'email',
             'class' : 'form-control',
            # 'placeholder' : 'client email',
              'required': 'true'
            }
        )
        self.fields["date"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : 'yyyy-mm-dd',
              'required': 'false'
            }
        )
        self.fields["time"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : 'hh:mm:ss',
              'required': 'true'
            }
        )
        
        
    class Meta:
        model = Meeting
        fields = ['topic','zoom_email','customer_email', 'duration', 'date','time', 'passcode']
        widgets={
            'date': forms.DateInput(attrs={'class': 'form-control','type': 'text'}, format='%Y-%m-%d'),
            'time': forms.TimeInput(attrs={'class': 'form-control','type': 'text'}, format='%H:%M:%S'),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            #'customer_email': forms.EmailField(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'passcode': forms.TextInput(attrs={'class': 'form-control'}),
            
     }
    