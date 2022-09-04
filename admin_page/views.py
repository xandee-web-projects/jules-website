import os
from this import s
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from portal.models import Class, ClassFees, PendingPhoto, Staff, Student, User
from .models import Blog, Contact, Message, Random
from datetime import date
import string, random
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.template import loader

# Create your views here.

def admin_login_required(f):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return f(request, *args, **kwargs)
        else:
            raise Http404
    return wrapper

def del_photo(photo):
    try:
        if not photo.path.endswith("\default.png"):
            os.remove(photo.path)
    except:
        pass

@login_required
@admin_login_required
def website(request):
    return render(request, 'admin-page/website.html')

@login_required
@admin_login_required
def editblogs(request):
    return render(request, 'admin-page/edit-blogs.html', {"blogs": Blog.objects.all().order_by("-date")})

@login_required
@admin_login_required
def new_blog(request):
    if request.method == "POST":
        heading = request.POST.get('heading')
        desc = request.POST.get('desc')
        photo = request.FILES.get('photo')
        date = request.POST.get('date')
        blog = Blog(heading=heading, desc=desc, photo=photo)
        if date:
            blog.date = date
        blog.save()
        messages.success(request, "Blog created")
    return redirect('edit_blogs')

@login_required
@admin_login_required
def update_blog(request):
    if request.method == "POST":
        id = request.POST.get('id')
        blog = Blog.objects.get(id=id)
        if blog:
            messages.success(request, f"Blog {blog.heading} updated")
            heading = request.POST.get('heading')
            desc = request.POST.get('desc')
            date = request.POST.get('date')
            photo = request.FILES.get('photo')
            blog.heading = heading
            blog.desc = desc
            blog.date = parse_date(date)
            if photo:
                del_photo(blog.photo)
                blog.photo = photo
            blog.save()
        else:
            messages.error(request, "Blog was not found. Try refreshing the page")
    return redirect('edit_blogs')

@login_required
@admin_login_required
def delete_blog(request, id):
    blog = Blog.objects.get(id=id)
    if blog:
        messages.success(request, f"Blog {blog.heading} deleted")
        del_photo(blog.photo)
        blog.delete()
    else:
        messages.error(request, "Blog was not found. Try refreshing the page")
    return redirect('edit_blogs')

@login_required
@admin_login_required
def staff(request):
    return render(request, 'admin-page/staff.html', {"staff": Staff.objects.all().order_by('first_name')})

@login_required
@admin_login_required
def new_staff(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        onames = request.POST.get('onames')
        role = request.POST.get('role')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        salary = request.POST.get('salary')
        pwd = request.POST.get('password')
        date_employed = request.POST.get('date_employed')
        last = Staff.objects.last()
        yr = str(date.today().year)[2:]
        if last:
            num = int(last.username[-3:])
        else:
            num = 1
        rand_pwd = ''.join(random.choices(string.ascii_lowercase+string.digits, k=8))
        password = rand_pwd if pwd == "" else pwd
        staff = Staff.objects.create_user(username=f'1{yr}{str(num+1).zfill(3)}', password=password, email=email, gender=gender,
            first_name=fname, last_name=lname, other_names=onames, role='staff', staff_role=role.lower(), phone=phone, salary=salary, date_employed=parse_date(date_employed))
        staff.save()

        if email != "":
            err = account_created_message(staff.email, staff.get_full_name(), staff.username, password if pwd != password else "*"*len(password), staff.staff_role)
            if err != 1:
                messages.error(request, "An email containing this user's credentials wasn't sent.")
            else:
                messages.success(request, "An email containing this user's credentials was sent successfully.")
        messages.success(request, f"Staff created")
    return redirect('staff')

@login_required
@admin_login_required
def update_staff(request):
    if request.method == "POST":
        uid = request.POST.get('id')
        staff = Staff.objects.filter(username=str(uid)).first()
        if staff:
            staff.first_name = request.POST.get('fname')
            staff.last_name = request.POST.get('lname')
            staff.other_names = request.POST.get('onames')
            staff.email = request.POST.get('email')
            staff.phone = request.POST.get('phone')
            staff.salary = request.POST.get('salary')
            
            role = request.POST.get('role')
            password = request.POST.get('password')
            if role != "norole":
                staff.role = role
            if password != "":
                staff.set_password(password)
            staff.save()
            messages.success(request, f"Staff {staff.username} Updated")
        else:
            messages.error(request, "Staff was not found. Try refreshing the page")
    return redirect('staff')

@login_required
@admin_login_required
def delete_staff(request, id):
    staff = Staff.objects.filter(username=id).first()
    if staff:
        del_photo(staff.photo)
        staff.delete()
    return HttpResponse()

@login_required
@admin_login_required
def classes(request):
    if request.method == "POST":
        cid = request.POST.get('class')
        tid = request.POST.get('teacher')
        c = Class.objects.get(id=cid)
        teacher = Staff.objects.filter(username=tid).first()
        if tid == "None" and c:
            c.teacher = None
            c.save()
            messages.success(request, f"{c.name} has been set to no teacher")
        elif teacher and c:
            c.teacher = teacher
            c.save()
            messages.success(request, f"{teacher.first_name} is now the teacher of {c.name}")
        else:
            messages.error(request, f"The staff or the class were nor found")
    return render(request, 'admin-page/classes.html', {"classes":Class.objects.all(), "teachers":Staff.objects.filter(staff_role__endswith="teacher").order_by("first_name")})

@login_required
@admin_login_required
def students(request):
    c = None
    class_id = request.GET.get('class')
    if class_id:
        get_class = Class.objects.get(id=class_id)
        if get_class:
            s = Student.objects.filter(current_class=get_class).order_by('first_name')
            c = get_class.name
    else:
        s = Student.objects.all().order_by('first_name')
    return render(request, 'admin-page/students.html', {'students': s, 'classes':Class.objects.all(), "c":c})

@login_required
@admin_login_required
def new_student(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        onames = request.POST.get('onames')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        pwd = request.POST.get('password')
        date_admitted = request.POST.get('date_admitted')
        dob = request.POST.get('dob')
        last = Student.objects.last()
        yr = str(date.today().year)[2:]
        _class = Class.objects.filter(id=request.POST.get('class')).first()
        if last:
            num = int(last.username[-3:])
        else:
            num = 0
        rand_pwd = ''.join(random.choices(string.ascii_lowercase+string.digits, k=8))
        password = rand_pwd if pwd == "" else pwd
        student = Student.objects.create_user(username=f'{yr}{str(num+1).zfill(3)}', password=password, email=email, gender=gender,
            first_name=fname, last_name=lname, other_names=onames, role='student', current_class=_class, phone=phone, dob=parse_date(dob), date_admitted=parse_date(date_admitted))
        student.save()
        if email != "":
            err = account_created_message(student.email, student.get_full_name(), student.username, password if pwd != password else "*"*len(password), student.current_class)
            if err != 1:
                messages.error(request, "An email containing this user's credentials wasn't sent.")
            else:
                messages.success(request, "An email containing this user's credentials was sent successfully.")
        # Send message with twilio api

        messages.success(request, f"Student created")
    return redirect('students')

@login_required
@admin_login_required
def update_student(request):
    if request.method == "POST":
        uid = request.POST.get('id')
        student = Student.objects.get(username=str(uid))
        if student:
            student.first_name = request.POST.get('fname')
            student.last_name = request.POST.get('lname')
            student.other_names = request.POST.get('onames')
            student.email = request.POST.get('email')
            student.phone = request.POST.get('phone')
            
            _class = Class.objects.filter(id=request.POST.get('class')).first()
            password = request.POST.get('password')
            if _class != None:
                student.current_class = _class
            if password != "":
                student.set_password(password)
            student.save()
            messages.success(request, f"Student {student.username} Updated")
        else:
            messages.error(request, "Student was not found. Try refreshing the page")
    return redirect('students')

@login_required
@admin_login_required
def delete_student(request, id):
    student = Student.objects.get(username=id)
    if student: 
        del_photo(student.photo)
        student.delete()
    return HttpResponse()

@login_required
@admin_login_required
def get_messages(request):
    return render(request, 'admin-page/messages.html', {'message_list':Message.objects.all().order_by('-time')})

@login_required
@admin_login_required
def delete_message(request, id):
    m = Message.objects.get(id=id)
    if m:
        m.delete()
    return JsonResponse("ok", safe=False)

@login_required
@admin_login_required
def randoms(request, id):
    return redirect('messages')

@login_required
@admin_login_required
def pending_photos(request):
    return render(request, 'admin-page/pending-photos.html', {"pending_photos": PendingPhoto.objects.all()})

@login_required
@admin_login_required
def accept_photo(request, id):
    photo = PendingPhoto.objects.get(id=id)
    if photo:
        u = User.objects.filter(username=photo.user.username).first()
        u.photo = photo.photo
        u.save()
        photo.delete()
    return JsonResponse("ok", safe=False)

@login_required
@admin_login_required
def discard_photo(request, id):
    photo = PendingPhoto.objects.get(id=id)
    if photo:
        del_photo(photo.photo)
        photo.delete()
    return JsonResponse("ok", safe=False)

@login_required
@admin_login_required
def randoms(request):
    if request.method == "POST":
        for i in request.FILES.getlist('photo'):
            Random(photo=i).save()
    return render(request, 'admin-page/randoms.html', {'randoms':Random.objects.all().order_by("-id")})

@login_required
@admin_login_required
def delete_random(request, id):
    r = Random.objects.get(id=id)
    if r:
        del_photo(r.photo)
        r.delete()
    return JsonResponse("ok", safe=False)

@login_required
@admin_login_required
def edit_fees(request):
    if request.method == "POST":
        id = request.POST.get('id')
        c = ClassFees.objects.get(id=id)
        if c:
            new_fee = request.POST.get('new_fee')
            return_fee = request.POST.get('return_fee')
            c.new_fee = new_fee
            c.return_fee = return_fee
            c.save()
            messages.success(request, f"{c.name}'s school fees has been updated")
        else:
            messages.error(request, f"The class you are trying to edit was not found")
    return render(request, "admin-page/edit-fees.html", {"classes":ClassFees.objects.all()})

@login_required
@admin_login_required
def delete_class(request, id):
    c = Class.objects.get(id=id)
    if c:
        c.delete()
    return HttpResponse()

@login_required
@admin_login_required
def new_subclass(request):
    if request.method == "POST":
        _class = request.POST.get('parent_class')
        try:
            c = Class.objects.get(id=_class)
            name1 = request.POST.get('subclass1')
            name2 = request.POST.get('subclass2')
            Class(name=c.name, subclass=name1).save()
            Class(name=c.name, subclass=name2).save()
        except Exception as e:
            print(e)
            messages.error(request, "Could not carry out this operation")
    return redirect('classes')

@login_required
@admin_login_required
def contact_list(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        whatsapp = request.POST.get('phone')
        Contact(first_name=fname, last_name=lname, email=email, gender=gender, phone=phone, whatsapp=whatsapp).save()
    return render(request, "admin-page/contact-list.html", {"contact_list": Contact.objects.all().order_by('first_name')})

@login_required
@admin_login_required
def update_contact(request):
    if request.method == "POST":
        id = request.POST.get('id')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        Contact.objects.filter(id=id).update(first_name=fname, last_name=lname, email=email, phone=phone)
    return redirect('contact_list')

@login_required
@admin_login_required
def delete_contact(request, id):
    contact = Contact.objects.get(id=id)
    if contact:
        contact.delete()
    return HttpResponse()


def account_created_message(to, name, id, pwd, category):
    html = loader.render_to_string(
        "new_user_email.html", {"id": id, "name":name, "password":pwd, "class":category, "portal_url": settings.PORTAL_DOMAIN}
    )
    err = send_mail("Jules Account Created", message="", from_email=settings.EMAIL_HOST_USER, recipient_list=[to], html_message=html, fail_silently=True)
    return err

def email_broadcast(subject, message, people):
    send_mass_mail(((subject, message, settings.EMAIL_HOST_USER, [p.email]) for p in people.objects.all()), fail_silently=True)

def broadcast(request):
    if request.method == "POST":
        people = request.POST.get('set')
        subject = request.POST.get('subject')
        message = request.POST.get('msg')
        to_email = request.POST.get('toEmail')
        to_WA = request.POST.get('toWA')
        if message and subject:
            if to_email:
                email_broadcast(subject, message, people_filter(people))
            if to_WA:
                pass
    return redirect(request.META.get('HTTP_REFERER'))

def people_filter(_set):
    if _set == "staff":
        return Staff
    elif _set == "students":
        return Student
    elif _set == "contact":
        return Contact
