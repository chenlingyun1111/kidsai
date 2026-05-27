import uuid

from fastapi import APIRouter, HTTPException, UploadFile
from sqlalchemy import select

from app.api.deps import CurrentParent, DbSession
from app.models.courseware import Courseware

router = APIRouter()


@router.get("")
async def list_courseware(parent: CurrentParent, db: DbSession):
    result = await db.execute(select(Courseware).where(Courseware.parent_id == parent.id))
    return result.scalars().all()


@router.post("/upload", status_code=201)
async def upload_courseware(
    title: str,
    file: UploadFile,
    parent: CurrentParent,
    db: DbSession,
    description: str | None = None,
):
    file_type = _detect_file_type(file.filename or "")
    content = await file.read()

    # TODO: store file in MinIO and get URL
    file_url = f"uploads/{parent.id}/{file.filename}"

    courseware = Courseware(
        parent_id=parent.id,
        title=title,
        description=description,
        file_type=file_type,
        file_url=file_url,
        file_size_bytes=len(content),
        status="processing",
    )
    db.add(courseware)
    await db.commit()
    await db.refresh(courseware)

    # TODO: dispatch Celery task for courseware processing
    # process_courseware.delay(str(courseware.id))

    return {"id": courseware.id, "status": "processing"}


@router.get("/{courseware_id}")
async def get_courseware(courseware_id: uuid.UUID, parent: CurrentParent, db: DbSession):
    cw = await db.get(Courseware, courseware_id)
    if not cw or cw.parent_id != parent.id:
        raise HTTPException(status_code=404, detail="Courseware not found")
    return cw


@router.delete("/{courseware_id}", status_code=204)
async def delete_courseware(courseware_id: uuid.UUID, parent: CurrentParent, db: DbSession):
    cw = await db.get(Courseware, courseware_id)
    if not cw or cw.parent_id != parent.id:
        raise HTTPException(status_code=404, detail="Courseware not found")
    await db.delete(cw)
    await db.commit()


def _detect_file_type(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    mapping = {"pdf": "pdf", "png": "image", "jpg": "image", "jpeg": "image", "mp3": "audio", "wav": "audio", "txt": "text"}
    return mapping.get(ext, "text")
