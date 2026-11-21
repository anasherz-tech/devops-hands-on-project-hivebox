"""Test HiveBox Endpoints"""
import datetime as dt
import requests
import pytest
from project import VERSION
from hivebox import print_version
from hivebox import avg_temp
from hivebox import app

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
@pytest.fixture(name="api_link")
def check_api():
    """Test API"""
    return app.test_client()
def test_version_api(api_link):
    """Version API Test"""
    response = api_link.get("/version")
    assert response.status_code == 200
    assert response.json["version"] == VERSION
def test_metrics_api(api_link):
    """Metrics API Test"""
    response = api_link.get("/metrics")
    assert response.status_code == 200
    assert "flask_http_request_exceptions_total" in response.text
def test_temperature_api(api_link,monkeypatch):
    """Temperature API Test"""
    def mock_get(*_args, **_kwargs):
        return MockResponse()
    monkeypatch.setattr(requests, "get", mock_get)
    response = api_link.get("/temperature")
    assert response.status_code == 200
    assert response.json["temperature"] == 11.83
    assert response.json["status"] == 'Good'
