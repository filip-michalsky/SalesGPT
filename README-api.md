
# API Guide


## Installation

There are two methods for installing the required packages:

### Method 1: Using `requirements.txt`

append the following packages to the `requirements.txt`:

```plaintext
uvicorn~=0.23.2
fastapi~=0.99.1
pydantic~=1.10.12
setuptools~=68.0.0
```

Then, run:

```bash
pip install -r requirements.txt
```

### Method 2: Direct Installation

Execute the following command:

```bash
pip install "fastapi[all]"
```

## Running the API

To run the API, execute:

```bash
python run_api.py
```

## Testing the API

To test if your API setup is working correctly, use the following curl request:

```bash
curl --location 'http://127.0.0.1:8000/chat' \
--header 'Content-Type: application/json' \
--data '{
    "human_say": "my pain always pain, so I cannot sleep well",
    "conversation_history": [
        "Ted Lasso: Hey, good morning! How are you? <END_OF_TURN>",
        "User: hi, how are you? why calling? <END_OF_TURN>",
        "Ted Lasso: Hi there! I'\''m Ted Lasso from Sleep Haven. I'\''m calling to see if you'\''re looking to achieve better sleep by purchasing a premium mattress. How have you been sleeping lately? <END_OF_TURN>"
    ]
}'
```

If everything is set up correctly, you should receive an appropriate response from your API.

