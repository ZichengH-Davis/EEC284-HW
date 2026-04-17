import math
from functools import reduce
from fractions import Fraction

p = [3,5,6,2]
c = [4,3,5,3]

q_frac = [Fraction(1, 1)] 
#p[i] * q[i] = c[i] * q[i+1]
#q[i+1] = q[i] * (p[i] / c[i])
for i in range(len(p)):
    next_q = q_frac[i] * Fraction(p[i], c[i])
    q_frac.append(next_q)

denoms = [x.denominator for x in q_frac]

lcm = denoms[0]
for i in range(1, len(denoms)):
    a = lcm
    b = denoms[i]

    lcm = abs(a * b) // math.gcd(a, b)
    
    
q = []
for x in q_frac:
    value = x * lcm
    value = int(value)
    q.append(value) 

print("q:", q)

n = len(q)

a = ord('A')
actor = []
for i in range(n):
    actor.append(chr(a + i))

table = [[0 for _ in range(n)] for _ in range(n)]
split_table = [[0 for _ in range(n)] for _ in range(n)]

def computeB(i, j):
    qgcd = reduce(math.gcd, q[i:j+1])
    min_buffer = float('inf')

    for k in range(i, j):
        new_buffer = table[i][k] + table[k+1][j] + q[k]*p[k] /qgcd
        #min_buffer = min(min_buffer, new_buffer)
        if(new_buffer<min_buffer):
            min_buffer = new_buffer
            record_k = k
            
    split_table[i][j] = record_k
        
    return min_buffer

for length in range(1, n):     
    for i in range(n - length): 
        j = i + length  
        table[i][j]= computeB(i, j)
        
# for i in range(n):
#         print(table[i])
best = int(table[0][n-1])
        
print(f"Best buffer size: {best}")

def buildSchedule(i, j, div):
    if i == j:
        coeff = q[i] // div
        if coeff == 1:
            return actor[i]
        else:
            return str(coeff) + actor[i]

    k = split_table[i][j]
    current_gcd = reduce(math.gcd, q[i:j+1])
    left = buildSchedule(i, k, current_gcd)
    right = buildSchedule(k + 1, j, current_gcd)

    factor = current_gcd // div
    
    if factor == 1:
        return left + " " + right
    else:
        return str(factor) + "(" + left + " " + right + ")"



print(buildSchedule(0, n-1, 1))
