from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django import forms
import bcrypt
# Create your views here.


def index(request):
    return render(request, "login/index.html")


def register(request):
    # include some logic to validate user input before adding them to the database!
    if request.method == "POST":
        errors = Login.objects.basic_validator(request.POST)
        # see if the email provided exists in the database
        all_email = Login.objects.all()
        for single_email in all_email:
            if single_email.email == request.POST["email"]:
                errors["unique"] = "Email already existed in the database"
        if len(errors) > 0:
                # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                    # Adding errors into messages
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            print(errors)
            return redirect("/")
        else:
            print(request.POST)
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print(pw_hash)
            logged_user = Login.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"],
                                               email=request.POST["email"], password=pw_hash, birthday=request.POST["birthday"])
            request.session['userid'] = logged_user.id
            return redirect("/success")
    else:
        return redirect("/")


def login(request):
    # see if the email provided exists in the database
    if request.method == "POST":
        # why are we using filter here instead of get?
        email_exist = Login.objects.filter(email=request.POST['email'])
        if email_exist:  # note that we take advantage of truthiness here: an empty list will return false
            logged_user = email_exist[0]
            # assuming we only have one user with this username, the user would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                # if we get True after checking the password, we may put the user id in session
                request.session['userid'] = logged_user.id
                # never render on a post, always redirect!
                return redirect('/success')
            else:
                print("Password doesn't match")
                return redirect("/")
        # if we didn't find anything in the database by searching by username or if the passwords don't match,
        # redirect back to a safe route
        else:
            print("No email matched")
            return redirect("/")
    else:
        return redirect("/")


def success(request):
    if "userid" in request.session:
        user = Login.objects.get(id=request.session["userid"])
        context = {
            "first_name": user.first_name,
        }
        return render(request, "login/welcome.html", context)
    else:
        return redirect("/")


def logout(request):
    request.session.flush()
    request.session.modified = True
    # delete keys without logging out the user
    # for key in list(request.session.keys()):
    #   if not key.startswith("_"): # skip keys set by the django system
    # del request.session[key]
    return redirect("/")
