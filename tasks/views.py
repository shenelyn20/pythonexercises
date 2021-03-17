from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

#tasks = ["foo", "bar", "baz "]

class NewTaskForm(forms.Form): #form class that inherits built in form lib from Django
    task = forms.CharField(label="New Task") #textfield for task
                                            # Using View Page Source on html, it shows that the name created in html
                                            #is the same as variable name
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=5) #integerfield for priority
                                                                            # min and max val = built in client side validation

def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", { #renders the index.html page
        #"tasks": tasks  #will be passed the array list of ["foo", "bar", "baz "] to "tasks" name which is accessible by html
                    #key "tasks" is a string name accessible by html
        "tasks": request.session["tasks"]
    })

def add(request):
    if request.method == "POST": #if user submits data while on route add
        #process the result of request
        form = NewTaskForm(request.POST) #populates form using data input submitted by the user 
        if form.is_valid(): #valid client side
            task = form.cleaned_data["task"]#form.cleaned data gives access to all data submitted by the user
                                            #accessed the string task provided 
            #tasks.append(task)
            print(request.session["tasks"])
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
            #reverse engineer to find the url
        else: #server side validation
            return render (request, "tasks/add.html", {
                "form": form #instead of sending back a new form like below,
                            # existing form data will be sent back so the user so 
                            # it displays error information that may come up
            })
    return render(request, "tasks/add.html",{ #default return of accessed add route, when user get the page
        "form": NewTaskForm() #creates a blank form
    })