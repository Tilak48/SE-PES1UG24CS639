import pytest

from weather_alert import (
    wind_alert,
    rain_alert,
    heat_alert,
    overall_alert
)
def test_negative_wind():
    with pytest.raises(ValueError):
        wind_alert(-10)

def test_negative_rain():
    with pytest.raises(ValueError):
        rain_alert(-5, False)

def test_invalid_temperature():
    with pytest.raises(ValueError):
        heat_alert(150, 50)

def test_invalid_humidity():
    with pytest.raises(ValueError):
        heat_alert(30, 150)

# Test invalid wind input type
def test_invalid_wind_type():
    with pytest.raises(ValueError):
        wind_alert("fast")


# Test infinite wind speed
def test_infinite_wind():
    with pytest.raises(ValueError):
        wind_alert(float("inf"))


# Test invalid soil saturation
def test_invalid_soil_saturation():
    with pytest.raises(ValueError):
        rain_alert(20, "yes")
