#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:44:27 (CST) daisuke>
#

# making a dictionary
dic_star_mag = {
    'Sirius': -1.46,
    'Canopus': -0.72,
    'Rigil Kentaurus': -0.27,
    'Arcturus': -0.04,
    'Vega': 0.03,
    'Capella': 0.08,
    'Rigel': 0.12,
    'Procyon': 0.38,
    'Achernar': 0.46,
    'Betelgeuse': 0.50,
}

# printing a dictionary
print (dic_star_mag)

# adding an element
dic_star_mag['Hadar'] = 0.61

# printing a dictionary
print (dic_star_mag)

# accessing an element
print ("visual mag of Vega =", dic_star_mag['Vega'])

# making a dictionary of dictionaries
dic_stars = {
    'Sirius': {
        'mag': -1.46,
        'dist': 2.670,
        'sptype': 'A0V',
    },
    'Canopus': {
        'mag': -0.72,
        'dist': 95,
        'sptype': 'A9II',
    },
    'Rigil Kentaurus': {
        'mag': -0.27,
        'dist': 1.339,
        'sptype': 'G2V',
    },
    'Arcturus': {
        'mag': -0.04,
        'dist': 11.26,
        'sptype': 'K1.5III',
    },
    'Vega': {
        'mag': -0.04,
        'dist': 7.68,
        'sptype': 'A0V',
    },
}

# printing dictionary of dictionaries
print (dic_stars)

# accessing to an element
print ("dic_stars['Canopus']['dist'] =", dic_stars['Canopus']['dist'], "pc")
