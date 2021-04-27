from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q

from .models import MyUser, Course

class loginView(View):
    def get(self, request):
        print(request)
        return render(request, 'login.html', {})

    def post(self, request):
        pw = request.POST["pw"]
        email = request.POST["email"]
        print(request.POST)
        try:
            login_user = MyUser.objects.get(email=email, password=pw)
            print(login_user)


            if login_user == None:
                return render(request, 'login.html', {
                    "alert": True,
                    "message": "login failed."
                })
            elif login_user.email != email:
                return render(request, 'login.html', {
                    "alert": True,
                    "message": "login failed."
                })
            login_myuser = MyUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return render(request, 'login.html', {
                "alert": True,
                "message": "login failed."
            })
        request.session["name"] = login_myuser.name
        request.session["password"] = login_myuser.password
        request.session["email"] = login_myuser.email
        request.session["user_type"] = login_myuser.user_type
        print(request.session["name"])
        print(request.session["email"])
        print(request.session["password"])



        if login_myuser.user_type == 'AD':
            return redirect('admin-homepage.html')
        elif login_myuser.user_type == 'IN':
            return redirect('instructor-homepage.html')
        elif login_myuser.user_type == 'TA':
            return redirect('ta-homepage.html')
        else:
            return render(request, 'login.html', {
                "alert": True,
                "message": "login failed."
            })


class AdminMainView(View):
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'admin-homepage.html')


    def post(self, request):
        pw = request.POST["pw"]
        email = request.POST["email"]
        user_type = request.POST['']

        userExist = User.objects.filter(Q(email=email)).exists()

        if userExist:
            return render(request, 'createaccount.html', {
                "alert": True,
                "message": "이미 존재하는 id거나 email입니다",
            })
        else:
            newUser = MyUser.objects.create(password=pw, email=email)
            newUser.myuser.user_type = user_type
            newUser.save()
            return render(request, 'createaccount.html', {
                "alert": True,
                "message": "account created",
            })


class InstructorMainView(View):
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'instructor-homepage.html', {})


class TaMainView(View):
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'ta-homepage.html', {})


class CreateAccount(View):
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'createaccount.html', {})

    def post(self, request):
        name = request.POST['name']
        email = request.POST["email"]
        pw = request.POST["pw"]
        status = request.POST['user_type']
        print(request.POST)


        MyUser.objects.create(name=name, password=pw, email=email, user_type=status)
        return render(request, 'admin-homepage.html', {})


class CreateCourse(View):
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        obj = MyUser.objects.all()
        return render(request, 'createcourse.html', {"obj": obj})

    def post(self, request):
        name = request.POST['name']
        subject = request.POST['select-subject']
        course_number = request.POST['course_number']
        section_instructor = request.POST['section-instructor']
        section_ta = request.POST['section-ta']
        lab_instructor = request.POST['lab-instructor']
        lab_ta = request.POST['lab-ta']
        x = Course.objects.create(name=name, subject=subject, course_number=course_number, section_instructor=section_instructor,
        section_ta=section_ta, lab_instructor=lab_instructor, lab_ta=lab_ta)
        x.save()
        print(request.POST)
        return render(request, 'admin-homepage.html', {})


class CreateAssignment(View):

    def get(self, request):
        return render(request, 'createassignment.html', {})

class ViewAssignment(View):

    def get(self, request):
        return render(request, 'viewassignments.html', {})

class EditAssignment(View):

    def get(self, request):
        return render(request, 'editassignments.html', {})


class AddSection(View):

    def get(self, request):
        return render(request, 'addsection.html', {})

class AssignUser(View):

    def get(self, request):
        return render(request, 'assignuser.html', {})


class DeleteAccount(View):

    def get(self, request):
        return render(request, 'deleteaccount.html', {})


class DeleteCourse(View):

    def get(self, request):
        return render(request, 'deletecourse.html', {})

class DeleteSection(View):

    def get(self, request):
        return render(request, 'deletesection.html', {})

class EditAccount(View):

    def get(self, request):
        return render(request, 'editaccount.html', {})

class EditCourse(View):

    def get(self, request):
        return render(request, 'editcourse.html', {})


class EditRemoveUser(View):

    def get(self, request):
        return render(request, 'editremoveuser.html', {})


class EditSection(View):

    def get(self, request):
        return render(request, 'editsection.html', {})

class FindCourse(View):

    def get(self, request):
        return render(request, 'findcourse.html', {})

class FindUser(View):

    def get(self, request):
        return render(request, 'finduser.html', {})