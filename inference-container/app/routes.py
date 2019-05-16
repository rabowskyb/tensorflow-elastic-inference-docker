import boto3
import cv2
import numpy
import requests
import flask

from app import app, coco_label_map

ENDPOINT = "http://localhost:8501/v1/models/default:predict"
TMP_FILE = "./tmp.mov"

s3 = boto3.client('s3')

def get_prediction_from_image_array(image_array):
    payload = {"instances": [image_array.tolist()]}
    res = requests.post(ENDPOINT, json=payload)
    return res.json()['predictions'][0]

def get_classes_with_scores(predictions):
    num_detections = int(predictions['num_detections'])
    detected_classes = predictions['detection_classes'][:num_detections]
    detected_classes =[coco_label_map.label_map[int(x)] for x in detected_classes]
    detection_scores = predictions['detection_scores'][:num_detections]
    return list(zip(detected_classes, detection_scores))

def process_video_from_file(file_path):
    frames = []
    vidcap = cv2.VideoCapture(file_path)
    success, frame = vidcap.read()
    success = True
    while success:
      frames.append(frame)
      success, frame = vidcap.read()

    pred_list = []
    for frame in frames:
        preds = get_prediction_from_image_array(frame)
        classes_with_scores = get_classes_with_scores(preds)
        pred_list.append(str(classes_with_scores))
        pred_list.append('\n')
        # TODO:  delete this conditional
        if len(pred_list) > 6:
            break

    return pred_list


@app.route('/detect-objects', methods=['POST'])
def predict():
    s3_video = flask.request.get_json(force=True)
    s3.download_file(s3_video['bucket'], s3_video['object'], TMP_FILE)
    predictions_for_frames = process_video_from_file(TMP_FILE)

    # output is a string where each line is an array of predictions for a frame
    return ''.join(e for e in predictions_for_frames)

