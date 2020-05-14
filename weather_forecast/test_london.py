import requests
import pytest
import allure


class TestLondon:
    request = "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us&appid=b6907d289e10d714a6e88b30761fae22"

    @allure.severity(allure.severity_level.BLOCKER)
    def test_check_status_code(self):
        global request
        response = requests.get(self.request)
        assert response.status_code == 200

    @allure.severity(allure.severity_level.CRITICAL)
    def test_number_of_days_data_check(self):
        global request
        response = requests.get(self.request)
        response_body = response.json()
        count = len(response_body["list"])
        list1 = []
        for i in range(count):
            date_time = response_body["list"][i]["dt_txt"]
            date = date_time.split(" ")[0]
            if date not in list1:
                list1.append(date)
        assert len(list1) == 4

    @allure.severity(allure.severity_level.CRITICAL)
    def test_forecast_hourly_interval_check(self):
        global request
        response = requests.get(self.request)
        response_body = response.json()
        count = len(response_body["list"])
        list1 = []
        for i in range(count):
            date_time = response_body["list"][i]["dt_txt"]
            time = int(date_time.split(" ")[1].split(":")[0])
            list1.append(time)
            if i != 0 and time != 00:
                if list1[i-1] != (time - 1):
                    assert False
            if i != 0 and time == 00 and list1[i-1] != 23:
                assert False
        assert True

    @allure.severity(allure.severity_level.CRITICAL)
    def test_temperature_check(self):
        global request
        response = requests.get(self.request)
        response_body = response.json()
        count = len(response_body["list"])
        for i in range(count):
            temp = float(response_body["list"][i]["main"]["temp"])
            min_temp = float(response_body["list"][i]["main"]["temp_min"])
            max_temp = float(response_body["list"][i]["main"]["temp_max"])
            if temp < min_temp or temp > max_temp:
                assert False
            assert True

    @allure.severity(allure.severity_level.CRITICAL)
    def test_weather_description_check(self):
        global request
        response = requests.get(self.request)
        response_body = response.json()
        count = len(response_body["list"])
        for i in range(count):
            weather_id = int(response_body["list"][i]["weather"][0]["id"])
            if weather_id == 500:
                assert response_body["list"][i]["weather"][0]["description"] == 'light rain'
            if weather_id == 800:
                assert response_body["list"][i]["weather"][0]["description"] == 'clear sky'
