from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import EmployeeInvite, User


class CustomerRegistrationForm(UserCreationForm):
    
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make all normal account registration fields mandatory.
       
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
