# pylint: disable=redefined-outer-name
from datetime import datetime
from unittest.mock import patch, MagicMock
import pytest

from client import Itinerary, Flight, Price, ViaComClient


@pytest.fixture
def first_xml():
    return """<?xml version="1.0" encoding="utf-8"?>
<AirFareSearchResponse RequestTime="28-09-2015 20:23:49" ResponseTime="28-09-2015 20:23:56">
    <RequestId>123ABCD</RequestId>
    <PricedItineraries>
        <Flights>
            <OnwardPricedItinerary>
                <Flights>
                    <Flight>
                        <Carrier id="AI">AirIndia</Carrier>
                        <FlightNumber>996</FlightNumber>
                        <Source>DXB</Source>
                        <Destination>DEL</Destination>
                        <DepartureTimeStamp>2015-10-22T0005</DepartureTimeStamp>
                        <ArrivalTimeStamp>2015-10-22T0445</ArrivalTimeStamp>
                        <Class>G</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                    <Flight>
                        <Carrier id="AI">AirIndia</Carrier>
                        <FlightNumber>332</FlightNumber>
                        <Source>DEL</Source>
                        <Destination>BKK</Destination>
                        <DepartureTimeStamp>2015-10-22T1350</DepartureTimeStamp>
                        <ArrivalTimeStamp>2015-10-22T1935</ArrivalTimeStamp>
                        <Class>G</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                </Flights>
            </OnwardPricedItinerary>
            <ReturnPricedItinerary>
                <Flights>
                    <Flight>
                        <Carrier id="AI">AirIndia</Carrier>
                        <FlightNumber>333</FlightNumber>
                        <Source>BKK</Source>
                        <Destination>DEL</Destination>
                        <DepartureTimeStamp>2015-10-30T0850</DepartureTimeStamp>
                        <ArrivalTimeStamp>2015-10-30T1205</ArrivalTimeStamp>
                        <Class>U</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                    <Flight>
                        <Carrier id="AI">AirIndia</Carrier>
                        <FlightNumber>995</FlightNumber>
                        <Source>DEL</Source>
                        <Destination>DXB</Destination>
                        <DepartureTimeStamp>2015-10-30T2040</DepartureTimeStamp>
                        <ArrivalTimeStamp>2015-10-30T2245</ArrivalTimeStamp>
                        <Class>U</Class>
                        <NumberOfStops>0</NumberOfStops>
                        <FareBasis>
                            2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0
                        </FareBasis>
                        <WarningText/>
                        <TicketType>E</TicketType>
                    </Flight>
                </Flights>
            </ReturnPricedItinerary>
            <Pricing currency="SGD">
                <ServiceCharges type="SingleAdult" ChargeType="BaseFare">117.00</ServiceCharges>
                <ServiceCharges type="SingleAdult" ChargeType="AirlineTaxes">429.80</ServiceCharges>
                <ServiceCharges type="SingleAdult" ChargeType="TotalAmount">546.80</ServiceCharges>
            </Pricing>
        </Flights>
    </PricedItineraries>
</AirFareSearchResponse>"""


@pytest.fixture
def first_xml_objects():
    return Itinerary(
        onward_flights=[
            Flight(
                carrier_id='AI',
                carrier_name='AirIndia',
                flight_number=996,
                source='DXB',
                destination='DEL',
                departure_time=datetime(2015, 10, 22, 0, 5),
                arrival_time=datetime(2015, 10, 22, 4, 45),
                flight_class='G',
                number_of_stops=0,
                ticket_type='E'
            ),
            Flight(
                carrier_id='AI',
                carrier_name='AirIndia',
                flight_number=332,
                source='DEL',
                destination='BKK',
                departure_time=datetime(2015, 10, 22, 13, 15),
                arrival_time=datetime(2015, 10, 22, 19, 35),
                flight_class='G',
                number_of_stops=0,
                ticket_type='E'
            )
        ],
        return_flights=[
            Flight(
                carrier_id='AI',
                carrier_name='AirIndia',
                flight_number=333,
                source='BKK',
                destination='DEL',
                departure_time=datetime(2015, 10, 30, 8, 50),
                arrival_time=datetime(2015, 10, 30, 12, 5),
                flight_class='U',
                number_of_stops=0,
                ticket_type='E'
            ),
            Flight(
                carrier_id='AI',
                carrier_name='AirIndia',
                flight_number=995,
                source='DEL',
                destination='DXB',
                departure_time=datetime(2015, 10, 30, 20, 40),
                arrival_time=datetime(2015, 10, 30, 22, 45),
                flight_class='U',
                number_of_stops=0,
                ticket_type='E'
            )
        ],
        prices=[
            Price(
                currency='SGD',
                flight_type='SingleAdult',
                price_type='BaseFare',
                price=117.0
            ),
            Price(
                currency='SGD',
                flight_type='SingleAdult',
                price_type='AirlineTaxes',
                price=429.8
            ),
            Price(
                currency='SGD',
                flight_type='SingleAdult',
                price_type='TotalAmount',
                price=546.8
            )
        ]
    )


@patch('client.FromFileAdapter')
def test_get_itineraries(data_mock, first_xml, first_xml_objects):
    data_mock.get_data.return_value = first_xml
    client = ViaComClient(data_mock)
    assert client.itineraries
    itinerary = client.itineraries[0]
    assert itinerary == first_xml_objects
    assert itinerary.onward_flights[0] == first_xml_objects.onward_flights[0]
    assert itinerary.get_onward_route() == first_xml_objects.get_onward_route()
    assert itinerary.get_onward_datetimes() == first_xml_objects.get_onward_datetimes()


def test_itinerary_str(first_xml_objects):
    result = """DXB-DEL-BKK | BKK-DEL-DXB
2015-10-22 00:05:00 - 2015-10-22 19:35:00
---------------------------
Flights:
AI996
DXB - DEL
2015-10-22 00:05:00 - 2015-10-22 04:45:00
AI332
DEL - BKK
2015-10-22 13:15:00 - 2015-10-22 19:35:00
---------------------------
Prices:
SingleAdult: 546.8 SGD
---------------------------"""
    assert str(first_xml_objects) == result


def test_flights_eq(first_xml_objects):
    flight = MagicMock(spec=Flight)
    flight.carrier_id = 'AI'
    flight.flight_number = 996
    assert flight == first_xml_objects.onward_flights[0]
