# Project: ML-Powered Logistics for Scones Unlimited

## Introduction

This project demonstrates the development and deployment of a scalable and robust machine learning workflow on Amazon SageMaker and AWS serverless technologies. The goal is to create an image classification model that can automatically distinguish between bicycles and motorcycles. This capability allows a scone-delivery-focused logistics company, `Scones Unlimited`, to optimize its operations by routing delivery drivers to the correct loading bays and assigning orders based on their vehicle type.

The project showcases a complete end-to-end MLOps pipeline, from data staging and model training to automated inference and performance monitoring.

## Project Architecture

The solution is built on a serverless, event-driven architecture that combines AWS SageMaker with AWS Lambda and Step Functions.

- **Data Staging:** The CIFAR-100 dataset is used as a stand-in for real-world images. A custom Python notebook handles the data extraction, transformation (filtering for `bicycle` and `motorcycle` classes), and loading to an S3 bucket.  
- **Model Training & Deployment:** An image classification model is trained using the SageMaker built-in algorithm and the prepared data in S3. The model is then deployed to a SageMaker Endpoint for real-time inference, with `DataCaptureConfig` enabled for monitoring.  
- **Serverless Workflow:** An automated, event-driven workflow is created using AWS Step Functions, which orchestrates three separate AWS Lambda functions:  
  - `ImageSerializer`: Fetches an image from S3 based on an event and base64-encodes it.  
  - `ImageClassifier`: Takes the encoded image and calls the SageMaker Endpoint to get a prediction.  
  - `InferenceFilter`: Acts as a business logic safeguard, checking the prediction's confidence score against a predefined threshold. The workflow "fails loudly" if the threshold is not met.  
- **Monitoring and Evaluation:** The deployed endpoint's performance is monitored by running multiple test cases that are designed to both succeed and fail, confirming the robustness of the system.

## Project Files

- `starter.ipynb`: A Jupyter Notebook containing the code for data preparation, model training, and model deployment to an AWS SageMaker Endpoint.  
- `lambda.py`: A Python script containing the code for the three AWS Lambda functions (`ImageSerializer`, `ImageClassifier`, and `InferenceFilter`) that form the core of the serverless workflow.  
- `execution.json`: The JSON definition of the AWS Step Functions state machine that orchestrates the Lambda functions into a single workflow.  
- `screencap_step_function_pass.png`: A screenshot demonstrating a successful execution of the Step Functions workflow.  
- `screencap_step_function_fail.png`: A screenshot demonstrating a failed execution of the Step Functions workflow, triggered by a low-confidence prediction.

## Results and Observations

- **Model Performance:** The trained model achieved a validation accuracy of approximately **86%**, which is well above the project's target threshold of `.8` validation accuracy for the simulated dataset.  
- **Workflow Reliability:** The serverless workflow successfully demonstrates its ability to handle both high-confidence predictions (passing the result to the next step) and low-confidence predictions (failing the workflow as a safeguard), a critical feature for a production environment.

This project provides a comprehensive and portfolio-ready example of how to build, deploy, and monitor scalable machine learning applications on AWS.
