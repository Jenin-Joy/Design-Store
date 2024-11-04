from django.urls import path
from Guest import views
app_name = "Guest"

urlpatterns = [
    path("company/",views.company,name="company"),
    path("designer/",views.designer,name="designer"),
    path("ajaxplace/",views.ajaxplace,name="ajaxplace"),

    path("login/",views.login,name="login"),
    path("",views.index,name="index"),

]