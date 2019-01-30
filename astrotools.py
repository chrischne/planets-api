'''
Created on 10 Aug 2017

@author: chrischne
'''
from vector2d import Vec2d
import math 
import swisseph as swe

planetNames = ["sun", "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "moon"];

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

def getPlanets( _day, _month, _year):
    julday = swe.julday(_year, _month, _day, 12.0, swe.GREG_CAL)
        
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
    
    return {
        'planets': results
    }

def calcMidPoint(angle1,angle2):
    v1 = Vec2d(1, 0);
    v2 = Vec2d(1, 0);

    v1.rotate(angle1);
    v2.rotate(angle2);

    v3 = v1.interpolate_to(v2, 0.5)
    #print(angle2, math.degrees(v2.get_angle()))

    heading = v3.get_angle();
   
    
    if heading < 0:
        heading += 360
        
    return heading;


def compositePlanets(arr1, arr2):
    if len(arr1) == 0 or len(arr2) == 0: 
        return []
    
    compArr = []
    
    #print(arr1)
    
    for s in planetNames:
        p1 = next((p for p in arr1 if p['name'] == s), None)
        p2 = next((p for p in arr2 if p['name'] == s), None)

        v1 = p1['pos']
        v2 = p2['pos']
        midpoint = calcMidPoint(v1,v2);

        compPlanet = {
            'name': s,
            'pos': midpoint,
            'distance': p1['distance']
        };
        compArr.append(compPlanet)

    return compArr;


def aspects(_planets):
    arr = [];
    
    for i, p1 in enumerate(_planets):
        for j in range(i+1,len(_planets)):
            p2 = _planets[j]
            asp = aspect(p1,p2)
            arr.append(asp)
    
    #print(arr)
    #remove earth from aspects
    arr = [asp for asp in arr if asp['planet1'] != 'earth' and asp['planet2'] != 'earth' ]
    
    #remove all no aspects for test
    arr = [asp for asp in arr if asp['aspect'] != 'noaspect' ]
    
    return arr;


def aspect(p1, p2):
    v1 = Vec2d(1, 0);
    v1.rotate(p1['pos']);

    v2 = Vec2d(1, 0);
    v2.rotate(p2['pos']);
    
    angle = v1.get_angle_between2(v2);

    name = aspectName(angle);

    return {
        'planet1': p1['name'],
        'planet2': p2['name'],
        'pos1': p1['pos'],
        'pos2': p2['pos'],
        'aspect': name,
        'angle': angle
    };


def aspectName(angle):
    #source https://en.wikipedia.org/wiki/Astrological_aspect
    if angle <= 10:
        return 'conjunction';
    elif angle >= 56 and angle <= 64:
        return 'sextile'
    elif angle >= 85 and angle <= 95:
        return 'square';
    elif angle >= 115 and angle <= 125:
        return 'trine'
    elif angle >= 170 and angle <= 180:
        return 'opposition';
    else:
        return 'noaspect';




    