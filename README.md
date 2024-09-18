# ModelStack

**ModelStack** is a backend framework designed for creating, training, and deploying PyTorch neural networks. It provides a simple API for building and managing custom models, *currently* focused on image classification tasks using the MNIST dataset. Users can create models, configure training parameters such as learning rate and epochs, and submit jobs for model training, all through API endpoints.

![](./docs/assets/SystemDiagram.drawio.svg)

The framework is containerized using Docker, making it easy to set up and use. The MNIST dataset and user-created models are stored locally, and the system allows users to upload new images for prediction once the models are trained.

## Quick Start

1. **Clone the repository:**
    ```
    git clone https://github.com/RichardNooooh/ModelStack modelstack
    cd modelstack
    ```
2. **Run the system with Docker Compose:**
    ```
    docker-compose up --build
    ```
3. **Access the API:** Once the containers are up and running, the API will be available at `http://localhost:8000/`. For a basic interactive interface, you can access the [Swagger](http://localhost:8000/docs) or [ReDoc UI](http://localhost:8000/redoc).

## Example

Here is a simple example with creating, running, and using a fully connected network. If you don't want to use the interactive interfaces, I listed the cURL commands.

1. **Create model**:
    
    A user can create a model through the `/models` endpoint. The JSON body below will create a PyTorch model with a 28x28 input tensor that will flatten this image into a vector, send it through 2 linear layers with the ReLU activation function, then output a length-10 vector that will correspond to the 10 different image labels.

    ```json
    curl -X 'POST' \
    'http://localhost:8000/models/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '
    {
        "name": "linear_test1",
        "input_shape": [
            28,
            28
        ],
        "output_shape": 10,
        "layers": [
            {
            "layer_type": "Flatten"
            },
            {
            "layer_type": "Linear",
            "size": 512
            },
            {
            "layer_type": "Activation",
            "activation": "ReLU"
            },
            {
            "layer_type": "Linear",
            "size": 512
            },
            {
            "layer_type": "Activation",
            "activation": "ReLU"
            }
        ]
    }'
    ```
    Running this example, this is a sample response:
    ```json
    {
    "id": "7904e863-034f-469e-bca4-16c7c267b0ec", // random UUID
    "model": {
        "name": "linear_test1",
        "input_shape": [
        28,
        28
        ],
        "output_shape": 10,
        "layers": [
        {
            "layer_type": "Flatten"
        },
        {
            "layer_type": "Linear",
            "size": 512
        },
        {
            "layer_type": "Activation",
            "activation": "ReLU"
        },
        {
            "layer_type": "Linear",
            "size": 512
        },
        {
            "layer_type": "Activation",
            "activation": "ReLU"
        }
        ]
    },
    "is_trained": false
    }
    ```

    The `/models` endpoint returned the original model JSON inside of the "model" field, along with two additional fields: "id" and "is_trained". "id" is a random UUID4 string that will be used to submit jobs and retrieve inference results. 
    
    The "is_trained" field is currently not used (pending feature).

2. **Submit a job:**

    With our newly created model in `./storage/` and the database, we can submit a job through the `/jobs` endpoint. We specify the model's id, the dataset name (currently only mnist), along with the learning parameters.

    ```json
    curl -X 'POST' \
    'http://localhost:8000/jobs/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '
    {
        "model_id": "7904e863-034f-469e-bca4-16c7c267b0ec",
        "dataset_name": "mnist",
        "parameters": {
            "learning_rate": 0.01,
            "num_epochs": 5
        }
    }'
    ```

    ```json
    {
        "id": "b4d99ed2-e797-4377-8333-aa983cd88ad3",
        "model_id": "7904e863-034f-469e-bca4-16c7c267b0ec",
        "dataset_name": "mnist",
        "job_status": "pending",
        "start_time": "2024-09-18T00:15:29.224740",
        "parameters": {
            "learning_rate": 0.01,
            "num_epochs": 5
        }
    }
    ```

    You can check the status of all of the jobs in the queue with a GET request. "pending" jobs are in the job queue, "done" jobs are completed by the `compute` server, and the "running" job is the current job operating on the server.
    ```json
    curl -X 'GET' \
    'http://localhost:8000/jobs/?num=5' \
    -H 'accept: application/json'
    ```
    ```json
    [
        {
            "id": "b4d99ed2-e797-4377-8333-aa983cd88ad3",
            "model_id": "7904e863-034f-469e-bca4-16c7c267b0ec",
            "dataset_name": "mnist",
            "job_status": "running", // will say "done" once the job is completed
            "start_time": "2024-09-18T00:15:29.224740", // UTC time
            "parameters": {
                "learning_rate": 0.01,
                "num_epochs": 5
            }
        }
    ]
    ```

    While the job is running, the `docker-compose` command will spit out the test set accuracy and training loss values for each epoch. These metrics will be available through the API in a future update.

3. **Use Model For Inference**:
    
    Now that the model is trained, we can begin using this model to predict the labels on new images with the `/inference/` endpoint. I hand-drew new sample images in the `./inference_examples` directory for easy testing, but any black background image of a number should work. In the cURL example below, I am uploading 3 images, where `a.png` is an image of a `1`, `h.png` is a `6`, and `d.png` is a `0`.

    ```json
    curl -X 'POST' http://localhost:8000/inference/ \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'data={"mod_id":"0bc1d158-b5ca-40c1-9118-b5467e2554bc"}' \
    -F 'files=@./inference_examples/a.png;type=image/png' \
    -F 'files=@./inference_examples/h.png;type=image/png' \
    -F 'files=@./inference_examples/d.png;type=image/png'
    ```

    The API will return the predicted classification with the highest probability.

    ```json
    {
        "mod_id": "0bc1d158-b5ca-40c1-9118-b5467e2554bc",
        "results": [
            {
            "file_name": "a.png",
            "classification": 1,
            "probability": 0.9980536699295044
            },
            {
            "file_name": "h.png",
            "classification": 6,
            "probability": 0.9753394722938538
            },
            {
            "file_name": "d.png",
            "classification": 0,
            "probability": 0.9129588007926941
            }
        ]
    }
    ```

## Planned Features

ModelStack is an ongoing project, with the following features planned:

- Convergence metrics stored in database and accessed through a `/metrics` endpoint
- Google Cloud bucket storage instead of local `./storage/` folder
- Text data support
- Small LLM creation and generation
- Custom dataset upload to `/datasets` endpoint
- Full Cloud Deployment
    - `server` API container on Google Cloud Run
    - `db` container on Google CloudSQL
    - `compute` container on Google Cloud Compute Engine
- Simple React frontend for interacting with API in the `./client` directory
    - Dashboard with convergence metrics data visualizer
    - Simple forms to GET/POST to endpoints
