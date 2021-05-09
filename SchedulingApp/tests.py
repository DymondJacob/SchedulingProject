from django.test import TestCase, Client
from django.urls import reverse, resolve
from SchedulingApp.views import *
from SchedulingApp.models import MyUser, Course

# Create your tests here.

# Create your tests here.
class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('login')
        self.name = "Jacob Dymond"
        self.password = "skater1234"
        self.email = "dymondjacob@gmail.com"
        self.user_type = "AD"


        self.instructor_name = "Troy"
        self.instructor_email = "troy@gmail.com"
        self.instructor_password = "troy"
        self.instructor_user_type = "IN"

        self.ta_name = "Sungwoong"
        self.ta_email = "sungwoong@gmail.com"
        self.ta_password = "sungwoong"
        self.ta_user_type = "TA"

    def test_url(self):
        self.assertEquals(resolve(self.home_url).func.view_class, loginView)

    def test_login_get(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200, msg="GET Request to Login Failed")
        self.assertTemplateUsed(response, 'login.html', msg_prefix="Wrong Template was Rendered for Login")

    def test_admin_login_post(self):
        MyUser.objects.create(name=self.name, password=self.password, email=self.email, user_type=self.user_type )
        response = self.client.post(self.home_url, {'email': self.email, 'pw': self.password}, follow=True)
        self.assertEquals(response.status_code, 200, msg="GET Request to Admin Home Page Failed")

        existingUser = MyUser.objects.get(email=self.email)
        self.assertEquals(existingUser.password, self.password, msg="Passwords do not match from database")

    def test_instructor_login_post(self):
        MyUser.objects.create(name=self.instructor_name, password=self.instructor_password, email=self.instructor_email, user_type=self.instructor_user_type )
        response = self.client.post(self.home_url, {'email': self.instructor_email, 'pw': self.instructor_password}, follow=True)
        self.assertEquals(response.status_code, 200, msg="GET Request to Instructor Home Page Failed")

        existingUser = MyUser.objects.get(email=self.instructor_email)

        self.assertEquals(existingUser.password, self.instructor_password, msg="Passwords do not match from database")

    def test_ta_login_post(self):
        MyUser.objects.create(name=self.ta_name, password=self.ta_password,
                              email=self.ta_email, user_type=self.ta_user_type)
        response = self.client.post(self.home_url, {'email': self.ta_email, 'pw': self.ta_password},
                                    follow=True)
        self.assertEquals(response.status_code, 200, msg="GET Request to TA Home Page Failed")

        existingUser = MyUser.objects.get(email=self.ta_email)
        self.assertEquals(existingUser.password, self.ta_password, msg="Passwords do not match from database")


    def test_login_form_name_field(self):
        response = self.client.get(self.home_url)
        print(response)
        self.assertContains(response, '<input class="form-input" id="login_email" name="email" type="text" placeholder="email">',
                            status_code=200, msg_prefix="Login Page does not contain email field")

    def test_login_form_password_field(self):
        response = self.client.get(self.home_url)
        self.assertContains(response, '<input class="form-input" id="login_pw" name="pw" type="password" placeholder="password">',
                            status_code=200, msg_prefix="Login Page does not contain password field")

    def test_login_form_submit_button(self):
        response = self.client.get(self.home_url)
        self.assertContains(response, '<input class="button action-button" type="submit" value="login">',
                            status_code=200,  msg_prefix="Home Page does not contain submit field")
    def test_login(self):
        MyUser.objects.create(password=self.password, email=self.email)
        test_user = MyUser.objects.get(email=self.email)
        self.assertEquals(test_user.password, self.password, msg="Wrong Password")


class AdminMainView(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["user_type"] = "AD"
        session.save()
        self.url = reverse('admin-homepage')

    def test_admin_main_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200, msg="GET Request to Admin Home Page Failed")
        self.assertTemplateUsed(response, 'admin-homepage.html', msg_prefix="Wrong Template was Rendered for Login")


    def test_create_account_link(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<a href="createaccount.html">',
                            status_code=200, msg_prefix="Admin Home Page does not contain create account link")
    def test_create_course_link(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<a href="createcourse.html">',
                            status_code=200, msg_prefix="Admin Home Page does not contain create course link")



class CreateCourse(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["user_type"] = "AD"
        session.save()
        self.url = reverse('createcourse')
        self.name = "Jacob"
        self.subject = "Mathematical Sciences"
        self.course_number = "123"
        self.section_instructor = "Troy"
        self.section_ta = "Sungwoong"
        self.lab_instructor = "Troy"
        self.lab_ta = "Sungwoong"


    def test_create_course_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200, msg="GET Request to CreateCourse Failed")
        self.assertTemplateUsed(response, 'createcourse.html', msg_prefix="Wrong Template was Rendered for Login")

    def test_create_course_post(self):
        response = self.client.post(self.url, {'name': self.name, 'select-subject': self.subject, 'course_number': self.course_number,
                                               'section-instructor': self.section_instructor, 'section-ta': self.section_ta,
                                               'lab-instructor': self.lab_instructor, 'lab-ta': self.lab_ta})
        self.assertEquals(response.status_code, 200, msg="GET Request to CreateCourse Failed")

    def test_subject_button(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<select name="select-subject" id="select-subject">',
                            status_code=200, msg_prefix="Create Course does not contain subject select button")

    def test_course_name_field(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input class="form-input" id="create_id" name="name" type="text" placeholder="course name">',
                        status_code=200, msg_prefix="Create Course does not contain course name input")
    def test_course_number_field(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input class="form-input" id="create_pw" name="course_number" type="text" placeholder="course number">',
                        status_code=200, msg_prefix="Create Course does not contain course number input")


class CreateAccount(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["user_type"] = "AD"
        session.save()
        self.url = reverse('createaccount')
        self.email = "bob@gmail.com"
        self.name = "Bob"
        self.password = "bob"
        self.status = 'AD'

    def test_create_account_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200, msg="GET Request to CreateCourse Failed")
        self.assertTemplateUsed(response, 'createaccount.html', msg_prefix="Wrong Template was Rendered for Create Account")

    def test_create_account_post(self):
        response = self.client.post(self.url, {'email': self.email, 'pw': self.password, 'name': self.name, 'user_type': self.status},
                                    follow=True)
        newAccount = MyUser.objects.get(email=self.email)
        self.assertEquals(newAccount.password, self.password, msg="Passwords do not match from database")
        self.assertEquals(response.status_code, 200, msg="Request Failed")

    def test_create_account_form(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<form action="/createaccount.html" method="post">',
                            status_code=200, msg_prefix="Create Account does not contain form")

    def test_create_name_field(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input class="form-input" id="create_id" name="name" type="text" placeholder="username">',
                        status_code=200, msg_prefix="Create Account does not contain course name input")
    def test_create_email_field(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input class="form-input" id="create_email" name="email" type="email" placeholder="email">',
                        status_code=200, msg_prefix="Create Account does not contain course email input")
    def test_create_password_field(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input class="form-input" id="create_pw" name="pw" type="text" placeholder="password">',
                        status_code=200, msg_prefix="Create Account does not contain course password input")


class InstructorPage(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["user_type"] = "IN"
        session.save()
        self.url = reverse('instructor-homepage')

    def test_instructor_page(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200, msg="GET Request to CreateCourse Failed")
        self.assertTemplateUsed(response, 'instructor-homepage.html', msg_prefix="Wrong Template was Rendered for Create Account")

    def test_instructor_planner(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<div class="header-title">UWM Instructor Planner</div>',
                            status_code=200, msg_prefix="Instructor Planner HTML is on incorrect page")

    # def test_view_assignments(self):
    #     response = self.client.get(self.url)
    #     self.assertContains(response, '<a href="viewassignments.html">',
    #                     status_code=200, msg_prefix="Create Account does not contain view assignment input")
    # def test_add_section(self):
    #     response = self.client.get(self.url)
    #     self.assertContains(response, '<a href="addsection.html">',
    #                     status_code=200, msg_prefix="Create Account does not contain add course section link")
    def test_find_course(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<a href="allcourses.html">',
                        status_code=200, msg_prefix="Create Account does not contain find course link")

    def test_log_out(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<a href="/" class="button logout-button">Log Out</a>',
                            status_code=200, msg_prefix="Instructor Planner doesn't contain logout")

class TAPage(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session["user_type"] = "TA"
        session.save()
        self.url = reverse('ta-homepage')

    def test_ta_homepage_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200, msg="GET Request to CreateCourse Failed")
        self.assertTemplateUsed(response, 'ta-homepage.html', msg_prefix="Wrong Template was Rendered for TA Input")

    def test_ta_planner(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<div class="header-title">UWM TA Planner</div>',
                            status_code=200, msg_prefix="TA Planner HTML is on incorrect page")

    def test_view_assignments(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<a href="viewassignments.html">',
                        status_code=200, msg_prefix="TA Planner does not contain view assignment link")
    def test_log_out(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<a href="/" class="button logout-button">Log Out</a>',
                        status_code=200, msg_prefix="TA Planner doesn't contain logout")
