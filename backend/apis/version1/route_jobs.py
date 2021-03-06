from typing import List
from db.models.users import User
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session, session
from db.session import get_db
from db.models.jobs import Job
from schemas.jobs import JobCreate,ShowJob
from db.repository.jobs import create_new_job,retrive_job,list_jobs,update_job_by_id,delete_job_by_id
from apis.version1.route_login import get_current_user_from_token

router =APIRouter()

@router.post("/create-job",response_model=ShowJob)
def create_job(job:JobCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user_from_token)):
    owner_id = current_user.id
    job = create_new_job(job=job,db=db,owner_id=owner_id)
    return job

@router.get("/get/{id}",response_model=ShowJob)
def retrive_job_by_id(id:int,db:Session=Depends(get_db)):
    job = retrive_job(id=id,db=db)
    if not job :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Job with {id} does not exist")
    return job

@router.get("/all",response_model = List[ShowJob])
def retrive_all_jobs(db:session=Depends(get_db)):
    jobs = list_jobs(db=db)
    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details=f"No job found")
    return jobs

@router.put("/update/{id}")
def update_job(id:int,job:JobCreate,db:Session=Depends(get_db)):
    owner_id = 1 
    message = update_job_by_id(id=id,job=job,db=db,owner_id=owner_id)
    if message == 0 :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,details=f"Job with {id} does not exist...")
    return {"detail":"Succesfully updated data."}

@router.delete("delete/{id}")
def delete_job(id:int,db:Session=Depends(get_db),current_user : User = Depends(get_current_user_from_token)):
    owner_id = 1
    job = retrive_job(id=id,db=db)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Job with {id} does not exist")
    if job.owner_id == current_user.id or current_user.is_superuser:
        delete_job_by_id(id,db,current_user.id)
        return {"detail":"Job succesfuly deleted"}
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail="You are not permitted") 

