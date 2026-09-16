from app.storage.supabase import TemplateStorage
from uuid import UUID
from app.templates.models import Template, TemplateCreate
from app.templates.repository import TemplateRepository
from app.templates.analyzer import TemplateAnalyzer

from app.templates.models import (
    Template,
    TemplateCreate,
    TemplateExample,
    TemplateExampleCreate,
)

from app.templates.repository import (
    TemplateExampleRepository,
    TemplateRepository,
)

class TemplateService:
    
    def __init__(self):
        self.repository = TemplateRepository()
        self.example_repository = TemplateExampleRepository()
        
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
        
    def register_example(
        self,
        template_id: UUID,
        local_file_path: str,
    ) -> TemplateExample:
        
        template = self.repository.get_by_id(
            template_id
        )
        
        if template is None:
            raise ValueError(
                f"Template not found: {template_id}"
            )
            
        example = self.example_repository.create(
            TemplateExampleCreate(
                template_id=template_id,
            )
        )
        
        storage_path = self.storage.upload_example(
            template_id=template_id,
            example_id=example.id,
            file_path=local_file_path,
        )
        
        example = self.example_repository.update_file_path(
            example_id=example.id,
            file_path=storage_path,
        )
        
        return example
    
    
    def analyze_example(
        self,
        template_id: UUID,
    ) -> list[dict]:
        
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
            
        examples = self.example_repository.get_by_template_id(
            template_id
        )
        
        template_local_path = self.storage.download_template(
            storage_path=template.file_path,
            destination_path=(
                f"tmp/templates/{template.id}/template.xlsx"
            )
        )
        
        results = []
        
        for example in examples:
            if example.file_path is None:
                continue
            
            example_local_path = self.storage.download_template(
                storage_path=example.file_path,
                destination_path=(
                    f"tmp/templates/{template.id}/examples/"
                    f"{example.id}.xlsx"
                )
            )
            
            differences = self.analyzer.compare_workbooks(
                template_path=str(template_local_path),
                example_path=str(example_local_path),
            )
            
            results.append({
                "example_id": str(example.id),
                "differences": differences,
            })
            
        return results
        
