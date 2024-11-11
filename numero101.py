import time

base = int(input("escreva o numero base"))


print("HENRIQUE")
inicioH = time.time()
henrique = 0
num101 = 1

restos = dict()

for i in range(base + 1):
    r = num101%base
    if r in restos:
        henrique = num101 - restos[r]
        break
    restos[r] = num101
    num101 = 10*num101 + 1
fim = time.time() - inicioH

# print("henrique levou: ", fim, "achou : ",henrique)
print("henrique levou: ", fim)


print("RODRIGO")
timeR = time.time()
# num101 = "1"
num101 = 1
# intnum101 = int(num101)

while(num101 < base):
    # num101 += "1"
    # intnum101 = int(num101)
    num101 = 10*num101 + 1

resto01 = num101%base

num102 = 10*num101 + 1
resto02 = num102%base

while(resto02!=resto01):
    num102 = num102*10 + 1
    resto02 = num102%base

numFinal = num102 - num101
fimR = time.time() - timeR
multiplo = numFinal//base
# print("rodrigo levou:",fimR,"achou = ",numFinal," = ",base," * ", multiplo)
print("rodrigo levou:",fimR)

print("R/H = ",100*fimR/fim,"%")
