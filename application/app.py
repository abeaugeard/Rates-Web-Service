import falcon

from application.rates import RatesResource

api = application = falcon.API()

rates = RatesResource()
api.add_route('/rates',rates)
api.add_route('/rates/status', rates, suffix='status')
api.add_route('/rates/info', rates, suffix='info')

