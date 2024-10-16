from django.urls import path
from Designer import views
app_name = "Designer"

urlpatterns = [
    path("homepage",views.homepage,name="homepage"),

    path("profile/",views.profile,name="profile"),
    path("editprofile/",views.editprofile,name="editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),

    path("adddesign/",views.adddesign,name="adddesign"),
    path("deletedesign/<int:id>",views.deletedesign,name="deletedesign"),
]