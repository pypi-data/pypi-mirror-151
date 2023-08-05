#!/usr/bin/env python3
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import joblib
import numpy as np
from pkg_resources import resource_filename
import fire


class Regbot:
  reg_model_path = resource_filename(__name__, 'btcgrad_model.h5') 
  model_scaler_path = resource_filename(__name__, 'btcgradcaler.gz') 


  def __init__(self,*args):
  	pass



  @classmethod  
  def loadmodel(cls):
    loaded_model = joblib.load(open(f'{cls.reg_model_path}', 'rb'))
    return loaded_model


  @classmethod  
  def prepareInput(cls,opening,high,low,closing):
    testdata = np.array([[opening,high,low,closing]])
    scaler = joblib.load(f'{cls.model_scaler_path}')
    testdata = scaler.transform(testdata)

    return testdata


  @classmethod
  def buySignalGenerator(cls,opening,high,low,closing):
    scalledInput = cls.prepareInput(opening,high,low,closing)
    return np.round(np.clip(cls.loadmodel().predict(scalledInput), 0, 1) > 0)[0].astype(int)





def signal(opening,high,low,closing):
  try:
    return Regbot.buySignalGenerator(opening,high,low,closing)
  except Exception as e:
    print(e)


if __name__ == '__main__':
  fire.Fire(signal)
