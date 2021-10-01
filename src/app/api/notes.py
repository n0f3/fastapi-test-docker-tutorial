from typing import List
import fastapi
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Path
from fastapi.routing import APIRouter

from app.api import crud
from app.api.models import NoteDB, NoteSchema

router = APIRouter()

@router.post('/', response_model=NoteDB, status_code=201)
async def create_node(payload: NoteSchema):
    # payload is available only if validation
    # of the body succeeds
    note_id = await crud.post(payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description
    }
    return response_object

@router.get('/{id}/', response_model=NoteDB, status_code=fastapi.status.HTTP_200_OK)
async def get_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

@router.get('/', response_model=List[NoteDB], status_code=fastapi.status.HTTP_200_OK)
async def get_all_notes():
    return await crud.get_all()

@router.put('/{id}/', response_model=NoteDB)
async def update_note(payload: NoteSchema, id: int = Path(..., gt=0)):
    note = await crud.get(id)
    # TODO: check how we can raise this same exact
    # exception from inside the crud call
    if not note:
        raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Note not found")

    note_id = await crud.put(id, payload=payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description
    }
    return response_object
    
@router.delete('/{id}/', response_model=NoteDB, status_code=fastapi.status.HTTP_200_OK)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    await crud.delete(id)

    return note
