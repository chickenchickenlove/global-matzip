import asyncio
import sys

import yaml
from where_am_i import Coordinator
from position_constant import CityCoordinator
from place_getter import FoodAggregator


def load_config(file_path):
    with open(file_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def valid(config: dict, city_coordinator: CityCoordinator):
    is_valid = True
    for city in config['search']['city']:
        is_valid = is_valid and city_coordinator.is_valid_city(city)

    return is_valid


def main():

    config_file_path = sys.argv[1]
    config = load_config(file_path=config_file_path)
    valid(config, CityCoordinator())

    city_names = config['search']['city']
    position_list = [CityCoordinator().get_start_end_position(city_name)
                     for city_name in city_names]

    diameter = config['search']['diameter']
    coordinators = [Coordinator(*position, diameter) for position in position_list]

    api_key = config['google']['api_key']
    find_type = config['search']['find_type']

    food_aggregators = [FoodAggregator(city_name, coordinator, diameter, api_key, find_type)
                        for coordinator, city_name in zip(coordinators, city_names)]

    is_async = config['is_async']
    for food_aggregator in food_aggregators:
        asyncio.run(food_aggregator.get_place(is_async=is_async))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception('config file is need. for example, $python google_information_getter.py config.yaml')
    main()
