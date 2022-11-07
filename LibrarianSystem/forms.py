from django import forms

class signupForm(forms.Form):
    first_name = forms.CharField(label='First Name', required=True ,max_length=200, 
    help_text='Please enter the first name of the person registering', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Last Name', required=True, max_length=200, 
    help_text='Please enter the last name of the person registering', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='User Email', required=True, max_length=200, 
    help_text='Please enter the email of the person registering', widget=forms.TextInput(attrs={'class':'form-control'}))