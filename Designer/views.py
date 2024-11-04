from django.shortcuts import render,redirect
from Guest.models import tbl_designer,tbl_company
from Designer.models import *
import os
import cv2
import numpy as np

# Create your views here.

def homepage(request):
    if "did" in request.session:
        designer = tbl_designer.objects.get(id=request.session["did"])
        return render(request,"Designer/HomePage.html",{"designer":designer})
    else:
        return redirect("Guest:login")

def logout(request):
    del request.session["did"]
    return redirect("Guest:login")

def profile(request):
    if "did" in request.session:
        designer = tbl_designer.objects.get(id=request.session["did"])
        return render(request,"Designer/MyProfile.html",{"designer":designer})
    else:
        return redirect("Guest:login")

def editprofile(request):
    if "did" in request.session:
        designer = tbl_designer.objects.get(id=request.session["did"])
        if request.method == "POST":
            designer.designer_name = request.POST["txt_name"]
            designer.designer_email = request.POST["txt_email"]
            designer.designer_contact = request.POST["txt_contact"]
            designer.save()
            return render(request,"Designer/MyProfile.html",{"msg":"Profile updated"})
        else:
            return render(request,"Designer/EditProfile.html",{"designer":designer})
    else:
        return redirect("Guest:login")

def changepassword(request):
    if "did" in request.session:
        designer = tbl_designer.objects.get(id=request.session["did"])
        if request.method == "POST":
            old_password = request.POST["txt_old"]
            new_password = request.POST["txt_new"]
            confirm_password = request.POST["txt_con"]
            if designer.designer_password == old_password:
                if new_password == confirm_password:
                    designer.designer_password = new_password
                    designer.save()
                    return render(request,"Designer/MyProfile.html",{"msg":"Password changed"})
                else:
                    return render(request,"Designer/ChangePassword.html",{"msg":"Confirm Passwords do not match"})
            else:
                return render(request,"Designer/ChangePassword.html",{"msg":"Old Password is incorrect"})
        else:
            return render(request,"Designer/ChangePassword.html")
    else:
        return redirect("Guest:login")

def adddesign(request):
    if "did" in request.session:
        design = tbl_design.objects.all()
        if request.method == "POST":
            design = tbl_design.objects.create(
                design_caption=request.POST.get('txt_caption'),
                design_rate=request.POST.get('txt_rate'),
                design_file=request.FILES.get("txt_design"),
                design_description=request.POST.get('txt_description'),
                designer=tbl_designer.objects.get(id=request.session["did"]),
            )
            # print(design)
            tbl_designcopyright.objects.create(
                design = tbl_design.objects.get(id=design.id)
            )
            # ImageEncode(design.id)
            checkdesign = tbl_design.objects.get(id=design.id)
            photo = checkdesign.design_file.url
            photo=photo[1:]
            # print(photo)
            decoded_data = decode(photo)
            # print("decoded_data",decoded_data)
            try:
                designer = tbl_designer.objects.filter(id=decoded_data).count()
                company = tbl_company.objects.filter(id=decoded_data).count()
            except:
                ImageEncode(design.id,request.session["did"])
                return render(request,"Designer/Add_design.html",{"msg":"Design added successfully"})
            if(designer > 0 or company > 0):
                cdesign = tbl_design.objects.get(id=design.id)
                os.remove(str(cdesign.design_file))  # Remove the file
                tbl_designcopyright.objects.get(design=cdesign.id).delete()
                cdesign.delete()
                return render(request,"Designer/Add_design.html",{"msg":"CopyRight Issued By Another User Can not Use This Design"})
            else:
                return render(request,"Designer/Add_design.html",{"design":design})
        else:
            return render(request,"Designer/Add_design.html",{"design":design})
    else:
        return redirect("Guest:login")

def deletedesign(request,id):
    tbl_designcopyright.objects.get(design=id).delete()
    cdesign = tbl_design.objects.get(id=id)
    # print("path" ,type(str(cdesign.design_file)))
    os.remove(str(cdesign.design_file))  # Remove the file
    cdesign.delete()
    return render(request,"Designer/Add_design.html",{"msg":"Design deleted successfully"})

def ImageEncode(designid,designerid):
        ds=tbl_design.objects.get(id=designid)
        photo=ds.design_file.url
        photo=photo[1:]
        # print(photo)
        text=designerid
        text=str(text)
        output_image =  photo
    
    
        encoded_image = Encode(photo,text)
        # print("encoded image", encoded_image)
    
        cv2.imwrite(output_image, encoded_image)
    
        # decoded_data = decode(output_image)
        # print("decoded data :", decoded_data)

        return True
    
def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes):
        return ''.join([ format(i, "08b") for i in data ])
    elif isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

    
def Encode(image_name, secret_data):
    image = cv2.imread(image_name)
    # print('image=',image.shape)
    # maximum bytes to encode
    x=image.shape[0]
    y=image.shape[1]
    n_bytes = image.shape[0] * (image.shape[1]//2) * 3 // 8
    # print("[*] Maximum bytes to encode:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    # print("[*] Encoding data...")
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    for row in image[:x,:y//2,:]:                       #for buyer y//2:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return image

def decode(image_name):

    # print("[+] Decoding...")
    # read the image
    image = cv2.imread(image_name)
    x=image.shape[0]
    y=image.shape[1]
    binary_data = ""
    for row in image[:x,:y//2,:]:                # for buyer y//2:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]

def complaints(request):
    if "did" in request.session:
        complaint = tbl_complaint.objects.filter(designer=request.session["did"])
        if request.method == "POST":
            tbl_complaint.objects.create(complaint_title=request.POST.get("txt_title"),complaint_content=request.POST.get("txt_content"),designer=tbl_designer.objects.get(id=request.session["did"]))
            return render(request,"Designer/Complaint.html",{"msg":"Complaint Send Sucessfully.."})
        else:
            return render(request,"Designer/Complaint.html",{"complaint":complaint})
    else:
        return redirect("Guest:login")

def viewbooking(request):
    if "did" in request.session:
        design = tbl_designcopyright.objects.filter(copyright_status=1,design__designer=request.session["did"])
        return render(request,"Designer/ViewBooking.html",{"booking":design})
    else:
        return redirect("Guest:login")