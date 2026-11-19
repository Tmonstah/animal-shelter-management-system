from django.test import TestCase
from accounts.models import CustomerProfile, EmployeeInvite, EmployeeAccessRequest, generate_invite_code, User
from accounts.forms import CustomerRegistrationForm
from accounts.admin import EmployeeAccessRequestAdmin
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

#*****************************************TESTING THE MODELS ***************************

# Test the CustomerProfile Model
class customer_profile_test (TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username= "testuser1",
            email= "testuser1@gmail.com",
            password= "TestUser1Pass",
        )
    # Tests valid customer profile
    def test_valid_profile (self):
        self.customer = CustomerProfile.objects.create(
            user= self.user,
            phone_number= "+12781234567",
            address_line_1= "123 Home St",
            address_line_2= "apt 7",
            city= "Irving",
            state= "Texas",
            postal_code= "75060"
        )
        cust = CustomerProfile.objects.get(user= self.user)
        self.assertIsNotNone(cust)

    # Test an invalid phone number
    def test_invalid_phone_num (self):
        with self.assertRaises(ValidationError):
            self.customer = CustomerProfile.objects.create(
                user= self.user,
                phone_number= "+1(278) 123-4567",
                address_line_1= "123 Home St",
                address_line_2= "apt 7",
                city= "Irving",
                state= "Texas",
                postal_code= "75060"
            )
            self.customer.full_clean()
        
#---------------------------------------------------------------
# Test the Employee Invite class model
class employee_invite_test (TestCase):
    def setUp(self):
        EmployeeInvite.objects.create(
            email = "abc1234@gmail.com",
            invite_code = generate_invite_code(),
            is_used = False,
        )
    # Tests whether a duplicate email causes issues.
    def test_duplicate_emails (self):
        with self.assertRaises(IntegrityError):
            EmployeeInvite.objects.create(
            email = "abc1234@gmail.com",
            invite_code = generate_invite_code(),
            is_used = False,
            )
    # Tests whether code only accepts proper email
    def test_not_email (self):
        emp =EmployeeInvite.objects.create(
            email = "abc1234gmailcom",
            invite_code = generate_invite_code(),
            is_used = False,
        )
        # Django does not necessarily check the email, but it 
        #   will with full_clean()
        with self.assertRaises(ValidationError):
            emp.full_clean()
    # Verify the results of creating an employee invite
    def test_create_invite (self):
        emp = EmployeeInvite.objects.create(
            email = "newEmail@gmail.com",
            invite_code = generate_invite_code(),
            is_used = False,
            )
        self.assertEqual(emp.email, 'newEmail@gmail.com')
        self.assertFalse(emp.invite_code is None or emp.invite_code == "")

#----------------------------------------------------------------
# Test the EmployeeAccessRequest class model
class employee_access_request_test (TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser1",
            email="testuser1@gmail.com",
            password="TestUser1Pass",
        )
        self.invite = EmployeeInvite.objects.create(
                    email = "abc1234@gmail.com",
                    invite_code = generate_invite_code(),
                    is_used = False,
        )
        self.emp_access_req = EmployeeAccessRequest.objects.create(
            user = self.user,
            invite = self.invite,
        )
    # Tests that the model properly links user and EmployeeAccessRequest user.
    # also EmployeeInvite and EmployeeAccessRequest invite
    def test_one_to_one_linkage(self):
        self.assertEqual(
            self.user, self.emp_access_req.user
        )
        self.assertEqual(
            self.invite, self.emp_access_req.invite
            )

    # Test that when deleting, model cascades the deletion properly
    def test_cascade_deletion(self):
        user1 = self.emp_access_req.user
        self.user.delete()
        self.user.save()
        self.assertFalse(
            EmployeeAccessRequest.objects.filter(user=user1).exists()
        )




#***************************************** TESTING THE FORMS ***************************
class customer_registration_form_test(TestCase):
    # Test valid input
    def test_valid_inputs(self):
            # Invalid username => empty
            register_form = CustomerRegistrationForm(
                data={
                    "username": "user1",
                    "first_name": "Userfirst",
                    "last_name": "Userlast",
                    "email": "user123@gmail.com",
                    "password1": "abcPass2",
                    "password2": "abcPass2",
                    "employee_invite_code": "",
                })
            self.assertTrue(register_form.is_valid())
    # Test invalid input types
    def test_invalid_input_1(self):
        # Invalid username => empty
        register_form = CustomerRegistrationForm(
            data={
                "username": "",
                "first_name": "Userfirst",
                "last_name": "Userlast",
                "email": "user123@gmail.com",
                "password1": "abcPass2",
                "password2": "abcPass2",
                "employee_invite_code": "",
            })
        self.assertFalse(register_form.is_valid())
    def test_invalid_input_2(self):
        # Invalid first name, space
        register_form = CustomerRegistrationForm(
            data={
                "username": "user123",
                "first_name": " ",
                "last_name": "Userlast",
                "email": "user123@gmail.com",
                "password1": "abcPass2",
                "password2": "abcPass2",
                "employee_invite_code": "",
            })
        self.assertFalse(register_form.is_valid())
    def test_invalid_input_3(self):
        # Invalid lastname
        register_form = CustomerRegistrationForm(
            data={
                "username": "user123",
                "first_name": "Userfirst",
                "last_name": "",
                "email": "user123@gmail.com",
                "password1": "abcPass2",
                "password2": "abcPass2",
                "employee_invite_code": "",
            })
        self.assertFalse(register_form.is_valid())
    def test_invalid_input_4(self):
        # Bad email
        register_form = CustomerRegistrationForm(
            data={
                "username": "user123",
                "first_name": "Userfirst",
                "last_name": "Userlast",
                "email": "user123.com",
                "password1": "abcPass2",
                "password2": "abcPass2",
                "employee_invite_code": "",
            })
        self.assertFalse(register_form.is_valid())
    def test_invalid_input_5(self):
        #  Missing Password
        register_form = CustomerRegistrationForm(
            data={
                "username": "user123",
                "first_name": "Userfirst",
                "last_name": "Userlast",
                "email": "user123@gmail.com",
                "password1": "",
                "password2": "abcPass2",
                "employee_invite_code": "",
            })
        self.assertFalse(register_form.is_valid())
    def test_invalid_input_6(self):
        # Different Passwords
        register_form = CustomerRegistrationForm(
            data={
                "username": "user123",
                "first_name": "Userfirst",
                "last_name": "Userlast",
                "email": "user123@gmail.com",
                "password1": "abcPass",
                "password2": "abcPass2",
                "employee_invite_code": "",
            })
        self.assertFalse(register_form.is_valid())
        #print(register_form.errors) #can use this to see what the error was

    # No employee codes have been made, test if it catches it
    def test_invalid_invite_code(self):
        register_form = CustomerRegistrationForm(
            data={
                "username": "user123",
                "first_name": "Userfirst",
                "last_name": "Userlast",
                "email": "user123@gmail.com",
                "password1": "abcPass2",
                "password2": "abcPass2",
                "employee_invite_code": "qr723",
            })
        result = register_form.is_valid()
        self.assertFalse(result)
        # Check if Invalid Code is found in any part of error
        #   pertaining to employee_invite_code
        self.assertIn(
            "Invalid Code",
            register_form.errors["employee_invite_code"][0]
        )

    # Test if code does not match email
    def test_invalid_email_code(self):
        self.invite = EmployeeInvite.objects.create(
                    email = "abc1234@gmail.com",
                    invite_code = generate_invite_code(),
                    is_used = False,
        )
        invite_code = str(self.invite.invite_code)
        register_form = CustomerRegistrationForm(
            data={
                "username": "user123",
                "first_name": "Userfirst",
                "last_name": "Userlast",
                "email": "user123@gmail.com",
                "password1": "abcPass2",
                "password2": "abcPass2",
                "employee_invite_code": invite_code,
            })
        result = register_form.is_valid()
        self.assertFalse(result)
        self.assertIn(
            "Does not match email",
            register_form.errors["employee_invite_code"][0]
        )
        
    # Test a valid employee code
    def test_valid_email_code(self):
        self.invite = EmployeeInvite.objects.create(
                    email = "abc1234@gmail.com",
                    invite_code = generate_invite_code(),
                    is_used = False,
        )
        invite_code = str(self.invite.invite_code)
        register_form = CustomerRegistrationForm(
            data={
                "username": "user123",
                "first_name": "Userfirst",
                "last_name": "Userlast",
                "email": "abc1234@gmail.com",
                "password1": "abcPass2",
                "password2": "abcPass2",
                "employee_invite_code": invite_code,
            })
        result = register_form.is_valid()
        self.assertTrue(result)

#---------------------------------------------------------------------
#***************************************** TESTING THE Views ***************************
# Testing all Views related to the Customer
class customer_views_test (TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username= "testuser1",
            email= "testuser1@gmail.com",
            password= "TestUser1Pass",
        )
        self.customer = CustomerProfile.objects.create(
            user= self.user,
            phone_number= "+12781234567",
            address_line_1= "123 Home St",
            address_line_2= "apt 7",
            city= "Irving",
            state= "Texas",
            postal_code= "75060"
        )
        
    #Test correct page when logged in
    def test_customerprofile_response_logged_in (self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("customer_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/customer_profile.html")

    def test_customer_dashboard_response_logged_in (self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("customer_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/customer_dashboard.html")

    #Test it redirects to login page, if not signed in
    def test_customerprofile_response_logged_out (self):
        response = self.client.get(reverse("customer_profile"))
        self.assertRedirects(response, "/login/?next=/customer/profile/")

    def test_customer_dashboard_response_logged_out(self):
        response = self.client.get(reverse("customer_dashboard"))
        self.assertRedirects(response, "/login/?next=/customer/dashboard/")

# Testing all Views related to the employee
class employee_views_test (TestCase):
    def setUp(self):
        self.super_user = User.objects.create_superuser(
            username="super123",
            email="super123@gmail.com",
            password="mysuperPass123",
        )
        self.invite = EmployeeInvite.objects.create(
            email = "abc1234@gmail.com",
            invite_code = generate_invite_code(),
            is_used = False,
        )
        invite_code = str(self.invite.invite_code)
        # Have new employee register

        data = {
            "username": "user123",
            "first_name": "Userfirst",
            "last_name": "Userlast",
            "email": "abc1234@gmail.com",
            "password1": "abcPass2",
            "password2": "abcPass2",
            "employee_invite_code": invite_code,
            "phone_number": "+12345671427",
            "address_line_1": "123 Random St",
            "city": "Arlington",
            "state": "Texas",
            "postal_code": "75060"
        }
        # Submit form
        url = reverse("register_customer")
        resp = self.client.post(url, data)
        # Verify status
        self.assertTrue(resp.status_code, 200) 
        # Verify object was created properly
        self.pendingEmp = EmployeeAccessRequest.objects.get(invite=self.invite.id)
        self.assertEqual(self.pendingEmp.status, "pending")
        # As super user, approve the employee requests
        self.client.force_login(self.super_user)
        url = reverse("admin:accounts_employeeaccessrequest_changelist")
        data = {
            "action": "approve_employee_requests",
            "_selected_action": [self.pendingEmp.pk],
        }
        resp = self.client.post(url, data)
        # Get user info for logging in
        self.user = self.pendingEmp.user

        self.client.logout()

        
    #Test correct page when logged in
    def test_employeeprofile_response_logged_in (self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("employee_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/employee_profile.html")

    def test_employee_dashboard_response_logged_in (self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("employee_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/employee_dashboard.html")

    #Test it redirects to login page, if not signed in
    def test_employeeprofile_response_logged_out (self):
        response = self.client.get(reverse("employee_profile"))
        self.assertRedirects(response, "/login/?next=/employee/profile/")

    def test_employee_dashboard_response_logged_out (self):
        response = self.client.get(reverse("employee_dashboard"))
        self.assertRedirects(response, "/login/?next=/employee/dashboard/")

class login_logout_view_test(TestCase):
    # Test the login and logout views to verify the show up
    def setUp(self):
        self.user = User.objects.create(
            username= "testuser1",
            email= "testuser1@gmail.com",
            password= "TestUser1Pass",
        )
        self.customer = CustomerProfile.objects.create(
            user= self.user,
            phone_number= "+12781234567",
            address_line_1= "123 Home St",
            address_line_2= "apt 7",
            city= "Irving",
            state= "Texas",
            postal_code= "75060"
        )
    def test_login_page (self):
            response = self.client.get(reverse("login"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_page (self):
            self.client.force_login(self.user)
            response = self.client.get(reverse("login"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "accounts/login.html")

#************************************* TESTING THE ADMIN CODE ***************************
class employee_access_request_admin_test(TestCase):
    def setUp(self):
        self.super_user = User.objects.create_superuser(
            username="super123",
            email="super123@gmail.com",
            password="mysuperPass123",
        )

    # Test that a normal user cannot access to admin page
    def test_invalid_admin(self):
        # Create a new user account
        self.normal_user = User.objects.create_user(
            username="normal123",
            email="normal123@gmail.com",
            password="myNormalPass123",  
        )
        # Login
        self.client.force_login(self.normal_user)
        #Create a url based on one of the registered andmin models
        url = reverse("admin:accounts_employeeaccessrequest_changelist") # NO CAPITALIZATION!!!
        result = self.client.get(url)
        self.assertEqual(result.status_code, 302)

    # Test new superuser can access to admin page
    def test_valid_admin(self):
        # Login
        self.client.force_login(self.super_user)
        # Create a url based on one of the registered andmin models
        url = reverse("admin:accounts_employeeaccessrequest_changelist") # NO CAPITALIZATION!!!
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

    # Test approve_employee_requests properly makes user a staff
    def test_approve_employee_requests(self):
        # Create a valid employee code
        self.invite = EmployeeInvite.objects.create(
            email = "abc1234@gmail.com",
            invite_code = generate_invite_code(),
            is_used = False,
        )
        invite_code = str(self.invite.invite_code)
        # Have new employee register

        data = {
            "username": "user123",
            "first_name": "Userfirst",
            "last_name": "Userlast",
            "email": "abc1234@gmail.com",
            "password1": "abcPass2",
            "password2": "abcPass2",
            "employee_invite_code": invite_code,
            "phone_number": "+12345671427",
            "address_line_1": "123 Random St",
            "city": "Arlington",
            "state": "Texas",
            "postal_code": "75060"
        }
        # Submit form
        url = reverse("register_customer")
        resp = self.client.post(url, data)
        # Verify status
        self.assertTrue(resp.status_code, 200) 
        # Verify object was created properly
        self.pendingEmp = EmployeeAccessRequest.objects.get(invite=self.invite.id)
        self.assertEqual(self.pendingEmp.status, "pending")
        # As super user, approve the employee requests
        self.client.force_login(self.super_user)
        url = reverse("admin:accounts_employeeaccessrequest_changelist")
        data = {
            "action": "approve_employee_requests",
            "_selected_action": [self.pendingEmp.pk],
        }
        resp = self.client.post(url, data)
        # Verify user was approved:
        self.pendingEmp = EmployeeAccessRequest.objects.get(invite=self.invite.id)
        self.assertEqual(self.pendingEmp.status, "approved")
