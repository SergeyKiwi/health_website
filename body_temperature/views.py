from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.views.generic import (
    CreateView,
)
from .models import TemperatureMeasurement
from .forms import TemperatureMeasurementForm


@require_GET
def index(request):
    top1_measurement_for_users = TemperatureMeasurement.objects.top_10_newest_users_measurement()
    dt_last_measurement = TemperatureMeasurement.objects.dt_last_measurement()
    average_temperature = TemperatureMeasurement.objects.average_temperature()
    users_count = User.objects.count()
    top1_measurement_for_users_gte37 = TemperatureMeasurement.objects.users_with_temperature_gte_37()
    context = {
        'top1_measurement_for_users': top1_measurement_for_users,
        'dt_last_measurement': dt_last_measurement,
        'average_temperature': average_temperature,
        'users_count': users_count,
        'top1_measurement_for_users_gte37': top1_measurement_for_users_gte37
    }
    return render(request, 'body_temperature/home.html', context=context)


@require_GET
def user_measurements(request, id):
    user = get_object_or_404(User, id=id)
    try:
        measurements = TemperatureMeasurement.objects.filter(user=user).order_by('-datetime_measurement')
        average_temperature = TemperatureMeasurement.objects.average_temperature_for_user(user)
        date_interval_for_user = TemperatureMeasurement.objects.date_interval_for_user(user)
        date_interval_for_user = td_format(date_interval_for_user)
    except ObjectDoesNotExist:
        measurements = None
        average_temperature = None
        date_interval_for_user = None
    context = {
        'measurements': measurements,
        'person': user,
        'average_temperature': average_temperature,
        'date_interval_for_user': date_interval_for_user
    }
    return render(request, 'body_temperature/user_measurements.html', context=context)


class UserMeasurementsNew(LoginRequiredMixin, CreateView):
    form_class = TemperatureMeasurementForm
    template_name = 'body_temperature/user_measurements_new.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bt_measurements_id', kwargs={'id': self.request.user.id})


def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('(годы)',        60*60*24*365),
        ('(месяцы)',       60*60*24*30),
        ('(дни)',         60*60*24),
        ('(часы)',        60*60),
        ('(минуты)',      60),
        ('(секунды)',      1)
    ]
    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            strings.append("%s %s" % (period_value, period_name))

    return ", ".join(strings)
