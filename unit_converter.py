class Term(object):
#    coefficient = 0
#    power = 1
    def __init__(self, *args):
        self.unit = None

        lead = args[0]
        if type(lead) == type(self):
            self.data = dict(lead.data)
            self.coefficient = lead.coefficient
        elif type(lead) == int:
            self.from_constant(lead)
        elif type(lead) == float:
            self.from_constant(lead)
        elif type(lead) == str:
            self.from_symbol(*args)
        elif type(lead) == dict:
            self.from_dictionary(*args)
        else:
            self.from_lists(*args)

    def from_constant(self, constant):
        #print constant
        self.coefficient = constant
        self.data = {}

    def from_symbol(self, symbol, coefficient=1, power=1):
        #print symbol
        #print type(symbol)
        power, self.unit = self.parser(symbol)
        self.coefficient = coefficient * power
        self.data = {self.unit: 1}

    def from_dictionary(self, data, coefficient=1):
        self.data = data
        self.coefficient = coefficient

    def from_lists(self, symbols=(), powers=(), coefficient=1):
        self.coefficient = coefficient
        self.data = {symbol: exponent for symbol, exponent in zip(symbols, powers)}

    def parser(self, something):
        suffix = ['meters','seconds']
        prefix = ['kilo', 'meters', 'seconds', 'deci', 'centi', 'milli']
        powers = {'kilo': 1000, 'meters': 1, 'seconds': 1,
                  'deci':0.1, 'centi': 0.01, 'milli': 0.001}

        tmp = ''
        something = str(something)
        while len(something) > 0:

            c = something[:1]
            something = something[1:]
            tmp += c

            if tmp in prefix:
                prefix = tmp
                suffix = something
                if len(suffix) == 0:
                    suffix = tmp

                break

        return powers[prefix], suffix

    def add(self, *others):
        return Expression((self,)+others)

    def multiply(self, *others):
        result_data = dict(self.data)
        result_coeff = self.coefficient
        # Convert arguments to Terms first if they are
        # constants or integers
        others = map(Term,others)
        for another in others:
            for symbol, exponent in another.data.iteritems():
                if symbol in result_data:
                    result_data[symbol] += another.data[symbol]
                else:
                    result_data[symbol] = another.data[symbol]
            result_coeff *= another.coefficient
        #print result_data, result_coeff

        newTerm = Term(result_data, result_coeff)
        if self.unit == None:
            newTerm.unit = others[0].unit
        else:
            newTerm.unit = self.unit

        return newTerm

    def to(self, format):
        divisors = {'minutes': 60.0, 'hours': 3600.0}

        if self.unit != 'seconds':
            raise IncompatibleUnitsError('Cannot convert meters to ' + str(format))

        self.coefficient /= divisors[format]
        self.unit = format
        self.data = {format: 1}

        return self;

    def equal(self, *others):
        # Convert arguments to Terms first if they are
        # constants or integers
        others = map(Term,others)

        if others[0].data != self.data:
            raise IncompatibleUnitsError('Cannot compare different units!')

        return self.coefficient == others[0].coefficient

    def __eq__(self, other):
        return self.equal(other)

    def __add__(self, other):
        return self.add(other)

    def __mul__(self, other):
        return self.multiply(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        def symbol_string(symbol, power):
            if power == 1:
                return symbol
            else:
                return symbol+'^'+str(power)
        symbol_strings = [symbol_string(symbol, power) for symbol, power in self.data.iteritems()]
        prod = '*'.join(symbol_strings)
        if not prod:
            return str(self.coefficient)
        if self.coefficient == 1:
            return prod
        else:
            return str(self.coefficient)+'*'+prod

    def __int__(self):
        #print self.data[0]
        return self.coefficient# * self.data[0]

############################################################

class Expression(object):
    def __init__(self, terms=[]):
        all_units = set()
        for term in list(terms):
            all_units.add(term.unit)

        if len(all_units) > 1:
            raise IncompatibleUnitsError('Cannot add elements of different unit!')

        self.terms=list(terms)

    def add(self, *others):
        result = Expression(self.terms)

        for another in others:
            if type(another) == Term:
                result.terms.append(another)
            else:
                result.terms += another.terms
        return result

    def multiply(self, another):
        # Distributive law left as exercise
        pass

    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        return '+'.join(map(str,self.terms))


class IncompatibleUnitsError(Exception):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return repr(self.value)