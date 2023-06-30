"""Skill Models for the Division 2 DB App"""

from django.db import models

from division.core.models.generics import BaseModel


class Slot(BaseModel):
    """
    Skill object slot.

    Which type of slot by skill
    - Agitator Slot
    - Battery Slot
    - Gyro Slot
    - etc
    """

    slot_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.slot_name



class SlotModificationType(BaseModel):
    """
    Skill object slot.

    Which type of slot by skill
    - Agitator Slot
    - Battery Slot
    - Gyro Slot
    - etc
    """

    percent_value = models.BooleanField(default=True)
    max_value = models.IntegerField(default=0)
    slot_modification_type_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.slot_modification_type_name

class Skill(BaseModel):
    """
    Skill object.

    Which type of kill
    - Turret
    - Ballistic Shield
    - % Skill Haste
    - etc
    """

    skill_name = models.CharField(max_length=64, unique=True)
    skill_description = models.CharField(max_length=2048, unique=True)
    slot = models.ManyToManyField(Slot)

    def __str__(self):
        return self.skill_name


class SkillVariant(BaseModel):
    """
    Skill object variant.

    Which type of variant by skill
    - Defender Drone
    - Artillery Turret
    - Reviver Hive
    """

    skill_variant_name = models.CharField(max_length=64, unique=True)
    skill_variant_description = models.CharField(max_length=2048, unique=True)
    skill = models.ForeignKey(
        Skill,
        related_name="variant_skill",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.skill_variant_name



class SlotModification(BaseModel):
    """
    Skill object slot.

    Which type of slot by skill
    - Agitator Slot
    - Battery Slot
    - Gyro Slot
    - etc
    """

    slot = models.ForeignKey(
        Slot,
        related_name="slot",
        on_delete=models.PROTECT,
    )
    slot_modification_type = models.ForeignKey(
        SlotModificationType,
        related_name="slot_modification_type",
        on_delete=models.PROTECT,
    )

    skill = models.ForeignKey(
        Skill,
        related_name="modification_skill",
        on_delete=models.PROTECT,
    )

