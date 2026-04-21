from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from  typing import Annotated,Literal
import json
app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='Id of patient',examples=['P005'])]
    name:Annotated[str,Field(...,description='Name of pateint',max_length=50)]
    city:Annotated[str,Field(description='City patient belongs to')]
    age:Annotated[int,Field(...,description='Age of patient',gt=0,lt=150)]
    gender:Annotated[str,Literal['male','female','others'],Field(...,description='Gender of patient')]
    height:Annotated[float,Field(...,description='Height of patient in mtrs')]
    weight:Annotated[float,Field(...,description='Weight of pateint in kg')]

    @computed_field
    @property
    def bmi(self)->float:
        return (self.weight)/(self.height**2)
    

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18:
            return 'UnderWeight'
        elif self.bmi<24:
            return 'Normal'
        elif self.bmi<26:
            return 'OverWeight'
        else:
            return 'Obese'


def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data


def savedata(data):
    with open('patients.json','w') as f:
        json.dump(data,f)


@app.get("/")
def hello():
    return {"message":"Hello World"}

@app.get("/about")
def about():
    return {"message":"I am from Poornima College of Engineering"}

@app.get("/views")
def views():
    data=load_data()
    return data


@app.get('/patient/{patient_id}')
def patient_view(patient_id:str=Path(...,description="Enter the patient ID",example="P003")):
    data=load_data()
    if patient_id in data :
        return data[patient_id]
    else:
        # return {"message":"Patient not found"}
        raise HTTPException(status_code=404,detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='Chose on which height,weight,bmi to sort the patients on'),
                  order_by:str=Query('aesc',description='Chose between aescending/descending')):
    
    valid_feilds=['height','weight','bmi']
    valid_by=['aesc','desc']

    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400,detail=f'{sort_by} not present in valid_feilds')
    if order_by not in ['aesc','desc']:
        raise HTTPException(status_code=400,detail=f'{order_by} not present in valid')
    else:
        data=load_data()
        sort_order=True if order_by=='desc' else False
        sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
        return sorted_data
    

@app.post('/create')
def create_patient(patient:Patient):
    data=load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already Exists')
    
    data[patient.id]=patient.model_dump(exclude=['id'])

    savedata(data)

    return JSONResponse(status_code=200,content={'message':'Patient addedd succesfully'})
        
    

