#---------------------------------------------------------------------------------------------------------------
# Program Name: Class Collection
# Programmer: Ava Oveisi
# Date: June 16, 2019
# Inptut: data.xls file containing information about the cities in the displayed map (city names, UTM coordinates,
#   population and population per square km), the UTM of the top left corner of the map, the UTM, depth and magnitude
#   of the earthquake, the inclusion of an I/O file and display options which is all on the PySimpleGUI input window,
#   and the classCollections.py file containing all the required classes
# Output: Creates a map using all data given, graphs the earthquake, colors the gridsquares based on the earthquake
#   intensity or the estimated population of the region, outputs the number of people effected by which intensity of
#   the earthquake. Options for display can be turned on and off.
#---------------------------------------------------------------------------------------------------------------
#imports
import os
import PySimpleGUI as sg
import pygame
import math
from classCollections import *

#colors
white = (255,255,255)
darkgrey = (200,200,200)

#variables
isRunning = True
inInput = True
createMapWindow = False

#screen and map dimensions
#In kms
mapWindowWidth = 300
mapWindowHeight = 150
#In pixels
screenWidth = 600
screenHeight = 300

#pysimplegui layout
inputLayout = [[sg.Text('UTM Coordinates of Top Left Corner of Map')],
               #put the middle of the screen as default coordinatese for the x and y
               #Decrease the field of input
               [sg.Text('UTM-x'),sg.Input(default_text ='611127.64',key = 'mapTopLeftx',size = (20,20)),sg.Text('UTM-y'),sg.Input(default_text='4973647.18',key = 'mapTopLefty',size = (20,20)),sg.Text('Grid Square Width'),sg.Input(default_text ='5',key = 'squareWidth',size = (20,20))],
               [sg.Text('Earthquake Coordinates')],
               #put the middle of the screen as default coordinatese for the x and y
               #800 x 400 km 660349.41+800000    4873817.33 - 400000
               [sg.Text('UTM-x'),sg.Input(default_text ='891127.64',key = 'earthquakex',size = (20,20)),sg.Text('UTM-y'),sg.Input(default_text ='4848647.18',key = 'earthquakey',size = (20,20))],
               [sg.Text('Magnitude')],
               [sg.Slider((1,7),resolution =0.1,orientation = 'h', size = (30,20),key = 'mag'),sg.Text('Earthquake Depth'),sg.Input(default_text ='5',key = 'depth',size = (20,20))],
               [sg.Checkbox('I/O file is being used',key='I/O')],
               [sg.Text('Select option to display')],
               [sg.Checkbox('Earthquake',key='earthquakeDisplay'),sg.Checkbox('Gridlines',key = 'gridlines'), sg.Checkbox('Cities',key = 'citiesVisible')],
               #if time include this in the map
               [sg.Radio('Colour based on population','color',key='populationColor'),sg.Radio('Colour based on earthquake intensity','color',key='intensityColor'), sg.Radio('Colour based on both','color',key='both color')],
               [sg.Text('')],
               #integrating pygame
               [sg.Graph((screenWidth,screenHeight), (0,0), (screenWidth,screenHeight), background_color='lightblue', key='_GRAPH_' )],
               [sg.Button('Apply'),sg.Button('Intensity and Population Effected'),sg.Exit()]] #cancel and ok are default buttons

#functions
def clearScreen():
    '''clean pygame window screen'''
    mapWindow.fill(white)
    pygame.display.update()

def ispositivefloat(value):
    '''return True of False if given string can be converted to float'''
    try:
        float(value)
        return True
    except ValueError:
        return False

#pygame implementation in PySimpleGUI
inputWindow = sg.Window('Input Data',inputLayout).Finalize()
graph = inputWindow.Element('_GRAPH_')
embed = graph.TKCanvas
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

#pygame window
mapWindow = pygame.display.set_mode((screenWidth,screenHeight))
pygame.init()
clearScreen()

#main loop
while True:
    event, values = inputWindow.Read(timeout = 10)
    #exit if exit button is clicked
    if event in (None, 'Exit'):
        break
    #apply all changes made to inputs if apply is clicked
    elif event == 'Apply':
        #make a pop up window if not all the input values are the correct type
        if not(ispositivefloat(values['mapTopLeftx']) and ispositivefloat(values['mapTopLefty']) and \
                  ispositivefloat(values['earthquakex']) and ispositivefloat(values['earthquakey']) and \
                  ispositivefloat(values['depth']) and ispositivefloat(values['squareWidth'])):
            sg.Popup('The input type for the UTM corrdinates or the Earthquake depth or grid square width was not correct. Please try again.')
        #all inputs should be positive
        elif not(float(values['mapTopLeftx']) >= 0 and float(values['mapTopLefty'])>= 0 and \
                  float(values['earthquakex'])>= 0 and float(values['earthquakey'])>= 0 and \
                  float(values['depth'])>= 0 and float(values['squareWidth'])>= 0):
            sg.Popup('Input values should all be positive. Please try again.')
        #the minimum value for the square width is 2 since 1 will give it a recusion error
        elif float(values['squareWidth']) < 2:
            sg.Popup('The minimum square width is 2')
        elif mapWindowWidth % float(values['squareWidth']) != 0 or mapWindowHeight % float(values['squareWidth']) != 0:
            sg.Popup('The square width should divide evenly in the map width (300km) and height (150km). Give values such as 2,5,10...')
        else:
            clearScreen()
            #store all input values
            #UTM coordinates of top left corner of map
            mapUTMx = float(values['mapTopLeftx'])
            mapUTMy = float(values['mapTopLefty'])
            squareWidth = float(values['squareWidth'])
            #UTM coordinates of earthquake
            eqUTMx = float(values['earthquakex'])
            eqUTMy = float(values['earthquakey'])
            #magnitude
            mag = values['mag']
            depth = float(values['depth'])
            IOincluded = values['I/O']
            earthquakeDisplay = values['earthquakeDisplay']
            gridlinesDisplay = values['gridlines']
            citiesVisible = values['citiesVisible']
            populationColorDisplay = values['populationColor']
            intensityColorDisplay = values['intensityColor']
            #color based on both earthquake intensity and population
            bothColor = values['both color']
            #create earthquake instance
            earthquake = Earthquake((mapUTMx,mapUTMy),(int(eqUTMx),int(eqUTMy)),mag,depth, mapWindowWidth,mapWindowHeight\
                                    ,screenWidth = screenWidth, screenHeight = screenHeight, intensityRadiusVisible = intensityColorDisplay or bothColor)
            if not earthquakeDisplay:
                earthquake.visible = False
            earthquake.draw(mapWindow)
            #use I/O file is being used
            if IOincluded:
                data = InputData()
                #create Map instance with information given in the I/O file
                themap = Map((mapUTMx,mapUTMy),mapWindowWidth,mapWindowHeight,squareWidth, screenWidth = screenWidth, \
                             screenHeight = screenHeight, cityNames = data.citites, cityCoordinates = data.UTMxy, \
                             cityPopulations = data.population, cityPopulationsPerSquareKm = data.populationPerKm, \
                             isColorBasedonPopulation = populationColorDisplay or bothColor,gridlineColor = darkgrey, \
                             areCitiesVisible = citiesVisible, isGridlinesVisible = gridlinesDisplay)
            else:
                #create Map instance without using the I/O file
                themap = Map((mapUTMx,mapUTMy),mapWindowWidth,mapWindowHeight,squareWidth, screenWidth = screenWidth,\
                             screenHeight = screenHeight, gridlineColor = darkgrey, isColorBasedonPopulation = populationColorDisplay or bothColor,\
                             isGridlinesVisible = gridlinesDisplay, areCitiesVisible = citiesVisible)
            themap.drawGridlines(mapWindow)
    #output the number of poeple effected by what earthquake intensity
    elif event == 'Intensity and Population Effected':
        IOincluded = values['I/O']
        if IOincluded:
            popIntensityEffected = themap.popIntensityEffected((eqUTMx,eqUTMy), data.population, earthquake.intensityRadius)
            print = sg.EasyPrint
            for popEffected in popIntensityEffected:
                sg.Print('A total of ' + str(int(popEffected[1])) + ' number of people experienced an Earthquake Intensity of ' + str(popEffected[0]))
    pygame.display.update()
        
inputWindow.Close()
pygame.quit()
'''
References:
Integrating pygame in pysimplegui:
https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_PyGame_Integration.py

Pysimplegui documentation: 
https://pysimplegui.readthedocs.io/en/latest/#popup-output

Checking if string can be converted to float:
https://stackoverflow.com/questions/736043/checking-if-a-string-can-be-converted-to-float-in-python
'''
