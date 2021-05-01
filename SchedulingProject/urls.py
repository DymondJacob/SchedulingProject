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
    path('instructor-homepage.html', InstructorMainView.as_view(), name='instructor-homepage'),
    path('ta-homepage.html', TaMainView.as_view(), name='ta-homepage'),
    path('createaccount.html', CreateAccount.as_view(), name='createaccount'),
    path('createcourse.html', CreateCourse.as_view(), name='createcourse'),
    path('addsection.html', AddSection.as_view(), name='addsection'),
    path('assignuser.html', AssignUser.as_view(), name='assignuser'),
    path('deleteaccount.html', DeleteAccount.as_view(), name='deleteaccount'),
    path('deletecourse.html', DeleteCourse.as_view(), name='deletecourse'),
    path('deletesection.html', DeleteSection.as_view(), name='deletesection'),
    path('editaccount.html', EditAccount.as_view(), name='editaccount'),
    path('editcourse.html', EditCourse.as_view(), name='editcourse'),
    path('editremoveuser.html', EditRemoveUser.as_view(), name='editremoveuser'),
    path('editsection.html', EditSection.as_view(), name='editsection'),
    path('findcourse.html', FindCourse.as_view(), name='findcourse'),
    path('finduser.html', FindUser.as_view(), name='finduser'),
    path('createassignment.html', CreateAssignment.as_view(), name='createassignment'),
    path('viewassignments.html', ViewAssignment.as_view(), name='viewassignments'),
    path('editassignments.html', EditAssignment.as_view(), name='editassignments'),
    path('allcourses.html', AllCourses.as_view(), name='allcourses'),
]
