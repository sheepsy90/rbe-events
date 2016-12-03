import datetime
from django import forms
from django.forms import widgets
from django.forms import ModelForm
from django.utils import timezone

from events.models import Event


class EventForm(ModelForm):

    start_date = forms.CharField(max_length=100, widget=widgets.TextInput(attrs={
        'class': 'form-control date-picker', 'placeholder': "Event start date"
    }))
    start_time = forms.CharField(max_length=100, widget=widgets.TextInput(attrs={
        'class': 'form-control clock', 'placeholder': "Event start time"
    }))

    end_date = forms.CharField(max_length=100, widget=widgets.TextInput(attrs={
        'class': 'form-control date-picker', 'placeholder': "Event end date"
    }), required=False)

    end_time = forms.CharField(max_length=100, widget=widgets.TextInput(attrs={
        'class': 'form-control clock', 'placeholder': "Event end time"
    }))

    class Meta:
        model = Event
        exclude = ['creator', 'begin_time', 'end_time']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.Textarea(attrs={'class': 'form-control'}),
            'language': widgets.Select(attrs={'class': 'form-control'}),
            'medium': widgets.Select(attrs={'class': 'form-control'})
        }

    def _start_datetime(self, cleaned_data):
        start_date = cleaned_data.get("start_date")
        start_time = cleaned_data.get("start_time")

        year, month, day = start_date.split('-')
        hour, minute = start_time.split(':')
        return datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))

    def _end_datetime(self, cleaned_data):
        start_date = cleaned_data.get("start_date")

        end_date = cleaned_data.get("end_date")
        end_time = cleaned_data.get("end_time")

        if not end_date:
            end_date = start_date

        year, month, day = end_date.split('-')
        hour, minute = end_time.split(':')
        return datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))

    @property
    def start_datetime(self):
        return self._start_datetime(self.cleaned_data)

    @property
    def end_datetime(self):
        return self._end_datetime(self.cleaned_data)

    def clean(self):
        cleaned_data = super(EventForm, self).clean()

        try:
            start_datetime = self._start_datetime(cleaned_data)
        except Exception as e:
            raise forms.ValidationError("Start time is not perfect: {}".format(e.message))

        try:
            end_datetime = self._end_datetime(cleaned_data)
        except Exception as e:
            raise forms.ValidationError("Start time is not perfect: {}".format(e.message))

        if start_datetime > end_datetime:
            raise forms.ValidationError("Event cannot end before it begins!")

        if start_datetime < timezone.now():
            raise forms.ValidationError("Event needs to be in the future!")
