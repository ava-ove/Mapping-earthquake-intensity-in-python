#---------------------------------------------------------------------------------------------------------------
# Program Name: Class Collection
# Programmer: Ava Oveisi
# Date: June 16, 2019
# Description: Contains the Grid, Earthquake, Map, GridSquare, InputData and Label class to be used in the MainProgram.py
#---------------------------------------------------------------------------------------------------------------
#imports
import pygame
import math
import csv

class Grid:
    def __init__(self, rect, cellWidth, cellHeight, gap=0, visible = True, itemData = None):
        pygame.init()
        self.rect = rect
        self.x = self.rect[0]
        self.y = self.rect[1]
        self.width = self.rect[2]
        self.height = self.rect[3]
        self.cellWidth = cellWidth 
        self.cellHeight = cellHeight 
        self.r = (self.x,self.y, self.cellWidth, self.cellHeight)
        
        #get rows and columns
        self.rows = int(math.ceil(self.height // self.cellHeight))
        self.clmns = int(math.ceil(self.width // self.cellWidth))

        self.gap = gap
        self.visible = visible
        self.itemData = itemData
        
        self.coordinates = self.loadCoordinates()
        self.totalCells = self.rows * self.clmns
        self.currentCell = -1

    def loadCoordinates(self):
        '''return the x,y coordinates of the cells in a list'''
        xycoord = []
        xc = self.x + self.gap
        yc = self.y + self.gap
        for r in range(self.rows):
            for c in range(self.clmns):
                xycoord.append([xc, yc])
                xc += self.gap + self.cellWidth
            yc += self.gap + self.cellHeight
            xc = self.x + self.gap
        return xycoord
            
    def draw(self, w, rect):
        '''draw cells if grid is visible'''
        if self.visible:
            for i,c in enumerate(self.coordinates):
                if i == self.currentCell:
                    pygame.draw.rect(w,(255,0,0),(c[0],c[1],self.cellWidth,self.cellHeight),1)
                else:
                    pygame.draw.rect(w,(0,0,0),(c[0],c[1],self.cellWidth,self.cellHeight),1)
    
    def  overOrClickedInd(self,mp):
        '''return the cell that was clicked or was over, if no cell was on or clicked, returns -1'''
        for i,bxy in enumerate(self.coordinates):
            #check if x and y coordinates of mp are inside button
            inx = bxy[0] < mp[0] < bxy[0]+self.cellWidth
            iny = bxy[1] < mp[1] < bxy[1]+self.cellHeight
            if inx and iny:
                self.currentCell = i
                return i
        self.currentCell = -1
        return -1

    def isOver(self,mp):
        '''returns True if inside a rectangle is clicked, else returns False'''
        return pygame.Rect(self.r).collidepoint(mp) == 1

    def arrowInput(self, key):
        '''move current cell focus using up,down,left and right arrows'''
        '''return true if focused cell is eneterd, else return False'''
        if key == pygame.K_UP:
            if self.currentCell - self.clmns >= 0:
                self.currentCell -= self.clmns
        elif key == pygame.K_DOWN:
            if self.currentCell + self.clmns < self.totalCells:
                self.currentCell += self.clmns
        elif key == pygame.K_LEFT:
            if self.currentCell % self.clmns != 0:
                self.currentCell -= 1
        elif key == pygame.K_RIGHT:
            if self.currentCell % self.clmns != self.clmns - 1:
                self.currentCell += 1
        elif key == pygame.K_RETURN:
            return True
        return False

class Earthquake:
    def __init__(self, mapUTM, UTMposition, magnitude, depth, mapWidth,mapHeight,screenWidth = 300, screenHeight = 150, \
                 pointColor = (0,0,0),pointRadius = 5, intensityRadiusVisible = True, visible = True, itemData = None):
        pygame.init()
        #UTM of top left corner of map 
        self.mapUTM = mapUTM
        self.mapUTMx = self.mapUTM[0]
        self.mapUTMy = self.mapUTM[1]
        #UTM of top left corner of earthquake 
        self.UTMposition = UTMposition
        self.UTMx = self.UTMposition[0]
        self.UTMy = self.UTMposition[1]

        self.magnitude = magnitude
        self.depth = depth
        
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        
        self.pointColor = pointColor
        self.pointRadius = pointRadius
        self.intensityRadiusVisible = intensityRadiusVisible
        self.visible = visible
        self.itemData = itemData

        #get pygame xy coordinates of the earthquake
        self.xy = Map.UTM_to_xy_point((self.mapUTMx,self.mapUTMy), (self.UTMx,self.UTMy), self.mapWidth,self.mapHeight,self.screenWidth,self.screenHeight)
        self.x = self.xy[0]
        self.y = self.xy[1]
        #intensity/radius list 
        self.intensityRadius = self.getIntensityRadius(self.magnitude, self.depth)
        #color for each integer intensity
        self.colorBasedonIntensity = []
        for intensityRadius in self.intensityRadius:
            self.colorBasedonIntensity.append(self.getIntensityColor(intensityRadius[0]))

    @staticmethod
    def getIntensityColor(intensity):
        '''return color based on intensity, each intensity from 1 to 9 gets its own color
        the higher the intensity the darker the red color'''
        if intensity == 9:
            return (102,0,0)
        elif intensity == 8:
            return (153,0,0)
        elif intensity == 7:
            return (204,0,0)
        elif intensity == 6:
            return (255,0,0)
        elif intensity == 5:
            return (255,51,51)
        elif intensity == 4:
            return (255,102,102)
        elif intensity == 3:
            return (255,153,153)
        elif intensity == 2:
            return (255,204,204)
        elif intensity == 1:
            return (255,230,230)
        else:
            return (255,0,0)

    @staticmethod
    def getIntensityRadius(M, d):
        '''return nested list containing the intensity/radius pair'''
        e = (2.7 ** (3.3089 * M)) * (10  ** -8) * 2
        eerg = e * (10 ** 20)
        ezero = eerg / (4 * math.pi * (d ** 2))
        Mzero = (math.log10(ezero/(2*(10^12)))) / (math.log10(2.7)*3.3089)
        Izero = round(1.5 * (Mzero - 1) + 1.5)
        intensityRadiusL = []
        for intensity in range(1, Izero):
            kk = eerg/(10**(1.42733*(1+(2/3)*intensity)+math.log10(2*(10**12))))
            rr = round(0.28217* math.sqrt(kk))
            intensityRadiusL.append([intensity, rr])
        #remove all but one of the zero radii
        for i,intR in enumerate(intensityRadiusL):
            if intR[1] == 0 and i != len(intensityRadiusL) - 1:
                return intensityRadiusL[:i+1]
        return intensityRadiusL

    @staticmethod
    def intensityOfUTMpoint(pointxy, eqxy, intensityRadius):
        '''based on intensity/radius pair list, the UTM of a point and the UTM of the earhtquake
        output the intensity of the point'''
        distx = abs(pointxy[0] - eqxy[0])/1000
        disty = abs(pointxy[1] - eqxy[1])/1000
        distance = math.sqrt(distx**2 + disty**2)
        #20
        for i,intRadius in enumerate(intensityRadius):
            if distance >= intRadius[1]:
                if i == 0:
                    return 0
                return intensityRadius[i-1][0]

    def draw(self,w):
        if self.visible:
            if self.intensityRadiusVisible:
                #draw from least intensity to most
                for i,intenRadius in enumerate(self.intensityRadius):
                    pygame.draw.circle(w, self.colorBasedonIntensity[i], (int(self.x),int(self.y)), intenRadius[1])
            #earthquake epicenter point
            pygame.draw.circle(w, self.pointColor, (int(self.x),int(self.y)), self.pointRadius)

class Map(Grid):
    def __init__(self, UTM00, mapWidth, mapHeight, squareWidth, screenWidth = 300, screenHeight = 200, \
                 cityNames = [],cityCoordinates = [], cityPopulations = [], cityPopulationsPerSquareKm = [], \
                 gridlineColor = (0,0,0), isColorBasedonPopulation = False, areCitiesVisible = True, \
                 isGridlinesVisible = True):
        pygame.init()
        self.fnt = pygame.font.SysFont('arial',10)
        #mao dimensions
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        #screen dimensions
        self.screenWidth =screenWidth
        self.screenHeight = screenHeight
        #width of each grid square in km and pixels
        self.squareWidth = squareWidth 
        self.pixelSquareWidth = self.UTM_to_xy_distance(self.squareWidth,self.screenWidth,self.mapWidth)

        #if gridsquares are chopped off on the sides of the screen, display them properly
        '''
        if self.screenWidth % self.pixelSquareWidth != 0 and self.screenHeight % self.pixelSquareWidth == 0:
            self.screenWidth += self.pixelSquareWidth

        elif self.screenWidth % self.pixelSquareWidth == 0 and self.screenHeight % self.pixelSquareWidth != 0:
            self.screenHeight += self.pixelSquareWidth
        else:
            self.screenWidth += self.pixelSquareWidth
            self.screenHeight += self.pixelSquareWidth
        '''

        Grid.__init__(self,(0,0,self.screenWidth,self.screenHeight),self.pixelSquareWidth,self.pixelSquareWidth)
        #UTM of top left corner of screen
        self.UTM00 = UTM00
        self.UTM00x = UTM00[0]
        self.UTM00y = UTM00[1]
        #city and population information
        self.cityNames = cityNames
        self.cityCoordinates = cityCoordinates
        self.cityPopulations = cityPopulations
        self.gridlineColor = gridlineColor
        self.popPerSquareKm = cityPopulationsPerSquareKm
        self.areCitiesVisible = areCitiesVisible
        self.isGridlinesVisible = isGridlinesVisible
        #list of colors based on population per square km
        self.isColorBasedonPopulation = isColorBasedonPopulation
        if self.cityNames != []:
            self.popColor = self.colorForPopulation()
        else:
            self.popColor = []
        self.gridSquaresProp = self.loadGridSquaresProp()
        self.gridsSquares = self.loadGridsSquares()

    @staticmethod
    def distanceBetween2Points(x1, y1, x2, y2):
        distx = abs(x1 - x2)
        disty = abs(y1 - y2)
        return math.sqrt(distx**2 + disty**2)
    
    @staticmethod
    def UTM_to_xy_point(UTM00, UTMpoint, mapWidth,mapHeight,screenWidth,screenHeight):
        '''convert UTM coordinates to xy corrdinates on a pygame window'''
        x = screenWidth*((UTMpoint[0]-UTM00[0])/1000)/mapWidth
        y = screenHeight*((UTM00[1]-UTMpoint[1])/1000)/mapHeight
        return (x,y)
    
    @staticmethod
    def UTM_to_xy_distance(distance,screenWidth,mapWidth):
        '''convert input distance in kms to the screen width in pixels'''
        xydistance = distance * screenWidth / mapWidth
        return xydistance

    def xy_to_UTM_point(self, UTM00, xypoint, mapWidth,mapHeight,screenWidth,screenHeight):
        '''convert xy coordinates in a pygame window to UTM coordinates'''
        x = (mapWidth*1000)*xypoint[0]/screenWidth
        x += self.UTM00x 
        y = (mapHeight*1000)*xypoint[1]/screenHeight
        y = self.UTM00y - y
        return (x,y)
        
    def loadGridSquaresProp(self):
        gridSquareProp = []
        for i,sRect in enumerate(self.coordinates):
            gridSquareProp.append([sRect[0],sRect[1]])
        return gridSquareProp
        
    def loadGridsSquares(self):
        squares = []
        for i,s in enumerate(self.gridSquaresProp):
            UTMsquare = self.xy_to_UTM_point(self.UTM00,(s[0],s[1]),self.mapWidth,self.mapHeight, self.screenWidth, self.screenHeight)
            square = GridSquare(UTMsquare,(s[0],s[1]), self.mapWidth, self.mapHeight, self.pixelSquareWidth, ocolor = self.gridlineColor)
            squares.append(square) 
        return squares

    def colorForPopulation(self):
        '''get color based on the number of different population per km exists'''
        numDiffPopulation = len(self.popPerSquareKm)
        colorgap = 255 // numDiffPopulation
        popColor = []
        for i in range(len(self.popPerSquareKm)):
            #decrease red color
            color = (255 - ((i+1)*colorgap),200,255)
            popColor.append(color)
        return popColor

    def populationPerSquare(self, cityName, UTM, population, popPerSquareKm, popColor):
        #calculate population per squaer only if the cityUTM falls in the map
        if (self.UTM00x < UTM[0] < self.UTM00x + self.mapWidth * 1000) and (self.UTM00y > UTM[1] > self.UTM00y - self.mapHeight * 1000):
            #get the xy coordinates of the closest square to the cityUTM given (adjusted)
            cityUTMxamountToAdjust = (UTM[0] - self.UTM00x) % (self.squareWidth * 1000)
            cityUTMyamountToAdjust = (self.UTM00y - UTM[1]) % (self.squareWidth * 1000)
            cityAdjustedUTMx = UTM[0] - cityUTMxamountToAdjust
            cityAdjustedUTMy = UTM[1] + cityUTMyamountToAdjust

            ifocusSquare = -1
            for i,square in enumerate(self.gridsSquares):
                if square.UTMCoordinates == (cityAdjustedUTMx,cityAdjustedUTMy):
                    ifocusSquare = i
                    break
            if ifocusSquare != -1:
                self.setPopulationToSquare(ifocusSquare, population, popPerSquareKm,popColor)
        
    def setPopulationToSquare(self, i, population, popPerSquareKm, popColor, populationCovered = 0):
        '''recursive formula calculates and estimated population per square of the map and sets it to all squares'''
        popPerSquare = popPerSquareKm * (self.squareWidth ** 2)
        totalCityPopulation = 0
        if populationCovered <= population:
            self.gridsSquares[i].population = popPerSquareKm
            self.gridsSquares[i].fcolor = popColor
            
            #upper gridsquare
            if i not in range(0,self.clmns) and self.gridsSquares[i-self.clmns].population == 0:
                self.gridsSquares[i-self.clmns].population = popPerSquare
                self.gridsSquares[i-self.clmns].fcolor = popColor
                self.setPopulationToSquare(i-self.clmns, population, popPerSquareKm, popColor, populationCovered+popPerSquare)
                
            #right gridsquare
            if (i+1)%self.clmns != 0 and self.gridsSquares[i+1].population == 0:
                self.gridsSquares[i+1].population = popPerSquare
                self.gridsSquares[i+1].fcolor = popColor
                self.setPopulationToSquare(i+1, population, popPerSquareKm, popColor, populationCovered+popPerSquare)
                
            #bottom square
            if i not in range(len(self.gridsSquares) - self.clmns,len(self.gridsSquares))\
               and self.gridsSquares[i+self.clmns].population == 0:
                self.gridsSquares[i+self.clmns].population = popPerSquare
                self.gridsSquares[i+self.clmns].fcolor = popColor
                self.setPopulationToSquare(i+self.clmns, population, popPerSquareKm, popColor, populationCovered+popPerSquare)
                
            #left square
            if i%self.clmns != 0 and self.gridsSquares[i-1].population == 0:
                self.gridsSquares[i-1].population = popPerSquare
                self.gridsSquares[i-1].fcolor = popColor
                self.setPopulationToSquare(i-1, population, popPerSquareKm, popColor, populationCovered+popPerSquare)
        else:
            return 0

    def popIntensityEffected(self, eqUTM, populations, intensityRadius):
        '''calculate and return the numeber of people effected by each intensity'''
        popEffectedbyIntensity = []
        for i in range(10):
            popEffectedbyIntensity.append([i,0])
        for i,square in enumerate(self.gridsSquares):
            #if the gridsquare has population
            if square.population != 0:
                #find intensity of that gridsquare
                intensity = Earthquake.intensityOfUTMpoint(square.UTMCoordinates, eqUTM, intensityRadius)
                #add its population to popEffectedbyIntensity
                popEffectedbyIntensity[int(intensity)][1] += square.population
        return popEffectedbyIntensity
    
    def drawGridlines(self,w):
        #if color is based on popualtion and cities are included as an input
        if self.isColorBasedonPopulation and self.cityNames != []:
            #give each square its population
            for i,cityName in enumerate(self.cityNames):
                self.populationPerSquare(self.cityNames[i],self.cityCoordinates[i],self.cityPopulations[i],\
                                         self.popPerSquareKm[i], self.popColor[i])
        if self.isGridlinesVisible:
            for i,s in enumerate(self.gridsSquares):
                s.draw(w)
        if self.areCitiesVisible:
            for i,cityName in enumerate(self.cityNames):
                #blit city names
                cityNameSurface = self.fnt.render(cityName, False, (0,0,0))
                cityxy = Map.UTM_to_xy_point(self.UTM00,(self.cityCoordinates[i][0],self.cityCoordinates[i][1]), self.mapWidth,self.mapHeight,self.screenWidth,self.screenHeight)
                w.blit(cityNameSurface, cityxy)
                #blit circle for city locatioon
                pygame.draw.circle(w, (0,0,0), (int(cityxy[0]),int(cityxy[1])), 2)
        
    def changeLtrsFont(self,Type = 'arial',Size = 20):
        self.fnt = pygame.font.SysFont(Type,Size)
        for b in self.buttons:
            b.changeFont(Type,Size)

class GridSquare:
    pygame.font.init()
    fontsize = 25
    fonttype = 'arial'
    fnt = pygame.font.SysFont(fonttype,fontsize)

    def __init__(self, UTMCoordinates, xyCoordinates, mapWidth, mapHeight, squareWidth, population = 0, fcolor = None,\
                 ocolor = (0,0,0), font = None, visible = True, data = None):
        #all the properties and characteristics of a gridsquare
        pygame.init()
        #top left corner of map
        self.UTMCoordinates = UTMCoordinates
        self.UTMx = UTMCoordinates[0]
        self.UTMy = UTMCoordinates[1]
        #top left corner of the square
        self.xyCoordinates = xyCoordinates
        self.xCoordinate = self.xyCoordinates[0]
        self.yCoordinate = self.xyCoordinates[1]
        #map dimensions
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.squareWidth = squareWidth
        self.population = population
        #colors
        self.fcolor = fcolor
        self.ocolor = ocolor
        
        self.rect = (self.xCoordinate,self.yCoordinate,self.squareWidth, self.squareWidth)
        self.visible = visible
        self.data = data
        
    def draw(self,w):
        if self.visible:
            #if no color is given only draw the outline
            if self.fcolor != None:
                pygame.draw.rect(w,self.fcolor,self.rect,0)
            pygame.draw.rect(w,self.ocolor,self.rect,1)
                
    @staticmethod
    def getCenterOffset(x, y, wc, hc, wt, ht):
        '''return coordinates to center object'''
        xcenter = x + wc/2 - wt/2
        ycenter = y + hc/2 - ht/2
        return (xcenter, ycenter)

    def changeFont(self, Type = 'arial' , Size = 20):
        self.txt.changeFont(Type,Size)
        #center text if changes to size is made
        if Size != 20:
            xytxt = self.getCenterOffset(self.x,self.y,self.width, self.height,self.txt.width, self.txt.height)
            self.txt.x = xytxt[0]
            self.txt.y = xytxt[1]

class InputData:
    def __init__(self):
        self.citites = []
        self.UTMx = []
        self.UTMy = []
        self.UTMxy = []
        self.population = []
        self.populationPerKm = []
        #read file until getting to nothing in a cell
        with open('data.csv','r') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            for i,row in enumerate(data):
                #dont include first row that has the titles
                if i != 0:
                    self.citites.append(row[0])
                    self.UTMx.append(float(row[1]))
                    self.UTMy.append(float(row[2]))
                    self.population.append(float(row[3]))
                    self.populationPerKm.append(float(row[4]))

        for i in range(len(self.UTMx)):
            self.UTMxy.append((self.UTMx[i],self.UTMy[i]))
        
class Label:
    #font variables
    pygame.font.init()
    fontsize = 20
    fonttype = 'arialblack'
    fnt = pygame.font.SysFont(fonttype,fontsize)
    
    def __init__(self, x, y, text, color = (0,0,0), itemData = None):
        pygame.init()
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.surf = self.fnt.render(self.text, False, self.color)
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()
        self.itemData = itemData
        
    def draw(self, w):
        w.blit(self.surf, (self.x,self.y))
        
    def changeFont(self, Type = 'arialblack' , Size = 20):
        '''change the font type and font size of label'''
        self.fnt = pygame.font.SysFont(Type,Size)
        self.surf = self.fnt.render(self.text, False, self.color)
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()
'''
References
Earthquake intensity calculations: 
https://authors.library.caltech.edu/48033/1/105.full.pdf
'''
