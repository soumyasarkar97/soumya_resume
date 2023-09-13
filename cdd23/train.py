# from scikits.audiolab import wavread
from pylab import *
import os
import librosa
from scipy import signal
import time
import shutil
import splitfolders


def f_high(y,sr):
    b,a = signal.butter(10, 2000/(sr/2), btype='highpass')
    yf = signal.lfilter(b,a,y)
    return yf

def clear():
    #empty Mel_Dataset/Distress folder from previous query runs
    shutil.rmtree(os.path.dirname(os.path.realpath(__file__)) + '/Mel_Dataset/Distress')
    os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/Mel_Dataset/Distress')
    #empty Mel_Dataset/Egg folder from previous query runs
    shutil.rmtree(os.path.dirname(os.path.realpath(__file__)) + '/Mel_Dataset/Egg')
    os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/Mel_Dataset/Egg')
    #empty Mel_Dataset/Feed folder from previous query runs
    shutil.rmtree(os.path.dirname(os.path.realpath(__file__)) + '/Mel_Dataset/Feed')
    os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/Mel_Dataset/Feed')

def run_method():
    start = time.time()
    current_dir = os.path.dirname(os.path.realpath(__file__))

    #Distress Data
    os.chdir(current_dir + '/Dataset/Distress')
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        # print("File ", f)
        y, sr = librosa.load(f)

        #preprocessing
        y, _ = librosa.effects.trim(y, top_db=20)
        y = f_high(y, sr)

        S = librosa.feature.melspectrogram(y=y,
                                        sr=sr,
                                        n_mels=128 * 2,)
        # print(" y = ", y) #DEBUG
        # print(" sr = ", sr) #DEBUG
        S_db_mel = librosa.amplitude_to_db(S, ref=np.max)
        fig, ax = plt.subplots(figsize=(4, 1.75), frameon=False)
        # Plot the mel spectogram
        img = librosa.display.specshow(S_db_mel,
                                    x_axis='time',
                                    y_axis='log',
                                    ax=ax)
        ax.set_axis_off()
        os.chdir(current_dir + '/Mel_Dataset/Distress')
        f_name = str(f.rsplit('/')[-1]).split('.')[0]+".jpg"
        # print(" f_name = ", f_name) #DEBUG
        fig.savefig(f_name, bbox_inches='tight', transparent=True, pad_inches=0)
        plt.close(fig)
        os.chdir(current_dir + '/Dataset/Distress')
    os.chdir(current_dir)


    #Egg Data
    os.chdir(current_dir + '/Dataset/Egg')
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        # print("File ", f)
        y, sr = librosa.load(f)
        S = librosa.feature.melspectrogram(y=y,
                                        sr=sr,
                                        n_mels=128 * 2,)
        # print(" y = ", y) #DEBUG
        # print(" sr = ", sr) #DEBUG
        S_db_mel = librosa.amplitude_to_db(S, ref=np.max)
        fig, ax = plt.subplots(figsize=(4, 1.75), frameon=False)
        # Plot the mel spectogram
        img = librosa.display.specshow(S_db_mel,
                                    x_axis='time',
                                    y_axis='log',
                                    ax=ax)
        ax.set_axis_off()
        os.chdir(current_dir + '/Mel_Dataset/Egg')
        f_name = str(f.rsplit('/')[-1]).split('.')[0]+".jpg"
        # print(" f_name = ", f_name) #DEBUG
        fig.savefig(f_name, bbox_inches='tight', transparent=True, pad_inches=0)
        plt.close(fig)
        os.chdir(current_dir + '/Dataset/Egg')
    os.chdir(current_dir)


    #Feed Data
    os.chdir(current_dir + '/Dataset/Feed')
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        # print("File ", f)
        y, sr = librosa.load(f)
        S = librosa.feature.melspectrogram(y=y,
                                        sr=sr,
                                        n_mels=128 * 2,)
        # print(" y = ", y) #DEBUG
        # print(" sr = ", sr) #DEBUG
        S_db_mel = librosa.amplitude_to_db(S, ref=np.max)
        fig, ax = plt.subplots(figsize=(4, 1.75), frameon=False)
        # Plot the mel spectogram
        img = librosa.display.specshow(S_db_mel,
                                    x_axis='time',
                                    y_axis='log',
                                    ax=ax)
        ax.set_axis_off()
        os.chdir(current_dir + '/Mel_Dataset/Feed')
        f_name = str(f.rsplit('/')[-1]).split('.')[0]+".jpg"
        # print(" f_name = ", f_name) #DEBUG
        fig.savefig(f_name, bbox_inches='tight', transparent=True, pad_inches=0)
        plt.close(fig)
        os.chdir(current_dir + '/Dataset/Feed')
    os.chdir(current_dir)


    end = time.time()
    print("Execution time = ", (end-start), " seconds")


def split_directories(train, valid, test):
    current_dir = os.path.dirname(os.path.realpath(__file__))

    #clear folders
    os.chdir(current_dir)
    try:
        #empty Mel_Dataset/split_Distress folder from previous query runs
        shutil.rmtree(os.path.dirname(os.path.realpath(__file__)) + '/split_mel_test_train')
    except:
        print("split_mel_test_train folder doesn't exist")
    # os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/Mel_Dataset/split_Distress')
    # try:
    #     #empty Mel_Dataset/split_Egg folder from previous query runs
    #     shutil.rmtree(os.path.dirname(os.path.realpath(__file__)) + '/Mel_Dataset/split_Egg')
    # except:
    #     print("split_Egg folder doesn't exist")
    # os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/Mel_Dataset/split_Egg')
    # try:
    #     #empty Mel_Dataset/split_Feed folder from previous query runs
    #     shutil.rmtree(os.path.dirname(os.path.realpath(__file__)) + '/Mel_Dataset/split_Feed')
    # except:
    #     print("split_Feed folder doesn't exist")
    # os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/Mel_Dataset/split_Feed')


    #split
    os.chdir(current_dir)
    splitfolders.ratio('Mel_Dataset', output="split_mel_test_train", seed=1337, ratio=(train, valid, test))
    # splitfolders.ratio('Egg', output="split_Egg", seed=1337, ratio=(train, valid, test))
    # splitfolders.ratio('Feed', output="split_Feed", seed=1337, ratio=(train, valid, test))
    


# clear()
# run_method()
split_directories(0.8, 0.1, 0.1)