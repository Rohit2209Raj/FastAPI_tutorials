from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
import pickle
import pandas as pd
import sklearn
app=FastAPI()

# importing model
with open('model.pkl','rb') as f:
    model=pickle.load(f)


tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# creating pyndantic model
class UserInput(BaseModel):
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the user")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the user")]
    height:Annotated[float,Field(...,gt=0,lt=2.5,description="Height of the user")]
    income_lpa:Annotated[float,Field(...,gt=0,description="Salary of the user")]	
    smoker:Annotated[bool,Field(...,description="Is user a smoker?")]
    city:Annotated[str,Field(...,description="city of the user")]	
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description="Jobs of the user")]


    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.bmi>30 and self.smoker:
            return "high"
        elif self.bmi>30 or self.smoker:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"   
    
    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        

# creating end points:

@app.post('/predict')
def predict_output(user_input:UserInput):

    input=pd.DataFrame([{
        'bmi':user_input.bmi,
        "age_group":user_input.age_group,
        "lifestyle_risk":user_input.lifestyle_risk,
        "city_tier":user_input.city_tier, 
        "income_lpa":user_input.income_lpa, 
        "occupation":user_input.occupation
    }])

    prediction = model.predict(input)[0]

    return JSONResponse(status_code=200,content={ 'predicted_category': str(prediction) })





