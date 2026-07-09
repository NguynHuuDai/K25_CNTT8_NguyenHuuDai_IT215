from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

rooms = [
    {"id": 1, "code": "R101", "name": "Room 101", "capacity": 30, "status": "AVAILABLE"},
    {"id": 2, "code": "R102", "name": "Room 102", "capacity": 20, "status": "AVAILABLE"},
    {"id": 3, "code": "R103", "name": "Room 103", "capacity": 40, "status": "MAINTENANCE"}
]

room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING"
    }
]


class Room(BaseModel):
    code: str
    name: str = Field(min_length=1)
    capacity: int = Field(gt=0)
    status: str


class RoomBooking(BaseModel):
    room_id: int
    class_name: str = Field(min_length=1)
    student_count: int = Field(gt=0)
    date: str
    slot: str


@app.post("/rooms")
def add_room(room: Room):
    for item in rooms:
        if item["code"] == room.code:
            return {"message": "Mã phòng đã tồn tại"}

    if room.status not in ["AVAILABLE", "IN_USE", "MAINTENANCE"]:
        return {"message": "Trạng thái phòng không hợp lệ"}

    new_room = {
        "id": len(rooms) + 1,
        "code": room.code,
        "name": room.name,
        "capacity": room.capacity,
        "status": room.status
    }

    rooms.append(new_room)

    return {
        "message": "Thêm phòng học thành công",
        "data": new_room
    }


@app.get("/rooms")
def get_rooms(keyword: str = "", status: str = "", min_capacity: int = 0):
    result = []

    for item in rooms:
        ma = keyword.lower() in item["code"].lower()
        ten = keyword.lower() in item["name"].lower()

        if keyword != "":
            if not ma and not ten:
                continue

        if status != "":
            if item["status"] != status:
                continue

        if item["capacity"] < min_capacity:
            continue

        result.append(item)

    return result


@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    for item in rooms:
        if item["id"] == room_id:
            return item

    return {"message": "Không tìm thấy phòng học"}


@app.put("/rooms/{room_id}")
def update_room(room_id: int, room: Room):
    for item in rooms:
        if item["code"] == room.code and item["id"] != room_id:
            return {"message": "Mã phòng đã tồn tại"}

    if room.status not in ["AVAILABLE", "IN_USE", "MAINTENANCE"]:
        return {"message": "Trạng thái phòng không hợp lệ"}

    for item in rooms:
        if item["id"] == room_id:
            item["code"] = room.code
            item["name"] = room.name
            item["capacity"] = room.capacity
            item["status"] = room.status

            return {
                "message": "Cập nhật phòng học thành công",
                "data": item
            }

    return {"message": "Không tìm thấy phòng học"}


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    for i in range(len(rooms)):
        if rooms[i]["id"] == room_id:
            deleted_room = rooms.pop(i)

            return {
                "message": "Xóa phòng học thành công",
                "data": deleted_room
            }

    return {"message": "Không tìm thấy phòng học"}


@app.post("/room-bookings")
def add_booking(booking: RoomBooking):
    room = None

    for item in rooms:
        if item["id"] == booking.room_id:
            room = item
            break

    if room is None:
        return {"message": "Không tìm thấy phòng học"}

    if room["status"] != "AVAILABLE":
        return {"message": "Phòng không sẵn sàng sử dụng"}

    if booking.student_count > room["capacity"]:
        return {"message": "Số lượng học viên vượt quá sức chứa của phòng"}

    if booking.slot not in ["MORNING", "AFTERNOON", "EVENING"]:
        return {"message": "Ca học không hợp lệ"}

    for item in room_bookings:
        if item["room_id"] == booking.room_id:
            if item["date"] == booking.date:
                if item["slot"] == booking.slot:
                    return {"message": "Phòng đã được đặt trong ca học này"}

    new_booking = {
        "id": len(room_bookings) + 1,
        "room_id": booking.room_id,
        "class_name": booking.class_name,
        "student_count": booking.student_count,
        "date": booking.date,
        "slot": booking.slot
    }

    room_bookings.append(new_booking)

    return {
        "message": "Đặt phòng thành công",
        "data": new_booking
    }


@app.get("/room-bookings")
def get_bookings():
    return room_bookings
