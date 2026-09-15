from app.storage.supabase import TemplateStorage
from uuid import UUID
from app.templates.models import Template, TemplateCreate
from app.templates.repository import TemplateRepository
from app.templates.analyzer import TemplateAnalyzer

class TemplateService:
    
    def __init__(self):
        self.repository = TemplateRepository()
        self.storage = TemplateStorage()
        self.analyzer = TemplateAnalyzer()
        
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
    
    def analyze(
        self,
        template_id: UUID,
    ) -> dict:
        
        template = self.repository.get_by_id(
            template_id
        )
        
        if template is None:
            raise ValueError(
                f"Template not found: {template_id}"
            )
            
        if template.file_path is None:
            raise ValueError(
                f"Template file is not registered: {template_id}"
            )
            
        local_path = self.storage.download_template(
            storage_path=template.file_path,
            destination_path=(
                f"tmp/templates/{template.id}/template.xlsx"
            )
        )
        
        return self.analyzer.analyze_workbook(
            str(local_path)
        )
        
        
        
