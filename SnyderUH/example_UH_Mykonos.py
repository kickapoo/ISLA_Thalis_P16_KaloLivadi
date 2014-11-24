from hydrograph import SnyderUH

name= "Kalo Livadi"
A = 2.7
L = 2.10
Lc = 1.37
C1 = 1
Ct = 1.9
Cp = 0.65
tR = 0.25

#Make ShyderUH
mykonosUH = SnyderUH(name, A, L, Lc, C1, Ct, Cp, tR)

# Calculate ShyderUh
print mykonosUH.calc()

# View plot
mykonosUH.plot()

for item in [0.25,0.5,1,2,3,4]:
	UH = SnyderUH(name, A, L, Lc, C1, Ct, Cp, item)
	UH.calc()
	UH.plot()
	print "tR: {} hr, Q: {}, Tb:{} hr".format(UH.tR, UH.QPR, UH.Tb)

