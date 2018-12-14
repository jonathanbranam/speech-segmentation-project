#!/usr/bin/env python3
# masking.py
# Audio masking functions (NMF, IRM, cIRM)
# By Jamie ISrael
# Indiana University
# ENG-R 511 Fall 2018

""" 
Collection of masking functions to perform Non-negative Matrix Factorization, Ideal Ratio Mask and complex Ideal Ratio Mask.
"""

import numpy as np
from scipy.signal import stft, istft
import librosa
from numpy import random

def NMF(X, max_iter=10000, bv=30):

    """
    Homegrown NMF implementation to calculate basis vectors (W) and activations (H) from frequency spectrum representation.

    Parameters:

    X: STFT of audio signal
    max_iter: maximum number of iterations to allow for convergence of W and H updates
    bv: number of basis vectors with which to represent data

    Returns:

    W: basis vector representation of signal frequency in form (STFT freq bins, bv)
    H: temporal activations correponding to basis vectors (W) in form (bv, STFT time bins)
    """
    
    W = random.rand(X.shape[0],bv)
    H = random.rand(bv,X.shape[1])
  
    for i in range(max_iter):

        Wfrac = np.dot((X/np.dot(W,H)), H.T) / np.dot(np.ones((X.shape[0],X.shape[1])),H.T)
        Wnew = np.multiply(W, Wfrac)
        Wnew = np.where(Wnew==0, 1e-20, Wnew)

        Hfrac = np.dot(Wnew.T, (X/np.dot(Wnew,H))) / np.dot(Wnew.T, np.ones((X.shape[0],X.shape[1])))
        Hnew = np.multiply(H, Hfrac)
        Hnew = np.where(Hnew==0, 1e-20, Hnew)

        if np.all(np.isclose(W,Wnew, .01, .01)):
            break

        W = Wnew
        H = Hnew

    return W, H

def NMFH(X, S1W, S2W, max_iter=1000):

    """
    Homegrown NMF implementation to calculate temporal activations based on previously determined basis vectors.

    Parameters:

    X: STFT of the new (mixed) audio signal
    W: Basis vectors of the original (isolated) source generated with NMF
    max_iter: maximum number of iterations to allow for convergence of H updates

    Returns:

    H: temporal activations correponding to the input basis vectors (W) in form (W.shape[1], STFT time bins)
    """
    
    H = random.rand(W.shape[1],X.shape[1])
    W1W2 = np.concatenate((S1W, S2W), axis=1)
    W1W2 = np.where(W1W2==0, 1e-20, W1W2)
    
    for i in range(max_iter):
        Hfrac = np.dot(W.T, (X/np.dot(W,H))) / np.dot(W.T, np.ones((X.shape[0],X.shape[1])))
        Hnew = np.multiply(H, Hfrac)
        Hnew = np.where(Hnew==0, 1e-20, Hnew)

        if np.all(np.isclose(Hnew, H, .01, .01)):
            break

        H = Hnew

    return H

def NMFtransform(W1W2H, ZX):

    """
    Separate speech using NMF mask from previously generated basis vectors and joint activations.

    Parameters:

    W1W2H: Temporal activations corresponding to concatenation of basis vectors S1W, S2W
    ZX: STFT of the mixed audio signal

    Returns:

    speaker1: recovered signal for speaker 1 in the original audio domain
    speaker2: recovered signal for speaker 2 in the original audio domain
    """
    
    bv1 = S1W.shape[1]
    bv2 = S2W.shape[1]
    M1 = np.dot(S1W,WS1WS2H[:bv1,:]) / np.dot(W1W2, WS1WS2H)
    M2 = np.dot(S2W,WS1WS2H[bv1:bv2,:]) / np.dot(W1W2, WS1WS2H)
    SX1 = np.multiply(M1,ZX)
    SX2 = np.multiply(M2,ZX)
    _, speaker1 = istft(SX1)
    _, speaker2 = istft(SX2)

    return speaker1, speaker2

def IRM(Z, ZX):

    """
    Separate speech using an Ideal Ratio Mask from STFT of original source and STFT of mixed source signal.

    Parameters:

    Z: STFT of the original signal (or speaker sample)
    ZX: STFT of the mixed audio signal

    Returns:

    recovered: separated (recovered) speech in the original audio domain 
    """

    IRM = (Z**2/(Z**2+ZX**2))**.5
    sound = ZX*IRM
    _, recovered = istft(sound)

    return recovered


def cIRM(Z, ZX):

    """
    Separate speech using a complex Ideal Ratio Mask from STFT of original source and STFT of mixed source signal.

    Parameters:

    Z: STFT of the original signal (or speaker sample)
    ZX: STFT of the mixed audio signal

    Returns:

    recovered: separated (recovered) speech in the original audio domain 
    """

    cIRM_r = ((np.real(ZX)*np.real(Z)) + (np.imag(ZX)*np.imag(Z)))/(np.real(ZX)**2 + np.imag(ZX)**2)
    cIRM_i = (np.real(ZX)*np.imag(Z) - np.imag(ZX)*np.real(Z)) / (np.real(ZX)**2 + np.imag(ZX)**2)
    cIRM = cIRM_r+cIRM_i*1j
    sound = ZX*cIRM
    _, recovered = istft(sound)

    return recovered

def SNR(recovered, original):

    """
    Separate speech using a complex Ideal Ratio Mask from STFT of original source and STFT of mixed source signal.

    Parameters:

    recovered: denoised (recovered) signal in original audio domain
    original: mixed (noisy) signal in original audio domain

    Returns:

    ratio: signal-to-noise ratio

    """
    
    dim = len(original)
    num = np.dot(original.T,original)
    den = np.dot((original - recovered[:dim]).T, original - recovered[:dim])
    ratio = 10 * np.log10(num / den)

    return ratio