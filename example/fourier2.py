import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack
import pandas as pd 
import math

def make_signal(freqs, amps, phase, begin=0, end=2, framerate=100):
    t = np.linspace(begin, end, (end - begin) * framerate, endpoint=False)
    y = np.zeros(len(t))
    
    max_freq = np.max(amps)
    for i in range(len(freqs)):
        
        #plot everything
        if(freqs[i] < 0): continue
        
    
        # Isolate gemoetry
        #if (freqs[i] == max_freq): continue
    
        # Isolate textures
        # if (freqs[i] != max_freq): continue
    
        sig = amps[i] * np.cos(freqs[i] * 2 * np.pi * t + phase[i])
        plt.plot(t, sig, 'r--', alpha=0.9 if amps[i] == max_freq else 0.1)
        #plt.plot(t, sig, alpha=0.2)
        if amps[i] == max_freq: print("The frequency of the characteristic wave is %f Hz and the corresponding amplitude is %f. The wavelength is %f mm" %(freqs[i], amps[i], cycles_per_unit_to_wavelength(freqs[i])))
        
        y += sig
            
    return t, y

def make_specific_signal(freqs, amps, phase, begin=0, end=2, framerate=100):
    
    t = np.linspace(begin, end, (end - begin) * framerate, endpoint=False)
    z = np.zeros(len(t))
    
    for i in range(len(freqs)):
        
        if(freqs[i] < 0): continue
        sig = amps[i] * np.cos(freqs[i] * 2 * np.pi * t + phase[i])

        # Isolate range of desired frequencies
        if(freqs[i] > 0.06):
            z += sig
            
    return t, z

def cycles_per_unit_to_wavelength(freq):
    
    degrees_per_unit = 0.088
    units_per_degree = 1/degrees_per_unit
    
    cycles_per_degree = freq * units_per_degree
    degrees_per_cycle = 1/cycles_per_degree
    
    arm_length = 291.5 # in mm

    wavelength = math.sin(math.radians(degrees_per_cycle)) * arm_length
    return wavelength


    
def run_fourier():    
    # make signal
    f_s = 50
    df = pd.read_csv('scan.csv').dropna()
    for i in range(len(df)): df.loc[i, 'c1'] = df.loc[df['p1'] == df.loc[i, 'p1'], 'c1'].mean()
    df = df.drop_duplicates(subset=['p1'])
    df = df.sort_values('p1')
    
    # Start at 0 on x-axis
    df.loc[:, 'p1'] = df.loc[:, 'p1'] - df.loc[:, 'p1'].min(0)
    
    old_p_values = list(df['p1'])
    begin, end = float(df.loc[:, 'p1'].min(0)), float(df.loc[:, 'p1'].max(0))
    new_df = pd.DataFrame(columns=['p1', 'c1'])
    for i in range(len(old_p_values)-1):
        p_b, p_e = old_p_values[i], old_p_values[i+1]
        c_b, c_e = df.loc[df['p1'] == p_b, 'c1'], df.loc[df['p1'] == p_e, 'c1']
        p_values = np.linspace(p_b, p_e, int(f_s * (p_e - p_b)))
        c_values = np.linspace(c_b, c_e, len(p_values))
        for j in range(len(p_values)):
            new_df = new_df.append(other={'p1': p_values[j], 'c1': c_values[j]}, ignore_index=True)
        # if(len(df.loc[df['p1'] == i]) == 0):
        #     df = df.append(other={'p1': i, 'c1': float(df.loc[df['p1'] == i-1, 'c1'])}, ignore_index=True)
    new_df = new_df.drop_duplicates(subset=['p1'])
    new_df = new_df.sort_values('p1')
    new_df = new_df.reindex()
    new_df.loc[:, 'c1'] = new_df.loc[:, 'c1'] - new_df.loc[:, 'c1'].mean()
    
    plt.plot(df['p1'], df['c1'], 'c--', label='original', alpha = 0.5)
    plt.plot(new_df['p1'], new_df['c1'], 'g--', label='processed', alpha =0.5)
    plt.ylabel("Torque 1 (mA)")
    plt.xlabel("Horizontal Position")
    # plt.show()
    # t, x = make_signal([10, 13], [1, 2], framerate=f_s)

    # ax.plot(t, x)
    # ax.set_xlabel('Time [s]')
    # ax.set_ylabel('Signal amplitude')
    
    # Store the freqs and amps in a new file
    
    
    # transform signal
    X = 2 * (fftpack.fft(new_df['c1'])) / f_s / (end - begin)
    phi = np.arctan2(np.imag(X), np.real(X))
    # X = np.real(X) * np.abs(X) / np.abs(np.real(X))
    X = np.abs(X)
    freqs = fftpack.fftfreq(len(new_df['c1'])) * f_s
    # remake signal
    pt, px = make_signal(freqs, X, phi, begin=begin, end=end, framerate=f_s/2)
    #plt.plot(pt, px, 'r-', label='reconstructed')
    
    # plt.set_xlabel('Time [s]')
    # plt.set_ylabel('Signal amplitude')
    
    ptt, pxx = make_specific_signal(freqs, X, phi, begin=begin, end=end, framerate=f_s/2)
    plt.plot(ptt, pxx, 'b-', label='texture')
    plt.legend()
    
    
    # plot fourier
    fig, ax = plt.subplots()
    ax.stem(freqs, X)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Amplitude ')
    ax.set_xlim(left=0)
    # ax.set_ylim(-5, 110)
    plt.show()
    
    #fname = "fourier_new.csv"
    #fout = open(fname, "w")
    #print("freq, amp", file = fout)
    #fout.close()
    
    combined = np.vstack((freqs, X)).T
    #print(combined)
    np.savetxt('fourier.csv', combined, delimiter=',', fmt=['%f' , '%f'], header='Freq,Amp')
    
if __name__=='__main__':
    run_fourier()