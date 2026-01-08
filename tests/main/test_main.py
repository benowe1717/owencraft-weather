#!/usr/bin/env python3
"""TestMain() class file"""
import pytest
import random

import main


class TestMain():
    """Tests for functions in main.py"""

    def test_map_weather_id_to_minecraft_weather(self) -> None:
        weather_id = -1
        assert main.map_weather_id_to_minecraft_weather(weather_id) == 'clear'

        weather_id = random.randint(700, 1000)
        assert main.map_weather_id_to_minecraft_weather(weather_id) == 'clear'

        weather_id = random.randint(300, 699)
        assert main.map_weather_id_to_minecraft_weather(weather_id) == 'rain'

        weather_id = random.randint(200, 299)
        assert main.map_weather_id_to_minecraft_weather(
            weather_id) == 'thunder'

        weather_id = random.randint(-1000, 199)
        assert main.map_weather_id_to_minecraft_weather(weather_id) == 'clear'
