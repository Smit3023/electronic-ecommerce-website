from django import forms
from .models import ContactU, JoinU

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactU
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'subject', 'message']
        widgets = {
            'first_name':   forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name':    forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'email':        forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'subject':      forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}),
            'message':      forms.Textarea(attrs={'placeholder': 'Your Message', 'class': 'form-control', 'rows': 5}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) < 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone


class JoinForm(forms.ModelForm):
    class Meta:
        model = JoinU
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'resume']
        widgets = {
            'first_name':   forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name':    forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'email':        forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            ext = resume.name.split('.')[-1].lower()
            if ext not in ['pdf', 'doc', 'docx']:
                raise forms.ValidationError("Only PDF, DOC, DOCX files are allowed.")
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 5 MB.")
        return resume