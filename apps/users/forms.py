from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'address',
            'department', 'position', 'date_of_hire', 'emergency_contact_name',
            'emergency_contact_number', 'role', 'status'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        elif not user.pk:
            # Set a default password for new users if not provided
            user.set_password('hainna2026') 
            user.requires_password_change = True
        
        if not user.username:
            user.username = user.email.split('@')[0]
            
        if commit:
            user.save()
        return user
