from collections import defaultdict
from pprint import pprint
from typing import List, Dict

from client import ViaComClient, Itinerary, Flight, FromFileAdapter


def map_itineraries(itineraries: List[Itinerary]) -> Dict[str, List[Flight]]:
    """
    Map ititeraties to dict
    :param itineraries:
    :return:
    """
    result = defaultdict(list)
    for itinerary in itineraries:
        result[itinerary.get_onward_route()].extend(itinerary.onward_flights)
    return result


def calculate_flights_diff(
        map_via_3: Dict[str, List[Flight]],
        map_via_ow: Dict[str, List[Flight]]
) -> Dict[str, List[Flight]]:
    """
    Calculate flights difference between two api requests.
    :param map_via_3: {'DBX-BKK': [Flight, Flight]}. Dict with itenerary and all flights from api.
    :param map_via_ow: {'DBX-BKK': [Flight, Flight]}. Dict with itenerary and all flights from api.
    :return: Dict with new flights from second api request
    """
    result = defaultdict(list)
    for route, flights in map_via_ow.items():
        for flight in flights:
            if map_via_3.get(route):
                if not any(list(map(lambda x: x == flight, map_via_3[route]))):
                    result[route].append(flight)
    return result


def get_route_difference(list_via_3: List[Itinerary], list_via_ow: List[Itinerary]) -> List[Itinerary]:
    """
    :param list_via_3: List of itineraries from first api
    :param list_via_ow:List of itineraries from second api
    :return: List of new itineraries
    """
    return [route for route in list_via_ow if route not in list_via_3]


# pylint: disable=invalid-name
if __name__ == '__main__':
    via_3, via_ow = ViaComClient(FromFileAdapter('RS_Via-3.xml')), ViaComClient(FromFileAdapter('RS_ViaOW.xml'))
    routes_map_via_3 = map_itineraries(via_3.itineraries)
    routes_map_via_ow = map_itineraries(via_ow.itineraries)

    print('New flights from second api request: ')
    pprint(calculate_flights_diff(routes_map_via_3, routes_map_via_ow))

    print('New routes from second API request:')
    routes_diff = get_route_difference(via_3.itineraries, via_ow.itineraries)
    print('\n\n'.join([str(x) for x in routes_diff]))
