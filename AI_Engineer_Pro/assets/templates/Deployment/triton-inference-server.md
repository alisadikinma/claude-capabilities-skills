# Triton Inference Server

High-performance model serving for production ML at scale.

## Setup

```bash
# Pull Triton image
docker pull nvcr.io/nvidia/tritonserver:23.10-py3

# Run Triton
docker run --gpus all --rm -p8000:8000 -p8001:8001 -p8002:8002 \
  -v $(pwd)/model_repository:/models \
  nvcr.io/nvidia/tritonserver:23.10-py3 \
  tritonserver --model-repository=/models
```

## Model Repository Structure

```
model_repository/
└── pcb_detector/
    ├── config.pbtxt
    └── 1/
        └── model.onnx (or model.plan for TensorRT)
```

## Config File (config.pbtxt)

```protobuf
name: "pcb_detector"
platform: "onnxruntime_onnx"  # or "tensorrt_plan"
max_batch_size: 8
input [
  {
    name: "images"
    data_type: TYPE_FP32
    dims: [ 3, 640, 640 ]
  }
]
output [
  {
    name: "output"
    data_type: TYPE_FP32
    dims: [ 25200, 85 ]  # Adjust based on model
  }
]
dynamic_batching {
  preferred_batch_size: [ 4, 8 ]
  max_queue_delay_microseconds: 100
}
```

## Client

```python
import tritonclient.http as httpclient
import numpy as np
from PIL import Image

# Initialize client
client = httpclient.InferenceServerClient(url="localhost:8000")

# Prepare input
image = Image.open("test.jpg").resize((640, 640))
img_array = np.array(image).transpose(2, 0, 1).astype(np.float32) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Create input
inputs = [
    httpclient.InferInput("images", img_array.shape, "FP32")
]
inputs[0].set_data_from_numpy(img_array)

# Inference
outputs = [httpclient.InferRequestedOutput("output")]
response = client.infer("pcb_detector", inputs, outputs=outputs)

# Get result
output_data = response.as_numpy("output")
print(output_data.shape)
```

## Python Backend (Custom Processing)

```python
# model_repository/pcb_detector/1/model.py
import triton_python_backend_utils as pb_utils
import numpy as np

class TritonPythonModel:
    def initialize(self, args):
        # Load model
        import torch
        self.model = torch.jit.load("model.pt")
        self.model.eval()
    
    def execute(self, requests):
        responses = []
        
        for request in requests:
            # Get input
            input_tensor = pb_utils.get_input_tensor_by_name(request, "images")
            img = input_tensor.as_numpy()
            
            # Inference
            with torch.no_grad():
                output = self.model(torch.from_numpy(img))
            
            # Create response
            out_tensor = pb_utils.Tensor("output", output.numpy())
            responses.append(pb_utils.InferenceResponse([out_tensor]))
        
        return responses
```

## Ensemble Model (Multi-stage)

```
model_repository/
├── preprocessing/
│   └── 1/model.py
├── detection/
│   └── 1/model.onnx
└── postprocessing/
    └── 1/model.py
```

## gRPC Client (Faster)

```python
import tritonclient.grpc as grpcclient

client = grpcclient.InferenceServerClient(url="localhost:8001")

# Same inference as HTTP
response = client.infer("pcb_detector", inputs, outputs=outputs)
```

## Performance Tips

- Use **TensorRT** for NVIDIA GPUs (2-5x speedup)
- Enable **dynamic batching** for throughput
- Use **model ensemble** for complex pipelines
- Monitor with **Prometheus** metrics
