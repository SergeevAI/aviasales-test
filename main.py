from collections import defaultdict
from pprint import pprint
from typing import List, Dict

from client import ViaComClient, Itinerary, Flight


def map_itineraries(itineraries: List[Itinerary]) -> Dict[str, List['Flight']]:
    result = defaultdict(list)
    for itinerary in itineraries:
        result[itinerary.get_onward_route()].extend(itinerary.onward_flights)
    return result


def calculate_diff(via_3, via_ow):
    result = defaultdict(list)
    for route, flights in via_ow.items():
        for flight in flights:
            if via_3.get(route):
                if not any(list(map(lambda x: flight == x, via_3[route]))):
                    result[route].append(flight)
    return result


if __name__ == '__main__':
    via_3, via_ow = ViaComClient('RS_Via-3.xml'), ViaComClient('RS_ViaOW.xml')
    routes_map_via_3 = map_itineraries(via_3.itineraries)
    routes_map_via_ow = map_itineraries(via_ow.itineraries)

    result = calculate_diff(routes_map_via_3, routes_map_via_ow)
    print('New flights from second api request: ')
    pprint(result)
