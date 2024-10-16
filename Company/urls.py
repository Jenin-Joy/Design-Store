from django.urls import path
from Company import views
app_name = "Company"

urlpatterns = [
    path("homepage",views.homepage,name="homepage"),

    path("profile/",views.profile,name="profile"),
    path("editprofile/",views.editprofile,name="editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),

    path("viewdesign/",views.viewdesign,name="viewdesign"),
    path("viewdesigndetails/<int:id>",views.viewdesigndetails,name="viewdesigndetails"),

    path('payment/<int:id>',views.payment,name="payment"),
    path('loader/', views.loader, name='loader'),
    path('paymentsuc/', views.paymentsuc, name='paymentsuc'),

    path('buydesign/', views.buydesign, name='buydesign'),
]