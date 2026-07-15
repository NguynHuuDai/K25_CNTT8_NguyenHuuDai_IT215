from fastapi import FastAPI, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime, timezone

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"

app = FastAPI()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_code = Column(String(50), unique=True, nullable=False)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ParkingSlotCreate(BaseModel):
    slot_code: str
    zone_name: str = Field(min_length=3)
    max_weight: int = Field(gt=0)


def response(status_code, message, error, data, path):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.post("/parking-slots", status_code=status.HTTP_201_CREATED)
def create_parking_slot(
    parking: ParkingSlotCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    existed = db.query(ParkingSlot).filter(
        ParkingSlot.slot_code == parking.slot_code
    ).first()

    if existed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã vị trí đỗ xe đã tồn tại"
        )

    new_slot = ParkingSlot(
        slot_code=parking.slot_code,
        zone_name=parking.zone_name,
        max_weight=parking.max_weight
    )

    try:
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        return response(
            201,
            "Thêm vị trí đỗ xe thành công",
            None,
            {
                "id": new_slot.id,
                "slot_code": new_slot.slot_code,
                "zone_name": new_slot.zone_name,
                "max_weight": new_slot.max_weight,
                "is_available": new_slot.is_available
            },
            str(request.url.path)
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Đã xảy ra lỗi cơ sở dữ liệu"
        )


@app.get("/parking-slots", status_code=status.HTTP_200_OK)
def get_all_parking_slots(
    request: Request,
    db: Session = Depends(get_db)
):
    slots = db.query(ParkingSlot).all()

    data = []
    for slot in slots:
        data.append({
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        })

    return response(
        200,
        "Lấy danh sách vị trí đỗ xe thành công",
        None,
        data,
        str(request.url.path)
    )


@app.get("/parking-slots/{slot_id}", status_code=status.HTTP_200_OK)
def get_parking_slot_detail(
    slot_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    slot = db.query(ParkingSlot).filter(
        ParkingSlot.id == slot_id
    ).first()

    if slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy vị trí đỗ xe"
        )

    return response(
        200,
        "Lấy thông tin vị trí đỗ xe thành công",
        None,
        {
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        },
        str(request.url.path)
    )
