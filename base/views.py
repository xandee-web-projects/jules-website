from django.shortcuts import render
from random import randint
from admin_page.models import Blog, Message, Random
from portal.models import ClassFees

# Create your views here.
def index(request):
    randoms = []
    all_randoms = list(Random.objects.all())
    for i in range(4):
        chosen = randint(1, 1000)%len(all_randoms)
        r = all_randoms[chosen]
        randoms.append(r)
        all_randoms.remove(r)
    return render(request, "index.html", {"blogs":Blog.objects.all().order_by('-date')[:3], "randoms":randoms})

def about(request):
    return render(request, "about.html")
def blog(request):
    return render(request, "blog.html", {"blogs":Blog.objects.all().order_by('-date')})
def contact(request):
    content = {}
    if request.method == "POST":
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        sub = request.POST.get('subject')
        msg = request.POST.get('msg')
        Message(name=name, contact=contact, subject=sub, message=msg).save()
        content = {"name": name}
    return render(request, "contact.html", content)

def fees(request):
    return render(request, "fees.html", {"fees": ClassFees.objects.all()})
