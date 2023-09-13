import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import librosa
# import sox
import os
import soundfile as sf  # Missing import
# from pydub import AudioSegment
import shutil
from scipy import signal

#frequency gating
def f_high(y,sr):
    b,a = signal.butter(10, 2000/(sr/2), btype='highpass')
    yf = signal.lfilter(b,a,y)
    return yf


def split_audio(filepath):

    curr_dir = os.path.dirname(os.path.realpath(__file__))
    out_dir = r'/split_audio'

    #create wav file from other format
    os.chdir(curr_dir+'/audio_data')
    file_name = os.path.basename(filepath)
    #convert to wav file
    cmd = 'ffmpeg -y -i '+ file_name+' ' + file_name[:-4] + '.wav '
    os.system(cmd)
    os.chdir(curr_dir)

    #update filepath
    filepath = filepath[:-4] + ".wav"

    y, sr = librosa.load(filepath)
    # print("type y 1:                        ",type(y))
    y, _ = librosa.effects.trim(y, top_db=20) #remove silent (<20 dB) parts
    y = f_high(y, sr)
    
    # print("y = ", y) #DEBUG

    # print("type y 2:                        ",type(y), y[0],)
    os.makedirs("."+out_dir, exist_ok=True)
    segment_dur_secs = 1 
    segment_length = sr * segment_dur_secs
    
    

    split = []

    # slice_length=1
    # overlap=0.3
    # slices=np.arange(0,len(y),slice_length-overlap,dtype=np.int)
    overlap = 0.0
    start = 0
    end = segment_length
    num_sections = 0
    while start<len(y):
        # t = y[i * segment_length: (i + 1) * segment_length]
        if(end<len(y)):
            t = y[start: end]
        else:
            t = y[start: ]
        start = int(segment_length*(1-overlap) + start)
        end = int(start+segment_length)
        split.append(t.astype("float64"))
        num_sections+=1

    split_audio_dir = os.path.join(curr_dir, out_dir)
    os.chdir("."+split_audio_dir)

    # print("Number of sections = ", num_sections)

    for i in range(num_sections):
        recording_name = os.path.basename(filepath[:-4])
        out_file = f"{recording_name}_{str(i)}.wav"
        print("Split[", i, "] = ", split[i]) #DEBUG
        sf.write(out_file, split[i], sr)
    os.chdir(curr_dir)
    print("Data split.")




def preprocess_data(filepath) -> list:
    curr_dir = os.getcwd()
    split_audio(filepath)
    out_dir = r'/split_audio'
    file_name = []
    for file in os.listdir("."+out_dir):
        fp=""
        if file.endswith(".wav"):
            fp = os.path.join("."+out_dir, file)

        # audio_file = filepath
        y, sr = librosa.load(fp)
        # y, _ = librosa.effects.trim(y, top_db=20)
        S = librosa.feature.melspectrogram(y=y,
                                    sr=sr,
                                    n_mels=128 * 2,)
        S_db_mel = librosa.amplitude_to_db(S, ref=np.max)

        fig, ax = plt.subplots(figsize=(4, 1.75), frameon=False)
        # Plot the mel spectogram
        img = librosa.display.specshow(S_db_mel,
                                    x_axis='time',
                                    y_axis='log',
                                    ax=ax)
        ax.set_axis_off()
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(current_dir + '/mel_data')
        f_name = str(fp.rsplit('/')[-1]).split('.')[0]+".jpg"
        fig.savefig(f_name, bbox_inches='tight', transparent=True, pad_inches=0)
        plt.close(fig)
        file_name.append(f_name)
        os.chdir(current_dir)
        
    print("Data processed.")
    try:
        shutil.rmtree(os.path.join(curr_dir, 'split_audio'), ignore_errors=True)
        print("Deleted split_audio.")
    except:
        print("Could not delete split_audio.")
    
    return file_name





def model_predict(filepath_list):
    BATCH_SIZE = 32
    IMG_WIDTH, IMG_HEIGHT = 64, 64

    sum = 0

    current_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_dir + '/mel_data')
    model = tf.keras.models.load_model(current_dir + '/cdd_model_2.h5')
    for filepath in filepath_list:
        img = tf.keras.preprocessing.image.load_img(filepath, target_size=(IMG_WIDTH, IMG_HEIGHT))
        x = tf.keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])
        classes = model.predict(images, batch_size=BATCH_SIZE)
        print('predicted class  ',classes)
        # print(classes) #[x, y] where x is the probability of class="Distress", and y is the probability of class="Not Distress"
        if(classes[0][0]>0.5):
            sum+=1
    os.chdir(current_dir)

    return sum