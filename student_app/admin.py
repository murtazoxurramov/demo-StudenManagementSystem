from django.contrib import admin
from .models import Attendance, AttendanceReport, FeedBackStudent, Group, LeaveReportStaff, LeaveReportStudent, Parents,Staffs, Students, Subjects,CustomUser
from django.contrib.auth.admin import UserAdmin


class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser,UserModel)
admin.site.register(Staffs)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Group)
admin.site.register(Parents)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackStudent)
admin.site.register(LeaveReportStudent)