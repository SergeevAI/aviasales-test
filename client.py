from dataclasses import dataclass
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, Tag


@dataclass
class Itinerary:
    """ Dataclass for storing route information """
    onward_flights: List['Flight']
    return_flights: List['Flight']
    prices: List['Price']

    def get_onward_route(self) -> str:
        """ String representation of onward route """
        return '-'.join([fl.source for fl in self.onward_flights] + [self.onward_flights[-1].destination]) \
            if self.onward_flights else ''

    def get_return_route(self) -> str:
        """ String representation of return route """
        return '-'.join([fl.source for fl in self.return_flights] + [self.return_flights[-1].destination]) \
            if self.return_flights else ''

    def __repr__(self) -> str:
        return f'{self.get_onward_route()}' + (f' - {self.get_return_route()}' if self.get_return_route() else '')

    def get_route(self, route_name: str) -> 'Itinerary':
        if str(self) == route_name:
            return self


@dataclass
class Flight:
    """ Dataclass for one flight instance"""
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
    """ Dataclass for price instance """
    currency: str
    flight_type: str
    price_type: str
    price: float


class ViaComClient:
    """
    Client for via.com API.
    Parse incoming xml and return list of itineraries
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.itineraries = self._get_itineraries()

    def _get_itineraries(self) -> List[Itinerary]:
        """
        Open xml file, parse and return list of itineraries to self.itineraries
        :return: List of Itineraries
        """
        result = []
        with open(self.filename) as file:
            soup = BeautifulSoup(file, "xml")

        for flight in soup.PricedItineraries.children:
            if isinstance(flight, Tag):
                result.append(
                    Itinerary(
                        onward_flights=self._get_flights(flight, 'OnwardPricedItinerary'),
                        return_flights=self._get_flights(flight, 'ReturnPricedItinerary'),
                        prices=self.get_flight_prices(flight),
                    )
                )
        return result

    def _get_flights(self, data: Tag, flights_type: str) -> List[Flight]:
        """
        Parse flight information
        :param data: One Itinerary with List of flights from xml. Instance of BeautifulSoup.Tag class
        :param flights_type: String for parse flights of concrete type [OnwardPricedItinerary/ReturnPricedItinerary]
        :return: List of Flight instances
        """
        result = []
        for flights in data.select(flights_type):
            for flight in flights.Flights.children:
                if isinstance(flight, Tag):
                    result.append(
                        Flight(
                            carrier_id=flight.Carrier.get('id'),
                            carrier_name=flight.Carrier.text,
                            flight_number=int(flight.FlightNumber.text),
                            source=flight.Source.text,
                            destination=flight.Destination.text,
                            departure_time=datetime.strptime(flight.DepartureTimeStamp.text, '%Y-%m-%dT%H%M'),
                            arrival_time=datetime.strptime(flight.ArrivalTimeStamp.text, '%Y-%m-%dT%H%M'),
                            flight_class=flight.Class.text,
                            number_of_stops=int(flight.NumberOfStops.text),
                            fare_basis=flight.FareBasis.text,
                            ticket_type=flight.TicketType.text,
                        )
                    )
        return result

    def get_flight_prices(self, data: Tag) -> List[Price]:
        """
        Parse Price information
        :param data: One Itinerary with List of prices from xml.
        :return: List of Price instances
        """
        result = []
        for prices in data.select('Pricing'):
            for price in prices:
                if isinstance(price, Tag):
                    result.append(
                        Price(
                            currency=prices.get('currency'),
                            flight_type=price.get('type'),
                            price_type=price.get('ChargeType'),
                            price=float(price.text)
                        )
                    )
        return result
