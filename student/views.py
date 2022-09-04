from django.shortcuts import render

# Create your views here.
def write_test(request):
    return render("test.html")
