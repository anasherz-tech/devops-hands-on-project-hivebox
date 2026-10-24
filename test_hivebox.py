"""Test HiveBox Endpoints"""
import datetime as dt
import requests
from project import VERSION
from hivebox import print_version
from hivebox import avg_temp


def test_version():
    """Test /version Endpoint"""
    result = print_version()
    assert result == {"version":VERSION}


class MockResponse:  # pylint: disable=too-few-public-methods
    """mock json() method always returns a specific testing dictionary"""
    @staticmethod
    def json():
        """mock json() method always returns a specific testing dictionary"""
        return {"sensors" : [{'title': 'Temperatur', 'unit': '°C', 'sensorType': 'BME280',
                 'icon': 'osem-thermometer', '_id': '5eba5fbad46fb8001b799789', 'lastMeasurement': 
                 {'createdAt': str(dt.datetime.now(tz=dt.UTC)), 'value': '11.83'}}]}
def test_temperature(monkeypatch):
    """Test /temperature Endpoint"""
    def mock_get(*_args, **_kwargs):
        return MockResponse()
    monkeypatch.setattr(requests, "get", mock_get)
    result = avg_temp()
    assert "temperature" in result
    assert isinstance(result["temperature"], float)
