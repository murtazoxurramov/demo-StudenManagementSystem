from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import HttpResponseRedirect


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "student_app.adminViews":
                    pass
                elif modulename == "student_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "student_app.staffViews":
                    pass
                elif modulename == "student_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "3":
                if modulename == "student_app.parentViews":
                    pass
                elif modulename == "student_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("parent_home"))
            else:
                return HttpResponseRedirect(reverse("showlogin"))
        else:
            if request.path == reverse("showlogin") or request.path == reverse("dologin") or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("showlogin"))