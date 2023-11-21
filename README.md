# Crypto Bill of Materials Action

Create a Crypto Bill of Materials using CodeQL

## Usage

```yaml
name: Create Crypto Bill of Materials

on:
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  build-matrix:
    name: Build analysis matrix
    runs-on: ubuntu-latest
    outputs:
      repositories: ${{ steps.build-matrix-action.outputs.repositories }}
    steps:
      - uses: advanced-security/cbom-action/build-matrix@v1
        id: build-matrix-action
        with:
          repositoryNameWithOwner: ${{ github.repository }}
          analyzeDependencies: true
          minimumLanguageBytes: 0
  run-cbom-action:
    name: ${{ fromJson(matrix.repository).nameWithOwner }} - ${{ fromJson(matrix.repository).language }}
    runs-on: ubuntu-latest
    needs: build-matrix
    continue-on-error: true
    strategy:
      fail-fast: false
      matrix:
        repository: ${{ fromJSON(needs.build-matrix.outputs.repositories) }}
    steps:
      - uses: advanced-security/cbom-action/analyze@v1
        with:
          repositoryNameWithOwner: ${{ fromJson(matrix.repository).nameWithOwner }}
          language: ${{ fromJson(matrix.repository).language }}
  add-workflow-summary:
    name: CBOM results
    runs-on: ubuntu-latest
    needs: run-cbom-action
    steps:
      - uses: advanced-security/cbom-action/workflow-summary@v1
```

### Build analysis matrix options

```yaml
  repositoryNameWithOwner:
    description: The base repository to analyze
    required: false
    default: ${{ github.repository }}
  minimumLanguageBytes:
    description: |
      The minimum number of detected bytes a language must have
      to be included in the matrix
    required: false
    default: "5000"
  analyzeDependencies:
    description: Whether to analyze dependencies
    required: false
    default: "false"
```

### Analyze options

```yaml
  repositoryNameWithOwner:
    description: The repository to analyze
    required: false
    default: ${{ github.repository }}
  language:
    description: The language to analyze
    required: true
  createCodeQLDatabaseIfRequired:
    description: |
      Whether to create a CodeQL database if 'repositoryNameWithOwner:' does
      not have a CodeQL database stored
    required: false
    default: "true"
  queryTimeout:
    description: The maximum time in seconds to run a query
    required: false
    default: "300"
  requestGitHubAnalysis:
    description: |
      Whether to request an analysis by GitHub if 'repositoryNameWithOwner:' does
      not have a CodeQL database stored or the workflow run is unable to create
      a database using CodeQL Autobuild
    required: false
    default: "false"
  uploadToCodeScanning:
    description: Whether to upload the results to GitHub Code Scanning (not recommended)
    required: false
    default: "false"
```
