import pandas as pd
import math

df = pd.read_csv('data.csv')

#print(df.head())
#print(df.info())
#print( df[ (df['Outlook'] == 'Rainy') ] )
print( df[ (df['Outlook'] == 'Rainy') & (df['Play'] == 'Yes') ] )
print(df.iloc[0,0])

# S: Himpunan Kasus
# N: Jumlah Partisi Dalam S
# Pi: Proporsi Dari Si Terhadap S
def entropy(s, n):
    total = 0
    for pi in s:
        total += 0 if pi == 0 else (-pi/n * math.log(pi/n, 2))
    return total

# S: Entropy Dari Himpunan Kasus
# A: Atribut
# N: Jumlah Partisi Atribut A
# |Si|: Jumlah Kasus Pada Partisi Ke-i
# |S| / _s: Jumlah Kasus Dalam S
# Entropy(Si) = Entropy Dari Kasus Pada Partisi Ke-i
# gain([4, 10], [[0, 4],[1, 4],[3, 2]], [4, 5, 5], 14)
def gain(s, a, n, _s):
    # 0.863120569 - ((4/14 * 0) + (5/14 * 0.72193) + (5/14 * 0.97095)
    total = 0
    for si in range(len(n)):
        total += (n[si]/_s * entropy(a[si], n[si]))
    total = entropy(s, _s) - total
    return total

# S: Himpunan Kasus
# A: Atribut
# Si: Jumlah Sampel Untuk Atribut A    
def split_info(s, a):
    total = 0
    for si in a:
        total += 0 if si == 0 else (-si/s * math.log(si/s, 2))
    return total
    
# S: Himpunan Kasus
# A: Atribut
# Gain(S,A): Information Gain Pada Atribut A
# SplitInfo(S,A): Split Information Pada Atribut A
def gain_ratio(s, a, n, _s):
    return gain(s, a, n, _s) / split_info(_s, n)

print("\nEntropy Total = {}".format(entropy([4, 10], 14))) # Entropy Total
print("Entropy Atribut Outlook (Cloudy) = {}".format(entropy([0, 4], 4))) # Entropy Atribut Outlook (Cloudy)
print("Entropy Atribut Outlook (Rainy) = {}".format(entropy([1, 4], 5))) # Entropy Atribut Outlook (Rainy)
print("Entropy Atribut Outlook (Sunny) = {}".format(entropy([3, 2], 5))) # Entropy Atribut Outlook (Sunny)
print("Gain Atribut Outlook = {}".format(gain([4, 10], [[0, 4],[1, 4],[3, 2]], [4, 5, 5], 14))) # Gain Atribut Outlook
print("Split Information Outlook = {}".format(split_info(14, [4, 5, 5]))) # Split Information Outlook
print("Gain Ratio Outlook = {}".format(gain_ratio([4, 10], [[0, 4],[1, 4],[3, 2]], [4, 5, 5], 14))) # Gain Ratio Outlook

print("\nHasil Perhitungan Humidity")
print("Entropy")
print("<=65 {}".format(entropy([0, 1], 1))) # Entropy Atribut Humidity <= 65
print(">65 {}".format(entropy([4, 9], 13))) # Entropy Atribut Humidity > 65
print("<=70 {}".format(entropy([0, 4], 4))) # Entropy Atribut Humidity <= 70
print(">70 {}".format(entropy([4, 6], 10))) # Entropy Atribut Humidity > 70
print("<=75 {}".format(entropy([0, 5], 5))) # Entropy Atribut Humidity <= 75
print(">75 {}".format(entropy([4, 5], 9))) # Entropy Atribut Humidity > 75
print("<=78 {}".format(entropy([0, 6], 6))) # Entropy Atribut Humidity <= 78
print(">78 {}".format(entropy([4, 4], 8))) # Entropy Atribut Humidity > 78
print("<=80 {}".format(entropy([1, 8], 9))) # Entropy Atribut Humidity <= 80
print(">80 {}".format(entropy([3, 2], 5))) # Entropy Atribut Humidity > 80
print("<=85 {}".format(entropy([2, 8], 10))) # Entropy Atribut Humidity <= 85
print(">85 {}".format(entropy([2, 2], 4))) # Entropy Atribut Humidity > 85
print("<=90 {}".format(entropy([3, 9], 12))) # Entropy Atribut Humidity <= 90
print(">90 {}".format(entropy([1, 1], 2))) # Entropy Atribut Humidity > 90
print("<=95 {}".format(entropy([4, 9], 13))) # Entropy Atribut Humidity <= 95
print(">95 {}".format(entropy([0, 1], 1))) # Entropy Atribut Humidity > 95

print("Gain")
print("<>65 = {}".format(gain([4, 10], [[0, 1],[4, 9]], [1, 13], 14))) # Gain Atribut Humidity <> 65
print("<>70 = {}".format(gain([4, 10], [[0, 4],[4, 6]], [4, 10], 14))) # Gain Atribut Humidity <> 70
print("<>75 = {}".format(gain([4, 10], [[0, 5],[4, 5]], [5, 9], 14))) # Gain Atribut Humidity <> 75
print("<>78 = {}".format(gain([4, 10], [[0, 6],[4, 4]], [6, 8], 14))) # Gain Atribut Humidity <> 78
print("<>80 = {}".format(gain([4, 10], [[1, 8],[3, 2]], [9, 5], 14))) # Gain Atribut Humidity <> 80
print("<>85 = {}".format(gain([4, 10], [[2, 8],[2, 2]], [10, 4], 14))) # Gain Atribut Humidity <> 85
print("<>90 = {}".format(gain([4, 10], [[3, 9],[1, 1]], [12, 2], 14))) # Gain Atribut Humidity <> 90
print("<>95 = {}".format(gain([4, 10], [[4, 9],[0, 1]], [13, 1], 14))) # Gain Atribut Humidity <> 95

print("Split Info")
print("Split Info Humidity <>65 = {}".format(split_info(14, [1, 13]))) # Split Info Humidity <>65
print("Split Info Humidity <>70 = {}".format(split_info(14, [4, 10]))) # Split Info Humidity <>70
print("Split Info Humidity <>75 = {}".format(split_info(14, [5, 9]))) # Split Info Humidity <>75
print("Split Info Humidity <>78 = {}".format(split_info(14, [6, 8]))) # Split Info Humidity <>78
print("Split Info Humidity <>80 = {}".format(split_info(14, [9, 5]))) # Split Info Humidity <>80
print("Split Info Humidity <>85 = {}".format(split_info(14, [10, 4]))) # Split Info Humidity <>85
print("Split Info Humidity <>90 = {}".format(split_info(14, [12, 2]))) # Split Info Humidity <>90
print("Split Info Humidity <>95 = {}".format(split_info(14, [13, 1]))) # Split Info Humidity <>95

print("Gain Ratio")
print("Gain Ratio Humidity <>65 = {}".format(gain_ratio([4, 10], [[0, 1],[4, 9]], [1, 13], 14))) # Gain Ratio Humidity <>65
print("Gain Ratio Humidity <>70 = {}".format(gain_ratio([4, 10], [[0, 4],[4, 6]], [4, 10], 14))) # Gain Ratio Humidity <> 70
print("Gain Ratio Humidity <>75 = {}".format(gain_ratio([4, 10], [[0, 5],[4, 5]], [5, 9], 14))) # Gain Ratio Humidity <> 75
print("Gain Ratio Humidity <>78 = {}".format(gain_ratio([4, 10], [[0, 6],[4, 4]], [6, 8], 14))) # Gain Ratio Humidity <> 78
print("Gain Ratio Humidity <>80 = {}".format(gain_ratio([4, 10], [[1, 8],[3, 2]], [9, 5], 14))) # Gain Ratio Humidity <> 80
print("Gain Ratio Humidity <>85 = {}".format(gain_ratio([4, 10], [[2, 8],[2, 2]], [10, 4], 14))) # Gain Ratio Humidity <> 85
print("Gain Ratio Humidity <>90 = {}".format(gain_ratio([4, 10], [[3, 9],[1, 1]], [12, 2], 14))) # Gain Ratio Humidity <> 90
print("Gain Ratio Humidity <>95 = {}".format(gain_ratio([4, 10], [[4, 9],[0, 1]], [13, 1], 14))) # Gain Ratio Humidity <> 95