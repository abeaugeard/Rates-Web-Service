import json
import falcon
import requests
from datetime import date, timedelta


class RatesResource:
    data = {}
    price_indicator = {}
    data_yesterday = {}
    url = ""
    dico_init = {}
    dico_rates = {}

    def __init__(self):
        self.url = "https://api.ratesapi.io/api/"
        self.update_base()


    def on_get(self, req, resp):
        parameters = falcon.uri.parse_query_string(req.query_string.upper());
        key = parameters.keys()
        values = parameters.values()
        if "BASE" in key:
            self.update_base(parameters["BASE"])
        else :
            self.update_base()
        resp.body = json.dumps(self.dico_init)

    def on_get_status(self,req,resp):
        resp.body = resp.status

    def on_get_info(self,req,resp):
        parameters = falcon.uri.parse_query_string(req.query_string.upper());
        key = parameters.keys()
        base_names = self.get_base_names()
        if "BASE" in key:
            if isinstance(parameters["BASE"],str):
                if parameters["BASE"] in base_names:
                    self.update_base(parameters["BASE"])
                else :
                    resp.status = falcon.HTTP_400
                    output = {
                        "error" : "This parameter doesn't exist"
                    }
                    resp.body = json.dumps(output)
        else :
            self.update_base()
        if "SYMBOLS" in key:
            my_dict = {}
            my_final_dict = {}
            my_final_dict["base"] = self.dico_init["base"]
            if not isinstance(parameters["SYMBOLS"],str):
                is_in_names_base = True
                iterator = 0
                while is_in_names_base and iterator < len(parameters["SYMBOLS"]):
                    if parameters["SYMBOLS"][iterator] in base_names:
                        my_dict[parameters["SYMBOLS"][iterator]] = self.dico_init["rates"][parameters["SYMBOLS"][iterator]]
                        my_final_dict["rates"] = my_dict
                    else :
                        is_in_names_base = False
                        resp.status = falcon.HTTP_400
                        my_final_dict = {
                            "error" : "This parameter " + parameters["SYMBOLS"][iterator] + " doesn't exist"
                        }
                    iterator += 1
            elif parameters["SYMBOLS"] in base_names :
                my_dict[parameters["SYMBOLS"]] = self.dico_init["rates"][parameters["SYMBOLS"]]
                my_final_dict["rates"] = my_dict
            else :
                resp.status = falcon.HTTP_400
                my_final_dict = {
                    "error" : "This parameter " + parameters["SYMBOLS"] + " doesn't exist"
                }
            resp.body = json.dumps(my_final_dict)
        else :
            resp.body = json.dumps(self.dico_init)


    def update_base(self,base=None):
        if base!=None:
            req = requests.request("GET", self.url+'latest?base='+base)
            req1 = requests.request("GET", self.url + self.get_yesterday_date()+'?base='+base)
        else :
            req = requests.request("GET", self.url+'latest')
            req1 = requests.request("GET", self.url + self.get_yesterday_date())
        self.data_yesterday = req1.json()
        self.data = req.json()
        rates = self.data["rates"]
        self.dico_init["base"] = self.data["base"]
        for key,val in rates.items():
            dico_symbols = {}
            dico_symbols["current_price"] = val
            dico_symbols["price_indicator"] = self.get_price_indicator(key)
            self.dico_rates[key] = dico_symbols
        self.dico_init["rates"] = self.dico_rates

    def get_current_price_of_a_symbol(self, symbol):
        return self.data["rates"][symbol]

    def get_price_indicator(self,chosen_symbol):
        price_symbol_yesterday = self.data_yesterday["rates"][chosen_symbol]
        if (self.get_current_price_of_a_symbol(chosen_symbol)-price_symbol_yesterday) < 0 :
            return -1
        elif (self.get_current_price_of_a_symbol(chosen_symbol)-price_symbol_yesterday) == 0 :
            return 0
        else :
            return 1

    def get_yesterday_date(self):
        yesterday = date.today() - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    def get_base_names(self):
        base_names =list(self.dico_init["rates"].keys())
        base_names.append(self.dico_init["base"])
        return base_names

def main():
    obj = RatesResource()
    print(obj.dico_init)
    print(obj.get_base_names())

if __name__ == "__main__":
    main()



