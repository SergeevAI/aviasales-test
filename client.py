from dataclasses import dataclass
from datetime import datetime
from typing import List, NamedTuple


@dataclass
class Itinerary(NamedTuple):
    flights: List['Flight']
    price: List['Price']


@dataclass
class Flight:
    carrier_id: str
    carrier_name: str
    flight_number: int
    source: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    flight_class: str
    number_of_stops: int
    fare_basis: str
    ticket_type: str


@dataclass
class Price:
    flight_type: str
    base_fare: float
    airline_taxes: float
    total_amount: float


class ViaComClient:
    """ Client for via.com API """

    def __init__(self, filename):
        self.filename = filename
