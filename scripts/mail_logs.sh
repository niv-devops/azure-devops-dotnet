#!/bin/bash

if [ $? -ne 0 ]; then # Check if the previous step failed (non-zero exit status)
  echo "Step failed, capturing logs."

  # Capture detailed logs from the build
  curl -s --url "https://dev.azure.com/$(Build.Organization)/$(Build.ProjectName)/_apis/build/builds/$(Build.BuildId)/logs/$(Build.JobId)?api-version=6.0" \
    -H "Authorization: Bearer $(System.AccessToken)" > $(Build.ArtifactStagingDirectory)/build_logs.txt
  
  echo "Logs saved to $(Build.ArtifactStagingDirectory)/build_logs.txt"
  exit 1 # Fail the pipeline by exiting with a non-zero status
fi
