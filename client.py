import abc
from datetime import datetime
from typing import List, Tuple
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass


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

    def get_onward_datetimes(self) -> Tuple[datetime, datetime]:
        return self.onward_flights[0].departure_time, self.onward_flights[-1].arrival_time

    def __str__(self) -> str:
        """ String representation of Itinerary """
        start_time, end_time = self.get_onward_datetimes()
        result = f"{self.get_onward_route()} | {self.get_return_route()}\n" \
            f"{start_time} - {end_time}\n" \
            f"---------------------------\n" \
            f"Flights:\n{self.get_flights_str()}" \
            f"---------------------------\n" \
            f"Prices:\n{self._get_prices_str()}" \
            f"---------------------------"
        return result

    def __eq__(self, other):
        return self.get_onward_route() == other.get_onward_route()

    def _get_prices_str(self) -> str:
        result = ''
        for price in list(filter(lambda x: x.price_type == 'TotalAmount', self.prices)):
            result += f'{price.flight_type}: {price.price} {price.currency}\n'
        return result

    def get_flights_str(self) -> str:
        result = ''
        for flight in self.onward_flights:
            result += f'{flight.carrier_id}{flight.flight_number}\n'
            result += f'{flight.source} - {flight.destination}\n'
            result += f'{flight.departure_time} - {flight.arrival_time}\n'
        return result


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
    ticket_type: str

    def __eq__(self, other) -> bool:
        return self.carrier_id == other.carrier_id and self.flight_number == other.flight_number


@dataclass
class Price:
    """ Dataclass for price instance """
    currency: str
    flight_type: str
    price_type: str
    price: float


class DataAdapter(abc.ABC):
    """
    Strategy pattern.
    AbstractClass for data adapter
    """

    def __init__(self, source):
        """
        :param source: Filename/Url/Other source to getting xml file
        """
        self.source = source

    @abc.abstractmethod
    def get_data(self) -> str:
        """
        Abstract method for getting data and return XML from via.com api
        :return: XMl as a string
        """


class FromFileAdapter(DataAdapter):
    """
    Read XML from file. Concrete strategy to ViaComClient
    """
    def get_data(self) -> str:
        with open(self.source, 'r') as file:
            return file.read()


class ViaComClient:
    """
    Client for via.com API.
    Parse incoming xml and return list of itineraries
    """

    def __init__(self, adapter: DataAdapter):
        self.adapter = adapter
        self.itineraries = self._get_itineraries()

    def _get_itineraries(self) -> List[Itinerary]:
        """
        Open xml file, parse and return list of itineraries to self.itineraries
        :return: List of Itineraries
        """
        result = []
        soup = BeautifulSoup(self.adapter.get_data(), "xml")

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
