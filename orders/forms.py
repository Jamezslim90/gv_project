from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'country', 'state', 'city', 'pin_code']
        

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
                
        self.fields["first_name"].widget.attrs.update(
            {
                'type': 'text',
                'class' : 'form-control',
                'placeholder' : 'first name'
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {
                'type': 'text',
                'class' : 'form-control',
                'placeholder' : 'last name'
            }
        )
        self.fields["phone"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : 'phone number' 
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                'type': 'text',
                'class' : 'form-control',
                'placeholder' : 'email'
            }
        )
        self.fields["address"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : 'address' 
            }
        )
        self.fields["country"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : 'country' 
            }
        )
        self.fields["state"].widget.attrs.update(
            {
             'type': 'password',
             'class' : 'form-control',
             'placeholder' : 'state' 
            }
        )
        self.fields["city"].widget.attrs.update(
             {
              'type': 'password',
              'class' : 'form-control',
              'placeholder' : 'city' 
             }
         )
        self.fields["pin_code"].widget.attrs.update(
             {
              'type': 'password',
              'class' : 'form-control',
              'placeholder' : 'pin code' 
             }
         )
     
    