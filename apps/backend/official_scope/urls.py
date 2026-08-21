from django.urls import path

from .views import ActiveScopeView

urlpatterns = [path("active/", ActiveScopeView.as_view(), name="active-official-scope")]
