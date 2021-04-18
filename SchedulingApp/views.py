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

from .models import MyUser


# Create your views here.


class loginView(View):
    def get(self, request):
        return render(request, 'login.html', {})
        # return render(request, "index.html")

    def post(self, request):
        _id = request.POST["id"]
        pw = request.POST["pw"]
        email = request.POST["email"]

        try:
            login_user = authenticate(username=_id, password=pw, email=email)
            login(request, login_user)

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
            login_myuser = MyUser.objects.get(user=login_user)

        except ObjectDoesNotExist:
            return render(request, 'login.html', {
                "alert": True,
                "message": "login failed."
            })

        if login_myuser.user_type == 'AD':
            return redirect('main/admin')
        elif login_myuser.user_type == 'IN':
            return redirect('main/instructor')
        elif login_myuser.user_type == 'TA':
            return redirect('main/ta')
        else:
            return render(request, 'login.html', {
                "alert": True,
                "message": "login failed."
            })


class AdminMainView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        print(request.user)
        my = getMyUser(request.user)

        if my != None and my.user_type == 'AD':
            return render(request, 'admin_main.html', {})
        else:
            return redirect('/')

    def post(self, request):
        _id = request.POST["id"]
        pw = request.POST["pw"]
        email = request.POST["email"]
        user_type = request.POST.get("user_type")

        userExist = User.objects.filter(Q(username=_id) | Q(email=email)).exists()

        if userExist:
            return render(request, 'admin_main.html', {
                "alert": True,
                "message": "이미 존재하는 id거나 email입니다",
            })
        else:
            newUser = User.objects.create(username=_id, password=pw, email=email)
            newUser.myuser.user_type = user_type
            newUser.save()
            return render(request, 'admin_main.html', {
                "alert": True,
                "message": "account created",
            })


class InstructorMainView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        print(request.user)
        my = getMyUser(request.user)

        if my != None and my.user_type == 'IN':
            return render(request, 'instructor_main.html', {})
        else:
            return redirect('/')


class TaMainView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):

        print(request.user)
        my = getMyUser(request.user)

        if my != None and my.user_type == 'TA':
            return render(request, 'ta_main.html', {})
        else:
            return redirect('/')


def getMyUser(user):
    try:
        my = MyUser.objects.get(user=user)
        return my
    except ObjectDoesNotExist:
        return None
