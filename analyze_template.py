from pprint import pprint
from uuid import UUID
from app.templates.service import TemplateService

service = TemplateService()

template_id = UUID(
    "88c592ee-0aa9-4ca4-9f42-d51dc26c4c36"
)

result = service.analyze(template_id)

pprint(result)