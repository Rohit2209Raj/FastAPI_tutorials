#  An api to fetch data from placement data;

from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Annotated,Literal
import json
app=FastAPI()

class Placement(BaseModel):
    id:Annotated[str,Field(...,description="Enter the student id:",examples=['S006'])]
    name:Annotated[str,Field(...,description="Enter the student name:")]
    age:Annotated[int,Field(...,description="Enter the student age:")]
    branch:Annotated[str,Field(...,description="Enter the student branch:")]
    college:Annotated[str,Field(...,description="Enter the student college:")]
    cgpa:Annotated[float,Field(...,description="Enter the student cgpa:")]
    skills:Annotated[list[str],Field(...,description="Enter the student skills:")]
    company:Annotated[str,Field(...,description="Enter the placement company:")]
    package:Annotated[float,Field(...,description="Enter the student package:")]

def load_data():
    with open('placement.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('placement.json','w') as f:
        json.dump(data,f)


@app.get('/')
def home():
    return {'message':'Welcome to placement data website'}

@app.get('/about')
def home():
    return {'message':'Get information about placed students'}


@app.get('/data')
def getdata():
    data=load_data()
    return data

@app.get('/data/{id}')
def getdata(id:str):

    # load data
    data=load_data()

    # check
    if id in data:
        return data[id]
    
    else:
       raise HTTPException(status_code=400,detail='Student not present in data')
    
@app.get('/sort/{sort_by}/{order_by}')
def sort_data(sort_by:str,order_by:str):

    valid_sort=['age','cgpa','package']
    valid_order=['aesc','desc']

    # load data
    data=load_data()

    # check for sort and order

    if sort_by not in valid_sort or order_by not in valid_order:
        raise HTTPException(status_code=400,detail='Not proper entry')
    
    sorted_data=sorted(data.items(),
                       key=lambda x:x[1][sort_by],
                       reverse=True if order_by=='desc' else False
                       )
    return sorted_data

@app.post('/create/{new_student}')
def create(new_student:Placement):

    # load data
    data=load_data()

    # check
    new_id=new_student.id

    if new_id in data:
        raise HTTPException(status_code=400,detail='student already exist')
    # convert pydantic object to dictionary
    data[new_id]=new_student.model_dump(exclude=['id'])

    save_data(data)

    raise JSONResponse(status_code=400,content='Student added succesfully')




    


