import os
import sys
from pathlib import Path
import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = os.path.join(Path(os.path.relpath(ROOT, Path.cwd())), 'external', 'yolov5')  # relative

from external.yolov5.models.common import DetectMultiBackend
from external.yolov5.utils.torch_utils import select_device
from external.yolov5.utils.general import (check_img_size, non_max_suppression, scale_coords,
                                           clip_coords, xywh2xyxy, xyxy2xywh)
from external.yolov5.utils.plots import Annotator, colors
from external.yolov5.utils.augmentations import letterbox
import numpy as np


class YoloV5(object):
    def __init__(self,
                 weights=os.path.join(ROOT, 'yolov5s.pt'),
                 imgsz=(640, 640),
                 conf_thres=0.25,  # confidence threshold
                 iou_thres=0.45,  # NMS IOU threshold
                 max_det=1000,  # maximum detections per image
                 device='',
                 classes=None,  # filter by class: --class 0, or --class 0 2 3
                 agnostic_nms=False,  # class-agnostic NMS
                 line_thickness=3,  # bounding box thickness (pixels)
                 hide_labels=False,  # hide labels
                 hide_conf=False,  # hide confidences
                 half=False,  # use FP16 half-precision inference
                 dnn=False,  # use OpenCV DNN for ONNX inference
    ):
        """
        :weights: Path to the weights file,
        :imgsz: Inference size (height, width),
        :conf_thres: Infernece confidence threshold,
        :iou_thres: Non-max supression threshold,
        :max_det: Maximum detections per image,
        :device: Device to be used, ej. 'cpu' or gpu number: 0...,
        :classes: Filter by class: --class 0, or --class 0 2 3,
        :agnostic_nms: Class-agnostic NMS,
        :line_thickness: Bounding box thickness (pixels),
        :hide_labels: Hide labels,
        :hide_conf: Hide confidences,
        :half: Use FP16 half-precision inference,
        :dnn: Use OpenCV DNN for ONNX inference
        """
        self.weights = weights
        self.data = os.path.join(ROOT, 'data/coco128.yaml')
        self.imgsz = imgsz
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.max_det = max_det
        self.device = device
        self.classes = classes
        self.agnostic_nms = agnostic_nms
        self.augment = False
        self.line_thickness = line_thickness
        self.hide_labels = hide_labels
        self.hide_conf = hide_conf
        self.half = half
        self.dnn = dnn
        self.model, self.names = self.initialize()

    def initialize(self):
        """
        Initialize necessary dependencies to use Yolov5
        """
        # Select specified device
        self.device = select_device(self.device)
        # Instantiate the model
        model = DetectMultiBackend(self.weights, device=self.device, dnn=self.dnn, data=self.data)
        # Get model parameters
        self.stride, names, self.pt, = model.stride, model.names, model.pt
        # Check image size
        self.imgsz = check_img_size(self.imgsz, s=self.stride)
        # Run inference warmup
        model.warmup(imgsz=(1, 3, *self.imgsz))
        # set True to speed up constant image size inference
        cudnn.benchmark = True
        return model, names

    def preprocess_img(self, img0):
        """
        :img0: Frame to be preprocessed,
        :return ->
            img: Preprocessed image,
            img0: Original image
        """
        # Padded resize
        img = letterbox(img0, self.imgsz, stride=self.stride, auto=self.pt)[0]
        # Convert
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)
        return img, img0

    def crop_img(self, xyxy, im, BGR=True):
        """
        :xyxy: Boox coordinates,
        :im: Image to be cropped,
        :BGR: Change image to BGR format,
        :return ->
          crop: Crop of the image
        """
        xyxy = torch.tensor(xyxy).view(-1, 4)
        b = xyxy2xywh(xyxy)  # boxes
        b[:, 2:] = b[:, 2:] * 1.02 + 10  # box wh * gain + pad
        xyxy = xywh2xyxy(b).long()
        clip_coords(xyxy, im.shape)
        crop = im[int(xyxy[0, 1]):int(xyxy[0, 3]), int(xyxy[0, 0]):int(xyxy[0, 2]), ::(1 if BGR else -1)]
        return crop

    def detect_img(self, img, draw=True, crop=False, store_metadata=False):
        """
        :img: Image to be detected,
        :draw: Draw the box on the image,
        :crop: Store detection crops,
        :store_metadata: Store coordinates, confidences and classes,
        :return ->
          result: Dictionary which contains the image, crops if selected and metadata if selected
        """
        # Instantiate necessary objects
        crops, metadata, result = [], {'box': [], 'conf': [], 'label': []}, {}
        # Preprocess the image
        img, img0 = self.preprocess_img(img)
        # Transform to tensor and move to selected device
        im = torch.from_numpy(img).to(self.device)
        # Apply half precision if selected
        im = im.half() if self.half else im.float()  # uint8 to fp16/32
        # Normalize image between 0 and 1
        im /= 255  # 0 - 255 to 0.0 - 1.0
        # Expand for batch dim
        if len(im.shape) == 3: im = im[None]
        # Inference
        pred = self.model(im, augment=self.augment)
        # NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres,
                                   self.classes, self.agnostic_nms, max_det=self.max_det)
        # Process predictions
        for i, det in enumerate(pred):  # per image
            # Duplicate images in memory
            im0, imc = img0.copy(), img0.copy()
            # Initialize drawer
            annotator = Annotator(im0, line_width=self.line_thickness,
                                  example=str(self.names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)  # integer class
                    # Create label to be shown
                    label = None if self.hide_labels else (self.names[c] if self.hide_conf
                                                           else f'{self.names[c]} {conf:.2f}')
                    # Draw box
                    annotator.box_label(xyxy, label, color=colors(c, True))
                    # Get crops if selected
                    if crop: crops.append(self.crop_img(xyxy, imc))
                    # Store metadata if selected
                    if not draw or store_metadata:
                        metadata['box'].append(
                            dict(zip(['x1', 'y1', 'x2', 'y2'], torch.tensor(xyxy, device = 'cpu').numpy().tolist()))
                        )
                        metadata['conf'].append(f'{conf:.2f}')
                        metadata['label'].append(c)
            # Stream results
            img0 = annotator.result()
        # Store image to be returned
        result['img'] = img0
        # Store crops to be returned if selected
        if crop: result['crops'] = crops
        # Store metadata to be returned if selected
        if store_metadata or not draw: result['metadata'] = metadata
        return result
