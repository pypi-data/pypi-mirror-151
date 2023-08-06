
# pyChemEng

pyChemEng is a Python package for understanding and representing multiple adsorption and kinetic models in the chemical thermodynamics spectrum. This project is an initiative considering research scientists for the unequivocal representation of the models with all the useful information. 

## Installation

###  Dependencies

Users are encouraged to update the required dependencies with the latest version.

pyChemEng requires:

```bash
  Python 
  NumPy 
  SciPy 
  Matplotlib 
  Math
```
### User Installation

If you already have a working installation of required dependencies, the easiest way to install pyChemEng is using `PIP`:

```bash
  pip install chempy-ad
```

## Documentation

Soon to be updated

[Documentation](https://linktodocumentation)


## Changelog

See the changelog for a history of notable changes to pyChemEng.

## Examples

The variables `x` and `y` are established initially as a list. Later, the function isotherm is called with all the parameters set to `True` for the graphs that could be produced with the function. The same procedure adheres to the `kinetics` function.

The following is a precedent for implementing the package for adsorption isotherms models. All the available outputs are called for the current example. 

```
  plot    -->  Varying adsorption (i.e., y) with concentration in the solution at equilibrium (i.e., x)     
  comp    -->  Predicted values vs experimetal values 
  res     -->  Residuals 
  std_res -->  Standardised residuals
```


```
  from adsorption import *

  x = [0.36, 1.26, 2.69, 3.95, 5.93, 8.98, 16.89, 26.23]
  y = [3.76, 6.15, 12.35, 14.49, 17.39, 21.96, 22.93, 23.17]

  isotherm(x,y,ad_model=langmuir,plot=True,comp=True,res=True,std_res=True)

```

Currently available adsorption isotherm models in this package are:

```
  langmuir
  freundlich
  toth
  sips
  temkin
  dubinin
```


The following is a precedent for implementing the package for adsorption kinetic models. All the available outputs are called for the current example. 

```
  plot    -->  Varying adsorption (i.e., y) with time (i.e., x)     
  comp    -->  Predicted values vs experimetal values 
  res     -->  Residuals 
  std_res -->  Standardised residuals
```

```
  from kinetics import *

  x = [61.60,118.84,178.81,237.37,299.17,414.08,540.83]
  y = [7.77,10.02,11.45,13.09,13.91,14.32,14.32]
  
  kinetics(x,y,Kn_model=pfo,plot=True,comp=True,res=True,std_res=True)
```

Currently available adsorption kinetic models in this package are:

```
  pfo
  pso
  elovich
  sips
  temkin
  dubinin
```
pfo --> Pseudo First Order

pso --> Pseudo Second Order

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@Ashane Fernando](https://github.com/Ashane-F/)

