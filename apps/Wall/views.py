from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import datetime
# Create your views here.


def showWall(request):
    context = {
        "messages": Message.objects.all(),
        "message_time": Message.objects.all(),
        "user": Login.objects.get(id=request.session["userid"]),
        # "comments": Comment.objects.all(),
    }
    return render(request, "Wall/Wall.html", context)


def post_message(request):
    if request.method == "POST":
        cur_user = Login.objects.get(id=request.session["userid"])
        Message.objects.create(
            message=request.POST["message"], user=cur_user)
        return redirect("/wall")
    else:
        return render(request, "Wall/Wall.html")


def post_comment(request, message_id):
    if request.method == "POST":
        cur_user = Login.objects.get(id=request.session["userid"])
        which_message = Message.objects.get(id=message_id)
        Comment.objects.create(
            comment=request.POST["comment"], message=which_message, user=cur_user)
        return redirect("/wall")
    else:
        return render(request, "Wall/Wall.html")
    return


def delete_message(request, message_id):
    message_delete = Message.objects.get(id=message_id)
    message_delete.delete()
    return redirect("/wall")


def delete_comment(request, comment_id):
    comment_delete = Comment.objects.get(id=comment_id)
    comment_delete.delete()
    return redirect("/wall")
