
import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert


# WIND ALERT TEST CASES
def test_calm_wind():
    assert wind_alert(10) == "none"

def test_advisory_wind():
    assert wind_alert(39) == "advisory"

def test_watch_wind():
    assert wind_alert(62) == "watch"

def test_warning_wind():
    assert wind_alert(89) == "warning"

def test_high_wind():
    assert wind_alert(120) == "warning"


# RAIN ALERT TEST CASES
def test_no_rain():
    assert rain_alert(0, False) == "none"

def test_light_rain():
    assert rain_alert(10, False) == "advisory"

def test_heavy_rain():
    assert rain_alert(50, False) == "watch"

def test_saturated_heavy_rain():
    assert rain_alert(50, True) == "warning"

def test_saturated_light_rain():
    assert rain_alert(10, True) == "watch"


# HEAT ALERT TEST CASES
def test_normal_temperature():
    assert heat_alert(25, 30) == "none"

def test_advisory_heat():
    assert heat_alert(35, 40) == "advisory"

def test_watch_heat():
    assert heat_alert(40, 40) == "watch"

def test_warning_heat():
    assert heat_alert(45, 40) == "warning"

def test_high_humidity():
    assert heat_alert(40, 60) == "watch"


# OVERALL ALERT TEST CASES
def test_no_alerts():
    assert overall_alert([]) == "none"

def test_single_alert():
    assert overall_alert(["advisory"]) == "advisory"

def test_multiple_alerts():
    assert overall_alert(["none", "advisory", "warning"]) == "warning"

def test_highest_alert():
    assert overall_alert(["watch", "warning", "advisory"]) == "warning"

def test_invalid_alert():
    with pytest.raises(ValueError):
        overall_alert(["invalid"])
