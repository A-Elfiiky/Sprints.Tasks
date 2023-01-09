# Function where s= String, p= position, c= character
def mutate_string(s,p,c):
    s = s[:p] + c + s[p + 1:]
    return s
print(mutate_string("abracadabra", 2, "K"))