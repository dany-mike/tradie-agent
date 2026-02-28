#!/usr/bin/env python3
"""Fine-tune Mistral Small model using the Mistral AI SDK."""

import os
from mistralai.client import MistralClient
from mistralai.models.job import CreateFineTuningJobRequest

# Initialize the client
api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY environment variable not set")

client = MistralClient(api_key=api_key)

# Upload the dataset file
dataset_path = "rainmaker_finetune_v1.jsonl"
print(f"Uploading dataset file: {dataset_path}")
with open(dataset_path, "rb") as file:
    upload_response = client.files.upload(file=file, purpose="fine-tuning")

file_id = upload_response.id
print(f"File uploaded successfully. File ID: {file_id}")

# Start the fine-tuning job
print("Starting fine-tuning job...")
job_request = CreateFineTuningJobRequest(
    model="mistral-small-latest",
    training_file=file_id,
    hyperparameters={
        "training_steps": 500,
        "learning_rate": 1e-4,
    },
)

job_response = client.fine_tuning.jobs.create(job_request)
job_id = job_response.id
status_url = f"https://console.mistral.ai/jobs/{job_id}"

print(f"Fine-tuning job started successfully.")
print(f"Job ID: {job_id}")
print(f"Status URL: {status_url}")