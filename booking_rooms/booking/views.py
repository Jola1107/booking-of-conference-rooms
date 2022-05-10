import datetime

from django.shortcuts import render, redirect
from .models import Rooms, Reserve
from django.views import View
from django.http import HttpResponse
from datetime import datetime, date

# displays the home page
class RoomView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')

    def post(self, request, *args, **kwargs):
        pass

# adding a room (its name, capacity, projector availability) and saving it to db
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

# displaying all rooms with information about the availability of the current day
class ShowAllView(View):
    def get(self, request, *args, **kwargs):
        rooms = Rooms.objects.all()
        for room in rooms:
            reservation_date = [reserve.date for reserve in room.reserve_set.all()]
            room.reserve = date.today() in reservation_date

        return render(request, 'ShowAll.html', context={'rooms':rooms})


# removing the room
class DeleteView(View):
    def get(self, request, room_id):
        r = Rooms.objects.get(id=room_id)
        r.delete()
        return redirect('show-all')

# edition of the room
class ModifyView(View):
    def get(self, request, id):
        room = Rooms.objects.get(id=id) # fetching data to be changed from db
        context ={'name': room.name,
                  'seats': room.seats,
                  'projector': room.projector}

        return render(request, 'Modify.html', context)

    def post(self, request, id):
        room = Rooms.objects.get(id=id) # fetching data to be changed from db
        name = request.POST.get('name') # downloading new data from the form (from the website)
        seats = request.POST.get('seats')
        seats_int = int(seats) if seats else 0
        projector = request.POST.get('projector')
# projector availability
        if projector == "Yes":
            projector = True
        else:
            projector = False
# checking the correctness of the entered data
        if not name:
            return render(request, 'Modify.html', context={'error':'Enter the name of the room'})
        # if Rooms.objects.filter(name=name).exists():
        #     return render(request, 'Modify.html', context={'error':'That room exist'})
        if seats_int <= 0:
            return render(request, 'Modify.html', context={'error':'Enter a number greater than 0'})
        else:
            room.name = name # saving new data for the room
            room.seats = seats
            room.projector = projector
            room.save()

            return redirect('show-all')

# room reservation
class ReserveView(View):
    def get(self, request, id):
        room = Rooms.objects.get(id=id) # download information about the room with the given id
        reservations = room.reserve_set.filter(date__gte=str(date.today())).order_by('date')
        # display of downloaded data from the earliest date
        return render(request, 'Reserve.html', context={'room': room, 'reservations': reservations})

    def post(self, request, id):
        room = Rooms.objects.get(id=id)
        date = request.POST.get('date') # booking a room for a selected day and the possibility of adding a comment
        comment = request.POST.get('comment')
# checking if the room is available on that day
        if Reserve.objects.filter(date=date):
            return render(request, 'Reserve.html',
                          context={'error':'The room is reserved for the selected day. Please choose another.'})
# checking if the date has already passed
        if date < str(datetime.today()):
            return render(request, 'Reserve.html',
                          context={'error':'Invalid date. That day is over.'})
        else:
# booking a room
            Reserve.objects.create(id_reserve=room, date=date, comment=comment)
            return redirect('show-all')

# display information about the room
class ShowRoomView(View):
    def get(self, request, id):
        room = Rooms.objects.get(id=id)
        reservations = room.reserve_set.filter(date__gte=str(date.today())).order_by('date')
        return render(request, 'ShowRoom.html', context={'room': room, 'reservations': reservations})

# searching for a room
class SearchView(View):
    def get(self, request):
        name = request.GET.get('name')
        seats = request.GET.get('seats')
        seats_int = int(seats) if seats else 0
        camera = request.GET.get('projector')

        # if camera == "Yes":
        #     camera = True
        # else:
        #     camera = False
# download all rooms
        rooms = Rooms.objects.all()
        if camera is not None:
            if camera == "Yes":
                camera = True
                rooms = rooms.filter(projector=camera)
            else:
                camera = False
                rooms = rooms.filter(projector=camera)# filtration
        if seats:
            rooms = rooms.filter(seats__gte=seats_int)# filtration
        if name:
            rooms = rooms.filter(name=name)# filtration

        for room in rooms:
            reservation_date = [reserve.date for reserve in room.reserve_set.all()]
            room.reserve = date.today() in reservation_date
            context = {'rooms':rooms, 'date':date.today()}
        return render(request, 'ShowAll.html', context)





