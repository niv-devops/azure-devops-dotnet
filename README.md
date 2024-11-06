# Azure Devops - .Net "Hello World" Project

This project utilizes Azure DevOps to automate its build, test, package, and deployment processes using **CI/CD pipelines**. The pipeline is designed to run different tasks depending on the branch (either `dev` or `main`) and includes several stages to ensure code quality and proper versioning of NuGet packages. Below is an overview of the pipeline setup and its functionality.

[![Build Status](https://dev.azure.com/nivz267/hello%20world/_apis/build/status%2Fniv-devops.azure-devops-dotnet?branchName=main)](https://dev.azure.com/nivz267/hello%20world/_build/latest?definitionId=1&branchName=main)
[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-black.svg)](https://sonarcloud.io/summary/new_code?id=nivz267_hello_world)

---

## Table of Contents

1. [Pipeline Overview](#pipeline-overview)
   - [Trigger](#trigger)
   - [Jobs](#jobs)
     - [DevTasks](#1-devtasks-dev-branch-tasks-sonarqube-nuget-and-publish)
     - [MainTasks](#2-maintasks-main-branch-tasks-build-pack-and-publish-project)
2. [Versioning Strategy](#versioning-strategy)
3. [Pipeline Variables](#pipeline-variables)
4. [Tasks Overview](#tasks-overview)
5. [Environment Setup](#environment-setup)
6. [Customizing the Pipeline](#customizing-the-pipeline)
7. [Conclusion](#conclusion)
8. [License](#license)

---

## Pipeline Overview

### Trigger
The pipeline is triggered on changes to the following branches:
- `dev`
- `main`

## Jobs

### 1. `DevTasks`: Dev Branch Tasks (SonarQube, NuGet, and Publish)
This job is triggered when changes are pushed to the `dev` branch. It performs tasks related to dependency restoration, building, packaging, and publishing a NuGet package to Azure Artifacts. The version of the NuGet package is determined dynamically using the build ID and the branch name.

#### Key Steps:
1. **Checkout code**: Ensures the latest code from the repository is checked out.
2. **Install .NET SDK**: Installs the required .NET SDK version (`8.x`).
3. **Install NuGet Tool**: Installs the NuGet CLI to restore and publish packages.
4. **NuGet Authentication**: Authenticates to the Azure Artifacts feed.
5. **SonarQube Analysis**: Runs code quality analysis using SonarQube.
6. **Restore Dependencies**: Restores NuGet packages for the project.
7. **Build Project**: Builds the project in the Release configuration.
8. **SonarQube Analyze**: Analyzes the project for code quality.
9. **Pack Project**: Packs the project into a NuGet package, using a version derived from the branch and build ID.
10. **Push NuGet Package**: Pushes the generated NuGet package to the Azure Artifacts feed.
11. **Print Artifact Version**: Prints the version of the artifact that was pushed.

#### Dynamic Versioning:
The version is set dynamically based on the build ID and the branch name. For `dev` branch, the version follows the format:
```
1.0.<BuildId>-dev
```

### 2. `MainTasks`: Main Branch Tasks (Build, Pack, and Publish Project)
This job is triggered when changes are pushed to the `main` branch. It is primarily focused on building and packaging the project into a NuGet package, which is then published to Azure Artifacts. The versioning strategy here is based on the build ID and is updated with each release.

#### Key Steps:
1. **Install .NET SDK**: Installs the required .NET SDK version (`8.x`).
2. **Restore Dependencies**: Restores NuGet packages for the project.
3. **Build Project**: Builds the project in the Release configuration.
4. **Pack Project**: Packs the project into a NuGet package.
5. **Publish Universal Package**: Publishes the NuGet package to Azure Artifacts using Universal Packages.
6. **Print Artifact Version**: Prints the version of the artifact.
7. **Clean Up**: Cleans up the staging directory after the publish step.

---

## Versioning Strategy
- **Dev Branch**: The version is generated dynamically based on the build ID and branch name. For example, if the build ID is `32` and the branch is `dev`, the version will be `1.0.32-dev`.
- **Main Branch**: Uses a patch versioning scheme, with the version following the format `1.0.<BuildId>`.

---

## Pipeline Variables
- **artifactVersion**: This variable holds the version number for the artifact. It is set dynamically based on the branch and build ID. For `dev` branch, it uses the format `1.0.$(Build.BuildId)-$(Build.SourceBranchName)`.

---

## Tasks Overview

### 1. **UseDotNet**: Installs the required .NET SDK version.
- Version: `8.x`
  
### 2. **NuGetToolInstaller**: Installs the NuGet tool to manage NuGet packages.

### 3. **NuGetAuthenticate**: Authenticates to Azure Artifacts feeds to push and pull packages.

### 4. **SonarQubePrepare** and **SonarQubeAnalyze**: Integrates with SonarQube for static code analysis to ensure code quality.

### 5. **DotNetCoreCLI**:
- `restore`: Restores project dependencies.
- `build`: Builds the project with the `Release` configuration.
- `pack`: Packages the project into a NuGet package.
- `push`: Pushes the NuGet package to Azure Artifacts.

### 6. **UniversalPackages**: Publishes the built package to Azure Artifacts as a Universal Package (for `main` branch).

### 7. **Clean Up**: Removes the staging directory after the package is pushed.

---

## Environment Setup
1. **Azure Artifacts**: The pipeline pushes NuGet packages to the Azure Artifacts feed for your project.
2. **SonarQube**: Ensure your SonarQube instance is properly set up and integrated with Azure DevOps. Replace the `SonarQube` task parameters with your instance details (e.g., organization, project key).

---

## Customizing the Pipeline
You can customize the pipeline by modifying:
- **Versioning Logic**: Modify the version string to follow your preferred versioning scheme (major, minor, patch).
- **Branch Names**: Add additional conditions for other branches, such as `feature/*` for feature-specific builds.
- **Additional Tasks**: Add tasks like tests, deployments, or notifications as needed.

---

## Conclusion
This pipeline automates the build, test, and deployment process for the HelloWorld project. It integrates code quality checks, dependency management, and versioning to ensure that the project is continuously delivered with high standards. The versioning follows a **Semantic Versioning** approach with a dynamic version that adjusts depending on the branch and build number.

Feel free to modify and extend the pipeline as needed to suit the specific requirements of your project.

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
