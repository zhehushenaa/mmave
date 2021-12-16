a={"0":"1","2":"4"}
b={"0":"4"}
tempdict={1:(2,3,4,5,6,7),2:(3,2,5,6,7,0)}
tempdict1={1:(2,3,4,5,6,7)}
tt=[{0: (0.43, 0.34, 0.145, 0.0, 0.0, 0)}, {0: (0.43, 0.34, 0.145, 0.0, 0.0, 0)}, {0: (0.43, 0.34, 0.145, 0.0, 0.0, 0)}, {0: (0.43, 0.34, 0.145, 0.0, 0.0, 0)}, {0: (0.43, 0.34, 0.145, 0.0, 0.0, 0)}, None, None, None, None, None, None, None, None, None, None]
c=[]
# c.append(a)
# c.append(b)
c.append(tempdict)
c.append(tempdict1)
# print(c)
num=0
for i in tt:

    # print (i)
    if i!=None:
        num=num+1
        print(len(i))
        if len(i)<2:
            for j,v in i.items():
                print(j,v)
                print(v[2])

print(len(tt))
print(num)