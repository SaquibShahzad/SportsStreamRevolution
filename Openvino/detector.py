import cv2 as cv
import os

from openvino.inference_engine import IENetwork, IECore


class PedestrianDetector:
    def __init__(self):
        self.network = IENetwork(model='Openvino/data/intel/person-detection-retail-0013/FP32/person-detection-retail-0013.xml',
                                 weights='Openvino/data/intel/person-detection-retail-0013/FP32/person-detection-retail-0013.bin')
        # Get Input Layer Information
        self.input_layer = next(iter(self.network.inputs))
        print("Input Layer: ", self.input_layer)

        # Get Output Layer Information
        OutputLayer = next(iter(self.network.outputs))
        print("Output Layer: ", OutputLayer)

        # Get Input Shape of Model
        InputShape = self.network.inputs[self.input_layer].shape
        print("Input Shape: ", InputShape)

        # Get Output Shape of Model
        OutputShape = self.network.outputs[OutputLayer].shape
        print("Output Shape: ", OutputShape)

        core = IECore()

        self.exec = core.load_network(network=self.network, device_name='CPU')

    def detect(self, image):
        resized = cv.resize(image, (544, 320))
        resized = resized.transpose(2, 0, 1)
        input_image = resized.reshape((1, ) + resized.shape)

        return self.exec.infer(
            inputs={self.input_layer: input_image}
        )['detection_out']