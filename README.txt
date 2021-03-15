Input (I/O file called data.csv):
First row contains the titles (City Name, UTMx, UTMy, Population, Population per Square km). 
Each column should give the required information for each city. 
Note: The map will show a any 300 by 200 km surface given the top left coordinates of the map, therefore, the cities should have coordinates that falls in that map in order to be displayed.  



Input (PySimpleGUI window):
Default values are provided for some of the following inputs.
  - The UTMx and UTMy coordinates of the top left corner of the screen
  - The grid square width if gridlines are needed.
  - The UTMx and UTMy coordinates of the earthquake
  - Earthquake depth
  - Earthquake magnitude using a slider
The following are check box or radio inputs: 
  - I/O file is being used: If I/O file is being inputted
  - Earthquake: If earthquake is being displayed
  - Gridlines: If gridlines are being displayed
  - Colour based on population: If color of grid squares is based on population
  - Colour based on earthquake intensity: If color of grid square is based on earthquake intensity
  - Both: If color of gridsquares is based on both earthquake intensity and population 
Buttons at the bottom:
  - Apply: Apply the changes made in the inputs
  - Exit
  - Intensity and Population Effected: Displays the number of population effected by what intensity of the earthquake



Legend for Earthquake Intensity Color:
Black indicates the maximum intensity of 9 or above
White indicates an intensity of 0
Between black and white are a range of red shades, the darker the shade the higher the intensity in that region. 


Output:
Pygamewindow:
  - displays earthquake using a black dot
  - cities are indicated by smaller black dots with the city name written next to them
  - gridlines
  - colored circles around earthquake indicating the intensity
  - color in each square based on population, earthquake intensity or both.
EasyPrint window:
  - The intensity and the number of popualtion effected by it. 
IMPORTANT NOTE: For the easyPrint window to show the number of population effected by which intensity, the "color based on population" option should be 
selected and the "Apply" button should be clicked. Then the "Intensity and Population Effected" button should be clicked. 


