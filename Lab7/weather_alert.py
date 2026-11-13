
import math

SEVERITY = {
    "none": 0,
    "advisory": 1,
    "watch": 2,
    "warning": 3
}


# Validate numeric inputs
def validate_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")

    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


# Wind alert
def wind_alert(speed_kmh):
    validate_number(speed_kmh, "Wind speed")

    if speed_kmh < 0:
        raise ValueError("Wind speed cannot be negative")

    if speed_kmh >= 89:
        return "warning"
    if speed_kmh >= 62:
        return "watch"
    if speed_kmh >= 39:
        return "advisory"
    return "none"


# Rain alert
def rain_alert(mm_per_hour, soil_saturated):
    validate_number(mm_per_hour, "Rainfall")

    if mm_per_hour < 0:
        raise ValueError("Rainfall cannot be negative")

    if not isinstance(soil_saturated, bool):
        raise ValueError("Soil saturation must be True or False")

    if mm_per_hour >= 50:
        if soil_saturated:
            return "warning"
        return "watch"

    if mm_per_hour >= 10:
        if soil_saturated:
            return "watch"
        return "advisory"

    return "none"


# Heat alert
def heat_alert(temp_c, humidity):
    validate_number(temp_c, "Temperature")
    validate_number(humidity, "Humidity")

    if temp_c < -100 or temp_c > 100:
        raise ValueError("Temperature must be between -100 and 100")

    if humidity < 0 or humidity > 100:
        raise ValueError("Humidity must be between 0 and 100")

    index = temp_c

    if humidity > 40:
        index += (humidity - 40) * 0.1

    if index >= 45:
        return "warning"
    if index >= 40:
        return "watch"
    if index >= 35:
        return "advisory"

    return "none"


# Overall alert
def overall_alert(alerts):
    worst = "none"

    for alert in alerts:
        if alert not in SEVERITY:
            raise ValueError("unknown alert")

        if SEVERITY[alert] > SEVERITY[worst]:
            worst = alert

    return worst
