from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator


class UserForm(forms.ModelForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self). __init__(*args, **kwargs)
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
        self.fields["email"].widget.attrs.update(
            {
             'type': 'email',
             'class' : 'form-control',
             'placeholder' : 'email' 
            }
        )
        self.fields["username"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : 'username' 
            }
        )
        self.fields["password"].widget.attrs.update(
            {
             'type': 'password',
             'class' : 'form-control',
             'placeholder' : 'password' 
            }
        )
        self.fields["confirm_password"].widget.attrs.update(
             {
              'type': 'password',
              'class' : 'form-control',
              'placeholder' : 'confirm password' 
             }
         )
    
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )



class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'custom-file custom-file-input'}), validators=[allow_only_images_validator])
    
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'phone_number', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
                
        self.fields["profile_picture"].widget.attrs.update(
            {
             'type': 'file',
             'class' : 'form-control',
             
            }
        )
        self.fields["phone_number"].widget.attrs.update(
            {
             'type': 'text',
             'class' : 'form-control',
             'placeholder' : 'phone number' 
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
        self.fields["latitude"].widget.attrs.update(
             {
              'type': 'password',
              'class' : 'form-control',
              'placeholder' : 'latitude' 
             }
         )
        self.fields["longitude"].widget.attrs.update(
             {
              'type': 'password',
              'class' : 'form-control',
              'placeholder' : 'longitude' 
             }
         )
    
    
    