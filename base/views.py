#from django.forms.forms import Form
from django.db.models import Q
from django.http import HttpResponse
from django.http.response import HttpResponse
from .models import Room , Topic , Message
from .forms import RoomForm , UserForm ,UserCreateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout 
  
# Create your views here.







def loginPage(request):
    page = 'login'
    if request.user.is_authenticated :
        return redirect('home')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username').lower()
        try:
            user = User.objects.get(username=username) 
        except:
            messages.error(request, 'Bunday foydalanuvchi mavjud emas .')
        user = authenticate( request , username=username , password=password )
        
        if user is not None :
            login(request , user)
            return redirect('home')
        else:
            messages.error(request, 'Username yoki Password hato !')

    context = {'page':page}
    return render(request , 'base/login_register.html' , context)







def logoutUser(request):    
    logout(request)
    return redirect('home')







def registerPage(request):
    form = UserCreateForm()
    # form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        # form = UserCreationForm(request.POST)
        try:
            if form.is_valid :
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request , user)
                return redirect('home')
        except:
            messages.error( request , 'Hatolik yuz berdi boshqattan urinib ko\'ring !' )

    context = {'form':form }
    return render(request , 'base/login_register.html' , context)
    
    
    


 
 
def home(request):
    
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(Q(topic__name__icontains=q ) | Q(name__icontains=q ) | Q(description__icontains=q ))
    
    room_messages = Message.objects.all()
    
    message_count = room_messages.count()
    
    topics = Topic.objects.all()
    
    topics_count = topics.count()
    
    room_count = rooms.count()
    
    context={'rooms':rooms,'topics':topics,'room_count':room_count , 'room_messages':room_messages , 'message_count' : message_count , 'topics_count':topics_count}
    
    return render(request , 'base/home.html' , context)
  
  
  
  
  
  
  
  
@login_required(login_url='login')

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            body = request.POST.get('body'),
            img = request.FILES.get('img'),
            room = room, 
        )
        room.participants.add(request.user)
        return redirect('room' , pk = room.id )
    context={'room':room , 'room_messages':room_messages , 'participants':participants }
    return render( request , 'base/room.html' , context )




@login_required(login_url='login')
def userProfile(request , pk ):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    message_count = room_messages.count()
    context = {'user':user , 'rooms':rooms , 'room_messages':room_messages , 'topics':topics , 'message_count':message_count }
    return render(request , 'base/profile.html' , context)








@login_required(login_url='login')

def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic , create = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic , 
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
    context={'form':form , 'topics':topics  }
    return render( request , 'base/room_form.html' , context)









@login_required(login_url='login')

def uodateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Sizga ruxsat yo\'q' )
    
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic , create = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save() 
        return redirect('home')
    
    context = {'form':form , 'topics':topics , 'room':room }
    return render(request , 'base/room_form.html' , context )







 

@login_required(login_url='login')

def deleteRoom(request , pk ):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('Sizga ruxsat yo\'q' )
    
    if request.method=='POST':
        room.delete()
        return redirect('home')
    
    return render(request , 'base/delete.html' , {'room':room} )
       
        






@login_required(login_url='login')

def deleteMessage(request , pk ):
    message = Message.objects.get(id=pk) 
    room = message.room
    if request.user != message.user:
        return HttpResponse('Sizga ruxsat yo\'q' )
    
    if request.method=='POST':
        message.delete()
        return redirect('room' , room.id  )
    
    return render(request , 'base/delete.html' , {'room':message} )







@login_required(login_url='login')

def updateUser(request):

    user = request.user
    form = UserForm(instance=user)
    if request.method=='POST':
        form = UserForm(request.POST , instance=user)
        if form.is_valid :
            form.save()
            return redirect('home')
    context = {'user':user , 'form':form}
    
    return render(request , 'base/edit_user.html' , context )
