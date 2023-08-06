#==============================================================================#
#  Author:       Dominik Müller                                                #
#  Copyright:    2022 IT-Infrastructure for Translational Medical Research,    #
#                University of Augsburg                                        #
#                                                                              #
#  This program is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation, either version 3 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#==============================================================================#
# Abstract Base Class for Architectures
from aucmedi.neural_network.architectures.arch_base import Architecture_Base

#-----------------------------------------------------#
#                    Architectures                    #
#-----------------------------------------------------#
# Vanilla Classifier
from aucmedi.neural_network.architectures.image.vanilla import Architecture_Vanilla
# DenseNet
from aucmedi.neural_network.architectures.image.densenet121 import Architecture_DenseNet121
from aucmedi.neural_network.architectures.image.densenet169 import Architecture_DenseNet169
from aucmedi.neural_network.architectures.image.densenet201 import Architecture_DenseNet201
# EfficientNet
from aucmedi.neural_network.architectures.image.efficientnetb0 import Architecture_EfficientNetB0
from aucmedi.neural_network.architectures.image.efficientnetb1 import Architecture_EfficientNetB1
from aucmedi.neural_network.architectures.image.efficientnetb2 import Architecture_EfficientNetB2
from aucmedi.neural_network.architectures.image.efficientnetb3 import Architecture_EfficientNetB3
from aucmedi.neural_network.architectures.image.efficientnetb4 import Architecture_EfficientNetB4
from aucmedi.neural_network.architectures.image.efficientnetb5 import Architecture_EfficientNetB5
from aucmedi.neural_network.architectures.image.efficientnetb6 import Architecture_EfficientNetB6
from aucmedi.neural_network.architectures.image.efficientnetb7 import Architecture_EfficientNetB7
# InceptionResNet
from aucmedi.neural_network.architectures.image.inceptionresnetv2 import Architecture_InceptionResNetV2
# InceptionV3
from aucmedi.neural_network.architectures.image.inceptionv3 import Architecture_InceptionV3
# ResNet
from aucmedi.neural_network.architectures.image.resnet50 import Architecture_ResNet50
from aucmedi.neural_network.architectures.image.resnet101 import Architecture_ResNet101
from aucmedi.neural_network.architectures.image.resnet152 import Architecture_ResNet152
# ResNetv2
from aucmedi.neural_network.architectures.image.resnet50v2 import Architecture_ResNet50V2
from aucmedi.neural_network.architectures.image.resnet101v2 import Architecture_ResNet101V2
from aucmedi.neural_network.architectures.image.resnet152v2 import Architecture_ResNet152V2
# ResNeXt
from aucmedi.neural_network.architectures.image.resnext50 import Architecture_ResNeXt50
from aucmedi.neural_network.architectures.image.resnext101 import Architecture_ResNeXt101
# MobileNet
from aucmedi.neural_network.architectures.image.mobilenet import Architecture_MobileNet
from aucmedi.neural_network.architectures.image.mobilenetv2 import Architecture_MobileNetV2
# NasNet
from aucmedi.neural_network.architectures.image.nasnetlarge import Architecture_NASNetLarge
from aucmedi.neural_network.architectures.image.nasnetmobile import Architecture_NASNetMobile
# VGG
from aucmedi.neural_network.architectures.image.vgg16 import Architecture_VGG16
from aucmedi.neural_network.architectures.image.vgg19 import Architecture_VGG19
# Xception
from aucmedi.neural_network.architectures.image.xception import Architecture_Xception

#-----------------------------------------------------#
#       Access Functions to Architecture Classes      #
#-----------------------------------------------------#
# Architecture Dictionary
architecture_dict = {
    "Vanilla": Architecture_Vanilla,
    "ResNet50": Architecture_ResNet50,
    "ResNet101": Architecture_ResNet101,
    "ResNet152": Architecture_ResNet152,
    "ResNet50V2": Architecture_ResNet50V2,
    "ResNet101V2": Architecture_ResNet101V2,
    "ResNet152V2": Architecture_ResNet152V2,
    "ResNeXt50": Architecture_ResNeXt50,
    "ResNeXt101": Architecture_ResNeXt101,
    "DenseNet121": Architecture_DenseNet121,
    "DenseNet169": Architecture_DenseNet169,
    "DenseNet201": Architecture_DenseNet201,
    "EfficientNetB0": Architecture_EfficientNetB0,
    "EfficientNetB1": Architecture_EfficientNetB1,
    "EfficientNetB2": Architecture_EfficientNetB2,
    "EfficientNetB3": Architecture_EfficientNetB3,
    "EfficientNetB4": Architecture_EfficientNetB4,
    "EfficientNetB5": Architecture_EfficientNetB5,
    "EfficientNetB6": Architecture_EfficientNetB6,
    "EfficientNetB7": Architecture_EfficientNetB7,
    "InceptionResNetV2": Architecture_InceptionResNetV2,
    "InceptionV3": Architecture_InceptionV3,
    "MobileNet": Architecture_MobileNet,
    "MobileNetV2": Architecture_MobileNetV2,
    "NASNetMobile": Architecture_NASNetMobile,
    "NASNetLarge": Architecture_NASNetLarge,
    "VGG16": Architecture_VGG16,
    "VGG19": Architecture_VGG19,
    "Xception": Architecture_Xception
}
""" Dictionary of implemented 2D Architectures Methods in AUCMEDI.

    The base key (str) or an initialized Architecture can be passed to the [Neural_Network][aucmedi.neural_network.model.Neural_Network] class as `architecture` parameter.

    ???+ example "Example"
        ```python title="Recommended via Neural_Network class"
        my_model = Neural_Network(n_labels=4, channels=3, architecture="2D.Xception",
                                  input_shape(512, 512), activation_output="softmax")
        ```

        ```python title="Manual via architecture_dict import"
        from aucmedi.neural_network.architectures import Classifier, architecture_dict

        classification_head = Classifier(n_labels=4, activation_output="softmax")
        my_arch = architecture_dict["2D.Xception"](classification_head,
                                                   channels=3, input_shape=(512,512))

        my_model = Neural_Network(n_labels=None, channels=None, architecture=my_arch)
        ```

        ```python title="Manual via module import"
        from aucmedi.neural_network.architectures import Classifier
        from aucmedi.neural_network.architectures.image import Architecture_Xception

        classification_head = Classifier(n_labels=4, activation_output="softmax")
        my_arch = Architecture_Xception(classification_head,
                                        channels=3, input_shape=(512,512))

        my_model = Neural_Network(n_labels=None, channels=None, architecture=my_arch)
        ```

    ???+ warning
        If passing an architecture key to the Neural_Network class, be aware that you have to add "2D." in front of it.

        For example:
        ```python
        # for the image architecture "ResNeXt101"
        architecture="2D.ResNeXt101"
        ```

    Architectures are based on the abstract base class [aucmedi.neural_network.architectures.arch_base.Architecture_Base][].
"""

# List of implemented architectures
architectures = list(architecture_dict.keys())

#-----------------------------------------------------#
#       Meta Information of Architecture Classes      #
#-----------------------------------------------------#
# Utilized standardize mode of architectures required for Transfer Learning
supported_standardize_mode = {
    "Vanilla": "z-score",
    "ResNet50": "caffe",
    "ResNet101": "caffe",
    "ResNet152": "caffe",
    "ResNet50V2": "tf",
    "ResNet101V2": "tf",
    "ResNet152V2": "tf",
    "ResNeXt50": "torch",
    "ResNeXt101": "torch",
    "DenseNet121": "torch",
    "DenseNet169": "torch",
    "DenseNet201": "torch",
    "EfficientNetB0": "caffe",
    "EfficientNetB1": "caffe",
    "EfficientNetB2": "caffe",
    "EfficientNetB3": "caffe",
    "EfficientNetB4": "caffe",
    "EfficientNetB5": "caffe",
    "EfficientNetB6": "caffe",
    "EfficientNetB7": "caffe",
    "InceptionResNetV2": "tf",
    "InceptionV3": "tf",
    "MobileNet": "tf",
    "MobileNetV2": "tf",
    "NASNetMobile": "tf",
    "NASNetLarge": "tf",
    "VGG16": "caffe",
    "VGG19": "caffe",
    "Xception": "tf"
}
""" Dictionary of recommended [Standardize][aucmedi.data_processing.subfunctions.standardize] techniques for 2D Architectures Methods in AUCMEDI.

    The base key (str) can be passed to the [DataGenerator][aucmedi.data_processing.data_generator.DataGenerator] as `standardize_mode` parameter.

    ???+ info
        If training a new model from scratch, any Standardize technique can be used at will. <br>
        However, if training via transfer learning, it is required to use the recommended Standardize technique!

    ???+ example "Example"
        ```python title="Recommended via the Neural_Network class"
        my_model = Neural_Network(n_labels=8, channels=3, architecture="2D.DenseNet121")

        my_dg = DataGenerator(samples, "images_dir/", labels=None,
                              resize=my_model.meta_input,                  # (224, 224)
                              standardize_mode=my_model.meta_standardize)  # "torch"
        ```

        ```python title="Manual via supported_standardize_mode import"
        from aucmedi.neural_network.architectures import supported_standardize_mode
        sf_norm = supported_standardize_mode["2D.DenseNet121"]

        my_dg = DataGenerator(samples, "images_dir/", labels=None,
                              resize=(224, 224),                           # (224, 224)
                              standardize_mode=sf_norm)                    # "torch"
        ```

    ???+ warning
        If using an architecture key for the supported_standardize_mode dictionary, be aware that you have to add "2D." in front of it.

        For example:
        ```python
        # for the image architecture "ResNeXt101"
        from aucmedi.neural_network.architectures import supported_standardize_mode
        sf_norm = supported_standardize_mode["2D.ResNeXt101"]
        ```
"""
