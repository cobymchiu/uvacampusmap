# Hui Wen
# Date made: 24 July 2018
# Web browser Calendar source code
# https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html 
from datetime import timedelta
from datetime import date
import calendar
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import DeleteView
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from .models import *
from .forms import EventForm
from .utils import Calendar
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from geopy.geocoders import Nominatim

def index(request):
    return HttpResponse('hello')

class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/google/login'
    model = Event
    template_name = 'schedule/schedule.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        schedule = Calendar(d.year, d.month)
        # Call the formatmonth method, which returns our calendar as a table
        html_schedule = schedule.formatmonth(user=self.request.user, withyear=True)
        context['calendar'] = mark_safe(html_schedule)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return date.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, event_id=None):
    aut = request.user
    instance = Event(author=aut)
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event(author=aut)
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and 'save' in request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('schedule:schedule'))
    # if user presses the delete button
    if request.POST and 'delete' in request.POST:
        if event_id:
            Event.objects.filter(pk=event_id).delete()
            return HttpResponseRedirect(reverse('schedule:schedule'))
    if request.POST and 'location' in request.POST:
        if event_id:
            address = request.POST.get('address')
            title = request.POST.get('title')
            try:
                geolocator = Nominatim(user_agent="schedule")
                location = geolocator.geocode(str(address))
                args = {}
                args['lat'] = location.latitude
                args['long'] = location.longitude
                args['title'] = title
                return render(request, 'map/MapTemplate3.html', args)
            except:
                return render(request, 'schedule/event.html', {'form': form})
    return render(request, 'schedule/event.html', {'form': form})
# Hui Wen
# Date made: 24 July 2018
# Web browser Calendar source code
# https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html 
