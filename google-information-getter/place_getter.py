import asyncio
import logging
import googlemaps
import contextlib
import time

from file_writer import Writer
from where_am_i import Coordinator


@contextlib.contextmanager
def get_gmaps_client(api_key):
    gmap = googlemaps.Client(key=api_key)
    try:
        logging.info('gmaps open')
        yield gmap
    finally:
        logging.info('gmaps closed')


class FoodAggregator:

    def __init__(self,
                 city_name: str,
                 coordinator: Coordinator,
                 diameter: float,
                 api_key: str,
                 find_type: str):

        self._total_cnt = 0
        self._city_name = city_name
        self._coordinator = coordinator
        self._api_key = api_key
        self._radius = diameter / 2
        self._find_type = find_type

        # init directory for saving data.
        self._writer = Writer(self.city_name())

    def city_name(self) -> str:
        return self._city_name

    # {'html_attributions': [], 'results': [], 'status': 'ZERO_RESULTS'}
    # {'html_attributions': [], 'results': [dict1, dict2, ...], 'status': 'OK'}
    def get_place_data(self,
                       cur_location: tuple) -> None:

        # for logging.
        logging.info(f'{cur_location = }')
        print(f'{cur_location = }')

        file_path = self._writer.create_new_file_path()

        next_page_token = -1
        params = {
            'location': cur_location,
            'radius': self._radius,
            'language': 'ko',
            'type': self._find_type,
            'keyword': 'food'}

        with get_gmaps_client(self._api_key) as client:
            while next_page_token is not None:
                self._total_cnt += 1

                if next_page_token is None or next_page_token == -1:
                    result_dict = client.places_nearby(**params)
                else:
                    print('sleep 5, because we have next token. next token has delay for applying to server.')
                    time.sleep(5)
                    try:
                        result_dict = client.places_nearby(page_token=next_page_token)
                    except googlemaps.exceptions.ApiError as e:
                        print('Invalid API Request occur. we break this loop to escape big charge from google.')
                        logging.warning('Invalid API Request occur. we break this loop to escape big charge from google.')
                        break

                if result_dict['status'] != 'OK':
                    break

                response_list = result_dict['results']
                self._writer.write(response_list, file_path)

                next_page_token = None if 'next_page_token' not in result_dict else result_dict['next_page_token']

        print(f'now count = {self._total_cnt}')

    async def get_place(self, is_async) -> None:

        if not is_async:
            [self.get_place_data(cur_location.get_position_with_tuple())
             for cur_location in self._coordinator]

        else:
            loop = asyncio.get_running_loop()
            tasks = [loop.run_in_executor(None,
                                          self.get_place_data,
                                          cur_location.get_position_with_tuple())
                     for cur_location in self._coordinator]
            for t in tasks:
                await t