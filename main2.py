#  An api to fetch data from placement data;

from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Annotated,Literal,Optional
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


class Placement_update(BaseModel):
    name:Annotated[str,Field(Optional,description="Enter the student name:")]
    age:Annotated[int,Field(Optional,description="Enter the student age:")]
    branch:Annotated[str,Field(Optional,description="Enter the student branch:")]
    college:Annotated[str,Field(Optional,description="Enter the student college:")]
    cgpa:Annotated[float,Field(Optional,description="Enter the student cgpa:")]
    skills:Annotated[list[str],Field(Optional,description="Enter the student skills:")]
    company:Annotated[str,Field(Optional,description="Enter the placement company:")]
    package:Annotated[float,Field(Optional,description="Enter the student package:")]

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

# Better version made below
# @app.get('/data')
# def getdata():
#     data=load_data()
#     return data

# Better could have name it /student/id
# login below is not good
# @app.get('/data/{id}') 
# def getdata(id:str):

#     # load data
#     data=load_data()

#     # transfering logic here
#     valid_features=['name','branch','college','company']

#     if  id in valid_features:
#         return get_feature(id)
#     elif id != 'id':
#          raise HTTPException(status_code=400,detail='Not a valid Entry')
#     else:
#         # check
#         if id in data:
#             return data[id]
        
#         else:
#             raise HTTPException(status_code=400,detail='Student not present in data')
    


@app.get('/student/{id}') 
def getdata(id:str):

    # load data
    data=load_data()
    # check
    if id in data:
        return data[id]    
    else:
        raise HTTPException(status_code=400,detail='Student not present in data')
  
@app.get('/data')
def get_data(
    name: Optional[str] = Query(None, description="Name of the student"),
    # age: Optional[int] = Query(None, description="Age of the student"),
    branch: Optional[str] = Query(None),
    college: Optional[str] = Query(None),
    min_cgpa: Optional[float] = Query(None),
    max_cgpa: Optional[float] = Query(None),
    skills: Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    min_package: Optional[float] = Query(None),
    max_package: Optional[float] = Query(None)
):
    # load data
    data=load_data()

    # Now traversing and checking
    result=[]
    result=list(data.values())

    # for string features
    if name:
        result=[s for s in result if  s['name']==name]
    if branch:
        result=[s for s in result if  s['branch']==branch]
    if college:
        result=[s for s in result if  s['college']==college]
    if company:
        result=[s for s in result if  s['company']==company]
    if skills:
         result = [s for s in result if skills.lower() in [skill.lower() for skill in s["skills"]]]
    # for range and numerical feastures

    if min_package:
        result=[s for s in result if  s['package']>=min_package]
    if max_package:
        result=[s for s in result if  s['package']<=max_package]
    if min_cgpa:
        result=[s for s in result if  s['cgpa']>=min_cgpa]
    if max_cgpa:
        result=[s for s in result if  s['cgpa']<=max_cgpa]
        
    return result   
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

@app.post('/create')
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

    return JSONResponse(status_code=200,content='Student added succesfully')



@app.put('/edit/{id}')
def edit(id:str,new_data:Placement_update):

    # load data
    data=load_data()

    # check

    if id not in data:
        raise HTTPException(status_code=200,detail='Student Not Found')
    
    # create a dictionary out of pydanctic_update object

    new_dict=new_data.model_dump(exclude_unset=True)


    # change new_dict key and val in normal dict of that particular student

    # particular student
    student=data[id]

    for key,value in new_dict.items():
        student[key]=value

    save_data(data)

    return JSONResponse(status_code=200,content='Student details edited succesfully')


@app.delete('/delete/{id}')
def delete(id:str):
    # load data
    data=load_data()

    # check
    if id not in data:
        raise HTTPException(status_code=200,detail='Student Not Found')
    del data[id]

    save_data(data)

    return JSONResponse(status_code=400,content='Student deleted succesfully')





    




    


