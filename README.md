# PennyWise

# PennyWise - Financial Assistant

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)


## Introduction
PennyWise is an AI-powered financial assistant designed to help students manage their finances effectively. It provides personalized advice and tools to track expenses, create budgets, and improve financial literacy.

## Features
- User-friendly interface for data entry
- AI-driven financial advice based on user inputs
- Comprehensive financial resources and tips

## Technologies Used
- Python (Flask for backend)
- Streamlit for the frontend
- ChatGPT API for financial advice 

## Installation

Please note that you will have to get a OpenAPI key for use of the financial AI PennyWise. You can obtain one by signing up at [OpenAI's website](https://platform.openai.com/signup). Once you have your key, add it to your environment variables or include it in your configuration file as instructed in the documentation.

1. Clone the repository:
   ```bash
   git clone https://github.com/PennyWiseHackUTA24/PennyWise.git

2. Cd into PennyWise:
    ```bash
    cd PennyWise

4. Pip install requirements
    ```bash
    pip install -r requirements.txt

5. Backend .env
     Make a .env file and add following variables:
   ```bash
   CHATGPT_API_URL= 'https://api.openai.com/v1/chat/completions'
   CHATGPT_API_KEY=yourapikey

6. Config file
  (due to github secrets we had to remove contents of this file and re-add after pushing)
   Add the following code to config.py in the backend:

   ```bash
   config.py file:

   import os

   from dotenv import load_dotenv
   load_dotenv()


   CHATGPT_API_URL = os.getenv("CHATGPT_API_URL", "https://api.openai.com/v1/chat/completions")
   CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY", "yourapikeyhere")

7. Run backend
   ```bash
   flask run

8. Open another terminal and CD frontend
9. Run frontend
    ```bash
    streamlit run app.py


### API Endpoint
POST /userDataFrontend: Receives user data from the frontend and returns financial advice.

### Contributing
Contributions are welcome! Please submit a pull request or open an issue for discussion.
