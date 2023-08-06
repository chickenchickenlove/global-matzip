# latitude : > 0 → 북위
# longitude : > 0 → 동경

POSITION = 'position'
CITYS = {
    'BALI': {
        POSITION: (-8.063314, 114.468484, -8.818296, 115.682313)
    },
    'TEST': {
        'latitude': 21.0090571,
        'longitude': 105.8607507,
        'accuracy': 100,
        POSITION: (21.04378, 105.81020, 20.98680, 105.86385),
        'y1': 21.086136,
        'x1': 105.783786,
        'y2': 20.944381,
        'x2': 105.870684,
    },
    'HANOI': {
        'latitude': 21.0090571,
        'longitude': 105.8607507,
        'accuracy': 100,
        POSITION: (21.086136, 105.783786, 20.944381, 105.870684),
        'y1': 21.086136,
        'x1': 105.783786,
        'y2': 20.944381,
        'x2': 105.870684,
    },

    'HOIAN': {
        'latitude': 15.8818303,
        'longitude': 108.3030015,
        'accuracy': 100,
        POSITION: (15.932881, 108.275333, 15.784028, 108.418816),
        'y1': 15.932881,
        'x1': 108.275333,
        'y2': 15.784028,
        'x2': 108.418816,
    },

    'HOCHIMINH': {
        'latitude': 10.8230989,
        'longitude': 106.6296638,
        'accuracy': 100,
        POSITION: (10.908551, 106.537120, 10.715878, 106.845918),
        'y1': 10.908551,
        'x1': 106.537120,
        'y2': 10.715878,
        'x2': 106.845918,
    },

    'DANANG': {
        'latitude': 16.0544068,
        'longitude': 108.2021667,
        'accuracy': 100,
        POSITION: (16.110450, 108.116851, 15.946566, 108.292201),
        'y1': 16.110450,
        'x1': 108.116851,
        'y2': 15.946566,
        'x2': 108.292201,
    },

    # 'NATRANG': {
    #     'latitude': 11.9980556,
    #     'longitude': 109.219167,
    #     'accuracy': 100
    # },
    #
    # 'SAPA': {
    #     'latitude': 22.3402,
    #     'longitude': 103.844,
    #     'accuracy': 100
    # },
}


class CityCoordinator:
    def __init__(self):
        self.citys = CITYS

    def is_valid_city(self, city_name: str) -> bool:
        return city_name in self.citys

    '''
    return (y1, x1, y2, x2)
    '''

    def get_start_end_position(self, city_name: str) -> tuple:
        return self.citys[city_name][POSITION]
