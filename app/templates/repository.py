from uuid import UUID

from app.db.supabase import supabase
from app.templates.models import Template, TemplateCreate

from app.templates.models import(
    Template,
    TemplateCreate,
    TemplateExample,
    TemplateExampleCreate,
)


class TemplateRepository: 
    
    def create(
        self,
        template_data: TemplateCreate
        ) -> Template:
        
        response = (
            supabase
            .table("templates")
            .insert(
                template_data.model_dump()
            )
        .execute()
        )
        
        return Template.model_validate(
            response.data[0]
        )
        
        
    def get_by_id(
        self,
        template_id: UUID,
    ) -> Template | None:
        
        response = (
            supabase
            .table("templates")
            .select("*")
            .eq(
                "id",
                str(template_id)
            )
            .maybe_single()
            .execute()
        )
        
        if response.data is None:
            return None
        
        return Template.model_validate(
            response.data
        )
        
    def update_file_path(
    self,
    template_id: UUID,
    file_path: str,
    ) -> Template:
        
        response = (
        supabase
        .table("templates")
        .update({
            "file_path": file_path
        })
        .eq(
            "id",
            str(template_id),
        )
        .execute()
    )
        return Template.model_validate(
            response.data[0]
        )
        
class TemplateExampleRepository:
    
    def create(
        self,
        example_data: TemplateExampleCreate,
    ) -> TemplateExample:
        
        response = (
            supabase
            .table("template_examples")
            .insert(
                example_data.model_dump(
                    mode="json"
                )
            )
            .execute()
        
        )
        
        return TemplateExample.model_validate(
            response.data[0]
        )
        
    def get_by_template_id(
        self,
        template_id: UUID,
    ) -> list[TemplateExample]:
        
        response = (
            supabase
            .table("template_examples")
            .select("*")
            .eq(
                "template_id",
                str(template_id),
            )
            .order(
                "created_at"
            )
            .execute()
        )
        
        return [
            TemplateExample.model_validate(row)
            for row in response.data
        ]
        
    def update_file_path(
        self,
        example_id: UUID,
        file_path: str,
    ) -> TemplateExample:
        
        response = (
            supabase
            .table("template_examples")
            .update({
                "file_path": file_path
            })
            .eq(
                "id",
                str(example_id),
            )
            .execute()
        )
        
        return TemplateExample.model_validate(
            response.data[0]
        )