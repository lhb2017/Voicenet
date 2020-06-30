import pickle
import numpy as np
import os

from voicenet.utils.features_extraction import mfcc_features

MODELS = {'gmm': ['females_gmm_model.gmm', 'males_gmm_model.gmm']}

MODEL_DIR = 'models/'
FEMALE_GMM_MODELFILE = 'females_gmm_model.gmm'
MALE_GMM_MODELFILE = 'males_gmm_model.gmm'

class VoicePipeline():
    
    def __init__(self, model="gmm", trained_models= None):
        
        if model not in MODELS:
            raise ValueError("{0} model is not supported. Please provide model from following list: {1}".format(model, MODELS.keys()))
            
        self.trained_models = MODELS[str(model)]
    
    def identify_gender(self, female_model, male_model, vector):
    
        is_female_score = np.array(female_model.score(vector))
        is_female_log_likelihood = is_female_score.sum()
        
        is_male_score = np.array(male_model.score(vector))
        is_male_log_likelihood = is_male_score.sum()
        
        print("Female Likelihood {0}".format(is_female_log_likelihood))
        print("Male Likelihood {0}".format(is_male_log_likelihood))
            
        
        if is_male_log_likelihood > is_female_log_likelihood:
            winner = "Male" 
        else:
            winner = "Female"
        
        return winner   
    
    def predict(self, audiofile, trained_models=None):
        
        mfccfeatures = mfcc_features()
        
        trained_models = self.trained_models
        print(trained_models)

        # file = 'data/raw/ST-AEDS/TestingData/females/f0001_us_f0001_00005.wav'

        female_model = pickle.load(open(os.path.join(MODEL_DIR, trained_models[0]),'rb'))
        male_model = pickle.load(open(os.path.join(MODEL_DIR, trained_models[1]), 'rb'))

        vector = mfccfeatures.get_features(audiofile)

        winner = self.identify_gender(female_model,male_model,vector)
        print(winner)
        
        return winner
        
 
if __name__ == "__main__":
    
    voicenet = VoicePipeline()  
    
    voicenet.predict('data/raw/ST-AEDS/TestingData/females/f0001_us_f0001_00005.wav')


# def identify_gender(female_model, male_model, vector):
    
#     winner = ''
    
#     is_female_score = np.array(female_model.score(vector))
#     is_female_log_likelihood = is_female_score.sum()
    
#     is_male_score = np.array(male_model.score(vector))
#     is_male_log_likelihood = is_male_score.sum()
    
#     print("Female Likelihood {0}".format(is_female_log_likelihood))
#     print("Male Likelihood {0}".format(is_male_log_likelihood))
        
    
#     if is_male_log_likelihood > is_female_log_likelihood:
#         winner = "Male" 
#     else:
#         winner = "Female"
    
#     return winner

# mfccfeatures = mfcc_features()

# file = 'data/raw/ST-AEDS/TestingData/females/f0001_us_f0001_00005.wav'

# female_model = pickle.load(open(os.path.join(MODEL_DIR, FEMALE_GMM_MODELFILE),'rb'))
# male_model = pickle.load(open(os.path.join(MODEL_DIR, MALE_GMM_MODELFILE), 'rb'))

# vector = mfccfeatures.get_features(file)

# winner = identify_gender(female_model,male_model,vector)
# print(winner)




    
        
    