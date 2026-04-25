from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.shortcuts import render


import re

from bboard.forms import BbForm, IceCreamFormSet, ContactForm
from bboard.models import Bb, Rubric, IceCream, IceCreamSet, ContactMessage


def get_rubrics():
    return Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)


# -------------------------
# BB
# -------------------------
def index(request):
    bb_list = Bb.objects.all().order_by('-published')

    paginator = Paginator(bb_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'page_obj': page_obj,
        'rubrics': get_rubrics()
    })


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric_id=rubric_id)
    current_rubric = get_object_or_404(Rubric, pk=rubric_id)

    return render(request, 'by_rubric.html', {
        'bbs': bbs,
        'rubrics': get_rubrics(),
        'current_rubric': current_rubric
    })


def bb_detail(request, id):
    bb = get_object_or_404(Bb, pk=id)

    return render(request, 'bb_detail.html', {
        'bb': bb,
        'rubrics': get_rubrics()
    })


def bb_delete(request, id):
    bb = get_object_or_404(Bb, pk=id)

    if request.method == "POST":
        bb.delete()
        return redirect('index')

    return render(request, 'bb_confirm_delete.html', {
        'bb': bb,
        'rubrics': get_rubrics()
    })


class BbCreateView(CreateView):
    model = Bb
    form_class = BbForm
    template_name = 'create.html'
    success_url = reverse_lazy('index')


def bb_list(request):
    bbs = Bb.objects.all()
    return render(request, 'index.html', {'bbs': bbs})


# -------------------------
# ICECREAM
# -------------------------
def icecream_list(request):
    data = IceCream.objects.all()
    return render(request, "icecream/list.html", {"data": data})


def icecream_create(request):
    if request.method == "POST":
        formset = IceCreamFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("icecream_list")
    else:
        formset = IceCreamFormSet()

    return render(request, "icecream/create.html", {
        "formset": formset
    })


def icecream_sets_short(request):
    sets = IceCreamSet.objects.values('name')

    return render(request, 'icecream/sets.html', {
        'sets': sets
    })


def icecream_transaction_demo(request):
    try:
        with transaction.atomic():
            IceCream.objects.create(name="Шоколад", flavor="Шоколад", price=100, is_available=True)
            IceCream.objects.create(name="Ваниль", flavor="Ваниль", price=120, is_available=True)
            raise Exception("Rollback")
    except Exception:
        return HttpResponse("❌ Транзакция отменена")

    return HttpResponse("OK")


def available_icecream(request):
    data = IceCream.objects.available()
    return HttpResponse("<br>".join(i.name for i in data))


def queryset_demo(request):
    data = (
        IceCream.objects
        .filter(is_available=True)
        .exclude(price__lt=100)
        .order_by('-price')
    )
    return HttpResponse("<br>".join(i.name for i in data))


# -------------------------
# USERS
# -------------------------
class UserListView(ListView):
    model = User
    template_name = 'users_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'


# -------------------------
# CONTACT
# -------------------------
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                message=form.cleaned_data['message']
            )
            return HttpResponse("Сообщение сохранено")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


# -------------------------
# TAGS
# -------------------------
def tags_demo(request):
    bbs = Bb.objects.all()

    return render(request, 'tags_demo.html', {
        'bbs': bbs
    })


def bbcode_to_html(text):
    if not text:
        return ""

    text = re.sub(r'\[b\](.*?)\[/b\]', r'<b>\1</b>', text)
    text = re.sub(r'\[i\](.*?)\[/i\]', r'<i>\1</i>', text)
    text = re.sub(r'\[u\](.*?)\[/u\]', r'<u>\1</u>', text)

    return mark_safe(text)

def select_columns(request):
    bbs = Bb.objects.values('title', 'price')

    return render(request, 'select_columns.html', {
        'bbs': bbs,
        'rubrics': get_rubrics()
    })


def exclude_values(request):
    bbs = Bb.objects.exclude(price=0)

    return render(request, 'exclude_values.html', {
        'bbs': bbs,
        'rubrics': get_rubrics()
    })

def icecream_list(request):
    icecreams = IceCream.objects.all()

    return render(request, "icecream/list.html", {
        "icecreams": icecreams
    })