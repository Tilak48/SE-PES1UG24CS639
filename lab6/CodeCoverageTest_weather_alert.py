import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert


# --- starter tests ---
def test_calm_wind():
    assert wind_alert(10) == "none"


def test_no_alerts():
    assert overall_alert([]) == "none"


# --- wind ---
def test_wind_warning():
    assert wind_alert(100) == "warning"


def test_wind_watch():
    assert wind_alert(70) == "watch"


def test_wind_advisory():
    assert wind_alert(45) == "advisory"


# --- rain ---
def test_rain_heavy_saturated():
    assert rain_alert(60, True) == "warning"


def test_rain_heavy_not_saturated():
    assert rain_alert(60, False) == "watch"


def test_rain_moderate_saturated():
    assert rain_alert(20, True) == "watch"


def test_rain_moderate_not_saturated():
    assert rain_alert(20, False) == "advisory"


def test_rain_light():
    assert rain_alert(2, False) == "none"


# --- heat (humidity > 40 so the bonus line runs) ---
def test_heat_none():
    assert heat_alert(20, 60) == "none"


def test_heat_advisory():
    assert heat_alert(35, 60) == "advisory"   # index 37.0


def test_heat_watch():
    assert heat_alert(40, 60) == "watch"      # index 42.0


def test_heat_warning():
    assert heat_alert(45, 60) == "warning"    # index 47.0


# --- overall ---
def test_overall_single():
    assert overall_alert(["warning"]) == "warning"


def test_overall_unknown_raises():
    with pytest.raises(ValueError):
        overall_alert(["tornado"])