from collections import Counter

from client import ViaComClient


if __name__ == '__main__':
    via_3, via_ow = ViaComClient('RS_Via-3.xml'), ViaComClient('RS_ViaOW.xml')
    routes_via_3 = Counter([str(route) for route in via_3.itineraries])
    routes_via_ow = Counter([str(route) for route in via_ow.itineraries])
    print(routes_via_3)
    print(routes_via_ow)

    print(len(via_3.itineraries), len(via_ow.itineraries))

    print('-' * 30)
    print(routes_via_3 | routes_via_ow)
