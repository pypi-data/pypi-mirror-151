from tensorflow import keras
import glob
from grmrcnn import grmrcnn
model = keras.models.load_model("ResNet50.h5")
path = glob.glob("C:/Users/jjeng/Desktop/Maar maam/grmrcnn/Images/*.jpg")
fa=grmrcnn(model,path)
