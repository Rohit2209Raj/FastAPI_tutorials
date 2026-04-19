from fastapi import FastAPI,Path,HTTPException,Query
import json
app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data
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
        
    

