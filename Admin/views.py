from django.shortcuts import render
from Admin.models import *
# Create your views here.

def homepage(request):
    return render(request,"Admin/HomePage.html")

def district(request):
    district = tbl_district.objects.all()
    if request.method == "POST":
        tbl_district.objects.create(district_name=request.POST.get('txt_name'))
        return render(request,"Admin/District.html",{"msg":"Data Inserted"})
    else:
        return render(request,"Admin/District.html",{"district":district})

def deletedistrict(request,id):
    tbl_district.objects.get(id=id).delete()
    return render(request,"Admin/District.html",{"msg":"Data Deleted"})

def editdistrict(request,id):
    district = tbl_district.objects.get(id=id)
    if request.method == "POST":
        district.district_name = request.POST.get('txt_name')
        district.save()
        return render(request,"Admin/District.html",{"msg":"Data Updated"})
    else:
        return render(request,"Admin/District.html",{"editdistrict":district})

def place(request):
    district = tbl_district.objects.all()
    place = tbl_place.objects.all()
    if request.method == "POST":
        tbl_place.objects.create(place_name=request.POST.get('txt_name'), district=tbl_district.objects.get(id=request.POST.get('sel_district')))
        return render(request,"Admin/Place.html",{"msg":"Data Inserted"})
    else:
        return render(request,"Admin/Place.html",{"place":place,"district":district})

def deleteplace(request,id):
    tbl_place.objects.get(id=id).delete()
    return render(request,"Admin/Place.html",{"msg":"Data Deleted"})

def editplace(request,id):
    place = tbl_place.objects.get(id=id)
    district = tbl_district.objects.all()
    if request.method == "POST":
        place.place_name = request.POST.get('txt_name')
        place.district = tbl_district.objects.get(id=request.POST.get('sel_district'))
        place.save()
        return render(request,"Admin/Place.html",{"msg":"Data Updated"})
    else:
        return render(request,"Admin/Place.html",{"editplace":place,"district":district})

def adminreg(request):
    admin = tbl_admin.objects.all()
    if request.method == "POST":
        tbl_admin.objects.create(admin_name=request.POST.get('txt_name'), admin_email=request.POST.get('txt_email'), admin_password=request.POST.get('txt_password'))
        return render(request,"Admin/AdminReg.html",{"msg":"Data Inserted"})
    else:
        return render(request,"Admin/AdminReg.html",{"admin":admin})

def deleteadmin(request,id):
    tbl_admin.objects.get(id=id).delete()
    return render(request,"Admin/AdminReg.html",{"msg":"Data Deleted"})