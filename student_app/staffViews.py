from django.urls import reverse
import json
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from student_app.models import Attendance, AttendanceReport, FeedBackStaffs, Group, LeaveReportStaff, NotificationStaffs, Staffs, Students, Subjects
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


def staff_home(request):
    # For Fetch All Student Under Staff
    staff = Staffs.objects.get(admin=request.user.id)
    groups=Group.objects.filter(staff_id=staff)
    subject_id_list=[]
    for group in groups:
        subject=Subjects.objects.get(id=group.course_id.id)
        subject_id_list.append(subject)

    final_subject=[]
    for subject_id in subject_id_list:
        if subject_id not in final_subject:
            final_subject.append(subject)
    
    students=Students.objects.filter(course_id__in=final_subject).count()

    #fetch all attendance count
    attendance_count = Attendance.objects.filter(group_id__in=groups).count()

    #fetch all approve leave
    leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()

    group=Group.objects.filter(staff_id=staff).count()

    context = {
        "students":students,
        "attendance_count":attendance_count,
        "leave_count":leave_count,
        "group":group
    }
    return render(request,'oqituvchi_templates/staff_home_template.html',context)


def staff_take_attendance(request):
    groups = Group.objects.filter(staff_id=request.user.staffs.id)
    context = {
        "groups":groups
    }
    return render(request, 'oqituvchi_templates/staff_take_attendance.html',context)

@csrf_exempt
def get_students(request):
    group_id=request.POST.get("group")
    group=Group.objects.get(id=group_id)
    students = Students.objects.filter(group_id=group).filter(status="active")
    # student_data =serializers.serialize("python":students)        #for api
    # return JsonResponse(student_data,content_type="application/json",safe=False)

    list_data = []
    for student in students:
        data_small = {"id":student.id,"name":student.first_name+" "+student.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    group_id=request.POST.get("group_id")
    group = Group.objects.get(id=group_id)
    json_sstudent=json.loads(student_ids)
    try:
        attendance=Attendance(group_id=group)
        attendance.save()
        for stud in json_sstudent:
            student=Students.objects.get(id=stud['id'])
            attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_update_attendance(request):
    groups = Group.objects.filter(staff_id=request.user.staffs.id)
    context = {
        "groups":groups
    }
    return render(request, 'oqituvchi_templates/staff_update_attendance.html',context)

@csrf_exempt
def get_attendance_dates(request):
    group=request.POST.get("group")
    group_id=Group.objects.get(id=group)
    attendance=Attendance.objects.filter(group_id=group_id)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date)}
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def get_attendance_student(request):

    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)

    list_data = []
    for student in attendance_data:
        data_small = {"id":student.student_id.id,"name":student.student_id.first_name+" "+student.student_id.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    

    json_sstudent=json.loads(student_ids)
    try:
        attendance=Attendance.objects.get(id=attendance_date)
        for stud in json_sstudent:
            student=Students.objects.get(id=stud['id'])
            attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
            attendance_report.status= stud.get('status')
            attendance_report.save()
        return HttpResponse("OK")
    except Exception as e:
        print(e)
        return None
    return HttpResponse("ERR")


def staff_apply_leave(request):
    staff_obj=Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj).order_by("-id")
    context = {
        "leave_data":leave_data
    }
    return render(request, 'oqituvchi_templates/staff_apply_leave.html',context)


def staff_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('staff_apply_leave'))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get('leave_reason')

        staff_obj=Staffs.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStaff(
                staff_id=staff_obj,
                leave_date=leave_date,
                leave_message=leave_msg,
                leave_status=0
            )
            leave_report.save()
            messages.success(request, "Successfuly Applied for Leave")
            return HttpResponseRedirect(reverse('staff_apply_leave'))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse('staff_apply_leave'))


def staff_feedback(request):
    staff_obj=Staffs.objects.get(admin=request.user.id)
    feedback_data=FeedBackStaffs.objects.filter(staff_id=staff_obj).order_by("-id")
    context = {
        "feedback_data":feedback_data
    }
    return render(request, 'oqituvchi_templates/staff_feedback.html',context)

def staff_feedback_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('staff_feedback'))
    else:
        staff_obj=Staffs.objects.get(admin=request.user.id)
        feedback_msg=request.POST.get("feedback_msg")
        try:
            feedback=FeedBackStaffs(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfuly Send Feedback")
            return HttpResponseRedirect(reverse('staff_feedback'))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse('staff_feedback'))

@csrf_exempt
def staff_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        staff=Staffs.objects.get(admin=request.user.id)
        staff.fcm_token=token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_all_notification(request):
    staff = Staffs.objects.get(admin=request.user.id)
    notifications=NotificationStaffs.objects.filter(staff_id=staff.id)
    return render(request,'oqituvchi_templates/staff_all_notification.html',{"notifications":notifications})