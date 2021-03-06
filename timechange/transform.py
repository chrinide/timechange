"""Copyright 2017
Steven Sheffey <stevensheffey4@gmail.com>,
John Ford,
Eyasu Asrat,
Jordan Flowers,
Joseph Volmer,
Luke Stanley,
Serenah Smith, and
Chandu Budati

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import numpy as np
from scipy import signal

def extract(time_series, method="fft", chunk_size=None):
    """Extracts features from a time series or array of time series and outputs an image
    Keyword arguments:
    time_series -- A numpy array or array of numpy arrays representing the time series data
    method -- the type of feature extraction to use
    chunk_size -- Used for some feature extraction methods. Pads or truncates data
    """
    #Switches on method
    if method == "fft":
        return simple_fourier(time_series, chunk_size=chunk_size)
    elif method == "spectrogram":
        return spectrogram(time_series)
    else:
        raise ValueError("Invalid feature extraction method")

#Possible enhancements
#TODO: separate real and imaginary components so as not to lose data
#TODO: split time series into chunks
#TODO: ignoring values with little information
#TODO: version with axes
def simple_fourier(time_series, chunk_size = None):
    """Performs a basic fourier transform across the entire time series. The imaginary results are normalized.
    Keyword arguments:
    time_series -- The time series analyse as a 2d numpy array
    chunk_size -- The size value to be passed to numpy's FFT. Values higher than the data size will pad zeroes.
                 Values lower than the data size will remove elements.
                 With FFT, it is recommended to use powers of 2 here
    """
    #If default value is left for data size, use a placeholder
    #TODO: something better with this
    if chunk_size is None:
        chunk_size = 64
    # Pad the data to chunk size
    pad_length = chunk_size - (time_series.shape[1] % chunk_size)
    time_series = np.pad(time_series, ((0, 0), (0, pad_length)), 'constant', constant_values=0)
    # Reshape the data to chunks of suitable size
    time_series = time_series.reshape(int(np.product(time_series.shape) / chunk_size), chunk_size)
    # Perform FFT on the resulting data
    # Store in the time_series variable since that data is no longer needed
    time_series = np.fft.rfft(time_series)
    # Normalize the real and complex features
    #Extract real features
    real_features = time_series.real
    #Normalize against minimum value per row to avoid negative values
    #TODO: consider normalizing across the array to make standout values stand out more
    #TODO: better notation for this.
    real_features = (real_features.T - np.amin(real_features, axis=1).T).T
    #Normalize against maximum value per row to get all values between 0 and 1
    #Extract max values and replace 0s to avoid divide by 0 issue
    max_values = np.amax(real_features, axis=1)
    np.place(max_values, max_values == 0, 1)
    #TODO: consider normalizing across the array to make standout values stand out more
    #TODO: consider normalizing using L2 Norm
    #TODO: better notation for this.
    real_features = (real_features.T / max_values.T).T
    #Do the same thing for complex values
    complex_features = time_series.imag
    #Normalize against minimum value per row to avoid negative values
    #TODO: consider normalizing across the array to make standout values stand out more
    #TODO: better notation for this.
    complex_features = (complex_features.T - np.amin(complex_features, axis=1).T).T
    #Normalize against maximum value per row to get all values between 0 and 1
    #Extract max values and replace 0s to avoid divide by 0 issue
    max_values = np.amax(complex_features, axis=1)
    np.place(max_values, max_values == 0, 1)
    #TODO: consider normalizing across the array to make standout values stand out more
    #TODO: consider normalizing using L2 Norm
    #TODO: better notation for this.
    complex_features = (complex_features.T / max_values.T).T
    #Combine the real and complex features into an array
    #TODO: configure whether shuffled or stacked
    #return np.concatenate((real_features, complex_features), axis=1) #shuffled
    #Combine in color channels
    #Shape of this array is 3, W, H
    return np.stack((real_features, complex_features, np.zeros(real_features.shape)), axis=2)


def spectrogram(time_series):
    """Performs a basic fourier transform across the entire time series. The imaginary results are normalized.
    Keyword arguments:
    time_series -- The time series analyse as a numpy array. Can also be a 2d array.
                   In the case of a 2d array, the operation is performed on each subarray and returned
                   as an array of results.
    """
    #TODO: Implement scipy's spectrogram
    #Look here https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
    #Replace this with actual output
    return time_series
