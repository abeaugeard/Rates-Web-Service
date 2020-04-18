import falcon
from falcon import testing
import json
import pytest
from datetime import date, datetime

from web_service.app import api


@pytest.fixture
def client():
    return testing.TestClient(api)

def test_rates(client):
    symbol = 'EUR'

    response = client.simulate_get('/rates')
    result_rates = json.loads(response.content)

    assert result_rates["base"] == symbol
    assert response.status == falcon.HTTP_OK

    symbol = 'USD'

    response = client.simulate_get('/rates',params={'base':'USD'})
    result_rates = json.loads(response.content)

    assert result_rates["base"] == symbol
    assert response.status == falcon.HTTP_OK

    symbol = 'JPY'

    response = client.simulate_get('/rates',params={'base':'JPY'})
    result_rates = json.loads(response.content)

    assert result_rates["base"] == symbol
    assert response.status == falcon.HTTP_OK

    response = client.simulate_get('/rates',params={'base':('JPY','EUR')})
    result_rates = json.loads(response.content)

    assert result_rates == {"error" : "The service can't take more than one base at the same time"}
    assert response.status == falcon.HTTP_405

def test_info(client):

    symbol = 'JPY'

    response = client.simulate_get('/rates/info',params={'symbols':'JPY'})
    result_info = json.loads(response.content)

    result = result_info["rates"]

    key_symbols = list(result.keys())
    assert key_symbols[0] == symbol
    assert response.status == falcon.HTTP_OK

    response = client.simulate_get('/rates/info',params={'symbols':'EUR'})
    result_info = json.loads(response.content)

    assert result_info == {"error" : "The symbol EUR is not available"}
    assert response.status == falcon.HTTP_400

    response = client.simulate_get('/rates/info',params={'base':'USD','symbols':['JPY','PHO']})
    result_info = json.loads(response.content)

    assert result_info == {"error" : "The symbol PHO is not available"}
    assert response.status == falcon.HTTP_400

    response = client.simulate_get('/rates/info',params={'base' : 'GBP','symbols': ['JPY','GBP']})
    result_info = json.loads(response.content)

    key_symbols = result_info["rates"].keys()
    assert 'GBP' in key_symbols
    assert 'JPY' in key_symbols
    assert result_info['base'] == 'GBP'
    assert response.status == falcon.HTTP_OK

def test_status(client):

    response = client.simulate_get('/rates/status')
    result_status = json.loads(response.content)

    assert result_status["Status of the service"] == falcon.HTTP_200
    assert response.status == falcon.HTTP_OK

    #Simulating an error 400
    response = client.simulate_get('/rates/info',params={'base':'USD','symbols':['JPY','PHO']})
    result_info = json.loads(response.content)

    response = client.simulate_get('/rates/status')
    result_status = json.loads(response.content)

    assert response.status == falcon.HTTP_400

    #Simulating an error 405
    response = client.simulate_get('/rates',params={'base':('JPY','EUR')})
    result_rates = json.loads(response.content)

    response = client.simulate_get('/rates/status')
    result_status = json.loads(response.content)

    assert response.status == falcon.HTTP_405
