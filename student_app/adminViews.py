from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from .models import Attendance, AttendanceReport, CustomUser, FeedBackStaffs, FeedBackStudent, LeaveReportStaff, LeaveReportStudent, NotificationStaffs, NotificationStudent, Staffs, Students, Subjects,Group,Parents
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
import requests



def admin_home(request):
    students = Students.objects.all().count()
    total_pending_students = Students.objects.filter(status="pending").count()
    total_active_students = Students.objects.filter(status="active").count()
    total_attendance=AttendanceReport.objects.all().count()
    total_absent_attendance=AttendanceReport.objects.filter(status=False).count()
    if total_absent_attendance>0:
        attendance_absent = (total_absent_attendance * 100)/total_attendance
    else:
        attendance_absent=0
    total_present_attendance = AttendanceReport.objects.filter(status=True).count()
    if total_present_attendance>0:
        attendance_present = (total_present_attendance*100)/total_attendance
    else:
        attendance_present=0
    groups = Group.objects.all().count()
    subjects = Subjects.objects.all().count()
    context = {
        "students":students,
        "total_pending_students":total_pending_students,
        "total_active_students":total_active_students,
        "groups":groups,
        "total_attendance":total_attendance,
        "total_absent_attendance":total_absent_attendance,
        "attendance_absent":attendance_absent,
        "attendance_present":attendance_present,
        "subjects":subjects
    }
    return render(request, 'admin_templates/home_content.html',context)

def total_pending_students(request):
    total_pending_students = Students.objects.filter(status="pending")
    return render(request, 'admin_templates/total_pending_student.html',{"total_pending_students":total_pending_students})

def total_active_students(request):
    total_active_students = Students.objects.filter(status="active")
    return render(request, 'admin_templates/total_active_student.html',{"total_active_students":total_active_students})

def add_staff(request):
    return render(request,"admin_templates/add_staff_template.html")


def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.staffs.phone=phone
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_phone_exist(request):
    phone=request.POST.get("phone")
    user_obj=Parents.objects.filter(phone=phone).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def add_parent(request):
    return render(request,'admin_templates/add_parent_template.html')

def add_parent_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
            user.parents.address=address
            user.parents.phone=phone
            user.save()
            messages.success(request,"Successfully Added Parent")
            return HttpResponseRedirect(reverse("add_parent"))
        except:
            messages.error(request,"Failed to Add Parent")
            return HttpResponseRedirect(reverse("add_parent"))

def add_subject(request):
    return render(request, 'admin_templates/add_subject_template.html')

def add_stubject_save(request):
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course_name")
        try:
            course_model=Subjects(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_subject"))
        except Exception as e:
            print(e)
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_subject"))

def add_student(request):
    subjects = Subjects.objects.all()
    groups = Group.objects.all()
    parents = Parents.objects.all()
    
    context = {
        "subjects":subjects,
        "groups":groups,
        "parents":parents
        
    }
    return render(request, 'admin_templates/add_student_template.html',context)

def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        phone1=request.POST.get("phone1")
        phone2=request.POST.get("phone2")
        status=request.POST.get("status")
        subject_id=request.POST.get("subject")
        if subject_id !="":
            subject=Subjects.objects.get(id=subject_id)
        else:
            subject=None
        group_id=request.POST.get("group")
        if group_id != "":
            group=Group.objects.get(id=group_id)
        else:
            group=None
        parent_id = request.POST.get("parent")
        if parent_id != "":
            parent = CustomUser.objects.get(id=parent_id)
        else:
            parent = None
        try:
            student_model=Students(
                first_name=first_name,
                last_name=last_name,
                phone1=phone1,
                phone2=phone2,
                address=address,
                status=status,
                course_id=subject,
                group_id=group,
                parent=parent,
            )
            student_model.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect(reverse("add_student"))
        except Exception as e:
            print(e)
            messages.error(request,"Failed To Add Student")
            return HttpResponseRedirect(reverse("add_student"))

def add_group(request):
    subjects = Subjects.objects.all()
    teachers = Staffs.objects.all()

    context = {
        "subjects":subjects,
        "teachers":teachers,
    }
    return render(request,'admin_templates/add_group_template.html',context)

def add_group_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        name=request.POST.get("group_name")
        subject_id=request.POST.get("subject")
        if subject_id != "":
            subject=Subjects.objects.get(id=subject_id)
        else:
            subject=None
        teacher_id=request.POST.get("teacher")
        if teacher_id != "":
            teacher=Staffs.objects.get(id=teacher_id)
        else:
            teacher=None
        day=request.POST.getlist("days")
        start_date=request.POST.get("start_date")
        end_date=request.POST.get("end_date")
        try:
            group_model=Group(
                group_name=name,
                course_id=subject,
                staff_id=teacher,
                days=day,
                start_date=start_date,
                end_date=end_date
            )
            group_model.save()
            messages.success(request,"Successfully Added Group")
            return HttpResponseRedirect(reverse("add_group"))
        except Exception as e:
            print(e)
            messages.error(request,"Failed To Add Group")
            return HttpResponseRedirect(reverse("add_group"))


def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, 'admin_templates/manage_staff_template.html',{"staffs":staffs})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"admin_templates/edit_staff_template.html",{"staff":staff,"id":staff_id})



def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")
        phone = request.POST.get("phone")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.phone=phone
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))


def delete_staff(request, staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    staff.delete()
    messages.success(request, "Staff deleted successfully!")
    return redirect(reverse('manage_staff'))


def manage_parent(request):
    parents = Parents.objects.all()
    return render(request, 'admin_templates/manage_parent_template.html',{"parents":parents})


def edit_parent(request,parent_id):
    parent=Parents.objects.get(admin=parent_id)
    return render(request,"admin_templates/edit_parent_template.html",{"parent":parent,"id":parent_id})



def edit_parent_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        parent_id=request.POST.get("student_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")
        phone = request.POST.get("phone")

        try:
            user=CustomUser.objects.get(id=parent_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            parent_model=Parents.objects.get(admin=parent_id)
            parent_model.address=address
            parent_model.phone=phone
            parent_model.save()
            messages.success(request,"Successfully Edited Parent")
            return HttpResponseRedirect(reverse("edit_parent",kwargs={"parent_id":parent_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_parent",kwargs={"parent_id":parent_id}))


def delete_parent(request, parent_id):
    parent=Parents.objects.get(admin=parent_id)
    parent.delete()
    messages.success(request, "Parent deleted successfully!")
    return redirect(reverse('manage_parent'))


def manage_student(request):
    students = Students.objects.all()
    return render(request, 'admin_templates/manage_student_template.html',{"students":students})


def edit_student(request,student_id):
    student=Students.objects.get(id=student_id)
    subjects = Subjects.objects.all()
    groups = Group.objects.all()
    parents = Parents.objects.all()
    
    context = {
        "subjects":subjects,
        "groups":groups,
        "parents" : parents,
        "student":student,
        "id":student_id,
    }
    return render(request,"admin_templates/edit_student_template.html",context)



def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        student_id=request.POST.get("student_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        phone1=request.POST.get("phone1")
        phone2=request.POST.get("phone2")
        status=request.POST.get("status")
        subject_id=request.POST.get("subject")
        if subject_id != "":
            subject=Subjects.objects.get(id=subject_id)
        else:
            subject=None
        group_id=request.POST.get("group")
        if group_id != "":
            group=Group.objects.get(id=group_id)
        else:
            group=None
        parent_id = request.POST.get("parent")
        if parent_id != "":
            parent = CustomUser.objects.get(id=parent_id)
        else:
            parent = None
        try:
            student=Students.objects.get(id=student_id)
            student.first_name = first_name
            student.last_name=last_name
            student.phone1 = phone1
            student.phone2=phone2
            student.address=address
            student.status = status
            student.course_id=subject
            student.group_id=group
            student.parent=parent
            student.save()
            messages.success(request,"Successfully Edited Student")
            return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        except Exception as e:
            print(e)
            messages.error(request,"Failed To Edit Student")
            return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))



def delete_student(request, student_id):
    student=Students.objects.get(id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('manage_student'))

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"admin_templates/manage_subject_template.html",{"subjects":subjects})


def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    return render(request,"admin_templates/edit_subject_template.html",{"subject":subject,"id":subject_id})


def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_id = request.POST.get("subject_id")
        course_name=request.POST.get("course_name")
        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.course_name=course_name
            subject.save()
            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed To Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def delete_subject(request, subject_id):
    subject=Subjects.objects.get(id=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted successfully!")
    return redirect(reverse('manage_subject'))


def manage_group(request):
    groups=Group.objects.all()
    return render(request,"admin_templates/manage_group_template.html",{"groups":groups})



def edit_group(request,group_id):
    group=Group.objects.get(id=group_id)
    subjects = Subjects.objects.all()
    teachers = Staffs.objects.all()
    context = {
        "subjects":subjects,
        "group": group,
        "id":group_id,
        "teachers":teachers
    }
    return render(request,"admin_templates/edit_group_template.html",context)


def edit_group_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        group_id=request.POST.get("group_id")
        name=request.POST.get("group_name")
        subject_id=request.POST.get("subject")
        if subject_id != "":
            subject=Subjects.objects.get(id=subject_id)
        else:
            subject = None
        teacher_id=request.POST.get("teacher")
        if teacher_id != "":
            teacher=Staffs.objects.get(id=teacher_id)
        else:
            teacher=None
        day=request.POST.getlist("days")
        start_date=request.POST.get("start_date")
        end_date=request.POST.get("end_date")
        try:
            group = Group.objects.get(id=group_id)
            group.group_name=name
            group.course_id=subject
            group.staff_id=teacher
            group.days=day
            group.start_date=start_date
            group.end_date=end_date
            group.save()
            messages.success(request,"Successfully Edited Group")
            return HttpResponseRedirect(reverse("edit_group",kwargs={"group_id":group_id}))
        except:
            messages.error(request,"Failed To Edit Group")
            return HttpResponseRedirect(reverse("edit_group",kwargs={"group_id":group_id}))


def delete_group(request, group_id):
    group=Group.objects.get(id=group_id)
    group.delete()
    messages.success(request, "Group deleted successfully!")
    return redirect(reverse('manage_group'))



def parent_feedback_message(request):
    feedbacks=FeedBackStudent.objects.all()
    context = {
        "feedbacks":feedbacks
    }
    return render(request, 'admin_templates/student_feedback_template.html',context)

@csrf_exempt
def parent_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_feedback_message(request):
    feedbacks=FeedBackStaffs.objects.all()
    context = {
        "feedbacks":feedbacks
    }
    return render(request, 'admin_templates/staff_feedback_template.html',context)

@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves=LeaveReportStudent.objects.all().order_by("-id")
    context = {
        "leaves":leaves
    }
    return render(request, 'admin_templates/student_leave_view.html',context)

def student_approve_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_disapprove_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def staff_leave_view(request):
    leaves=LeaveReportStaff.objects.all().order_by("-id")
    context = {
        "leaves":leaves
    }
    return render(request, 'admin_templates/staff_leave_view.html',context)

def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_view_attendance(request):
    groups = Group.objects.all()
    context = {
        "groups":groups,
    }
    return render(request, 'admin_templates/admin_view_attendance.html',context)

@csrf_exempt
def admin_get_attendance_dates(request):
    group=request.POST.get("group")
    group_id=Group.objects.get(id=group)
    attendance=Attendance.objects.filter(group_id=group_id,)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date)}
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def admin_get_attendance_student(request):
    
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)

    list_data = []
    for student in attendance_data:
        data_small = {"id":student.student_id.id,"name":student.student_id.first_name+" "+student.student_id.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


def admin_send_notification_staff(request):
    staffs = Staffs.objects.all()
    return render(request, 'admin_templates/staff_notification.html',{"staffs":staffs})

def admin_send_notification_parent(request):
    parents = Parents.objects.all()
    return render(request,'admin_templates/parent_notification.html',{"parents":parents})

@csrf_exempt
def send_parent_notification(request):
    id =request.POST.get("id")
    message=request.POST.get("message")
    parent=Parents.objects.get(admin=id)
    token=parent.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body = {
        "notification":{
            "title":"Student Management System",
            "body":message,
            "click_action":"https://mycrmbybek.herokuapp.com/parent_all_notification"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=AAAA8GJLVvQ:APA91bHBPnKkY2v9FRNpqkaKK3cU2Yihil6JvlemoGIOFmeJQCV2MbzOHAvueRYwrqGa5eDozQI7OWkbQjXAGvHsRGI_kF0Y21B7Fge2keZKde3eAfkuC2hgrMW195_tSZvayG_eYHba"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationStudent(parent_id=parent,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")



@csrf_exempt
def send_staff_notification(request):
    id =request.POST.get("id")
    message=request.POST.get("message")
    staff=Staffs.objects.get(admin=id)
    token=staff.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body = {
        "notification":{
            "title":"Student Management System",
            "body":message,
            "click_action":"https://mycrmbybek.herokuapp.com/staff_all_notification"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=AAAA8GJLVvQ:APA91bHBPnKkY2v9FRNpqkaKK3cU2Yihil6JvlemoGIOFmeJQCV2MbzOHAvueRYwrqGa5eDozQI7OWkbQjXAGvHsRGI_kF0Y21B7Fge2keZKde3eAfkuC2hgrMW195_tSZvayG_eYHba"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationStaffs(staff_id=staff,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")