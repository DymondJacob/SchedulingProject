"""SchedulingProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from SchedulingApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginView.as_view(), name="login"),
    path('admin-homepage.html', AdminMainView.as_view(), name='admin-homepage'),
    path('assigninstructor.html', AssignInstructor.as_view(), name='assigninstructor'),
    path('instructor-homepage.html', InstructorMainView.as_view(), name='instructor-homepage'),
    path('ta-homepage.html', TaMainView.as_view(), name='ta-homepage'),
    path('createaccount.html', CreateAccount.as_view(), name='createaccount'),
    path('editaccount.html', EditAccount.as_view(), name='editaccount'),
    path('editcourse.html', EditCourse.as_view(), name='editcourse'),
    path('deletecourse.html', DeleteCourse.as_view(), name='deletecourse'),
    path('deleteaccount.html', DeleteAccount.as_view(), name='deleteaccount'),
    path('createcourse.html', CreateCourse.as_view(), name='createcourse'),
    path('allcourses.html', AllCourses.as_view(), name='allcourses'),
    path('instructor-courses.html', InstructorCourses.as_view(), name='instructor-courses'),
    path('addlab.html', AddLab.as_view(), name='addlab'),
    path('finduser.html', FindUser.as_view(), name='finduser'),
    path('ta-assignments.html', TaAssignments.as_view(), name='ta-assignments'),
]
