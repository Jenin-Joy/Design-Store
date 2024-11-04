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

    path("company/",views.company,name="company"),
    path("verifycompany/<int:id>/<int:status>",views.verifycompany,name="verifycompany"),
    path("acceptedcompany/",views.acceptedcompany,name="acceptedcompany"),
    path("rejectedcompany/",views.rejectedcompany,name="rejectedcompany"),

    path("designer/",views.designer,name="designer"),
    path("verifydesigner/<int:id>/<int:status>",views.verifydesigner,name="verifydesigner"),
    path("accepteddesigner/",views.accepteddesigner,name="accepteddesigner"),
    path("rejecteddesigner/",views.rejecteddesigner,name="rejecteddesigner"),

    path("viewdesign/",views.viewdesign,name="viewdesign"),

    path("viewcomplaint/",views.viewcomplaint,name="viewcomplaint"),
    path("reply/<int:id>",views.reply,name="reply"),
    path("replyedcomplaint/",views.replyedcomplaint,name="replyedcomplaint"),

    path("logout/",views.logout,name="logout"),
]