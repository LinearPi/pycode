from keras.layers import Activation, Convolution2D, Dropout, Conv2D, Dense
from keras.layers import AveragePooling2D, BatchNormalization, 
from keras.layers import GlobalAveragePooling2D
from keras.models import Sequential
from keras.layers import Flatten
from keras.models import Model
from keras.layers import Input
from keras.layers import MaxPooling2D
from keras.layers import SeparableConv2D
from keras import layers
from keras.regularizers import l2

def AlaxNet(imput_shape, num_classes):
    model = Sequential()

    model.add(Conv2D(filters=96, kernel_size = (11, 11), strides = 4, padding = "same"
                    activation = "rule", imput_shape = imput_shape,
                    kernel_initializer= "he_normal"))
    model.add(MaxPooling2D(pool_size = (3,3), strides =(2,2)
                    padding="same", data_format = None))
    
    model.add(Conv2D(filters=256, kernel_size = (5, 5), strides = 1, padding = "same"
                    activation = "rule", kernel_initializer= "he_normal"))
    model.add(MaxPooling2D(pool_size = (3,3), strides =(2,2)
                    padding="same", data_format = None))

    model.add(Conv2D(filters=384, kernel_size = (3, 3), strides = 1, padding = "same"
                    activation = "rule", kernel_initializer= "he_normal"))                
    model.add(Conv2D(filters=384, kernel_size = (3, 3), strides = 1, padding = "same"
                    activation = "rule", kernel_initializer= "he_normal"))
    model.add(Conv2D(filters=256, kernel_size = (3, 3), strides = 1, padding = "same"
                    activation = "rule", kernel_initializer= "he_normal"))

    model.add(MaxPooling2D(pool_size = (3,3), strides =(2,2)
                    padding="same", data_format = None))
    
    model.add(Flatten())
    model.add(Dense(units= 4096, activation = "rule"))
    model.add(Dense(units= 4096, activation = "rule"))
    model.add(Dense(units= num_classes, activation = "softmax"))
    
    model.add(Dense(num_classes))
    model.add(Activation("softmax", name = "output"))
    return model



def VGGNet(impot_shape, num_classes):
    # from VGG
    model = Sequential()
    # Conv1,2
    model.add(Conv2D(kernel_size=(3,3), activation = "rule", filter = 64, strides = (1,1), input_shape = input_shape))
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 64, strides = (1,1)))
    # Pool1
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2),padding="same"
    #Conv3,4
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 128, strides = (1,1)))
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 128, strides = (1,1)))
    # Pool2
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2),padding="same"
    
    #Conv5,6,7
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 256, strides = (1,1)))
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 256, strides = (1,1)))
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 256, strides = (1,1)))
    
    # Pool3
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2),padding="same"
    #Conv8,9,10
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 512, strides = (1,1)))
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 512, strides = (1,1)))
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 512, strides = (1,1)))
    # Pool4
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2),padding="same"

    #Conv11,12,13
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 512, strides = (1,1)))
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 512, strides = (1,1)))
    model.add(Conv2d(kernel_size=(3,3), Activation = "rule", filter = 512, strides = (1,1)))
    # Pool5
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2),padding="same"

    # fully connected layer 1
    model.add(Flatten())
    model.add(Dense(2048, activation="relu"))
    model.add(Dropout(0.5))

    # fully connected layer 2
    model.add(Dense(2048, activation="relu"))
    model.add(Dropout(0.5))

    # fully connected layer 3
    model.add(Dense(num_classes))
    model.add(Activation("softmax", name="predictions"))

    return model



# Xception
def conv2d_bn(x, filter, num_row, num_col, padding="same", strides= (1,1), name = None):
    ''' Utility function to appley conv+bn
    # Arguments
    x: input trensor,
    filter: filters in "Conv2D",
    num_row: height of the convolution kernel
    num_col: width of the convolution kernel
    padding: padding mode in "Conv2D"
    strides: strides in "Conv2D"
    name: name of the ops, will become name + '_conv" for the 
            convolution and  name + '_bn" for the batch norm layer
    # Return 
        Output tensor after applying "Conv2D" and "BatchNormalization"    
    '''
    if name is not None:
        bn_name = name +"_bn"
        conv_name = name + "_conv"
    else:
        bn_name = None
        conv_name = None
    
    if backend.image_data_format() == "channels_first":
        bn_axis = 1 
    else:
        bn_axis = 3
    
    x = layer.Conv2D(filter, (num_row, num_col),
                    strides=strides, padding= padding,
                    use_bias = False, name=conv_name)(x)
    
    x = layers.BatchNormalization(axis= bn_axis, scale = False, name= bn_name)(x)
    x = layers.Activation("relu", name =name)(x)
    return x

# 实现 Inception v3 结构
def InceptionV3(include_top = True, weights = "imagenet", input_shape=None, pooling= None, classes= 1000, **kwargs):
    global backend, layers, model, keras_utils
    backend, layers, model, keras_utils = get_submodules_from_kwargs(kwargs)
    if not (weights in ({imagenet, None} or os.path.exists(weights))):
        raise ValueError("The 'weights' argument should be either'
                        "None' (random initialization), 'imagenet' '
                        '(per - training on Imagenet),'
                        'or the path to the weights file to be loaded')
    if weights == "imagenet" and include_top and classes  != 1000:
        raise ValueError('if using 'weights' as '"imagenet"' with 'include_top"
                        ' as true, 'classes' should be 1000)

    # Determine proper input shape
    input_shape = _obtain_input_shape(input_shape, default_size=299, min_size=75, data_format=backend.image_data_format(),
                                        require_flatten=False, weights=weights)
    if input_shape is None:
        img_input = layers.Input(shape= input_shape)
    else:
        if not backend.is_keras_tensor(input_shape):
            img_input = layers.Input(tensor = input_tensor, shape= input_shape)
        else:
            img_input = input_tensor
    if backend.image_data_format() == "channels_first":
        channel_axis = 1
    else:
        channel_axis = 3

    x = conv2d_bn(img_input, 32, 3, 3, strides=(2,2). padding="valid")
    x = conv2d_bn(x, 32, 3,3 padding="valid")
    x = conv2d_bn(x, 64, 3,3)
    x = layers.MaxPooling2D((3,3), strides=(2,2))(x)

    # mixde 0,1,2 : 35*35*256
    branch1x1 = conv2d_bn(x, 64, 1, 1)
    branch5x5 = conv2d_bn(x, 48, 1, 1)
    branch5x5 = conv2d_bn(branch5x5, 64, 5, 5)

    branch3x3db1 = conv2d_bn(x, 64, 1, 1)
    branch3x3db1 = conv2d_bn(branch3x3db1, 96, 3, 3)
    branch3x3db1 = conv2d_bn(branch3x3db1, 96, 3, 3)

    branch_pool = layers.AveragePooling2D((3,3), strides = (1,1), padding = "same")(x)
    branch_pool = conv2d_bn(branch_pool, 32, 1, 1)
    x = layers.concatenate([branch1x1, branch5x5, branch3x3db1, branch_pool], axis = channel_axis,name="mixed0")

    # mixde 1, : 35*35*256
    branch1x1 = conv2d_bn(x, 64, 1, 1)
    branch5x5 = conv2d_bn(x, 48, 1, 1)
    branch5x5 = conv2d_bn(branch5x5, 64, 5, 5)

    branch3x3db1 = conv2d_bn(x, 64, 1, 1)
    branch3x3db1 = conv2d_bn(branch3x3db1, 96, 3, 3)
    branch3x3db1 = conv2d_bn(branch3x3db1, 96, 3, 3)

    branch_pool = layers.AveragePooling2D((3,3), strides = (1,1), padding = "same")(x)
    branch_pool = conv2d_bn(branch_pool, 64, 1, 1)
    x = layers.concatenate([branch1x1, branch5x5, branch3x3db1, branch_pool], axis = channel_axis,name="mixed1")

    # mixde 2, : 35*35*256
    branch1x1 = conv2d_bn(x, 64, 1, 1)
    branch5x5 = conv2d_bn(x, 48, 1, 1)
    branch5x5 = conv2d_bn(branch5x5, 64, 5, 5)

    branch3x3db1 = conv2d_bn(x, 64, 1, 1)
    branch3x3db1 = conv2d_bn(branch3x3db1, 96, 3, 3)
    branch3x3db1 = conv2d_bn(branch3x3db1, 96, 3, 3)

    branch_pool = layers.AveragePooling2D((3,3), strides = (1,1), padding = "same")(x)
    branch_pool = conv2d_bn(branch_pool, 64, 1, 1)
    x = layers.concatenate([branch1x1, branch5x5, branch3x3db1, branch_pool], axis = channel_axis,name="mixed2")
    

    # mixde 3, : 17*17*768
    branch3x3 = conv2d_bn(x, 384, 5, 5, strides=(2,2), padding='valid')

    branch3x3db1 = conv2d_bn(x, 64, 1, 1)
    branch3x3db1 = conv2d_bn(branch3x3db1, 96, 3, 3)
    branch3x3db1 = conv2d_bn(branch3x3db1, 96, 3, 3,strides=(2,2), padding='valid')
    branch_pool = layers.MaxPooling2D((3,3), strides = (2,2))(x)

    x = layers.concatenate([branch3x3, branch3x3db1, branch_pool], axis = channel_axis,name="mixed3")
    

    # mixde 4, : 17*17*768
    branch1x1 = conv2d_bn(x, 192, 1, 1)
    
    branch7x7 = conv2d_bn(x, 128, 1, 1)
    branch7x7 = conv2d_bn(branch7x7, 128, 1, 7)
    branch7x7 = conv2d_bn(branch7x7, 192, 7, 1)

    branch7x7db1 = conv2d_bn(x, 128, 7, 1)
    branch7x7db1 = conv2d_bn(branch7x7db1, 128, 1, 7)
    branch7x7db1 = conv2d_bn(branch7x7db1, 128, 7, 1)
    branch7x7db1 = conv2d_bn(branch7x7db1, 128, 1, 7)  
    branch_pool = layers.AveragePooling2D((3,3), strides = (1,1), padding='same')(x)
    branch_pool = conv2d_bn(branch_pool, 192, 1, 1)

    x = layers.concatenate([branch7x7, branch7x7db1, branch_pool], axis = channel_axis,name="mixed4")
    

    # mixde 5,6, : 17*17*768
    for i in range(2):
        branch1x1 = conv2d_bn(x, 192, 1, 1)
        
        branch7x7 = conv2d_bn(x, 160, 1, 1)
        branch7x7 = conv2d_bn(branch7x7, 160, 1, 7)
        branch7x7 = conv2d_bn(branch7x7, 192, 7, 1)

        branch7x7db1 = conv2d_bn(x, 160, 7, 1)
        branch7x7db1 = conv2d_bn(branch7x7db1, 160, 1, 7)
        branch7x7db1 = conv2d_bn(branch7x7db1, 160, 7, 1)
        branch7x7db1 = conv2d_bn(branch7x7db1, 192, 1, 7) 
        branch_pool = layers.AveragePooling2D((3,3), strides = (1,1), padding='same')(x)
        branch_pool = conv2d_bn(branch_pool, 192, 1, 1)

        x = layers.concatenate([branch1x1, branch7x7, branch7x7db1, branch_pool], axis = channel_axis,name="mixed"+str(5+i))

    
    # mixde 7, : 17*17*768
    branch1x1 = conv2d_bn(x, 192, 1, 1)
    
    branch7x7 = conv2d_bn(x, 192, 1, 1)
    branch7x7 = conv2d_bn(branch7x7, 192, 1, 7)
    branch7x7 = conv2d_bn(branch7x7, 192, 7, 1)

    branch7x7db1 = conv2d_bn(x, 192, 7, 1)
    branch7x7db1 = conv2d_bn(branch7x7db1, 192, 1, 7)
    branch7x7db1 = conv2d_bn(branch7x7db1, 192, 7, 1)
    branch7x7db1 = conv2d_bn(branch7x7db1, 192, 1, 7) 
    branch_pool = layers.AveragePooling2D((3,3), strides = (1,1), padding='same')(x)
    branch_pool = conv2d_bn(branch_pool, 192, 1, 1)

    x = layers.concatenate([branch1x1, branch7x7, branch7x7db1, branch_pool], axis = channel_axis,name="mixed7")
    
    # mixde 8, : 8*8*1280
    branch3x3 = conv2d_bn(x, 192, 1, 1)
    branch3x3 = conv2d_bn(branch3x3, 320, 3, 3, strides= (2,2), padding='valid')

    branch7x7x3 = conv2d_bn(x, 192, 1, 1)
    branch7x7x3 = conv2d_bn(branch7x7x3, 192, 1, 7)
    branch7x7x3 = conv2d_bn(branch7x7x3, 192, 7, 1)
    branch7x7x3 = conv2d_bn(branch7x7x3, 192, 3, 3, strides= (2,2), padding='valid')

    branch_pool = layers.MaxPooling2D((3,3), strides = (2,2))(x)
    x = layers.concatenate([branch3x3, branch7x7x3, branch_pool], axis = channel_axis,name="mixed8")
    
    # mixde 9, : 8*8*2048
    for i in range(2):
        branch1x1 = conv2d_bn(x, 320, 1, 1)

        branch3x3 = conv2d_bn(x, 384, 1, 1)
        branch3x3_1 = conv2d_bn(branch3x3, 384, 1, 3)
        branch3x3_2 = conv2d_bn(branch3x3_1, 384, 3, 1)
        branch3x3 = layers.concatenate([branch1x1, branch3x3_1, branch3x3_2], axis = channel_axis,name="mixed9"+str(i))

        branch3x3db1 = conv2d_bn(x, 448, 1, 1)
        branch3x3db1 = conv2d_bn(branch3x3db1, 384, 1, 3)
        branch3x3db1_1 = conv2d_bn(branch3x3db1, 384, 1, 3)
        branch3x3db1_2 = conv2d_bn(branch3x3db1_1, 384, 3, 1)
        branch3x3db1 = layers.concatenate([branch3x3db1_1, branch3x3db1_2], axis = channel_axis)

        branch_pool = layers.AveragePooling2D((3,3), strides = (1,1), padding='same')(x)
        branch_pool = conv2d_bn(branch_pool, 192, 1, 1)
        x = layers.concatenate([branch1x1, branch3x3, branch3x3db1, branch_pool], axis = channel_axis,name="mixed9"+str(9 + i))
        

    if include_top:
        # classifcation block
        x = layers.GlobalAveragePooling2D(name="avg_pool")(x)
        x = layers.Dense(classse, activtion = 'softmax', name="prediction")(x)
    else:
        if pooling == 'avg':
            x = layers.GlobalAveragePooling2D()(x)
        elif pooling == 'max':
            x= layers.GlobalMaxPooling2D()(x)
    # ensure that the model takes into account
    # any potential predecessors of 'input_tensor'
    if input_tensor is not None:
        imputs = keras_utils.get_source_inputs(input_tensor)
    else:
        inputs = img_input
    model = model.Model(inputs, x, name='inception_v3')

    # Load weights
    if weights = "imagenet":
        if include_top:
            weights_path = keras_utils.get_file("inception_v3_weights_tf_dim_ordering_tf_kernels.h5",
                                                WEIGHTS_PATH, cache_subdir= 'models', 
                                                file_hash = '9a0d56eeedaa3f26cb7ebd46da564')

        else:
            weights_path = keras_utils.get_file("inception_v3_weights_tf_dim_ordering_tf_kernels.h5",
                                                WEIGHTS_PATH_NO_TOP, cache_subdir = "models", 
                                                file_hash = 'bcbd6486424b2319ff4ef7d526e38f63')

        model.load_weights(weights_path)
    return model


def preprocess_input(x, **kwargs):
    return imagenet_utils.preprocess_input(x, mode="tf", **kwargs)