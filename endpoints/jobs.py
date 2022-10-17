from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from repositories.jobs import JobRepository
#from endpoints.depends import
from models.jobs import Job, JobIn

router = APIRouter()

router.get('/', response_model=Job)
async def read_jobs():

    return

async def create_jobs():
    return

async def update_jobs():
    return

async def delete_jobs():
    return
