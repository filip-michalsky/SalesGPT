# SalesGPT Frontend Application

### Overview

This repository contains the frontend application for SalesGPT, a tool designed for testing and debugging purposes. Built on the Next.js platform, it provides a user-friendly interface to interact with the SalesGPT functionalities.

### Installation

To set up the project environment, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the frontend directory: `cd frontend/`
3. Install all the necessary dependencies: `npm install`
  
### Running the Application

To start the frontend server, run the following command:
`npm run dev`
After starting the server, the application will be available at [localhost:3000/chat](http://localhost:3000/chat). 

### Backend Dependency

This frontend application is designed to work in conjunction with a FastAPI backend. To initiate the backend server, execute the following command from the SalesGPT/ directory: `uvicorn run_api:app --port 8000`


## Setup help 
If you want your setup to enable local startup using our frontend please make sure the ENVIRONMENT environment variable is set to a different value than "deployment". 


## Contributing

We welcome contributions to the SalesGPT frontend application. Please feel free to submit pull requests or open issues to suggest improvements or add new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.