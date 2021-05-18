from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import IntegrityError


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
    def get(self, request):
        if (request.session['user_type'] == 'IN'):
            return redirect('instructor-homepage.html', {
                "alert": True,
                "message": "You can't access this page"
            })
        elif (request.session['user_type'] == 'TA'):
            return redirect('ta-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        else:
            return render(request, 'admin-homepage.html', {'obj': request.session['name']})


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
    def get(self, request):
        if (request.session['user_type'] == 'AD'):
            return redirect('admin-homepage.html', {
                "alert": True,
                "message": "You can't access this page"
            })
        elif (request.session['user_type'] == 'TA'):
            return redirect('ta-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        else:
            return render(request, 'instructor-homepage.html',  {'obj': request.session['name']})


class TaMainView(View):
    def get(self, request):
        if (request.session['user_type'] == 'IN'):
            return redirect('instructor-homepage.html', {
                "alert": True,
                "message": "You can't access this page"
            })
        elif (request.session['user_type'] == 'AD'):
            return redirect('admin-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        else:
            print(request.session['name'])
            return render(request, 'ta-homepage.html', {'obj': request.session['name']})


class CreateAccount(View):
    def get(self, request):
        if (request.session['user_type'] == 'IN'):
            return redirect('instructor-homepage.html', {
                "alert": True,
                "message": "You can't access this page"
            })
        elif (request.session['user_type'] == 'TA'):
            return render('ta-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        else:
            return render(request, 'createaccount.html')

    def post(self, request):
        name = request.POST['name']
        email = request.POST["email"]
        pw = request.POST["pw"]
        status = request.POST['user_type']

        tryUser = MyUser.objects.filter(email=email).exists()

        if (tryUser == True):
            return redirect('createaccount.html', {
                "alert": True,
                "message": "Account exists already"
            })

        MyUser.objects.create(name=name, password=pw, email=email, user_type=status, ta_count=0)
        return redirect('admin-homepage.html', {
            "alert": True,
            "message": "Account created"
        })


class EditAccount(View):
    def get(self, request):
        if (request.session['user_type'] == 'IN'):
            return redirect('instructor-homepage.html', {
                "alert": True,
                "message": "You can't access this page"
            })
        elif (request.session['user_type'] == 'TA'):
            return redirect('ta-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        else:
            return render(request, 'editaccount.html')

    def post(self, request):
        print(request.POST)
        email = request.POST["email"]
        new_email = request.POST["new_email"]
        new_pw = request.POST["new_pw"]
        status = request.POST['user_type']
        tryUser = MyUser.objects.filter(email=email).exists()

        if (tryUser == False):
            return redirect('editaccount.html', {
                "alert": True,
                "message": "Account not found, please try again"
            })

        userExist = MyUser.objects.get(email=email)
        userExist.email = new_email
        userExist.password = new_pw
        userExist.user_type = status
        userExist.save()
        return render(request, 'editaccount.html')


class DeleteAccount(View):
    def get(self, request):
        if (request.session['user_type'] == 'IN'):
            return redirect('instructor-homepage.html', {
                "alert": True,
                "message": "You can't access this page"
            })
        elif (request.session['user_type'] == 'TA'):
            return redirect('ta-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        else:
            return render(request, 'deleteaccount.html')

    def post(self, request):
        print(request.POST)
        email = request.POST["email"]
        tryUser = MyUser.objects.filter(Q(email=email)).exists()
        if tryUser == False:
            return render(request, 'deleteaccount.html', {
                "alert": True,
                "message": "Account Not Found, try again"
            })

        userExist = MyUser.objects.get(email=email)
        userExist.delete()
        return render(request, 'deleteaccount.html', {
            "alert": True,
            "message": "Account Deleted"
        })


class CreateCourse(View):
    def get(self, request):
        if (request.session['user_type'] == 'IN'):
            return redirect('instructor-homepage.html', {
                "alert": True,
                "message": "You can't access this page"
            })
        elif (request.session['user_type'] == 'TA'):
            return redirect('ta-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        else:
            obj = MyUser.objects.all()
            return render(request, 'createcourse.html', {"obj": obj})

    def post(self, request):
        name = request.POST['name']
        subject = request.POST['select-subject']
        course_number = request.POST['course_number']
        section_instructor = request.POST['section-instructor']
        section_number = request.POST['section-number']
        x = Course.objects.create(name=name, subject=subject, course_number=course_number, section_instructor=section_instructor,
        section_number=section_number)
        x.save()
        print(request.POST)
        return render(request, 'admin-homepage.html', {})


class InstructorCourses(View):
    def get(self, request):
        if (request.session['user_type'] != 'IN'):
            return redirect('ta-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        else:
            obj = Course.objects.all()
            print(request.session['name'])
            return render(request, 'instructor-courses.html', {"obj": obj, 'name': request.session['name']})

class TaAssignments(View):
    def get(self, request):
        if (request.session['user_type'] != 'TA'):
            return redirect('instructor-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        else:
            obj = Course.objects.all()
            print(request.session['name'])
            for course in obj:
                print(course)
            return render(request, 'ta-assignments.html', {"obj": obj, 'name': request.session['name']})

class AllCourses(View):

    def get(self, request):
        obj = Course.objects.all()
        print(obj[0].name)
        return render(request, 'allcourses.html', {"obj": obj})


class EditCourse(View):

    def get(self, request):
        obj = Course.objects.all()
        print(obj[0].name)
        return render(request, 'editcourse.html', {"obj": obj})

    def post(self, request):
        print(request.POST)
        name = request.POST["course_name"]
        editCourse = Course.objects.get(name=name)
        if request.POST['edit_number'] != '':
            editCourse.course_number = request.POST['edit_number'][0]
        if request.POST['subject'] != '':
            editCourse.subject = request.POST['subject'][0]
        if request.POST['section-instructor'] != '':
            editCourse.section_instructor = request.POST['section-instructor']
        if request.POST['section-ta'] != '':
            editCourse.lab_ta = request.POST['section-ta'][0]
        if request.POST['section'] != '':
            editCourse.section_number = request.POST['section'][0]
        editCourse.save()
        obj = Course.objects.all()
        return render(request, 'editcourse.html', {'obj': obj})

class DeleteCourse(View):

    def get(self, request):
        obj = Course.objects.all()
        print(obj[0].name)
        return render(request, 'deletecourse.html', {"obj": obj})

    def post(self, request):
        print(request.POST)
        course_number = request.POST["course_number"]
        tryCourse = Course.objects.filter(Q(course_number=course_number)).exists()
        if tryCourse == False:
            return render(request, 'deletecourse.html', {
                "alert": True,
                "message": "Course Not Found"
            })



        currentCourse = Course.objects.get(course_number=course_number)
        currentCourse.delete()
        return render(request, 'admin-homepage.html', {
            "alert": True,
            "message": "Course Deleted"
        })


class FindUser(View):

    def get(self, request):
        obj = MyUser.objects.all()
        return render(request, 'finduser.html', {"obj": obj})

class AddLab(View):

    def get(self, request):

        if (request.session['user_type'] == 'TA'):
            return redirect('ta-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        elif (request.session['user_type'] == 'AD'):
            return redirect('admin-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        else:
            obj = Course.objects.all()
            user = MyUser.objects.all()
            print(obj[0].name)
            name = request.session['name']
            return render(request, 'addlab.html', {"obj": obj, 'name': name, 'ta': user})

    def post(self, request):
        classNum = Course.objects.get(section_number=request.POST['section-number'])




        taCheck = MyUser.objects.get(name=request.POST['section-ta'])
        if taCheck.ta_count == 2:
            messages.info(request, message="TA's can only have two assignments!")
            return redirect('addlab.html', {
                "alert": True,
                "message": "TA's can only be assigned to 2 courses max "
            })

        taCheck.ta_count +=1
        taCheck.save()
        classNum.lab_ta = request.POST['section-ta']
        classNum.save()
        return render(request, 'instructor-homepage.html', {})


class AssignInstructor(View):

    def get(self, request):
        if (request.session['user_type'] == 'TA'):
            return redirect('ta-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        elif (request.session['user_type'] == 'IN'):
            return redirect('instructor-homepage.html', {
                "alert": True,
                "message": "You can't access this page, "
            })
        else:
            obj = Course.objects.all()
            user = MyUser.objects.all()
            print(obj[0].name)
            print(len(user))
            name = request.session['name']
            return render(request, 'assigninstructor.html', {"obj": obj, 'name': name, 'instructor': user})

    def post(self, request):
        print(request.POST)
        classNum = Course.objects.get(section_number=request.POST['section-number'])
        classNum.section_instructor = request.POST['section-instructor']
        classNum.save()
        return render(request, 'admin-homepage.html', {})



