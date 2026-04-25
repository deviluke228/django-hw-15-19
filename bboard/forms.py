from django import forms
from django.forms import modelformset_factory
from .models import Bb, IceCream
from django import forms
from captcha.fields import CaptchaField

class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = ['title', 'content', 'price', 'rubric']


class IceCreamForm(forms.ModelForm):
    class Meta:
        model = IceCream
        fields = ['name', 'flavor', 'price', 'is_available']


# ✅ FormSet (главное для задания)
IceCreamFormSet = modelformset_factory(
    IceCream,
    fields=('name', 'flavor', 'price', 'is_available'),
    extra=3
)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Имя")
    message = forms.CharField(widget=forms.Textarea, label="Сообщение")

class ContactForm(forms.Form):
        name = forms.CharField(max_length=100, label="Имя")
        message = forms.CharField(widget=forms.Textarea, label="Сообщение")
        captcha = CaptchaField()

class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = ['title', 'content', 'content_bb', 'price', 'rubric']