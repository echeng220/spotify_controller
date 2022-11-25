from .models import Room

def get_room_by_code(code):
    rooms = Room.objects.filter(code=code)
    room = rooms[0] if rooms.exists() else None

    return room

def get_room_by_host_id(host_id):
    rooms = Room.objects.filter(host=host_id)
    room = rooms[0] if rooms.exists() else None

    return room

