# TensorFlow Serving (TFS) with Amazon Elastic Inference in containers

## Container for TFS

The TFS container in this repository incorporates Amazon Elastic Inference.  It also incorporates an object detection model trained on the COCO dataset.

To build the container, use the Dockerfile in the *tf-serving-container* directory, and then run the command:
`docker build --no-cache -t <container_tag> .`

To run the container, use the following command:
`docker run --net=host <container_tag>`

The container accepts TFS REST API requests on port 8501.  See the inference container below for example usage.


## Container for Inference

The inference container accepts a video from Amazon S3, parses the video into frames, then performs object detection on the individual frames using the TFS container described above.

To build the container, use the Dockerfile in the *inference-container* directory, and then run the command:
`docker build --no-cache -t <container_tag> .`

To run the container, use the following command:
`docker run --net=host <container_tag>`

The container accepts a POST request for a `detect-objects` API call on port 5000.  An example curl request:

```
curl -d '{"bucket": "sagemaker-projects-pdx", "object": "ei-eks/buddy.mov"}' \
    -X POST http://0.0.0.0:5000/detect-objects
```