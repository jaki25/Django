from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from .forms import CreateNewList
from .models import ToDoList


# Create your views here.

def index(response, id):
    ls= ToDoList.objects.get(id=id)
    if ls in response.user.todolist.all():
        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c"+str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")

                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("invalid input")
            elif response.POST.get("delete"):

                ls.delete()
                print("****IZBRISANA LISTA----")
                return render(response, "main/view.html", {"ls": ls})
            else:
                for item in ls.item_set.all():
                    if response.POST.get("delItem"+str(item.id)) == "clicked":
                        print(item.text)
                        item.delete()
                        print("uspijesno izbrisan ")
                    else:
                        print("usao u else granu")
                ls.save()
                print("uspijesno sacuvan ")


        return render(response, "main/list.html", {"ls": ls})
    return render(response, "main/view.html", {"ls":ls})

def home(response):
    el=ToDoList.objects.all()
    return render(response, "main/home.html", {"el":el})

def create(response):
    if response.method == "POST":

        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t=ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)

            return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()

    return render(response, "main/create.html", {"form": form})


def view(response):
    return render(response, 'main/view.html', {})
