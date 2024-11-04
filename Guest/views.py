from django.shortcuts import render,redirect
from Admin.models import tbl_district,tbl_place,tbl_admin
from Guest.models import *
# Create your views here.

def designer(request):
    district = tbl_district.objects.all()
    if request.method == "POST":
        tbl_designer.objects.create(
            designer_name = request.POST.get("txt_name"),
            designer_contact = request.POST.get("txt_contact"),
            designer_email = request.POST.get("txt_email"),
            designer_address = request.POST.get("txt_address"),
            designer_password = request.POST.get("txt_password"),
            designer_photo = request.FILES.get("txt_photo"),
            designer_proof = request.FILES.get("txt_proof"),
            place = tbl_place.objects.get(id=request.POST.get("sel_place")))
        return render(request,"Guest/Designer.html",{"msg":"You Registered Successfully"})
    else:
        return render(request,"Guest/Designer.html",{"district":district})

def company(request):
    district = tbl_district.objects.all()
    if request.method == "POST":
        tbl_company.objects.create(
            company_name = request.POST.get("txt_name"),
            company_contact = request.POST.get("txt_contact"),
            company_email = request.POST.get("txt_email"),
            company_address = request.POST.get("txt_address"),
            company_password = request.POST.get("txt_password"),
            company_logo = request.FILES.get("txt_photo"),
            company_proof = request.FILES.get("txt_proof"),
            place = tbl_place.objects.get(id=request.POST.get("sel_place")))
        return render(request,"Guest/Company.html",{"msg":"You Registered Successfully"})
    else:
        return render(request,"Guest/Company.html",{"district":district})

def ajaxplace(request):
    place = tbl_place.objects.filter(district=request.GET.get("did"))
    return render(request,"Guest/AjaxPlace.html",{"place":place})

def login(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        companycount = tbl_company.objects.filter(company_email=email,company_password=password).count()
        designercount = tbl_designer.objects.filter(designer_email=email, designer_password=password).count()
        admincount = tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        if companycount > 0:
            company = tbl_company.objects.get(company_email=email, company_password=password)
            if company.company_status == 0:
                return render(request,"Guest/Login.html",{"msg":"Your Registration is Pending"})
            elif company.company_status == 2:
                return render(request,"Guest/Login.html",{"msg":"Your Registration is Rejected"})
            else:
                request.session["cid"] = company.id
                return redirect("Company:homepage")
        elif designercount > 0:
            designer = tbl_designer.objects.get(designer_email=email, designer_password=password)
            if designer.designer_status == 0:
                return render(request,"Guest/Login.html",{"msg":"Your Registration is Pending"})
            elif designer.designer_status == 2:
                return render(request,"Guest/Login.html",{"msg":"Your Registration is Rejected"})
            else:
                request.session["did"] = designer.id
                return redirect("Designer:homepage")
        elif admincount > 0:
            admin = tbl_admin.objects.get(admin_email=email, admin_password=password)
            request.session["aid"] = admin.id
            return redirect("Admin:homepage")
        else:
            return render(request,"Guest/Login.html",{"msg":"Invalid Email or Password"})
    else:
        return render(request,"Guest/Login.html")

def index(request):
    return render(request,"Guest/index.html")