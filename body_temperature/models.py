import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max, F, Avg, Min


class TemperatureMeasurementManager(models.Manager):
    def top_10_newest_users_measurement(self):
        qs = self.annotate(max_dt=Max('user__temperaturemeasurement__datetime_measurement'))\
            .filter(datetime_measurement=F('max_dt')).order_by('-datetime_measurement')[:10]
        return qs

    def dt_last_measurement(self):
        qs = self.order_by('-datetime_measurement').values('datetime_measurement')[:1]
        return qs[0]['datetime_measurement']

    def average_temperature(self):
        qs = self.all().aggregate(Avg('temperature'))
        return qs['temperature__avg']

    def average_temperature_for_user(self, user):
        qs = self.filter(user=user).aggregate(Avg('temperature'))
        return qs['temperature__avg']

    def date_interval_for_user(self, user):
        dt_min = self.filter(user=user).aggregate(Min('datetime_measurement'))
        dt_min = dt_min['datetime_measurement__min']
        dt_max = self.filter(user=user).aggregate(Max('datetime_measurement'))
        dt_max = dt_max['datetime_measurement__max']
        if dt_max is None or dt_min is None:
            dt_delta = datetime.timedelta(0)
        else:
            dt_delta = dt_max - dt_min
        return dt_delta

    def users_with_temperature_gte_37_today(self):
        date_today = datetime.date.today()
        qs = self.filter(datetime_measurement__year=date_today.year,
                         datetime_measurement__month=date_today.month,
                         datetime_measurement__day=date_today.day)\
            .filter(temperature__gte=37)\
            .annotate(max_dt=Max('user__temperaturemeasurement__datetime_measurement'))\
            .filter(datetime_measurement=F('max_dt')).order_by('-datetime_measurement')
        return qs


class TemperatureMeasurement(models.Model):
    objects = TemperatureMeasurementManager()
    temperature = models.FloatField(verbose_name="Температура ({}C)".format(u'\N{DEGREE SIGN}'))
    datetime_measurement = models.DateTimeField(verbose_name="Дата-время измерения")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
