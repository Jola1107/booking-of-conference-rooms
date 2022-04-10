from django.shortcuts import render
from .models import Rooms
from django.views import View
from django.http import HttpResponse

class RoomView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')

    def post(self, request, *args, **kwargs):
        pass


class AddRoomView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'AddRoom.html')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        seats_int = int(seats) if seats else 0
        projector = request.POST.get('projector')
        #print(projector)
        if projector == "Yes":
            projector = True
        else:
            projector = False

        if not name:
            return render(request, 'AddRoom.html', context={'error':'Enter the name of the room'})
        if Rooms.objects.filter(name=name).exists():
            return render(request, 'AddRoom.html', context={'error':'That room exist'})
        if seats_int <= 0:
            return render(request, 'AddRoom.html', context={'error':'Enter a number greater than 0'})
        else:
            Rooms.objects.create(
                name=name,
                seats=seats,
                projector=projector
            )
            return render(request, 'base.html', context={'error':'Room added'})


class ShowAllView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ShowAll.html')