import json
import falcon
import requests
from datetime import date, timedelta


class RatesResource:
    data = {}
    url = ""
    chosen_symbol = ""

    def __init__(self):
        self.url = "https://api.ratesapi.io/api/"
        req = requests.request("GET", self.url+'latest')
        self.data = req.json()

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        if not req.params:
            resp.body = json.dumps(self.data)
        elif 'symbols' in req.params.keys():
            output = {
                req.params['symbols'] : self.get_current_price_of_a_symbol(req.params['symbols']),
                "Price indicator" : self.get_price_indicator()
            }
            resp.body = json.dumps(output)
        elif 'base' in req.params.keys():
            output = {
                "Actual base symbol" : self.get_current_base()
            }
            resp.body = json.dumps(output)
        else :
            resp.status = falcon.HTTP_400
            output = {
                "error" : "These parameters don't exist"
            }
            resp.body = json.dumps(output)

    def on_get_status(self,req,resp):
        resp.body = resp.status

    def on_get_info(self,req,resp):

        validate_params = True
        output = {}
        if "base" not in req.params or "symbols" not in req.params:
            validate_params = False
        elif req.params["symbols"] not in self.data["rates"].keys():
            validate_params = False
        else :
            output = self.get_infos(req.params["base"],req.params["symbols"])

        if validate_params == False :
            resp.status = falcon.HTTP_400
            output = {
                "error" : "These parameters don't exist"
            }

        resp.body = json.dumps(output)


    def get_infos(self,base,symbol):
        req = requests.request("GET",self.url + 'latest?base='+base+'&symbols='+symbol)
        return req.json()

    def get_current_base(self):
        return self.data["base"]

    def get_current_price_of_a_symbol(self, symbol):
        self.chosen_symbol = symbol
        endpoint = 'latest'
        req = requests.request("GET", self.url + endpoint + '?symbols=' + symbol)
        return req.json()["rates"][symbol]

    def get_price_indicator(self):
        endpoint = self.get_yesterday_date()
        req = requests.request("GET", self.url + endpoint + '?symbols=' + self.chosen_symbol)
        price_symbol_yesterday = req.json()["rates"][self.chosen_symbol]
        if (self.get_current_price_of_a_symbol(self.chosen_symbol)-price_symbol_yesterday) < 0 :
            return -1
        elif (self.get_current_price_of_a_symbol(self.chosen_symbol)-price_symbol_yesterday) == 0 :
            return 0
        else :
            return 1

    def get_yesterday_date(self):
        yesterday = date.today() - timedelta(days=2)
        return yesterday.strftime("%Y-%m-%d")


def main():
    obj = RatesResource()
    print(obj.get_current_base())
    print(obj.get_current_price_of_a_symbol('PHP'))
    print(obj.get_price_indicator())
    print(obj.get_infos("USD","GBP"))

if __name__ == "__main__":
    main()
