import numpy as np 
from scipy.signal import butter, sosfilt, welch
from scipy.integrate import simps
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pickle
from draw_art import draw

def extract_features(sample):
    """ 
    Extracts the following features from a sample into an array:
        mean voltage
        std of voltage
        mean % attention
        mean % meditation
        relative delta power
        relative theta power
        relative alpha power
        relative beta power
        
    parameter
    ---------
        sample: must be 3 x 1280 array where axis 0 is eeg, attention, meditation
    returns
    --------
        features: length 8 list containing 8 features
    """
    
    features = np.zeros(8)
    
    # mean/std of voltage
    features[0] = np.mean(sample[0])
    features[1] = np.std(sample[0])

    # mean attention/meditation as percentages
    features[2] = np.mean(sample[1]) / 100
    features[3] = np.mean(sample[2]) / 100
    
    # relative powers for each band
    delta = [1,4]
    theta = [4,8]
    alpha = [8,12]
    beta = [12,30]

    fs = 128

    freqs, psd = welch(sample[0], fs=fs)
    freq_res = freqs[1] - freqs[0]
    total_power = simps(psd, dx=freq_res)

    for i,band in enumerate([delta,theta,alpha,beta], start=4):
        band_idx = np.logical_and(freqs >= band[0], freqs < band[1])
        b_power = simps(psd[band_idx], dx=freq_res)

        features[i] = b_power / total_power

    return features


#################################################
# MAIN METHOD TO GET ALL FEATURES & PREDICTION ##
#################################################
def model_pipeline(raw_eeg, attention, meditation):
    """
    Pipeline for lda model including filtering, feature extraction, and prediction of labels, then creates the artwork

    parameters
    ----------
    eeg: 120 seconds of eeg data
    attention: 120 seconds of attention data
    meditation: 120 seconds of meditation data
    
    returns
    --------
    predictions: length 12 array of predicted emotions
    """

    ###### butterworth band pass filter #####
    # define filter parameters
    fs = 128 # sampling rate
    hp = 0.1 # high pass
    lp = 30 # low pass
    order = 3

    # filter
    sos = butter(order, [hp, lp], analog = False, btype = 'band', output = 'sos', fs = fs)
    eeg = sosfilt(sos, raw_eeg)

    ##### feature extraction #####
    nper_chunk = fs * 10 # 10 second chunks
    sample = np.array([[eeg], [attention], [meditation]]).reshape(3, 12, nper_chunk)

    # for each 10s chunk, get features
    model_input = []
    for i in range(12):
        model_input.append(extract_features(sample[:,i,:]))
    model_input = np.array(model_input)

    ##### run sample through LDA model #####
    LDA_model = pickle.load(open('lda_model.pkl', 'rb'))
    
    # get predictions
    emotion_preds = LDA_model.predict(model_input)

    # draw the artwork
    draw(600, 600, emotion_preds)

    return emotion_preds