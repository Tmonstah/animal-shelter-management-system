from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import EmployeeProfile, CustomerProfile, EmployeeInvite, User


class CustomerProfileForm(forms.ModelForm):
    # Form used by customers to create or update their profile information.
    class Meta:
        model = CustomerProfile
        fields = (
            "phone_number",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
        )

class EmployeeProfileForm(forms.ModelForm): #Employee form to creat update Metadata
    class Meta:
        model = EmployeeProfile
        fields = (
            "phone_number",
            "employee_id",
            "job_title",
            "department",
            "hire_date",
        )

class CustomerRegistrationForm(UserCreationForm):
    required_css_class = "required"
    employee_invite_code = forms.CharField(
        max_length=20,
        required=False,
        label="Employee Invite Code (Employee only)",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "employee_invite_code",
        )
        widgets = {
            'email': forms.TextInput(
                attrs={'placeholder': 'e.g, abc123@gmail.com'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make all fields mandatory to proceed
        self.fields["username"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True
        self.fields["password1"].required = True
        self.fields["password2"].required = True


    # Optional invite code for customers but verification for employees

    def clean_employee_invite_code(self):
        invite_code = self.cleaned_data.get("employee_invite_code")
        
        if not invite_code:
            return invite_code

        try:
            employee_invite = EmployeeInvite.objects.get(
                invite_code=invite_code,
                is_used=False,
            )
        except EmployeeInvite.DoesNotExist:
            raise forms.ValidationError(
                "Invalid Code or Expired Code."
            )

        # Make sure the invite belongs to the same email used during registration.
        registration_email = self.cleaned_data.get("email")

        if employee_invite.email.lower() != registration_email.lower():
            raise forms.ValidationError(
                "Invalid Code, Does not match email on file."
            )

        return invite_code

# This form allows user to fill out
class ProfileRegistrationForm(forms.Form):
    required_css_class = "required"
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        validators= [
            RegexValidator(
                regex='^\+[1-9]\d{1,14}$',
                message="Enter a phone number in the format +11231234567.",
                code="invalid_registration",
            ),
        ],
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g, +11231234567, includes country code'}
        ),
        label= "Phone Number",
    )
    address_line_1 = forms.CharField(
        max_length=150, 
        required=True,
        label="Address Line 1",
        widget=forms.TextInput(
            attrs={'placeholder': 'Street address (e.g, 123 Orange St)'}
        ),
    )
    address_line_2 = forms.CharField(
        max_length=150,
        required=False, 
        label="Address Line 2 (Optional)",
        widget=forms.TextInput(
            attrs={'placeholder': 'Apartment, suite, unit, building, etc.'}
        ),
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        label="City",
        widget=forms.TextInput(
            attrs={'placeholder': 'City'}
        ),
    )
    state = forms.CharField(
        max_length=100,
        required=True,
        label="State",
        widget=forms.TextInput(
            attrs={'placeholder': 'State'}
        ),
    )
    postal_code = forms.CharField(
        max_length=20,
        required=True,
        label="Zip Code",
        widget=forms.TextInput(
            attrs={'placeholder': 'Zip Code'}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
