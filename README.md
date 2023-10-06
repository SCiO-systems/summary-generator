## Summary Generator Coverage Report

For LLM model download (place in "models" folder):

```
# Make sure you have git-lfs installed (https://git-lfs.com)
git lfs install
git clone https://huggingface.co/pszemraj/long-t5-tglobal-base-16384-booksci-summary-v1
```

For coverage report:

- coverage run test_summarizer.py
- coverage report -i
- (if needed) coverage xml

#### Deployment
In order to run the Docker image, you must have NVIDIA Container Toolkit installed both on the host and the container runtime (https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

`docker run --name summary-generator --gpus all sciohub/summary-generator`