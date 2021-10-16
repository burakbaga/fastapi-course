from sqlalchemy.orm import Session
from db.repository.jobs import create_new_job,retrive_job
from schemas.jobs import JobCreate
from tests.utils.users import create_random_owner

def test_retrive_job_by_id(db_session:Session):
    title = "test title"
    company = "test company"
    company_url = "testcomp.com"
    location = "USA,NY"
    descriptions = "Foo bar"
    owner = create_random_owner(db=db_session)
    job_schema = JobCreate(title=title,company=company,company_url=company_url,location=location,descriptions=descriptions)
    job = create_new_job(job=job_schema,db=db_session,owner_id=owner.id)
    retrived_job = retrive_job(id=job.id,db=db_session)
    assert retrived_job.id == job.id
    assert retrived_job.title == "test title"
