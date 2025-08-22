import json
import boto3
import base64
import sagemaker
from sagemaker.serializers import IdentitySerializer
from sagemaker.predictor import Predictor

# --- Function 1: ImageSerializer ---
s3 = boto3.client('s3')

def imageSerializer_handler(event, context):
    """A function to serialize target data from S3"""
    
    key = event['s3_key']
    bucket = event['s3_bucket']
    
    s3.download_file(bucket, key, "/tmp/image.png")
    
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data.decode('utf-8'),
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

# --- Function 2: ImageClassifier ---
ENDPOINT = "<YOUR_ENDPOINT_NAME>" 

def imageClassifier_handler(event, context):
    
    image_data_str = event['body']['image_data']
    image = base64.b64decode(image_data_str)

    predictor = Predictor(ENDPOINT, sagemaker_session=sagemaker.Session())
    predictor.serializer = IdentitySerializer("image/png")
    
    inferences = predictor.predict(image).decode('utf-8')
    
    event['body']["inferences"] = inferences
    return {
        'statusCode': 200,
        'body': event['body']
    }

# --- Function 3: InferenceFilter ---
THRESHOLD = .93

def inferenceFilter_handler(event, context):
    
    inferences_str = json.loads(event['body'])['inferences']
    inferences = json.loads(inferences_str)
    
    meets_threshold = max(inferences) > THRESHOLD
    
    if meets_threshold:
        pass
    else:
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }