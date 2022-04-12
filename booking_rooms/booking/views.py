from django.shortcuts import render, redirect
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
            return redirect('show-all')


class ShowAllView(View):
    def get(self, request, *args, **kwargs):
        rooms=Rooms.objects.all()
        return render(request, 'ShowAll.html', context={'rooms':rooms})



class DeleteView(View):
    def get(self, request, room_id):
        r = Rooms.objects.get(pk=room_id)
        r.delete()
        return redirect('show-all')


class ModifyView(View):
    def get(self, request, id):
        room = Rooms.objects.get(id=id)

        return render(request, 'Modify.html')

    def post(self, request, id):
        room = Rooms.objects.get(id=id)
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        seats_int = int(seats) if seats else 0
        projector = request.POST.get('projector')

        if projector == "Yes":
            projector = True
        else:
            projector = False

        if not name:
            return render(request, 'Modify.html', context={'error':'Enter the name of the room'})
        if Rooms.objects.filter(name=name).exists():
            return render(request, 'Modify.html', context={'error':'That room exist'})
        if seats_int <= 0:
            return render(request, 'Modify.html', context={'error':'Enter a number greater than 0'})
        else:
            room.name = name
            room.seats=seats
            room.projector=projector
            room.save()

            return redirect('show-all')