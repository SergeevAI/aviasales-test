from collections import defaultdict
from pprint import pprint
from typing import List, Dict

from client import ViaComClient, Itinerary, Flight


def map_itineraries(itineraries: List[Itinerary]) -> Dict[str, List['Flight']]:
    result = defaultdict(list)
    for itinerary in itineraries:
        result[itinerary.get_onward_route()].extend(itinerary.onward_flights)
    return result


def calculate_flights_diff(via_3: Dict[str, List['Flight']], via_ow: Dict[str, List['Flight']]) -> Dict[str, List['Flight']]:
    """
    Calculate flights difference between two api requests.
    :param via_3: {'DBX-BKK': [Flight, Flight]}. Dict with itenerary and all flights from api.
    :param via_ow: {'DBX-BKK': [Flight, Flight]}. Dict with itenerary and all flights from api.
    :return: Dict with new flights from second api request
    """
    result = defaultdict(list)
    for route, flights in via_ow.items():
        for flight in flights:
            if via_3.get(route):
                if not any(list(map(lambda x: flight == x, via_3[route]))):
                    result[route].append(flight)
    return result


def get_route_difference(via_3: List[Itinerary], via_ow: List[Itinerary]) -> List['Itinerary']:
    """
    :param via_3: List of itineraries from first api
    :param via_ow:List of itineraries from second api
    :return: List of new itineraries
    """
    return [route for route in via_ow if route not in via_3]


if __name__ == '__main__':
    via_3, via_ow = ViaComClient('RS_Via-3.xml'), ViaComClient('RS_ViaOW.xml')
    routes_map_via_3 = map_itineraries(via_3.itineraries)
    routes_map_via_ow = map_itineraries(via_ow.itineraries)

    result = calculate_flights_diff(routes_map_via_3, routes_map_via_ow)
    print('New flights from second api request: ')
    pprint(result)

    print('New routes from second API request:')
    a = get_route_difference(via_3.itineraries, via_ow.itineraries)
    print('\n\n'.join([str(x) for x in a]))
