from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from Designer.models import *
# Create your views here.

def homepage(request):
    if "aid" in request.session:
        return render(request,"Admin/HomePage.html")
    else:
        return redirect("Guest:login")

def logout(request):
    del request.session["aid"]
    return redirect("Guest:login")

def district(request):
    if "aid" in request.session:
        district = tbl_district.objects.all()
        if request.method == "POST":
            tbl_district.objects.create(district_name=request.POST.get('txt_name'))
            return render(request,"Admin/District.html",{"msg":"Data Inserted"})
        else:
            return render(request,"Admin/District.html",{"district":district})
    else:
        return redirect("Guest:login")

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
    if "aid" in request.session:
        district = tbl_district.objects.all()
        place = tbl_place.objects.all()
        if request.method == "POST":
            tbl_place.objects.create(place_name=request.POST.get('txt_name'), district=tbl_district.objects.get(id=request.POST.get('sel_district')))
            return render(request,"Admin/Place.html",{"msg":"Data Inserted"})
        else:
            return render(request,"Admin/Place.html",{"place":place,"district":district})
    else:
        return redirect("Guest:login")

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
    if "aid" in request.session:
        admin = tbl_admin.objects.all()
        if request.method == "POST":
            tbl_admin.objects.create(admin_name=request.POST.get('txt_name'), admin_email=request.POST.get('txt_email'), admin_password=request.POST.get('txt_password'))
            return render(request,"Admin/AdminReg.html",{"msg":"Data Inserted"})
        else:
            return render(request,"Admin/AdminReg.html",{"admin":admin})
    else:
        return redirect("Guest:login")

def deleteadmin(request,id):
    tbl_admin.objects.get(id=id).delete()
    return render(request,"Admin/AdminReg.html",{"msg":"Data Deleted"})

def company(request):
    if "aid" in request.session:
        company = tbl_company.objects.filter(company_status=0)
        return render(request,"Admin/NewCompany.html",{'company':company})
    else:
        return redirect("Guest:login")

def verifycompany(request, id, status):
    company = tbl_company.objects.get(id=id)
    company.company_status = status
    company.save()
    return render(request,"Admin/HomePage.html",{"msg":"Company Verified"})

def acceptedcompany(request):
    if "aid" in request.session:
        company = tbl_company.objects.filter(company_status=1)
        return render(request,"Admin/AcceptedCompany.html",{'company':company})
    else:
        return redirect("Guest:login")
    
def rejectedcompany(request):
    if "aid" in request.session:
        company = tbl_company.objects.filter(company_status=2)
        return render(request,"Admin/RejectedCompany.html",{'company':company})
    else:
        return redirect("Guest:login")

def designer(request):
    if "aid" in request.session:
        designer = tbl_designer.objects.filter(designer_status=0)
        return render(request,"Admin/NewDesigner.html",{'designer':designer})
    else:
        return redirect("Guest:login")

def verifydesigner(request, id, status):
    designer = tbl_designer.objects.get(id=id)
    designer.designer_status = status
    designer.save()
    return render(request,"Admin/HomePage.html",{"msg":"Designer Verified"})

def accepteddesigner(request):
    if "aid" in request.session:
        designer = tbl_designer.objects.filter(designer_status=1)
        return render(request,"Admin/AcceptedDesigner.html",{'designer':designer})
    else:
        return redirect("Guest:login")
    
def rejecteddesigner(request):
    if "aid" in request.session:
        designer = tbl_designer.objects.filter(designer_status=2)
        return render(request,"Admin/RejectedDesigner.html",{'designer':designer})
    else:
        return redirect("Guest:login")

def viewdesign(request):
    if "aid" in request.session:
        design = tbl_design.objects.all()
        return render(request,"Admin/ViewDesign.html",{"design":design})
    else:
        return redirect("Guest:login")

def viewcomplaint(request):
    if "aid" in request.session:
        complaint = tbl_complaint.objects.filter(complaint_status=0)
        return render(request,"Admin/ViewComplaint.html",{"complaint":complaint})
    else:
        return redirect("Guest:login")

def reply(request, id):
    if request.method == "POST":
        complaint = tbl_complaint.objects.get(id=id)
        complaint.complaint_status = 1
        complaint.complaint_reply = request.POST.get("txt_reply")
        complaint.save()
        return render(request,"Admin/Reply.html",{"msg":"Reply Sent"})
    else:
        return render(request,"Admin/Reply.html")

def replyedcomplaint(request):
    if "aid" in request.session:
        complaint = tbl_complaint.objects.filter(complaint_status=1)
        return render(request,"Admin/ReplyedComplaint.html",{"complaint":complaint})
    else:
        return redirect("Guest:login")