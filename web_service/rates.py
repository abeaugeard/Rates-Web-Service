"""
author : Aurélie Beaugeard
"""
import json
import falcon
import requests
import requests_cache
from datetime import date, timedelta, datetime


class RatesResource:

    #Class attributes

    #Data of the Rates Api, type : dictionnary
    data = {}

    #Price indicator, type: dictionnary
    price_indicator = {}

    #Rates Api yesterday data, type : dictionnary
    data_yesterday = {}

    #Url usesd to get the ressources
    url = ""

    #General dictionnary of this RESTful web service
    dico_init = {}

    #Status of the service
    local_status = {}

    #Class constructor
    #Instantiation of the object
    def __init__(self):
        """
        Constructor of the class
        """
        #Results cache
        requests_cache.install_cache('rates_cache')#allowable_codes = (200), alowable_methods=(GET)

        #Initalization of the class attributes
        self.url = "https://api.ratesapi.io/api/"

        #Loading and creating the dictionnary
        self.update_base()

        #Status initialization
        self.set_status()

    #BASIC GET HTTP METHOD
    def on_get(self, req, resp):
        """
        Basic get http method. Displays the following information : the base symbol, the current symbol, the current price of a symbol and finally the price indicator.
        It's possible to change the base, indicating the required base symbol as a parameter. Be default the base symbol is EUR.
        :param req: the request
        :type falcon.Request
        :param resp: the result of the request
        :type falcon.Response
        """

        #Initialization of the status
        self.set_status(resp.status)

        #First step : Getting parameters as a sting to upper them in order to disable Case-sensitivity
        #Second-step : Converting this string to a dictionnary
        parameters = falcon.uri.parse_query_string(req.query_string.upper())

        #Getting keys parameters to recognize the kinf of parameter
        key = parameters.keys()

        #Getting possible base names to ensure that base names required exist
        base_names = self.get_base_names()

        if "BASE" in key :
            #Checking if there is only one parameter
            if isinstance(parameters["BASE"],str):
                if parameters["BASE"] in base_names:
                    self.update_base(parameters["BASE"])
                    self.set_status(resp.status)
                    output = self.dico_init
                #Display an error if the parameter doesn't exist
                else :
                    resp.status = falcon.HTTP_400
                    self.set_status(resp.status)
                    output = {
                        "error" : "The symbol "+parameters["BASE"]+" is not available"
                    }
            else :
                   #The API service of Rates.io doesn't provide more than one base at each request
                    resp.status = falcon.HTTP_405
                    self.set_status(resp.status)
                    output = {
                        "error" : "The service can't take more than one base at the same time"
                    }
        else:
            self.update_base()
            output = self.dico_init

        #Results
        resp.body = json.dumps(output)


    #STATUS GET HTTP METHOD
    def on_get_status(self,req,resp):
        """
        First endpoint of the web service. This function responds with the status of the service, displaying the information of the last request.
        :param req: the request
        :type falcon.Request
        :param resp: the result of the request
        :type falcon.Response
        """
        resp.status = self.local_status["Status of the service"]
        resp.body = json.dumps(self.local_status)

    #GET HTTP METHOD WITH PARAMETERS
    def on_get_info(self,req,resp):

        """
        Second endpoint of the web service. This function responds with the price information.
        :param req: the request
        :type falcon.Request
        :param resp: the result of the request
        :type falcon.Response
        """

        #First step : Getting parameters as a sting to upper them in order to disable Case-sensitivity
        #Second-step : Converting this string to a dictionnary
        parameters = falcon.uri.parse_query_string(req.query_string.upper())

        #Getting keys parameters to recognize the kinf of parameter
        key = parameters.keys()

        #Getting possible base names to ensure that base names required exist
        base_names = self.get_base_names()

        if "BASE" in key:
            #Checking if there is only one parameters
            if isinstance(parameters["BASE"],str):
                if parameters["BASE"] in base_names:
                    self.update_base(parameters["BASE"])
                    self.set_status(resp.status)
                    output = self.dico_init
                #Display an error if the parameter doesn't exist
                else:
                    resp.status = falcon.HTTP_400
                    self.set_status(resp.status)
                    output = {
                        "error" : "The symbol "+parameters["BASE"]+" is not available"
                    }
            else:
                    #The API service of Rates.io doesn't provide more than one base at each request
                    resp.status = falcon.HTTP_405
                    self.set_status(resp.status)
                    output = {
                        "error" : "The service can't take more than one base at the same time"
                    }
        else:#If base is not in parameters
            self.update_base()
            self.set_status(resp.status)
            output = self.dico_init

        base_names = self.get_base_names()
        if "SYMBOLS" in key:

            #Dictionnary that contains symbols as keys and price information as values
            my_dict = {}

            #Result dictionnary
            my_final_dict = {"base": self.dico_init["base"]}

            #Checking if there is more than one parameter
            if not isinstance(parameters["SYMBOLS"],str):
                is_in_names_base = True
                iterator = 0
                while is_in_names_base and iterator < len(parameters["SYMBOLS"]):
                    if parameters["SYMBOLS"][iterator] in base_names:
                        my_dict[parameters["SYMBOLS"][iterator]] = self.dico_init["rates"][parameters["SYMBOLS"][iterator]]
                        my_final_dict["rates"] = my_dict
                    #Display an error if the parameter doesn't exist
                    else:
                        is_in_names_base = False
                        resp.status = falcon.HTTP_400
                        self.set_status(resp.status)
                        my_final_dict = {
                            "error" : "The symbol "+parameters["SYMBOLS"][iterator]+" is not available"
                        }
                    iterator += 1
            #If there is only one parameter in the base names
            elif parameters["SYMBOLS"] in base_names:
                my_dict[parameters["SYMBOLS"]] = self.dico_init["rates"][parameters["SYMBOLS"]]
                my_final_dict["rates"] = my_dict
            #Display an error if the parameter doesn't exist
            else:
                resp.status = falcon.HTTP_400
                self.set_status(resp.status)
                my_final_dict = {
                    "error" : "The symbol "+parameters["SYMBOLS"]+" is not available"
                }
            output = my_final_dict
        resp.body = json.dumps(output)

    #UTILITIES FUNCTIONS

    #LOADING THE BASE IN A PROPER DICTIONNARY
    def update_base(self,base=None):
        """
        Update the main dictionary depending on the selected base
        :param base: the base symbol
        :type str
        """
        #Initialization of the parameter
        dico_rates = {}

        #Creating the base according to the base name
        if base != None:
            req = requests.request("GET", self.url+'latest?base='+base)
            req1 = requests.request("GET", self.url + self.get_yesterday_date()+'?base='+base)
        #Default : EUR
        else:
            req = requests.request("GET", self.url+'latest')
            req1 = requests.request("GET", self.url + self.get_yesterday_date())
        #Data of yesterday are necessary to calculate the price indicator
        self.data_yesterday = req1.json()
        self.data = req.json()
        rates = self.data["rates"]

        #Beginning of the main dictionnary creation
        self.dico_init["base"] = self.data["base"]
        #Creation of the sub_dictionnary with price symbols as key and price information as values
        for key,val in rates.items():
            dico_symbols = {"Current price": val, "Price indicator": self.get_price_indicator(key)}
            dico_rates[key] = dico_symbols
        self.dico_init["rates"] = dico_rates


    def get_current_price_of_a_symbol(self, symbol):
        """
        Function that returns the current price of a symbol
        :param symbol: the current symbol
        :return: the price
        :type int
        """
        return self.data["rates"][symbol]

    def get_price_indicator(self,chosen_symbol):
        """
        Calculates the price indicator of a price symbol
        :param chosen_symbol
        :type str
        :return: the price indicator
        """
        price_symbol_yesterday = self.data_yesterday["rates"][chosen_symbol]
        if (self.get_current_price_of_a_symbol(chosen_symbol)-price_symbol_yesterday) < 0 :
            return -1
        elif (self.get_current_price_of_a_symbol(chosen_symbol)-price_symbol_yesterday) == 0 :
            return 0
        else:
            return 1

    def get_yesterday_date(self):
        """
        Get the date of yesterday as a string
        :return: str
        """
        yesterday = date.today() - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    def get_base_names(self):
        """
        Generate all the possible price symbols as keys availables in the self.dico_init
        :return: the base_names as a list
        :type: list
        """
        base_names =list(self.dico_init["rates"].keys())
        return base_names

    def set_status(self,error=falcon.HTTP_200):
        """
        Function that permits to set the status of the service
        :param error: The type of error generated by the last request
        :type falcon.HTTPError
        :type dict, local_status
        """
        self.local_status = {"Status of the service": str(error),
                             "Date of the last request": date.today().strftime("%Y-%m-%d"),
                             "Hour of the last request": datetime.now().strftime("%H:%M:%S")}
