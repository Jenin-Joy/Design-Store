from django.urls import path
from Admin import views
app_name = "Admin"

urlpatterns = [
    path("homepage/",views.homepage,name="homepage"),
    
    path("district/",views.district,name="district"),
    path("deletedistrict/<int:id>",views.deletedistrict,name="deletedistrict"),
    path("editdistrict/<int:id>",views.editdistrict,name="editdistrict"),

    path("place/",views.place,name="place"),
    path("deleteplace/<int:id>",views.deleteplace,name="deleteplace"),
    path("editplace/<int:id>",views.editplace,name="editplace"),

    path("adminreg/",views.adminreg,name="adminreg"),
    path("deleteadmin/<int:id>",views.deleteadmin,name="deleteadmin"),
]