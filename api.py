from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful.utils import cors
import swisseph as swe
import astrotools as tools

app = Flask(__name__)

api = Api(app)
api.decorators = [cors.crossdomain(origin='*')]

planets = {
    'mercury': swe.MERCURY,
    'venus': swe.VENUS,
    'earth': swe.EARTH,
    'mars': swe.MARS,
    'jupiter': swe.JUPITER,
    'saturn': swe.SATURN,
    'uranus': swe.URANUS,
    'neptune': swe.NEPTUNE,
    'pluto': swe.PLUTO,
    'sun': swe.SUN,
    'moon': swe.MOON
}

class PlanetPos(Resource):
    def get(self, _mode, _planet, _day, _month, _year):
        print('PlanetPos')

        planet_data = tools.getPlanet(_mode,_planet,_day, _month, _year)

        print(planet_data)
        return planet_data

class MultiPlanetPos(Resource):
    def get(self, _mode, _day, _month, _year):
        print('PlanetPos')

        planet_data = tools.getPlanets(_mode,_day, _month, _year)

        print(planet_data)
        return planet_data

api.add_resource(PlanetPos, '/planet/<string:_mode>/<string:_planet>/<int:_day>/<int:_month>/<int:_year>')
api.add_resource(MultiPlanetPos, '/planets/<string:_mode>/<int:_day>/<int:_month>/<int:_year>')

if __name__ == '__main__':
    swe.set_ephe_path('')
    #threaded=True is important otherwise expremely painfully long lags when called in chrome
    #app.run(debug=False,threaded=True,host='0.0.0.0')
    app.run()
