"""Django admin customization."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from division.core import models
from division.core.models import gear
from division.core.models import skills


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ["id"]
    list_display = ["email", "first_name", "last_name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal Info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(gear.LoadOutSlot, admin.ModelAdmin)
admin.site.register(gear.GearModificationType, admin.ModelAdmin)
admin.site.register(gear.GearAttributeType, admin.ModelAdmin)
admin.site.register(gear.GearTalentType, admin.ModelAdmin)
admin.site.register(gear.GearModification, admin.ModelAdmin)
admin.site.register(skills.Slot, admin.ModelAdmin)
admin.site.register(skills.SlotModificationType, admin.ModelAdmin)


@admin.register(gear.GearAttribute)
class GearAttributeAdmin(admin.ModelAdmin):
    """Define the admin pages for GearAttribute."""

    list_display = ("gear_attribute_name", "max_value", "percent_value", "gear_attribute_type")

    class Meta:
        ordering = ("gear_attribute_type", "gear_attribute_name")


@admin.register(skills.Skill)
class SkillAdmin(admin.ModelAdmin):
    """Define the admin pages for SkillA."""

    list_display = ("skill_name", "skill_description", "created_at")

    class Meta:
        ordering = "skill_name"


@admin.register(skills.SkillVariant)
class SkillVariantAdmin(admin.ModelAdmin):
    """Define the admin pages for SkillVariant."""

    list_display = ("skill_variant_name", "skill_variant_description", "created_at")

    class Meta:
        ordering = "skill_variant_name"


@admin.register(gear.GearTalent)
class GearTalentAdmin(admin.ModelAdmin):
    """Define the admin pages for SkillVariant."""

    list_display = ("talent_name", "talent_description")


@admin.register(skills.SlotModification)
class SlotModificationAdmin(admin.ModelAdmin):
    """Define the admin pages for SlotModification."""

    list_display = ("get_skill", "get_slot", "get_slot_modification_type")

    def get_skill(self, obj):
        return obj.skill.skill_name

    get_skill.short_description = "Skill"

    def get_slot(self, obj):
        return obj.slot.slot_name

    get_slot.short_description = "Skill Slot"

    def get_slot_modification_type(self, obj):
        return obj.slot_modification_type.slot_modification_type_name

    get_slot_modification_type.short_description = "Slot Modification"
