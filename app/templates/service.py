from pathlib import Path

from app.storage.supabase import TemplateStorage
from app.templates.models import Template, TemplateCreate
from app.templates.repository import TemplateRepository

class TemplateService:
    
    def __init__(self):
        self.repository = TemplateRepository()
        self.storage = TemplateStorage()
        
    def register(
        self,
        name: str,
        local_file_path: str,
    ) -> Template:
        
        template = self.repository.create(
            TemplateCreate(
                name=name,
                output_type="excel",
            )
        )
        
        storage_path = self.storage.upload_template(
            template_id=template.id,
            file_path=local_file_path,
        )
        
        template = self.repository.update_file_path(
            template_id=template.id,
            file_path=storage_path,
        )
        
        return template
        
        
