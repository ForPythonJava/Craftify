from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime,date
from django.core.mail import send_mail

# Create your views here.


# def send_email(request):
#     if request.POST:
#         sub=request.POST['subject']
#         msg=request.POST['message']
#         receiver=request.POST['receiver']

#         from_email = 'forpythonjava@gmail.com'
#         recipient_list = [receiver]
#         result=send_mail(sub, msg, from_email, recipient_list)
#         print(result)
#     return render(request,"sendMail.html")

def logout(request):
    request.session.clear()
    messages.success(request, "Logged Out")
    return HttpResponseRedirect("/signin")


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def userRegister(request):
    return render(request, "COMMON/userRegister.html")


def artistRegister(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        address = request.POST["address"]
        skill = request.POST.getlist("skills")
        sk=str(skill)
        cleaned_word = sk.replace("[", "").replace("]", "").replace("'", "")# Retrieve the submitted skills value
        images = request.FILES.getlist("image") 
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email Already Exists")
        else:
            logQry=Login.objects.create_user(username=email,password=password,userType="Artist",viewPass=password,is_active=0)
            logQry.save()
            if logQry:
                artistReg=Artist.objects.create(name=name,email=email,phone=phone,address=address,skills=cleaned_word,image1=images[0],image2=images[1],image3=images[2],loginid=logQry)
                artistReg.save()
                messages.success(request,"Registration Successfull")
                return redirect("/signin")
        #skills = request.POST.getlist("skills")  # Retrieve the submitted skills value
        # skills_list = [skill.strip() for skill in skills.split(",") if skill.strip()]  # Split the skills string into a list
        # print(skills_list)
        # print(skills)
        # print(images)
        # print( "# Retrieve the submitted skills value")
        # print(images)
    return render(request, "COMMON/artistRegister.html")

def signin(request):
    if request.POST:
        email=request.POST['email']
        password=request.POST['password']
        try:
            userData=Login.objects.get(username=email)
            if userData:
                if userData.userType == "Artist":
                    checkPayStatus=Artist.objects.get(email=email)
                    if checkPayStatus.status == "Not Paid":
                        request.session['payMail']=email
                        messages.error(request,"Please Complete Payment 💸 To Login")
                        return redirect("/payFees")
                    else:
                        artist = authenticate(username=email, password=password)
                        if artist is not None:
                            id=artist.id
                            request.session["uid"] = id
                            messages.info(request, "Login Success")
                            return redirect("/artistHome")
                        else:
                            messages.error(request,"You Are Not Approved yet...Please Wait🙂")
                elif userData.userType == "User":
                    id = userData.id
                    request.session["uid"] = id
                    request.session["type"] = "User"
                    messages.info(request, "Login Success")
                    return redirect("/userHome")
                elif userData.userType == "Admin":
                    request.session["type"] = "Admin"
                    messages.info(request, "Login Success")
                    return redirect("/adminHome")
        except:
            messages.error(request,"Incorrect Email/Password..😥")
    return render(request, "COMMON/login.html")


######################################################--ARTIST--#########################################################

def artistHome(request):
    uid=request.session['uid']
    current_date = date.today()
    CheckPay=Login.objects.get(id=uid)
    rgDate=CheckPay.regDate
    diff=current_date-rgDate
    days=diff.days
    print(days)
    if days>=30:
        changeStatus=Artist.objects.filter(loginid=uid).update(status="Not Paid")
        messages.error(request,"Your membership has expired. Please renew to continue using our services.")
        return redirect("/logout")
    else:
        print("Helloo")
    return render(request,"ARTIST/artistHome.html")

def payFees(request):
    current_date = date.today()
    payMail=request.session['payMail']
    cartTotal=750
    if request.POST:
        payStatus=Artist.objects.get(email=payMail)
        payStatus.status='Paid'
        payStatus.save()
        regDate=Login.objects.get(username=payMail)
        regDate.regDate=current_date
        regDate.save()
        messages.success(request,"Payment Successfull..😀 Proceed to Login")
        return redirect("/signin")
    return render(request,"ARTIST/payFees.html",{"cartTotal":cartTotal})


######################################################--ADMIN--#########################################################


def adminViewArtist(request):
    data=Artist.objects.filter(status='Paid')
    return render(request,"ADMIN/adminViewArtist.html",{"data":data})

def manageRequest(request):
    id = request.GET["id"]
    status = request.GET["status"]
    updateData = Login.objects.get(id=id)
    if status == 'Approved':
        updateData.is_active=1
        updateData.save()
    elif status == 'Rejected':
        updateData.is_active=0
        updateData.save()
    else:
        updateData = Artist.objects.get(id=id).delete()
    messages.success(request, f"Request {status}")
    return redirect("/adminViewArtist")

def adminHome(request):
    return render(request,"ADMIN/adminHome.html")
######################################################--USER--#########################################################
def userHome(request):
    return render(request,"USER/userHome.html")