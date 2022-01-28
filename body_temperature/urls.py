from django.urls import path
from .views import index, user_measurements, UserMeasurementsNew

urlpatterns = [
    path('', index, name='bt_index'),
    path('measurements/<int:id>', user_measurements, name='bt_measurements_id'),
    path('measurements/<int:id>/new', UserMeasurementsNew.as_view(), name='bt_measurements_id_new'),
]
