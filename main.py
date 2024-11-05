'''
Impoting required libraries
'''
from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import ollama
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List
import json

app = FastAPI()

class StudentDetails(BaseModel):
    Student_ID: int
    Name:str = Field(min_length= 3)
    Age: int
    Email: EmailStr   

# Act as a DB
students_db: List[Dict] = []

@app.get("/health-check")
async def hc():
    '''
    Check if service is up or not
    '''
    return {"Status": "Congratulations! Service is Up and Running."}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    List down validation errors
    """
    errors = [{"field": error["loc"][-1], "message": error["msg"]} for error in exc.errors()]
    return JSONResponse(
        status_code= 400,
        content={ "status_code": 400, "detail": "Validation failed", "errors": errors}
    )

@app.post("/students")
async def createStudents(data: StudentDetails):
    """
    This end point creates a student based on StudentDetails, if the student doesnot exist.
    - Request: StudentDetails in the request.
    - Responses:
        200 OK: Student successfully created.
        409 Conflict: Student already exist
    """
    name = data.Name
    student_ID= data.Student_ID
    age= data.Age
    email= data.Email
    
    for student in students_db:
        if student["Student_ID"] == student_ID:
            return JSONResponse({ 
                    "status_code": 409, 
                    "message": "Student ID already exists!"
                }, 
                status_code= 409
            )
        
    students_db.append({
        "Student_ID": student_ID,
        "Name": name,
        "Age": age,
        "Email": email
    })
    
    return JSONResponse({ 
                            "status_code": 200, 
                            "message": "Student created successfully!"
                        }, 
                        status_code= 200
    )

@app.get("/students")
async def getAllStudents():
    """
    This end point returns a list of students.
    - Responses:
        200 OK: Student List returned successfully.
    """
    studentList=[]
    for student in students_db:
        studentList.append(student)
    
    return JSONResponse({ 
                            "status_code": 200, 
                            "message": studentList
                        }, 
                        status_code= 200
    )

@app.get("/students/{student_id}")
async def getStudentByID(student_id: int):
    """
    This end point search a student by its id and returns if found.
    - Request: Studentid in the param.
    - Responses:
        200 OK: Student found successfully.
        404 Conflict: Student not found
    """
    
    for student in students_db:
        if student["Student_ID"] == student_id:
            return JSONResponse({ 
                    "status_code": 200, 
                    "message": student
                }, 
                status_code= 200
            )
    
    return JSONResponse({ 
                            "status_code": 404, 
                            "message": "Student not found!"
                        }, 
                        status_code= 404
    )

@app.delete("/students/{student_id}")
async def deleteStudentByID(student_id: int):
    """
    This end point search a student by its id and delete it if found.
    - Request: Studentid in the param.
    - Responses:
        200 OK: Student deleted successfully.
        404 Conflict: Student not found
    """
    
    for student in students_db:
        if student["Student_ID"] == student_id:
            students_db.remove(student)
            return JSONResponse({ 
                    "status_code": 200, 
                    "message": "Student deleted successfully!"
                }, 
                status_code= 200
            )
    
    return JSONResponse({ 
                            "status_code": 404, 
                            "message": "Student not found!"
                        }, 
                        status_code= 404
    )

@app.put("/students/{student_id}")
async def updateStudentByID(student_id: int, data: StudentDetails):
    """
    This end point search a student by its id and update it with the new data if found.
    - Request: Studentid in the param and new student details in param
    - Responses:
        200 OK: Student updated successfully.
        404 Conflict: Student not found
    """
    
    for student in students_db:
        if student["Student_ID"] == student_id:

            student["Name"]= data.Name
            student["Age"]= data.Age
            student["Email"]= data.Email

            return JSONResponse({ 
                    "status_code": 200, 
                    "message": "Student updated successfully!"
                }, 
                status_code= 200
            )
    
    return JSONResponse({ 
                            "status_code": 404, 
                            "message": "Student not found!"
                        }, 
                        status_code= 404
    )

@app.get("/students/{student_id}/summary")
async def generate_summary(student_id: int):

    student= await getStudentByID(student_id)
    student_dict= (json.loads(student.body.decode('utf-8')))
    
    if student.status_code!= 200:
        return JSONResponse(student_dict, status_code= student.status_code)
    
    try:          
        student_detail= student_dict['message']
        name = student_detail['Name']
        student_ID= student_detail['Student_ID']
        age= student_detail['Age']
        email= student_detail['Email']
        prompt = f"Summarize the following student profile:\n\nStudent_ID: {student_ID}\nName: {name}\nAge: {age}\nEmail: {email}"  
        
        response = ollama.generate(model='llama3', prompt=prompt)
        
        return JSONResponse(
            { "status_code": 200, "summary": response['response']},
            status_code= 200,
        )
        
    except Exception as e:
        return JSONResponse(
            { "status_code": 500, "message": "Error in generating summary using OLLAM" },
            status_code= 500
        )
 