from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful.utils import cors
import swisseph as swe
import astrotools as tools
from starfit import Fitness 

app = Flask(__name__)

api = Api(app)
api.decorators = [cors.crossdomain(origin='*')]

configfile = 'scoreconfig2.json'
fit = Fitness(configfile)

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


class AstroDataHelio(Resource):
    def get(self, _name, _day, _month, _year, _hour,_minute):
        #print('get request');
        julday = swe.julday(_year, _month, _day, _hour, swe.GREG_CAL)
        
        
        planet_id = planets[_name]
        #print(planet_id)
        pos = swe.calc_ut(julday, planet_id, swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_HELCTR)
        
        #print(pos)
        # pos = swe.calc_ut(julday, swe.MERCURY)
        
        return { 'planet': _name,
                  'month': _month,
                  'year': _year,
                  'hour': _hour,
                  'minute': _minute,
                  'pos': pos[0],
                  'distance': pos[2]
                }
        
        
class AstroDataGeo(Resource):
    def get(self, _name, _day, _month, _year, _hour,_minute):
        #print('get request');
        
        #do we need local time or UTC here?
        julday = swe.julday(_year, _month, _day, _hour, swe.GREG_CAL)
        
        planet_id = planets[_name]
        #print(planet_id)
        pos = swe.calc_ut(julday, planet_id, swe.FLG_SWIEPH + swe.FLG_SPEED )
        
        print(pos)
        # pos = swe.calc_ut(julday, swe.MERCURY)
        
        return { 
                    'hi': 'hi',
                    'planet': _name,
                  'month': _month,
                  'year': _year,
                  'hour': _hour,
                  'minute': _minute,
                  'pos': pos[0],
                  'distance': pos[2]
                }
        
        
        
class AstroDataHelioAll(Resource):
    def get(self, _day, _month, _year, _hour,_minute):
        #print('get request');
        julday = swe.julday(_year, _month, _day, _hour, swe.GREG_CAL)
        
        results = []
        for planet in planets.keys():
            planet_id = planets[planet]
            pos = swe.calc_ut(julday, planet_id, swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_HELCTR)
            result = {
                'name': planet,
                'pos': pos[0],
                'distance': pos[2]
            }
            results.append(result)
        print('returning')
        return {
            'planets': results
        }
        
class AstroDataGeoAll(Resource):
    def get(self, _day, _month, _year, _hour,_minute):
        #print('get request');
        julday = swe.julday(_year, _month, _day, _hour, swe.GREG_CAL)
        
        results = []
        for planet in planets.keys():
            planet_id = planets[planet]
            pos = swe.calc_ut(julday, planet_id, swe.FLG_SWIEPH + swe.FLG_SPEED)
            result = {
                'name': planet,
                'pos': pos[0],
                'distance': pos[2]
            }
            results.append(result)
        print('returning')
        return {
            'planets': results
        }
        
        
class AstroDataGeoAll2(Resource):
    def get(self, _day1, _month1, _year1, _day2, _month2, _year2):
        #print('get request');
        julday1 = swe.julday(_year1, _month1, _day1, 12.0, swe.GREG_CAL)
        julday2 = swe.julday(_year2, _month2, _day2, 12.0, swe.GREG_CAL)
        
        results1 = []
        results2 = []
        
        for planet in planets.keys():
            planet_id = planets[planet]
            pos1 = swe.calc_ut(julday1, planet_id, swe.FLG_SWIEPH + swe.FLG_SPEED)
            pos2 = swe.calc_ut(julday2, planet_id, swe.FLG_SWIEPH + swe.FLG_SPEED)
            result1 = {
                'name': planet,
                'pos': pos1[0],
                'distance': pos1[2]
            }
            result2 = {
                'name': planet,
                'pos': pos2[0],
                'distance': pos2[2]
            }
            results1.append(result1)
            results2.append(result2)
        print('returning')
        return {
            'planets1': results1,
            'planets2': results2
        }

class Aspects(Resource):
    def get(self, _day1, _month1, _year1, _day2, _month2, _year2):
        #print('get request');
        julday1 = swe.julday(_year1, _month1, _day1, 12.0, swe.GREG_CAL)
        julday2 = swe.julday(_year2, _month2, _day2, 12.0, swe.GREG_CAL)
        
        results1 = []
        results2 = []
        
        #get planets for each date
        for planet in planets.keys():
            planet_id = planets[planet]
            pos1 = swe.calc_ut(julday1, planet_id, swe.FLG_SWIEPH + swe.FLG_SPEED)
            pos2 = swe.calc_ut(julday2, planet_id, swe.FLG_SWIEPH + swe.FLG_SPEED)
            result1 = {
                'name': planet,
                'pos': pos1[0],
                'distance': pos1[2]
            }
            result2 = {
                'name': planet,
                'pos': pos2[0],
                'distance': pos2[2]
            }
            results1.append(result1)
            results2.append(result2)
        
        #calculate composite planets
        compPlanets = tools.compositePlanets(results1,results2)
        aspects = tools.aspects(compPlanets);
        
        return aspects;
    
class Fit(Resource):
    def get(self, _day1, _month1, _year1, _day2, _month2, _year2):
        print('fitness:')
        #print('ha')
        planets1 = tools.getPlanets(_day1, _month1, _year1)
        planets2 = tools.getPlanets(_day2, _month2, _year2)
      
        #calculate composite planets
        compPlanets = tools.compositePlanets(planets1['planets'],planets2['planets'])
        aspects = tools.aspects(compPlanets);
        
       #print('hoi')
        fitness = fit.fitness(aspects)
        
        print(fitness)
        return fitness;

        


#api.add_resource(AstroDataHelio, '/planet/<string:_name>/<int:_day>/<int:_month>/<int:_year>/<int:_hour>/<int:_minute>')
#api.add_resource(AstroDataHelioAll, '/planets/<int:_day>/<int:_month>/<int:_year>/<int:_hour>/<int:_minute>')
#api.add_resource(AstroDataGeo, '/geoplanet/<string:_name>/<int:_day>/<int:_month>/<int:_year>/<int:_hour>/<int:_minute>')
#api.add_resource(AstroDataGeoAll, '/geoplanets/<int:_day>/<int:_month>/<int:_year>/<int:_hour>/<int:_minute>')
#api.add_resource(AstroDataGeoAll2, '/geoplanets2/<int:_day1>/<int:_month1>/<int:_year1>/<int:_day2>/<int:_month2>/<int:_year2>')
#api.add_resource(Aspects, '/aspects/<int:_day1>/<int:_month1>/<int:_year1>/<int:_day2>/<int:_month2>/<int:_year2>')
api.add_resource(Fit, '/fitness/<int:_day1>/<int:_month1>/<int:_year1>/<int:_day2>/<int:_month2>/<int:_year2>')



if __name__ == '__main__':
    swe.set_ephe_path('')
    #threaded=True is important otherwise expremely painfully long lags when called in chrome
    #app.run(debug=False,threaded=True,host='0.0.0.0')
    app.run()
