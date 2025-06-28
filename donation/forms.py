from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Donation
from .models import ContactMessage

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['food_type', 'quantity', 'address']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),

        }


class ContactReplyForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['reply_content']
        widgets = {
            'reply_content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your reply here...'}),
        }        