from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# Create your views here.


@login_required(login_url="login")
def Index(request):
    return render(request, "main/index.html")


@login_required(login_url="login")
def Airlines(request):
    airlines = Airline.objects.all()
    context = {"airlines": airlines}
    return render(request, "main/airlines.html", context)


@login_required(login_url="login")
def AirlineAdd(request):
    if request.method == "POST":
        form = AirlineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("airlines")
    else:
        form = AirlineForm()
        return render(request, "main/partials/airline_form.html", {"form": form})


@login_required(login_url="login")
def AirlineEdit(request, id=None, template_name="main/partials/airline_form.html"):
    if id:
        airline = get_object_or_404(Airline, pk=id)
    else:
        airline = Article()

    form = AirlineForm(request.POST or None, instance=airline)
    if request.POST and form.is_valid():
        form.save()
        return redirect("airlines")

    return render(request, template_name, {"form": form})


@login_required(login_url="login")
def AirlineDelete(request, id):
    if request.method == "POST":
        Airline.objects.filter(id=id).delete()
        return redirect("airlines")
    else:
        return render(
            request, "main/partials/airline_delete_form.html", {"recordid": id}
        )
