import asyncio
import logging
import googlemaps
import contextlib

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
                 coordinator: Coordinator,
                 diameter: float,
                 api_key: str,
                 find_type: str):

        self._coordinator = coordinator
        self._api_key = api_key
        self._radius = diameter / 2
        self._find_type = find_type

    # {'html_attributions': [], 'results': [], 'status': 'ZERO_RESULTS'}
    # {'html_attributions': [], 'results': [dict1, dict2, ...], 'status': 'OK'}
    def get_place_data(self,
                       cur_location: tuple):
        ret_dict = dict()
        next_page_token = -1

        with get_gmaps_client(self._api_key) as client:
            while next_page_token is not None:

                params = {
                    'location': cur_location,
                    'radius': self._radius,
                    'language': 'ko',
                    'type': self._find_type,
                    'keyword': '맛집'}

                if next_page_token != -1:
                    params.update(page_token=next_page_token)

                result_dict = client.places_nearby(**params)

                if result_dict['status'] != 'OK':
                    break

                response_list = result_dict['results']
                self.__transfer_dict(ret_dict, response_list)

                next_page_token = None if 'next_page_token' not in result_dict else result_dict['next_page_token']

        return ret_dict

    def __transfer_dict(self, ret_dict: dict, response_list: list):

        '''
        name, rating, vicinity
        key = name / vicinity
        value = (name, rating, vicinity)
        '''

        for response_dict in response_list:
            name = response_dict['name']
            vicinity = response_dict['vicinity']
            rating = 0 if 'rating' not in response_dict else response_dict['rating']

            key = name + '/' + vicinity
            value = (name, vicinity, rating)

            ret_dict[key] = value

    async def get_place(self):
        loop = asyncio.get_running_loop()
        tasks = [loop.run_in_executor(None,
                                      self.get_place_data,
                                      cur_location.get_position_with_tuple())
                 for cur_location in self._coordinator]

        result_dict = dict()
        ret_dicts = [await t for t in tasks]
        for each_result_dict in ret_dicts:
            result_dict.update(each_result_dict)

        return result_dict





# y1 = 21.04378
# x1 = 105.81020
# y2 = 20.98680
# x2 = 105.86385
# RADIUS = 10000


# async def amain():
#     coordinator = Coordinator(y1, x1, y2, x2, RADIUS * 2)
#
#     aggregator = FoodAggregator(
#         coordinator,
#         RADIUS * 2,
#         API_KEY,
#         FIND_TYPE)
#
#     print(aggregator)
#     my_list = await aggregator.get_place()
#     print(my_list)
#
#
# def main():
#     asyncio.run(amain())
#
#
# main()
