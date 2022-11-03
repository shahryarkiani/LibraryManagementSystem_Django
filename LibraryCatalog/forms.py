from django import forms

class searchForm(forms.Form):
    searchParam = forms.CharField(label='Search Books', max_length=200)
    