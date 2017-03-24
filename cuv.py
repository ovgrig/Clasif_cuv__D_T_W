import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import math

from scipy import signal
from mpl_toolkits.mplot3d.axes3d import Axes3D


spf = wave.open('A_01.wav','r')
#spf = wave.open('Antrenare/v016c29375.wav','r')

#Extract Raw Audio from Wav File
sg = spf.readframes(-1)
sg = np.fromstring(sg, 'Int16')


#If Stereo
if spf.getnchannels() == 2:
    print 'Just mono files'
    sys.exit(0)

plt.figure(1)
plt.title('Signal Wave...')
plt.plot(sg)
#plt.show()


fs= spf.getframerate();
print 'Frecv esant=',fs

winL=math.trunc(0.020*fs); # 20 ms = nr esantioane fereastra analiza
overL=math.trunc(0.010*fs); #10 ms overlap = nr esantioane deplasare fereastra
nFFT=4096;
 
dim=sg.size;

nFrames=(dim-winL)/overL
print 'Nr frames= ',nFrames

if winL%overL == 0 :
	nFrames+=1

if nFFT<winL :
	nFFT = winL

Frames=np.zeros(shape=(nFrames, nFFT),dtype=np.int16)
#specFr=np.zeros(shape=(nFrames, nFFT),dtype=np.int16)


wind = np.hamming(winL)

for i in range(nFrames): 
	ii=i*overL
	Frames[i,0:winL]=sg[ii:winL+ii]*wind
specFr = np.fft.fft(Frames)
modSpec= abs(specFr)
cepstrum = np.fft.ifft(np.log(abs(specFr)))
mCepstrum=abs(cepstrum)

#print specFr.shape, modSpec.shape
#print specFr
#print modSpec

mn=min(sg)
mx=max(sg)

plt.figure(2)
#ff=(Frames-mn)*255/(mx-mn)
#plt.pcolormesh(ff.T)
plt.title('Modul Spectru')
plt.pcolormesh(np.log(modSpec.T))

plt.figure(4)
plt.title('Modul Cepstru')
plt.pcolormesh(mCepstrum.T,cmap='RdBu', vmin=0, vmax=0.5)

frameN=6

plt.figure(3)
plt.title('Cepstrum')
plt.hold(True)
for i in range(nFrames): 
	plt.plot(abs(cepstrum[i,:])*10+0.9*i)
#plt.plot(abs(cepstrum[frameN,:]))
#plt.plot(cepstrum[40,:].real)
#plt.plot(np.real(cepstum[40,:]))

#fig = plt.figure()
#ax = Axes3D(fig)
#dx, dy = mCepstrum.shape
#x=range(dy)
#y=range(dx)
#xs, ys = np.meshgrid(x, y)
#ax.plot_surface(xs, ys, mCepstrum, rstride=1, cstride=1, cmap='hot')

plt.figure(5)
plt.title('Frame #')
plt.plot(Frames[frameN,:])

plt.figure(6)
plt.title('Modul Spectru')
plt.hold(True)
for i in range(nFrames): 
	plt.plot(modSpec[i,:]/2000+10*i)

plt.figure(7)
plt.title('Sectru + Spectru netezit pt Frame#')
plt.hold(True)
plt.plot(modSpec[frameN,:])
cc=cepstrum[frameN,:]
dimC=60;

cc[dimC:-dimC]=0

smoothSp=np.fft.fft(cc)
plt.plot(np.exp(abs(smoothSp)),'r')

plt.show()
