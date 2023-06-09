import numpy, sys, os

filename = "raw_2023-04-03_04-22-31.csv"

def printhelp():
  print("""Analyze a bcg log in csv format as per the
  Documentation provided, providing Frequency,
  Period and info about the per-message delay.
  Then it saves a new csv which has an integer
  number of 120-240ms couples and a simulated
  per-value timestamp.
  
  {} filename
     will save a file as newfilename in the same folder""".format(sys.argv[0]))

if len(sys.argv) != 2:
  printhelp()
  exit()
 
fpath = sys.argv[1]

if not os.path.isfile(fpath):
  printhelpt()
  exit()

vettone = numpy.genfromtxt(fpath, delimiter=",")
folder, _, filename = fpath.rpartition("/")

print("data imported of shape", vettone.shape)
#calcola delta1
delta1 = vettone[9][0]-vettone[0][0]
print("found delta1", delta1)
t0 = 0
idealstart = True
#delta1 non sarà né esattamente 120ms né esattamente 240ms, quindi si calcola il valore più vicino
if abs(delta1-0.120)<abs(delta1-0.240):
    t0 = vettone[1][0]-0.240
else:
    t0 = vettone[1][0]-0.120
    idealstart = False
print("ideal start, that is to say first delta is 120ms, and t0 = t1-240ms :", idealstart)
#deltan
deltan = vettone[-1][0] - vettone[-10][0]
print("found deltan", deltan)
if abs(deltan-0.120)>abs(deltan-0.240):
    if idealstart:
        new = vettone[:-9]
        print("Removed 9 values to obtain whole couples of messages 120+240")
    else:
        new = vettone
else:
    if idealstart:
        new = vettone
    else:
        new = vettone[:-9]
        print("Removed 9 values to obtain whole couples of messages 120+240")

#controllo gli indici:
if new[-1][0]!=new[-2][0]:
    new = new[:-1]
    print("gli indici erano sbagliati :s")

#calcolo frequenza totale:
last_timestamp = new[-1][0]
total_time = last_timestamp-t0
periodo = total_time / len(new)
print("periodo:",periodo,", frequenza:",1/periodo)

print("\ngenerating a new attribute, a per-sample simulated timestamp assuming a period of", periodo)

newattr = numpy.arange(1, new.shape[0]+1) * periodo + t0
print(newattr.shape, newattr[0],newattr[1], newattr[2], "...", newattr[-3], newattr[-2], newattr[-1])
newnew = numpy.c_[new, newattr]

print("new data shape", newnew.shape)
print("first tuple: from ", new[0], ", to ", newnew[0])
print("second last tuple: from ", new[-2], ", to ", newnew[-2])
print("last tuple: from ", new[-1], ", to ", newnew[-1], end="\n\n")

print("verify precision on last timestamp (they should match in precision and value):\nInitial csv: {:.36}\nfinal csv:   {:.36}".format(new[-1][0], newnew[-1][6]))

print("saving file new"+filename)
numpy.savetxt(folder+"/new"+filename, newnew, delimiter=",")
