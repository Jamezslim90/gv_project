from django import forms
from .models import Animal, Appointment, Category, AnimalType, Symptom
from asgiref.sync import sync_to_async
class AnimalForm(forms.ModelForm):
    animal_category = forms.ModelChoiceField(queryset=Category.objects.all())
    animal = forms.ModelChoiceField(queryset=AnimalType.objects.all())

    class Meta:
        model = Animal
        fields = ['name', 'animal_category', 'animal', 'dob', 'profile_pic', 'breed', 'weight']
        

    def __init__(self, *args, **kwargs):
        super(AnimalForm, self).__init__(*args, **kwargs)
       
        self.fields["profile_pic"].widget.attrs.update(
            {
             'type': 'file',
             'class' : 'form-control',
             
            }
        )
        self.fields["name"].widget.attrs.update(
            {
                'type': 'text',
                'class' : 'form-control',
                'placeholder' : ''
            }
        )
        self.fields["animal_category"].widget.attrs.update(
            {
             'type': 'select',
             'class' : 'form-control',
             'placeholder' : '' 
            }
        )
        self.fields["animal"].widget.attrs.update(
            {
             'type': 'select',
             'class' : 'form-control',
             'placeholder' : '' 
            }
        )
        self.fields["dob"].widget.attrs.update(
            {
             'type': 'date',
             'class' : 'form-control',
             'placeholder' : 'dd/mm/yyyy' 
            }
        )
        self.fields["breed"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : '' 
            }
        )
        self.fields["weight"].widget.attrs.update(
             {
              'type': 'text',
              'class' : 'form-control',
              'placeholder' : '' 
             }
         )
        


class AppointmentForm(forms.ModelForm):   
        
    animal_category = forms.ModelChoiceField(queryset=Category.objects.all())
    animal = forms.ModelChoiceField(queryset=AnimalType.objects.all())
    symptoms = forms.SelectMultiple(choices=[])
   
    
    class Meta:
        model = Appointment
        fields = [ 'animal_category', 'animal', 'symptoms', 'date', 'time', 'optional_message']
        widgets={
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'animal_category': forms.Select(attrs={'class': 'form-control'}),
            'animal': forms.Select(attrs={'class': 'form-control'}),
            'symptoms': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'optional_message': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['symptoms'].choices = sync_to_async(Symptom.objects.all())()
        # self.fields["profile_pic"].widget.attrs.update(
        #     {
        #      'type': 'file',
        #      'class' : 'form-control',
             
        #     }
        # )
        # self.fields["name"].widget.attrs.update(
        #     {
        #         'type': 'text',
        #         'class' : 'form-control',
        #         'placeholder' : ''
        #     }
        # )
        # self.fields["animal_category"].widget.attrs.update(
        #     {
        #      'type': 'select',
        #      'class' : 'form-control',
        #      'placeholder' : '' 
        #     }
        # )
        # self.fields["animal"].widget.attrs.update(
        #     {
        #      'type': 'select',
        #      'class' : 'form-control',
        #      'placeholder' : '' 
        #     }
        # )
        self.fields["dob"].widget.attrs.update(
            {
             'type': 'date',
             'class' : 'form-control',
             'placeholder' : 'yyyy-mm-dd' 
            }
        )
        # self.fields["breed"].widget.attrs.update(
        #     {
        #      'type': 'text',
        #      'class' : 'form-control',
        #      'placeholder' : '' 
        #     }
        # )
        # self.fields["weight"].widget.attrs.update(
        #      {
        #       'type': 'text',
        #       'class' : 'form-control',
        #       'placeholder' : '' 
        #      }
        #  )
                                                                           
        
        