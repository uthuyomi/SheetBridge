from pathlib import Path
from uuid import UUID

from app.db.supabase import supabase

TEMPLATE_BUCKET = "templates"

class TemplateStorage:
    
    def upload_template(
        self,
        template_id: UUID,
        file_path: str,
    ) -> str:
        
        source_path = Path(file_path)
        
        storage_path = (
            f"{template_id}/"
            f"{source_path.name}"
        )
        
        with source_path.open("rb") as file:
            supabase.storage.from_(
                TEMPLATE_BUCKET
            ).upload(
                path=storage_path,
                file=file,
                file_options={
                    "content-type":
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                }
            )
            
        return storage_path
    
    
    def download_template(
        self,
        storage_path: str,
        destination_path: str,
    ) -> Path:
        
        file_data = (
            supabase.storage
            .from_(TEMPLATE_BUCKET)
            .download(storage_path)
        )
        
        destination = Path(destination_path)
        
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        
        destination.write_bytes(file_data)
        
        return destination
    
    def upload_example(
        self,
        template_id: UUID,
        example_id: UUID,
        file_path: str,
    ) -> str:
        
        source_path = Path(file_path)
        
        storage_path = Path(
             f"{template_id}/examples/"
             f"{example_id}{source_path.suffix}"
        )
        
        with source_path.open("rb") as file:
            supabase.storage.from_(
                TEMPLATE_BUCKET
            ).upload(
                path=storage_path,
                file=file,
                file_options={
                    "content-type":
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                },
            )
            
        return storage_path
    
