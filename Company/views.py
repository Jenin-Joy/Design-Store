from django.shortcuts import render,redirect
from Guest.models import tbl_company
from Designer.models import tbl_design, tbl_designcopyright
import os
import cv2
import numpy as np
# Create your views here.

def homepage(request):
    return render(request,"Company/HomePage.html")

def profile(request):
    company = tbl_company.objects.get(id=request.session["cid"])
    return render(request,"Company/MyProfile.html",{"company":company})

def editprofile(request):
    company = tbl_company.objects.get(id=request.session["cid"])
    if request.method == "POST":
        company.company_name = request.POST["txt_name"]
        company.company_email = request.POST["txt_email"]
        company.company_contact = request.POST["txt_contact"]
        company.save()
        return render(request,"Company/MyProfile.html",{"msg":"Profile updated"})
    else:
        return render(request,"Company/EditProfile.html",{"company":company})

def changepassword(request):
    company = tbl_company.objects.get(id=request.session["cid"])
    if request.method == "POST":
        old_password = request.POST["txt_old"]
        new_password = request.POST["txt_new"]
        confirm_password = request.POST["txt_con"]
        if company.company_password == old_password:
            if new_password == confirm_password:
                company.company_password = new_password
                company.save()
                return render(request,"Company/MyProfile.html",{"msg":"Password changed"})
            else:
                return render(request,"Company/ChangePassword.html",{"msg":"Confirm Passwords do not match"})
        else:
            return render(request,"Company/ChangePassword.html",{"msg":"Old Password is incorrect"})
    else:
        return render(request,"Company/ChangePassword.html")

def viewdesign(request):
    design = tbl_design.objects.filter(design_status=0)
    return render(request,"Company/View_Design.html",{"design":design})

def viewdesigndetails(request,id):
    design = tbl_design.objects.get(id=id)
    return render(request,"Company/View_details.html",{"design":design})

def payment(request,id):
    design = tbl_design.objects.get(id=id)
    total = design.design_rate
    if request.method == "POST":
        copy = tbl_designcopyright.objects.get(design=id,copyright_status=0)
        copy.company = tbl_company.objects.get(id=request.session["cid"])
        copy.copyright_status = 1
        copy.save()
        design.design_status = 1
        design.save()
        ImageEncode(id,request.session["cid"])
        return redirect("Company:loader")
    else:
        return render(request,"Company/Payment.html",{"total":total})

def loader(request):
    return render(request,"Company/Loader.html")

def paymentsuc(request):
    return render(request,"Company/Payment_suc.html")

def buydesign(request):
    copy = tbl_designcopyright.objects.filter(company = request.session["cid"])
    designid = []
    for i in copy:
        designid.append(i.design.id)
    design = tbl_design.objects.filter(id__in=designid)
    return render(request,"Company/Buy_design.html",{"design":design})

def ImageEncode(designid,companyid):
        ds=tbl_design.objects.get(id=designid)
        photo=ds.design_file.url
        photo=photo[1:]
        # print(photo)
        text=companyid
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