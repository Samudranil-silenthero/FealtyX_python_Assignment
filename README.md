# FealtyX Python Assignment
<h3>Objective: </h3> Create a simple REST API that performs basic CRUD (Create, Read, Update, Delete) operations on a list of students. Each student has the following attributes:

- ID (integer)
- Name (string)
- Age (integer)
- Email (string)

*Additionally*, integrate with [Ollama](https://www.ollama.com/) to generate AI-based summary. Do the prompt engineering to get the summary for the Student.

<h3>Solution: </h3> Used FastAPI, a python based framework.

<h3>How to run? </h3>

- Clone the repo and install the requirements.txt. 
- Create a virtual environment. 
- Install the requirements.txt. 
- Run the server at port 5000. 

```terminal
    $ git clone https://github.com/Samudranil-silenthero/FealtyX_python_Assignment
    $ python -m venv myenv
    $ myenv\Scripts\activate 
    $ pip install -r requirements.txt
    $ uvicorn main:app --reload --port 5000
```

<h3>Different endpoints to be tested in POSTMAN </h3>

- Check the service status (GET): http://localhost:5000/health-check
- Create a student (POST): http://localhost:5000/students
  ```
    Sample payload:
  
      {
          "Student_ID": "1",
          "Name":"Arun",
          "Age": "13",
          "Email": "Arun@google.com"
      }
  ```  
- Delete a student (DELETE): http://localhost:5000/students/{ID}
- Get a student by ID (GET): http://localhost:5000/students/{ID}
- Get all students (GET): http://localhost:5000/students
- Update a student by ID (PUT): http://localhost:5000/students/{ID}
  ```
    Sample payload:
  
      {
          "Student_ID": "1",
          "Name":"Arun Das",
          "Age": "33",
          "Email": "Arun@google.com"
      }
  ``` 
- Generate summary of a student (GET): http://localhost:5000/students/{ID}/summary

## Replace {ID} in URL with an integer like 1, 2 or 33. 
