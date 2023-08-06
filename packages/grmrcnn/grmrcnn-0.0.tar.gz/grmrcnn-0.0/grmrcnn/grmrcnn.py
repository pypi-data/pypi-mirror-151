from mrcnn.visualize import display_instances
from keras.applications.resnet import ResNet50, preprocess_input, decode_predictions
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from scipy.ndimage.interpolation import zoom
import keras
from tensorflow import keras
from keras import backend as K
import tensorflow as tf
import numpy as np
import matplotlib.cm as cm
tf.compat.v1.disable_eager_execution()

def grad_plus(input_model, img, layer_name,H=224,W=224):
    model=input_model
    img1=img
    cls = np.argmax(input_model.predict(img))
    y_c = input_model.output[0, cls]
    conv_output = input_model.get_layer(layer_name).output
    grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(layer_name).output, model.output])
    #with tf.GradientTape() as tape:
    tape=tf.GradientTape()
    last_conv_layer_output, preds = grad_model(img)
    pred_index = tf.argmax(preds[0])
    class_channel = preds[:, pred_index]
    grads=K.gradients(class_channel, last_conv_layer_output)[0]
    first = K.exp(y_c)*grads
    second = K.exp(y_c)*grads*grads
    third = K.exp(y_c)*grads *grads*grads
    gradient_function = K.function([input_model.input], [y_c,first,second,third, conv_output, grads])
    y_c, conv_first_grad, conv_second_grad,conv_third_grad, conv_output, grads_val = gradient_function([img])
    global_sum = np.sum(conv_output[0].reshape((-1,conv_first_grad[0].shape[2])), axis=0)
    alpha_num = conv_second_grad[0]
    alpha_denom = conv_second_grad[0]*2.0 + conv_third_grad[0]*global_sum.reshape((1,1,conv_first_grad[0].shape[2]))
    alpha_denom = np.where(alpha_denom != 0.0, alpha_denom, np.ones(alpha_denom.shape))
    alphas = alpha_num/alpha_denom
    weights = np.maximum(conv_first_grad[0], 0.0)
    alpha_normalization_constant = np.sum(np.sum(alphas, axis=0),axis=0)
    alphas /= alpha_normalization_constant.reshape((1,1,conv_first_grad[0].shape[2]))
    deep_linearization_weights = np.sum((weights*alphas).reshape((-1,conv_first_grad[0].shape[2])),axis=0)
    #print deep_linearization_weights
    grad_CAM_map = np.sum(deep_linearization_weights*conv_output[0], axis=2)
    # Passing through ReLU
    cam = np.maximum(grad_CAM_map, 0)
    cam = zoom(cam,H/cam.shape[0])
    cam = cam / np.max(cam) # scale 0 to 1.0
    heatmap=cam
    numer = heatmap - np.min(heatmap)
    denom = (heatmap.max() - heatmap.min()) + 0.1
    heatmap = numer / denom
    heatmap = np.uint8(255 * heatmap)
    # Use jet colormap to colorize heatmap
    jet = cm.get_cmap("jet")
    # Use RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]
    # Create an image with RGB colorized heatmap
    jet_heatmap = keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap = keras.preprocessing.image.img_to_array(jet_heatmap)
    return cam,jet_heatmap


def grmrcnn(model,path):
 plt.rcParams['figure.figsize'] = 8,8
 plt.show(block=True)
 self=model
 def find_target_layer(self):
		# attempt to find the final convolutional layer in the network
		# by looping over the layers of the network in reverse order
		for layer in reversed(self.layers):
			# check to see if the layer has a 4D output
			if len(layer.output_shape) == 4:
				return layer.name
 ln=find_target_layer(model)
 labl=[]
 for imp in path:
    orig_img=cv2.imread(imp)
    orig_img= cv2.resize(orig_img, dsize=(224, 224))
    orig_img = orig_img.astype(np.uint8)
    img = np.expand_dims(orig_img,axis=0)
    img = preprocess_input(img)
    predictions = model.predict(img)
    i =np.argmax(predictions[0])
    top_n = 5
    top = decode_predictions(predictions, top=top_n)[0]
    cls = np.argsort(predictions[0])[-top_n:][::-1]
    [gradcamplus,je]=grad_plus(model,img,layer_name=ln)
    print(path)
    print("class activation map for:",top[0])
    fig, ax = plt.subplots(nrows=1,ncols=3)
    plt.subplot(121)
    plt.imshow(orig_img)
    plt.title("input image")
    s=je[:,:,1]
    s=s*0.8
    fimg=s+gradcamplus
    plt.subplot(122)
    plt.imshow(orig_img)
    plt.imshow(gradcamplus,alpha=0.8,cmap="jet")
    plt.title("Grad-CAM++")
    plt.show()
    ii=50
    ii=ii+1
    na=str(ii)+'.jpg'
    plt.imsave(na, gradcamplus,cmap="jet")
     # plt.savefig(na) # i changed  now worked well
    plt.close(fig)
    class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                   'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
                   'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
                   'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
                   'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon',
                   'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut',
                   'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
                   'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
                   'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

    # MRCNN
    # draw an image with detected objects
    def draw_image_with_boxes(filename, boxes_list):
        # load the image
        data = pyplot.imread(filename)
        # plot the image
        pyplot.imshow(data)
        # get the context for drawing boxes
        ax = pyplot.gca()
        # plot each box
        for box in boxes_list:
            # get coordinates
            y1, x1, y2, x2 = box
            # calculate width and height of the box
            width, height = x2 - x1, y2 - y1
            # create the shape
            rect = Rectangle((x1, y1), width, height, fill=False, color='red')
            # draw the box
            ax.add_patch(rect)
        # show the plot
        pyplot.show()
    # define the test configuration
    class TestConfig(Config):
        NAME = "test"
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        NUM_CLASSES = 1 + 80
    # define the model
    rcnn = MaskRCNN(mode='inference', model_dir='./', config=TestConfig())
    # load coco model weights from "https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5"
    rcnn.load_weights('mask_rcnn_coco.h5', by_name=True)
    # load photograph
    img1 = load_img('51.jpg') # this is result of Grad-CAM++
    img = img_to_array(img1)
    # make prediction
    results = rcnn.detect([orig_img], verbose=0)
    # visualize the results
    #draw_image_with_boxes(gradcamplus, results[0]['rois'])
    draw_image_with_boxes('51.jpg', results[0]['rois'])  #inba added (recent)
    r = results[0]
    # show photo with bounding boxes, masks, class labels and scores
    l1=display_instances(img, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])