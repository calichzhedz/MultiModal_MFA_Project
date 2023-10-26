
# Multi-Modal Authentication System

This project is a Flask-based web application for multi-modal authentication using voice and typing dynamics. This guide will help you set up and run the application on your local machine.

## Prerequisites:

1. Python (Preferably 3.6 or above)
2. pip (Python package installer)

## Installation Steps:

1. **Clone the Repository**: 
   If you have git installed, you can clone the repository using:
   
   git clone [repository_url]
   

   If not, you can download the zip file of the project and extract it.

2. **Navigate to the Project Directory**:
   
   cd path_to_project_directory
   

3. **Set Up a Virtual Environment (Optional but recommended)**:
   Setting up a virtual environment will help you avoid potential conflicts between package versions.
   - Install virtualenv:
     
     pip install virtualenv
     
   - Create a virtual environment named 'venv' (or any other name you prefer):
     
     virtualenv venv
     
   - Activate the virtual environment:
     - On macOS and Linux:
       
       source venv/bin/activate
       
     - On Windows:
       
       .\venv\Scripts\activate
       

4. **Install the Required Packages**:
   With the virtual environment activated (or globally if you chose to skip the virtual environment step), run:
   
   pip install -r requirements.txt
   

5. **Set the Flask Application Environment Variables**:
   - On macOS and Linux:
     
     export FLASK_APP=app.py
     export FLASK_ENV=development
     
   - On Windows:
     
     set FLASK_APP=app.py
     set FLASK_ENV=development
     

6. **Run the Flask Application**:
   
   flask run
   

7. **Access the Application**:
   Open your preferred web browser and navigate to:
   
   http://127.0.0.1:5000/
   

## Usage:

1. **Registration**:
   - Navigate to the registration page.
   - Enter a unique username.
   - Record your voice by reading out the prompted text.
   - Type out the provided passage.
   - Submit the form.

2. **Authentication**:
   - Navigate to the authentication page (implementation might be pending or added in future updates).
   - Follow similar steps as registration to authenticate.

