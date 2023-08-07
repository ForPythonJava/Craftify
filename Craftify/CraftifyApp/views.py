from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime, date
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

def about(request):
    return render(request,"COMMON/about.html")

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
        sk = str(skill)
        cleaned_word = (
            sk.replace("[", "").replace("]", "").replace("'", "")
        )  # Retrieve the submitted skills value
        images = request.FILES.getlist("image")
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email Already Exists")
        else:
            logQry = Login.objects.create_user(
                username=email,
                password=password,
                userType="Artist",
                viewPass=password,
                is_active=0,
            )
            logQry.save()
            if logQry:
                artistReg = Artist.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    address=address,
                    skills=cleaned_word,
                    image1=images[0],
                    image2=images[1],
                    image3=images[2],
                    loginid=logQry,
                )
                artistReg.save()
                messages.success(request, "Registration Successfull")
                return redirect("/signin")
    return render(request, "COMMON/artistRegister.html")


def userRegister(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        address = request.POST["address"]

        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email Already Exists")
        else:
            logQry = Login.objects.create_user(
                username=email,
                password=password,
                userType="User",
                viewPass=password,
                is_active=1,
            )
            logQry.save()
            if logQry:
                userReg = User.objects.create(
                    name=name, email=email, phone=phone, address=address, loginid=logQry
                )
                userReg.save()
                messages.success(request, "Registration Successfull")
                return redirect("/signin")
    return render(request, "COMMON/userRegister.html")


def signin(request):
    if request.POST:
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            userData = Login.objects.get(username=email)
            if userData:
                if userData.userType == "Artist":
                    checkPayStatus = Artist.objects.get(email=email)
                    if checkPayStatus.status == "Not Paid":
                        request.session["payMail"] = email
                        messages.error(request, "Please Complete Payment 💸 To Login")
                        return redirect("/payFees")
                    else:
                        artist = authenticate(username=email, password=password)
                        print(artist)
                        if artist is not None:
                            id = artist.id
                            request.session["uid"] = id
                            messages.info(request, "Login Success")
                            return redirect("/artistHome")
                        else:
                            messages.error(
                                request, "You Are Not Approved yet...Please Wait🙂"
                            )
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
            messages.error(request, "Incorrect Email/Password..😥")
    return render(request, "COMMON/login.html")


######################################################--ARTIST--#########################################################


def artistHome(request):
    uid = request.session["uid"]
    current_date = date.today()
    CheckPay = Login.objects.get(id=uid)
    rgDate = CheckPay.regDate
    diff = current_date - rgDate
    days = diff.days
    print(days)
    if days >= 30:
        changeStatus = Artist.objects.filter(loginid=uid).update(status="Not Paid")
        messages.error(
            request,
            "Your membership has expired. Please renew to continue using our services.",
        )
        return redirect("/logout")
    else:
        print("Helloo")
    return render(request, "ARTIST/artistHome.html")


def payFees(request):
    current_date = date.today()
    payMail = request.session["payMail"]
    cartTotal = 750
    if request.POST:
        payStatus = Artist.objects.get(email=payMail)
        payStatus.status = "Paid"
        payStatus.save()
        regDate = Login.objects.get(username=payMail)
        regDate.regDate = current_date
        regDate.save()
        messages.success(request, "Payment Successfull..😀 Proceed to Login")
        return redirect("/signin")
    return render(request, "ARTIST/payFees.html", {"cartTotal": cartTotal})


def profile(request):
    uid = request.session["uid"]
    myProfile = Artist.objects.get(loginid_id__id=uid)
    print(myProfile)
    return render(request, "ARTIST/profile.html", {"myProfile": myProfile})


def updateProfile(request):
    uid = request.session["uid"]
    myProfile = Artist.objects.get(loginid_id__id=uid)
    print(myProfile)

    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        address = request.POST["address"]
        skill = request.POST.getlist("skills")
        sk = str(skill)
        cleaned_word = (
            sk.replace("[", "").replace("]", "").replace("'", "")
        )  # Retrieve the submitted skills value
        images = request.FILES.getlist("image")

        updateProfile = Artist.objects.get(loginid=uid)
        updateProfile.name = name
        updateProfile.email = email
        updateProfile.phone = phone
        updateProfile.address = address
        updateProfile.skills = cleaned_word
        updateProfile.image1 = images[0]
        updateProfile.image2 = images[1]
        updateProfile.image3 = images[2]
        updateProfile.save()

        updateLogin = Login.objects.get(id=uid)
        updateLogin.username = email
        updateLogin.set_password(password)
        updateLogin.viewPass = password
        updateLogin.save()
        messages.success(request, "Profile Updated")
        return redirect("/profile")
    return render(request, "ARTIST/updateProfile.html", {"myProfile": myProfile})


def addItems(request):
    id = request.session["uid"]
    uid = Artist.objects.get(loginid=id)
    options = [
        "Jewelry",
        "Home Decor",
        "Pet Accessories",
        "Toys and Games",
        "Art and Craft Supplies",
        "Clothing and Accessories",
        "Beauty and Personal Care",
        "Stationery and Paper Goods",
        "Clay Pottery",
        "Bottle Art"
    ]
    if request.POST:
        name = request.POST["pdtname"]
        category = request.POST["category"]
        price = request.POST["price"]
        color = request.POST["color"]
        qty = request.POST["qty"]
        images = request.FILES.getlist("image")
        desc = request.POST["desc"]
        addItems = Products.objects.create(
            name=name,
            category=category,
            price=price,
            color=color,
            qty=qty,
            image=images[0],
            image1=images[1],
            image2=images[2],
            desc=desc,
            artistId=uid,
        )
        addItems.save()
        messages.success(request, "Product Added")
        return redirect("/viewItems")
    return render(request, "ARTIST/addItems.html", {"options": options})


def viewItems(request):
    uid = request.session["uid"]
    items = Products.objects.filter(artistId__loginid=uid)
    print(items)
    return render(request, "ARTIST/viewItems.html", {"items": items})


def deleteProduct(request):
    id = request.GET["id"]
    deletePdt = Products.objects.get(id=id).delete()
    messages.success(request, "Product Deleted")
    return redirect("/viewItems")


def updateProduct(request):
    id = request.GET["id"]
    options = [
        "Jewelry",
        "Home Decor",
        "Pet Accessories",
        "Toys and Games",
        "Art and Craft Supplies",
        "Clothing and Accessories",
        "Beauty and Personal Care",
        "Stationery and Paper Goods",
    ]
    pdtData = Products.objects.get(id=id)
    if request.POST:
        name = request.POST["pdtname"]
        category = request.POST["category"]
        price = request.POST["price"]
        color = request.POST["color"]
        qty = request.POST["qty"]
        image = request.FILES["image"]
        desc = request.POST["desc"]

        updateProduct = Products.objects.get(id=id)
        updateProduct.name = name
        updateProduct.category = category
        updateProduct.price = price
        updateProduct.color = color
        updateProduct.qty = qty
        updateProduct.image = image
        updateProduct.desc = desc
        updateProduct.save()
        messages.success(request, "Details Updated")
        return redirect("/viewItems")
    return render(request, "ARTIST/updateProduct.html", {"pdtData": pdtData, "category": options})
    
def viewRating(request):
    uid=request.session['uid']
    pdtData = Products.objects.filter(artistId__loginid=uid)
    rating = Feedback.objects.filter(oid__pid__artistId__loginid_id=uid)
    print(rating)
    combined_data = zip(pdtData, rating)
    merged_query = list(combined_data)
    print("MERGED",merged_query)
    return render(request,"ARTIST/viewratings.html",{"data":merged_query})


######################################################--ADMIN--#########################################################


def adminViewArtist(request):
    data = Artist.objects.filter(status="Paid")
    return render(request, "ADMIN/adminViewArtist.html", {"data": data})


def manageRequest(request):
    id = request.GET["id"]
    status = request.GET["status"]
    updateData = Login.objects.get(id=id)
    if status == "Approved":
        updateData.is_active = 1
        updateData.save()
    elif status == "Rejected":
        updateData.is_active = 0
        updateData.save()
    else:
        updateData = Artist.objects.get(id=id).delete()
    messages.success(request, f"Request {status}")
    return redirect("/adminViewArtist")


def adminHome(request):
    pdtData=Products.objects.all().order_by('-id')[:4]
    return render(request, "ADMIN/adminHome.html",{"pdtData":pdtData})


def adminViewProducts(request):
    productData = Products.objects.all()
    return render(request, "ADMIN/adminViewProducts.html", {"productData": productData})


def approveProduct(request):
    id = request.GET["id"]
    approvePdt = Products.objects.filter(id=id).update(status="Approved")
    return redirect("/adminViewProducts")


def admindeleteProduct(request):
    id = request.GET["id"]
    deletePdt = Products.objects.filter(id=id).delete()
    return redirect("/adminViewProducts")


######################################################--USER--#########################################################
def userHome(request):
    uid = request.session['uid']
    matching_categories = Cart.objects.filter(uid__loginid=uid).values_list('pid__category', flat=True).distinct()
    print(matching_categories)

    common_products = Products.objects.filter(Q(category__in=matching_categories)&Q(status="Approved"))
    return render(request, "USER/userHome.html",{"common_products":common_products})


def userViewProduct(request):
    uid = request.session["uid"]
    wishListData = Wishlist.objects.filter(uid__loginid=uid).values_list(
        "pid", flat=True
    )
    print(wishListData)
    productData = Products.objects.filter(status="Approved")
    return render(
        request,
        "USER/viewProducts.html",
        {"productData": productData, "wishListData": wishListData},
    )


def addToCart(request):
    uid = request.session["uid"]
    userid = User.objects.get(loginid=uid)
    if request.POST:
        qty = request.POST["qty"]
        pid = request.POST["pid"]
        price = request.POST["price"]
        total = int(price) * int(qty)
        pdtid = Products.objects.get(id=pid)
        addToCart = Cart.objects.create(
            uid=userid, pid=pdtid, quantity=qty, price=total
        )
        addToCart.save()
        stock = pdtid.qty
        finalstock = int(stock) - int(qty)
        updateStock = Products.objects.filter(id=pid).update(qty=finalstock)
        messages.success(request, "Added To Cart")
    return redirect("/userViewProduct")


def viewCart(request):
    uid = request.session["uid"]
    cartData = Cart.objects.filter(Q(uid__loginid=uid) & Q(status="InCart"))
    if not cartData.exists():
        messages.error(request, "Cart Is Empty")
        return redirect("/userViewProduct")
    cartTotal = Cart.objects.filter(
        Q(uid_id__loginid__id=uid) & Q(status="InCart")
    ).aggregate(total=Sum("price"))["total"]
    print(cartTotal)
    count = Cart.objects.filter(Q(uid_id__loginid__id=uid) & Q(status="InCart")).count()
    print(count)
    return render(
        request,
        "USER/viewCart.html",
        {"cartData": cartData, "count": count, "cartTotal": cartTotal},
    )


def removeFromCart(request):
    id = request.GET["id"]
    pid = request.GET["pid"]
    qty = request.GET["qty"]

    updatePdt = Products.objects.get(id=pid)
    stock = updatePdt.qty
    uStock = int(stock) + int(qty)
    updatePdt.qty = uStock
    updatePdt.save()
    updateCart = Cart.objects.get(id=id).delete()
    messages.success(request, "Product Removed")
    return redirect("/viewCart")


def paymentForm(request):
    id = request.GET["id"]
    cartData = Cart.objects.get(id=id)
    cartTotal = cartData.price
    if request.POST:
        updateStatus = Cart.objects.filter(id=id).update(status="Paid")
        messages.success(request, "Payment Success")
        return redirect("/viewOrders")
    return render(request, "USER/paymentForm.html", {"cartTotal": cartTotal})


def checkOut(request):
    uid = request.session["uid"]
    myCart = Cart.objects.filter(Q(uid_id__loginid__id=uid) & Q(status="InCart"))
    id_list = myCart.values_list("id", flat=True)
    cartTotal = Cart.objects.filter(
        Q(uid_id__loginid__id=uid) & Q(status="InCart")
    ).aggregate(total=Sum("price"))["total"]
    print(id_list)
    for i in id_list:
        print(i)
    if request.POST:
        for i in id_list:
            updateStatus = Cart.objects.filter(id=i).update(status="Paid")
        return redirect("/viewOrders")
    return render(request, "USER/paymentForm.html", {"cartTotal": cartTotal})


def viewOrders(request):
    uid = request.session["uid"]
    orderData = Cart.objects.filter(Q(uid_id__loginid__id=uid) & Q(status="Paid"))
    fdbkData = Feedback.objects.filter(uid__loginid=uid)
    print(fdbkData)
    id_list = fdbkData.values_list("oid__pid", flat=True)
    print(id_list)
    
    return render(
        request, "USER/viewOrders.html", {"orderData": orderData, "id_list": id_list}
    )


def addToWishList(request):
    id = request.GET["id"]
    uid = request.session["uid"]
    userid = User.objects.get(loginid=uid)
    pdtid = Products.objects.get(id=id)
    addWishList = Wishlist.objects.create(uid=userid, pid=pdtid)
    addWishList.save()
    messages.success(request, "Added to Wishlist")
    return redirect("/userViewProduct")


def removeFromWishList(request):
    id = request.GET["id"]
    uid = request.session["uid"]
    deleteWish = Wishlist.objects.filter(Q(pid_id=id) & Q(uid__loginid=uid)).delete()
    messages.success(request, "Removed from Wishlist")
    return redirect("/userViewProduct")


def wishList(request):
    uid = request.session["uid"]
    wishListData = Wishlist.objects.filter(uid__loginid=uid)
    return render(request, "USER/wishList.html", {"wishListData": wishListData})


def addFeedback(request):
    uid = request.session["uid"]
    userid = User.objects.get(loginid=uid)
    id = request.GET["id"]
    order_id = Cart.objects.get(id=id)
    if request.POST:
        rating = request.POST["rating"]
        review = request.POST["review"]
        addFdbk = Feedback.objects.create(
            uid=userid, oid=order_id, rating=rating, review=review
        )
        addFdbk.save()
        messages.success(request, "Feedback Added")
        return redirect("/viewOrders")
    return render(request, "USER/addFeedback.html")


def addAddress(request):
    id=request.GET.get("id")
    if id:
        if request.POST:
            name=request.POST['name']
            email=request.POST['email']
            state=request.POST['state']
            pincode=request.POST['pincode']
            address=request.POST['address']
            updateAddress=Cart.objects.filter(id=id).update(name=name,email=email,state=state,pincode=pincode,address=address)
            return redirect("/paymentForm?id="+id)
    else:
        uid = request.session["uid"]
        myCart = Cart.objects.filter(Q(uid_id__loginid__id=uid) & Q(status="InCart"))
        id_list = myCart.values_list("id", flat=True)
        if request.POST:
            name=request.POST['name']
            email=request.POST['email']
            state=request.POST['state']
            pincode=request.POST['pincode']
            address=request.POST['address']
            for i in id_list:
                updateStatus = Cart.objects.filter(id=i).update(name=name,email=email,state=state,pincode=pincode,address=address)
            return redirect("/checkOut")
    return render(request,"USER/addAddress.html")


def viewProductCategory(request):
    category=request.GET['category']
    productData=Products.objects.filter(category=category)
    print(productData)
    return render(request,"USER/viewProductCategory.html",{"productData":productData})

def userProfile(request):
    uid=request.session['uid']
    userData=User.objects.get(loginid__id=uid)
    print(userData)
    return render(request,"USER/userProfile.html",{"myProfile":userData})

def profileUpdate(request):
    uid=request.session['uid']
    userData=User.objects.get(loginid__id=uid)
    print(userData)
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        address = request.POST["address"]
        updateUser=User.objects.filter(loginid__id=uid).update(name=name,email=email,phone=phone,address=address)

        updateLogin = Login.objects.get(id=uid)
        updateLogin.username = email
        updateLogin.set_password(password)
        updateLogin.viewPass = password
        updateLogin.save()
        messages.success(request, "Profile Updated")
        return redirect("/userProfile")
    return render(request,"USER/profileUpdate.html",{"myProfile":userData})


def productView(request):
    pid=request.GET['id']
    pdtData=Products.objects.get(id=pid)
    return render(request,"USER/productView.html",{"pdtData":pdtData})

########################################### Chat Section###########################################

def chat(request):
    uid = request.session["uid"]
    # Artists
    name=""
    artistData = Artist.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(Q(uid__loginid=uid) & Q(artistid=id))
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")
    userid = User.objects.get(loginid__id=uid)
    if id:
        artistid = Artist.objects.get(id=id)
        name=artistid.name
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(uid=userid,message=message,artistid=artistid,time=formatted_time,utype="USER")
        sendMsg.save()
    return render(request,"USER/chat.html",{"artistData": artistData, "getChatData": getChatData,"artistid":name})


def reply(request):
    uid = request.session["uid"]
    print(uid)
    name=""
    userData = User.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(Q(artistid__loginid=uid) & Q(uid=id))
    print(getChatData)
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")
    artistid = Artist.objects.get(loginid__id=uid)
    if id:
        userid = User.objects.get(id=id)
        name=userid.name
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(uid=userid,message=message,artistid=artistid,time=formatted_time,utype="ARTIST")
        sendMsg.save()
    return render(request,"ARTIST/chat.html",{"userData": userData, "getChatData": getChatData,"userid":name})