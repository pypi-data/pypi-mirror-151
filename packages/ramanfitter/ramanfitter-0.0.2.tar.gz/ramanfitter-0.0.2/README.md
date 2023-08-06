# ramanfitter

This package seeks to provide and easy and efficient matter for fitting Raman data with Lorentzian, Gaussian, or Voigt models.

Developed by John Ferrier, NEU Physics (c) 2022

## Quickstart Example

For a simple run,
```python
import os
import numpy as np
from ramanfitter import RamanFitter

filename    = os.path.join( 'path', 'to', 'data.csv' )      # Get File
data        = np.genfromtxt( filename, delimiter = ',' )    # Open File

x           = data[ :, 0 ]                                  # Parse x-values
y           = data[ :, 1 ]                                  # Parse y-values

RF          = RamanFitter( x = x, y = y, autorun = True )   # Run Fitter automatically

components  = RF.comps                                      # Returns a dictionary of each curve plot
curveParams = RF.params                                     # Returns a dictionary of the parameters of each Lorentzian, Gaussian, or Voigt curve
bestFitLine = RF.fit_line                                   # Returns the plot data of the model
```

For more control over parameters

```python
import os
import numpy as np
from ramanfitter import RamanFitter

filename    = os.path.join( 'path', 'to', 'data.csv' )      # Get File
data        = np.genfromtxt( filename, delimiter = ',' )    # Open File

x           = data[ :, 0 ]                                  # Parse x-values
y           = data[ :, 1 ]                                  # Parse y-values

RF          = RamanFitter( x = x, y = y, autorun = False )  # Run Fitter automatically


''' Each step ran when autorun = False '''
RF.NormalizeData()
RF.Denoise( ShowPlot = True )
RF.FindPeaks( showPlot = True )
RF.FitData( type = 'Voigt', showPlot = True )


components  = RF.comps                                      # Returns a dictionary of each curve plot
curveParams = RF.params                                     # Returns a dictionary of the parameters of each Lorentzian, Gaussian, or Voigt curve
bestFitLine = RF.fit_line                                   # Returns the plot data of the model
```