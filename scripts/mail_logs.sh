#!/bin/bash

echo "Capturing logs for job $(Build.JobId)..."

curl -s --url "https://dev.azure.com/$(Build.Organization)/$(Build.ProjectName)/_apis/build/builds/$(Build.BuildId)/logs/$(Build.JobId)?api-version=6.0" \
    -H "Authorization: Bearer $(System.AccessToken)" > "$(Build.ArtifactStagingDirectory)/build_logs.txt"

if [ -f "$(Build.ArtifactStagingDirectory)/build_logs.txt" ]; then
  echo "Logs saved to $(Build.ArtifactStagingDirectory)/build_logs.txt"
else
  echo "Failed to capture logs."
fi

exit 0
