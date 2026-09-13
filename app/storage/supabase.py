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