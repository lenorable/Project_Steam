# ______        __       ____________________________________________________________________________________
#|  ____/\     /_ |     / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
#| |__ /  \     | |    / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / 
#|  __/ /\ \    | |   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /  
#| | / ____ \   | |  / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /   
#|_|/_/    \_\  |_| /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/ 

def get_delers(n):
    divisors = []
    
    for i in range(1, int(n / 2) + 1):
            if n % i == 0:
                divisors.append(i)
    divisors.append(n)

    return sorted(divisors)

def is_prime(n):
    if len(get_delers(n)) == 2:
        return True
    else:
        return False

def primes(num):
    primelist = []

    for i in range(1, int(num)):
        if is_prime(i) == True:
            primelist.append(i)

    return sorted(primelist)

def primefactors(n):
    factors = []

    usefull = []
    if n >= 2:
        terug = primes(n+1)
        for i in terug:
            usefull.append(i)

    for i in usefull:
        while (n % i) == 0:
            n = n/i
            factors.append(i)


    return sorted(factors)

def gcd(a, b):
    while (b) > 0:
            if (a - b) > 0: 
                a = a - b
            elif (a-b) == 0:
                return a
            else:
                x = a
                a = b
                b = x

    return x

def lcm(a, b):
    return int((a*b)/gcd(a, b))

# ______        ___        ____________________________________________________________________________________
#|  ____/\     |__ \      / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
#| |__ /  \       ) |    / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / 
#|  __/ /\ \     / /    / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /  
#| | / ____ \   / /_   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /   
#|_|/_/    \_\ |____| /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/  

def simple_sort(lst):
    lst = []

    for item in lst:
        lst.append(item)

    index = 0
    max_index = len(lst)-1
    
    while True:
        if index < max_index:
            if lst[index] > lst[index+1]:
                save = lst[index]
                lst[index] = lst[index+1]
                lst[index+1] = save
                index=0
            else:
                index += 1
        else:
            return lst

def binary_search_recursive(lst, target):
    high_index = len(lst)-1
    low_index =  0

    while True:
        if high_index <= low_index:
            if lst[round((low_index+high_index)/2)] == target:
                return True
            else:
                return False

        if lst[round((low_index+high_index)/2)] == target:
            return True
        elif lst[round((low_index+high_index)/2)] > target:
            high_index = round((low_index+high_index)/2) -1
        elif lst[round((low_index+high_index)/2)] < target:
            low_index = round((low_index+high_index)/2) +1

# ______        ____        ____________________________________________________________________________________
#|  ____/\     |___ \      / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
#| |__ /  \      __) |    / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / 
#|  __/ /\ \    |__ <    / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /  
#| | / ____ \   ___) |  / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /   
#|_|/_/    \_\ |____/  /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/    

def mean(lst):
    return sum(lst) / len(lst)

def rnge(lst): #Bepaal het bereik van een lijst getallen.
    lst.sort()
    return lst[len(lst)-1] - lst[0] 

def median(lst):
    lst.sort() #je werkt voor het mediaan met een gesoorteerde lijst. 

    if (len(lst) % 2) == 0: #als de lengte van de lijst even is zijn er 2 gemiddelde getallen anders is er 1
        return (lst[int((len(lst)+1)/2 -1)] + lst[int((len(lst)+1)/2)]) / 2 #pak het getal uit een gelijst dat net voor het gemiddelde licht, en het getal net achter het gemiddelde en deel de som daarvan door 2

    return float(lst[int((len(lst)+1)/2 -1)])

def q1(lst):
    max = median(lst)
    lst.sort()

    use =[]

    for item in lst:
        if item < max:
            use.append(item)

    return median(use)

def q3(lst):
    max = median(lst)
    lst.sort()

    use =[]

    for item in lst:
        if item > max: #het zelfde als Q1 maar dan groter dan de median inplaats van kleiner dan.
            use.append(item)

    return median(use)

def var(lst):
    gemiddelde = sum(lst) / len(lst) #bereken het gemiddelde

    var_res = sum((item - gemiddelde) ** 2 for item in lst) / len(lst) #pak de som van elk (item in de lijst - het gemiddelde) tot de macht 2 en deel die som door de lengte van de list

    return var_res #return het berekende getal

def std(lst):
    return var(lst) ** 0.5 #pak de wortel van de variantie van de lijst

def freq(lst):
    freqs = {} #maak de dictionary aan
    
    for item in lst:
        if item in freqs:
                freqs[item] += 1 #als het getal al een keer eerder is voorgekomen tel je hoe vaak die is gebruikt +1 op
        else:
                freqs[item] = 1 #als het getal niet eerder is voorgekomen voeg je deze met count 1 toe aan de dictionary

    return freqs #return de dictionary

def modes(lst):
    modi = [] #maak een lijst variabel aan
    max = 0 #maak een variabel aan die bijhoud hoe vaak het meest voorkomende getal voorkomt. begin met 0
    freqinfo = freq(lst) #krijg van elke getal in de lijst de frequensie door middel van de eerdergemaakte functie
    
    for item in freqinfo:
        if freqinfo[item] > max: #voor elk getal (met hoe vaak het voor komt) in "freqinfo" check je of het getal vaker voorkomt dan max.
            max = freqinfo[item] #als dat zo is verander je de max naar dit nieuwe getal
    
    for item in freqinfo:
        if freqinfo[item] == max: 
            modi.append(item) #als een getal even vaak voor komt als het variabel max is dit een modi en dus voeg je hem toe aan modi


    return sorted(modi) #return modi op een gesoorteerde manier