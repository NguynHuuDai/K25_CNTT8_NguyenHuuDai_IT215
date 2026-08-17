from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base


booking = Table(
    "booking",
    Base.metadata,
    Column("driver_id", Integer, ForeignKey("drivers.id"), primary_key=True),
    Column("car_id", Integer, ForeignKey("cars.id"), primary_key=True)
)


class Fleet(Base):
    __tablename__ = "fleets"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    drivers = relationship(
        "Driver",
        back_populates="fleet"
    )


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20))
    fleet_id = Column(Integer, ForeignKey("fleets.id"))

    fleet = relationship(
        "Fleet",
        back_populates="drivers"
    )

    cars = relationship(
        "Car",
        secondary=booking,
        back_populates="drivers"
    )


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    license_plate = Column(String(20), nullable=False)
    status = Column(String(20))

    drivers = relationship(
        "Driver",
        secondary=booking,
        back_populates="cars"
    )
