from django.template.exceptions import TemplateSyntaxError


class TemplateTagInitError(TemplateSyntaxError):
    """
    Custom exception for init errors in template tags.

    This exception automatically appends a message about not including a specific suffix

    example usage:
    raise TemplateTagInitError(f"Invalid group ID '{group_id}'.", "-toggled-button-group")
    """

    def __init__(self, msg: str, reserved_suffix: str = ""):
        if reserved_suffix:
            super().__init__(
                f"{msg}\n\nDo not include the '{reserved_suffix}' suffix in this tag's argument.\nIf your group's ID is 'example-abc{reserved_suffix}', use 'example-abc' as the argument."
        
            )
