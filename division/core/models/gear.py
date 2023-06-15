from django.db import models

from division.core.models.generics import BaseModel


class GearTalentType(BaseModel):
    """
    Gear Talent Type object.

    To which type of gear doe the talent belong
    - Backpack
    - Body Armour
    - Weapon
    - TBD
    """

    talent_type_name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.talent_type_name


class GearTalent(BaseModel):
    """
    The talents are special bonuses associated with specific weapons/armour.

    With some talents needing to meet a certain criteria in order to properly
    utilize them, while a few others do not need any requirements in order to
    use them. There are also Named Weapons and Armour pieces which have one
    Perfect/Perfected talent that is more powerful than the normal talent.
    """

    talent_type = models.ForeignKey(
        GearTalentType,
        related_name="gear_talent_type",
        on_delete=models.PROTECT,
    )
    talent_name = models.CharField(max_length=64, unique=True)
    talent_description = models.CharField(max_length=256)

    def __str__(self):
        return self.talent_name


class LoadOutSlot(BaseModel):
    """
    Gear Talent Type object.

    To which type of gear doe the talent belong
    - Backpack
    - Body Armour
    - Mask
    - Gloves
    - Knee-pads
    - Holster
    - Primary Weapon
    - Secondary Weapon
    - Sidearm
    - Primary Skill
    - Secondary Skill
    - Specialised
    """

    load_out_slot_name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.load_out_slot_name


class GearAttributeType(BaseModel):
    """
    Gear Attribute Type object.

    Which type of attribute does the gear have
    - Offensive
    - Defensive
    - Utility
    - Core
    """

    gear_attribute_type_name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.gear_attribute_type_name


class GearModificationType(BaseModel):
    """
    Gear Modification Type object.

    Which type of modification does the gear have
    - Offensive
    - Defensive
    - Utility
    """

    gear_modification_type_name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.gear_modification_type_name


class GearModification(BaseModel):
    """
    Gear Modification object.

    Which type of modification does the gear have
    - % Weapon Damage
    - Armour
    - Skill Tier
    - etc
    """

    gear_modification_type = models.ForeignKey(
        GearModificationType,
        related_name="gear_modification_type",
        on_delete=models.PROTECT,
    )
    percent_value = models.BooleanField(default=True)
    max_value = models.IntegerField(default=0)
    gear_modification_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.gear_modification_name


class GearAttribute(BaseModel):
    """
    Gear Attribute object.

    Which type of attribute does the gear have
    - % Critical Hit Damage
    - Armour on Kill
    - % Skill Haste
    - etc
    """

    gear_attribute_type = models.ForeignKey(
        GearAttributeType,
        related_name="gear_attribute_type",
        on_delete=models.PROTECT,
    )
    percent_value = models.BooleanField(default=True)
    max_value = models.IntegerField(default=0)
    gear_attribute_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.gear_attribute_name
