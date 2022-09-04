from datetime import time
import re
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from portal.models import Staff
from .models import Question, Option, Test
from django.contrib import messages
import string, random


def staff_login_required(f):
    def wrapper(request, *args, **kwargs):
        if Staff.objects.get(username=request.user.username):
            return f(request, *args, **kwargs)
        else:
            raise Http404
    return wrapper

# Create your views here.

@login_required
@staff_login_required
def edit_test(request, id):
    test = Test.objects.get(id=id)
    if not test:
        raise Http404
    elif test and request.user.username != test.teacher.username:
        messages.error(request, "You are not the user that created this test")
    elif request.method == "POST":
        form_data = request.POST
        print(form_data.get("time"))
        # time = construct_time(form_data.get("hrs"), form_data.get("mins"))
        new_test = Test(name=test.name, teacher=test.teacher, status=test.status, id=test.id, code=test.code)
        test.delete()
        del test
        if 'publish' in form_data:
            new_test.status = True
        new_test.save()
        test = new_test
        question = None
        for key in form_data.keys():
            if key == "csrfmiddlewaretoken":
                continue
            if key in ["hrs", "mins", 'publish']:
                continue
            elif key.find("-") == -1:
                question = Question.objects.create(number=key, text=form_data.get(key), test=test)
                continue
            elif key.find("-") != -1:
                question_ans = key.split("-")
                if "ans" in question_ans:
                    answer = True
                else:
                    answer = False
                if question:
                    Option.objects.create(text=form_data.get(key), question=question, option_id=question_ans[1], answer=answer)
                else:
                    messages.error(request, "Something went wrong while trying to save")
                    break
        
    return render(request, "edit-test.html", {"test": test})

@login_required
@staff_login_required
def tests(request):
    return render(request, "tests.html", {"tests":Test.objects.order_by("-id")})

@login_required
@staff_login_required
def new_test(request):
    if request.method == "POST":
        name = request.POST.get('name')
        test = Test(name=name, teacher=Staff.objects.get(username=request.user.username))
        test.save()
        test.code = f'{test.id}'.join(random.choices(string.ascii_lowercase+string.digits, k=3))
        test.save()
        messages.success(request, "Test created !")
    return redirect("edit_test", id=test.id)

@login_required
@staff_login_required
def tests(request):
    return render(request, "tests.html", {"tests":Test.objects.order_by("-id")})

@login_required
@staff_login_required
def preview_test(request, id):
    test = Test.objects.get(id=id)
    print(test)
    if not test:
        raise Http404
    messages.info(request, "This is only a preview page. Students cannot write the test from here.")
    return render(request, "preview-test.html", {"test":test})

@login_required
@staff_login_required
def new_test(request):
    if request.method == "POST":
        name = request.POST.get('name')
        test = Test(name=name, teacher=Staff.objects.get(username=request.user.username))
        test.save()
        test.code = f'{test.id}'.join(random.choices(string.ascii_lowercase+string.digits, k=3))
        test.save()
        messages.success(request, "Test created !")
    return redirect("edit_test", id=test.id)

@login_required
@staff_login_required
def delete_test(request, id):
    test = Test.objects.get(id=id)
    if test:
        n = test.name
        if request.user.username == test.teacher.username:
            test.delete()
            messages.success(request, f"Test \"{n}\" deleted")
        else:
            messages.error(request, "You are not the user that created this test so you cant delete it")
    else:
        messages.error(request, "Test not found")
    return HttpResponse("Test deleted")

def construct_time(hrs:str, mins:str):
    if int(hrs) == 0:
        hrs = "00"
    elif int(hrs) < 10:
        hrs = "0"+str(int(hrs))
    if int(mins) == 0:
        mins = "00"
    elif int(mins) < 10:
        mins = "0"+str(int(mins))
    return time.fromisoformat(f"{hrs}:{mins}")  