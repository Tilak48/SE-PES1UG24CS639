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


# ---------- extra tests for branch coverage ----------

# wind boundaries (just below / exactly at each threshold)
@pytest.mark.parametrize("speed, expected", [
    (38, "none"), (39, "advisory"),
    (61, "advisory"), (62, "watch"),
    (88, "watch"), (89, "warning"),
])
def test_wind_boundaries(speed, expected):
    assert wind_alert(speed) == expected


# rain boundaries, both soil states
@pytest.mark.parametrize("mm, saturated, expected", [
    (49.9, True, "watch"), (49.9, False, "advisory"),
    (50, True, "warning"), (50, False, "watch"),
    (9.9, True, "none"), (9.9, False, "none"),
    (10, True, "watch"), (10, False, "advisory"),
])
def test_rain_boundaries(mm, saturated, expected):
    assert rain_alert(mm, saturated) == expected


# heat: humidity <= 40 means NO bonus (False branch of `humidity > 40`)
@pytest.mark.parametrize("temp, humidity, expected", [
    (34, 40, "none"), (35, 40, "advisory"),
    (39, 40, "advisory"), (40, 40, "watch"),
    (44, 40, "watch"), (45, 40, "warning"),
    (30, 10, "none"),
    (44, 20, "watch"),   # low humidity adds nothing
])
def test_heat_no_humidity_bonus(temp, humidity, expected):
    assert heat_alert(temp, humidity) == expected


# heat: humidity just above 40 gives a small bonus
def test_heat_humidity_just_above_40():
    assert heat_alert(39, 41) == "advisory"   # 39.1
    assert heat_alert(40, 41) == "watch"      # 40.1


def test_heat_humidity_pushes_over_threshold():
    assert heat_alert(36, 80) == "watch"      # 36 + 4.0 = 40.0


# overall: covers `SEVERITY[alert] > SEVERITY[worst]` being False
def test_overall_keeps_worst_when_later_is_milder():
    assert overall_alert(["warning", "advisory"]) == "warning"


def test_overall_order_independent():
    assert overall_alert(["advisory", "warning", "watch"]) == "warning"


def test_overall_equal_severity():
    assert overall_alert(["watch", "watch"]) == "watch"


def test_overall_all_none():
    assert overall_alert(["none", "none"]) == "none"


def test_overall_unknown_after_valid():
    with pytest.raises(ValueError):
        overall_alert(["watch", "hurricane"])