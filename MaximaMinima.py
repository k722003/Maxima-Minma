import re, math

P = (r'\+?(\-?\s?\d*\.?\d*){}(\^?\-?\d*\.?\d*)')
def parse(y, var):
    """
    Parse the function y(var)
    """
    terms = re.findall(P.format(var), y)
    nterms = {}
    for i in range(len(terms)): #To fix empty elements in result
        b = 1 # a is the coeff and b is the power
        temp = terms[i][0].replace(' ', '')
        if temp == '-': a = -1
        elif not temp: a = 1 
        else: a = eval(temp)
        if terms[i][1]: b = eval(terms[i][1].strip('^'))
        if b in nterms: nterms[b] += a #To add elements with same powers
        else: nterms[b] = a
    #Get terms in decreasing order of power and skip canceled terms
    return sorted(((nterms[i], i) for i in nterms if nterms[i]), 
            key = lambda x: x[1], reverse = True) or [(eval(y), 0)]

def equation(terms, var):
    """
    Reverses the parse function and returns function y(var) as string
    """
    y = ''
    for i in terms:
        if i[0] == 1: a = ''
        elif round(i[0]) == i[0]: a = round(i[0])
        else: a = i[0]
        
        if i[1] not in (0, 1): b = '^' + str(i[1])
        elif round(i[1]) == i[1] and i[1] > 1: b = '^' + str(round(i[1]))
        else: b = ''
        
        y += '{} {}{}{}'.format(' +' if i[0]>0 else '', a, var if i[1] else '', b)
    return y.strip('+ ').replace('-', '- ').replace('^- ', '^-') or '0'

def derivative(y, var, n = 1):
    """
    Finds the nth order derivative of the function y(var)
    """
    if var not in y: return '0'
    for _ in range(n):
        terms = parse(y, var)
        for i in range(len(terms)):
            a, b = terms[i]
            terms[i] = (a*b, b - 1) #Computes derivative of term at index i
        y = equation(terms, var)
    return y

p1, p2, p3 = re.compile(r'\s{1}\*'), re.compile(r'\^'), re.compile(r'\-\*')
def fnify(y, var):
    """
    Returns a lambda function equivalent to:
    lambda <var>: <y>
    """
    return eval('lambda {}: {}'.format(var, 
    p1.sub('', ' ' +p3.sub('-', p2.sub('**', y).replace(var, '*'+var)))))

def generator(a, b, step = 1):
    A = B = (a+b)//2
    while a <= A and B <= b:
        yield (A, B)
        A, B = A - step, B + step

def roots(y, x0, x1, var):
    """
    Returns the roots of the function y(var)
    x0: Lower limit, x1: Upper limit
    """
    parsed, solutions, Len = parse(y, var), [], 0
    f, step, degree = fnify(y, var), 1, abs(max([(i[1]) for i in parsed]))
    #Naive Solution
    if re.findall(r'\^\d*\.\d*', y) and x0 < 0: x0 = 0
    while step > 0.001 and len(solutions) < degree:
        for k in generator(x0, x1, step): 
            i, j = round(k[0], Len), round(k[1], Len)
            try:
                if (i not in solutions) and f(i) == 0: 
                    solutions.append(i)
            except ZeroDivisionError: pass
            try:
                if (j not in solutions) and f(j) == 0: 
                    solutions.append(j)
            except ZeroDivisionError: pass
        step, Len = step/10, Len + 1
    return solutions

def signum_fn(x):
    if x < 0: return -1
    if x > 0: return 1
    return 0

def maxima_minima(y, x0, x1, var = 'x'):
    """
    Returns [(a, b, c)1, (a, b, c)2...] where
    a = Value of y at a, i.e y(a) = Maxmium/Minimum Value
    b = Point of maxima/minima
    c = SignumFunction(y2(b))
    """
    y1 = derivative(y, var)
    y2 = derivative(y1, var)
    f2, f = fnify(y2, var), fnify(y, var)
    crit_points = set(roots(y1, x0, x1, var) + [x0, x1])
    return sorted(((f(i), i, signum_fn(f2(i))) for i in crit_points))

if __name__ == '__main__':
    equ = [
        ('x^3 - 3x', -2, 2),
        ('0.5x + 2x^-1', -10, 10),
        ('41 - 72x - 18x^2', -10000, 10000),
        ('x^3 - 6x^2 +9x + 15', -10, 10),
        ('x^3', -2, 2),
        ('4s - 0.5s^2', -2, 4.5, 's'),
        ('3x^4 - 8x^3 + 12x^2 - 48x + 25', 0, 3),
        ('2x^3 - 24x + 107', 1, 3),
        ]
    k = -1
    print(maxima_minima(*equ[k]))