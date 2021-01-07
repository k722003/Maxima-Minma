# Maxima-Minma

Function maxima_minima takes 3 required arguments and 1 optional argument:  
    y - Equation of curve to find maxima/minima in the interval [x0,x1]  
    x0 - Lower limit  
    x1 - Upper Limit  
    var - Variable in equation, default value 'x'  

It returns [(a, b, c)1, (a, b, c)2...] where  
    a = Value of y at a, i.e y(a) = Maxmium/Minimum Value  
    b = Point of maxima/minima  
    c = SignumFunction(y2(b))  
Supports polynomial equations of the form ax^n + .... + z  

P.S: This was a school project
