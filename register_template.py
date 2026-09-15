from app.templates.service import TemplateService


service = TemplateService()

template = service.register(
    name="テストテンプレート",
    local_file_path="sample/template.xlsx",
)

print(template)