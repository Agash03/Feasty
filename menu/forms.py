from .models import *
from django import forms

class NVForm(forms.ModelForm):
    
    class Meta:
        model = NonVegMenu
        fields ='__all__'
        
        widgets ={
             'name':forms.TextInput(attrs={'class':'form-control'}),
             'description' : forms.Textarea(attrs={'class':'form-control'}),
             'price' : forms.NumberInput(attrs={'class':'form-control'}),
             'picture' : forms.FileInput(attrs={'class':'form-control'}),  
             'food_type': forms.Select(attrs={'class': 'form-control '}),
        }
        
class VegForm(forms.ModelForm):
    class Meta:
        model = VegMenu
        fields ='__all__'
        
        widgets ={
             'name':forms.TextInput(attrs={'class':'form-control'}),
             'description' : forms.Textarea(attrs={'class':'form-control'}),
             'price' : forms.NumberInput(attrs={'class':'form-control'}),
             'picture' : forms.FileInput(attrs={'class':'form-control'}),
             'food_type': forms.Select(attrs={'class': 'form-control stylish-dropdown'}),        
        }

class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ("street","address_line_1","address_line_2","state")
        
        CHOICES = [
            ('Select State', 'Select State'),
            ('Kerala', 'Kerala'),
            ('Tamil Nadu', 'Tamil Nadu'),
            ('Karnataka', 'Karnataka')
        ]
        
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}),
            'state': forms.Select(choices=CHOICES, attrs={'class': 'form-control stylish-dropdown'}),
        }
