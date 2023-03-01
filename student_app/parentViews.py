import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student_app.models import (Attendance, AttendanceReport, FeedBackStudent,
                                Group, LeaveReportStudent, NotificationStudent,
                                Parents, Staffs, Students, Subjects)


def parent_home(request):
    student_obj = Students.objects.get(parent=request.user.id)
    attendance_total = AttendanceReport.objects.filter(
        student_id=student_obj).count()
    attendance_present_total = AttendanceReport.objects.filter(
        student_id=student_obj, status=True).count()
    if attendance_present_total > 0:
        attendance_present = (attendance_present_total *
                              100) / attendance_total
    else:
        attendance_present = 0
    attendance_absent_total = AttendanceReport.objects.filter(
        student_id=student_obj, status=False).count()
    if attendance_absent_total > 0:
        attendance_absent = (attendance_absent_total * 100) / attendance_total
    else:
        attendance_absent = 0
    groups = Group.objects.filter(id=student_obj.group_id).count()
    context = {
        "attendance_total": attendance_total,
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "groups": groups
    }
    return render(request, 'parent_templates/parent_home_template.html', context)


def parent_view_attendance(request):
    student = Students.objects.get(parent=request.user.id)
    groups = Group.objects.filter(id=student.group_id)
    return render(request, 'parent_templates/parent_view_attendance.html', {"groups": groups})


def parent_view_attendance_post(request):
    group_id = request.POST.get("group")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    start_date_parse = datetime.datetime.strptime(
        start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    group_obj = Group.objects.get(id=group_id)
    student_obj = Students.objects.get(parent=request.user.id)

    attendance = Attendance.objects.filter(attendance_date__range=(
        start_date_parse, end_date_parse), group_id=group_obj)
    attendance_reports = AttendanceReport.objects.filter(
        attendance_id__in=attendance, student_id=student_obj)
    return render(request, 'parent_templates/student_attendance_data.html', {"attendance_reports": attendance_reports})


def student_apply_leave(request):
    parent_obj = Parents.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(
        parent_id=parent_obj).order_by("-id")
    context = {
        "leave_data": leave_data
    }
    return render(request, 'parent_templates/student_apply_leave.html', context)


def student_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('student_apply_leave'))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get('leave_reason')

        parent_obj = Parents.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(
                parent_id=parent_obj,
                leave_date=leave_date,
                leave_message=leave_msg,
                leave_status=0
            )
            leave_report.save()
            messages.success(
                request, "Ta'tilga muvaffaqiyatli ariza topshirildi")
            return HttpResponseRedirect(reverse('student_apply_leave'))
        except:
            messages.error(request, "Ta'til uchun ariza topshirib bo'lmadi")
            return HttpResponseRedirect(reverse('student_apply_leave'))


def student_feedback(request):
    parent_obj = Parents.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(
        parent_id=parent_obj).order_by("-id")
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'parent_templates/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('student_feedback'))
    else:
        parent_obj = Parents.objects.get(admin=request.user.id)
        feedback_msg = request.POST.get("feedback_msg")
        try:
            feedback = FeedBackStudent(
                parent_id=parent_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Fikr-mulohaza yuborildi")
            return HttpResponseRedirect(reverse('student_feedback'))
        except:
            messages.error(request, "Fikr-mulohaza yuborib bo‘lmadi")
            return HttpResponseRedirect(reverse('student_feedback'))


@csrf_exempt
def parent_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        parent = Parents.objects.get(admin=request.user.id)
        parent.fcm_token = token
        parent.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def parent_all_notification(request):
    parent = Parents.objects.get(admin=request.user.id)
    notifications = NotificationStudent.objects.filter(parent_id=parent.id)
    return render(request, 'parent_templates/parent_all_notification.html', {"notifications": notifications})
