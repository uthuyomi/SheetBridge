from uuid import UUID

from app.db.supabase import supabase
from app.templates.models import Template, TemplateCreate


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