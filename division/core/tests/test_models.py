"""Tests for models."""

from django.test import TestCase
from django.contrib.auth import get_user_model

from division.core.models import gear
from division.core.models import skills


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_gear_talent_type(self):
        """Test creating a gear set."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "test123",
        )
        gear_talent_type = gear.GearTalentType.objects.create(user=user, talent_type_name="Weapon Talent")

        self.assertEquals(str(gear_talent_type), gear_talent_type.talent_type_name)

    def test_create_gear_talent(self):
        """Test creating a gear set."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "test123",
        )
        gear_talent_type = gear.GearTalentType.objects.create(user=user, talent_type_name="Weapon Talent")
        gear_talent = gear.GearTalent.objects.create(
            user=user,
            talent_type=gear_talent_type,
            talent_name="Perfect Test Talent",
            talent_description="Perfect Test Talent Description",
        )
        self.assertEquals(str(gear_talent), gear_talent.talent_name)

    def test_create_load_out_slot(self):
        """Test creating a load-out slot."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "test123",
        )
        load_out_slot = gear.LoadOutSlot.objects.create(user=user, load_out_slot_name="Primary Weapon")

        self.assertEquals(str(load_out_slot), load_out_slot.load_out_slot_name)

    def test_create_gear_attribute_type(self):
        """Test creating a gear attribute type."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "test123",
        )
        gear_attribute_type = gear.GearAttributeType.objects.create(
            user=user, gear_attribute_type_name="Weapon attribute"
        )

        self.assertEquals(str(gear_attribute_type), gear_attribute_type.gear_attribute_type_name)

    def test_create_gear_modification_type(self):
        """Test creating a gear mod type."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "test123",
        )
        gear_modification_type = gear.GearModificationType.objects.create(
            user=user, gear_modification_type_name="Weapon Modification"
        )

        self.assertEquals(str(gear_modification_type), gear_modification_type.gear_modification_type_name)

    def test_create_gear_modification(self):
        """Test creating a gear mod."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "test123",
        )
        gear_modification_type = gear.GearModificationType.objects.create(
            user=user, gear_modification_type_name="Weapon Modification"
        )

        gear_modification = gear.GearModification.objects.create(
            user=user,
            gear_modification_type=gear_modification_type,
            gear_modification_name="Weapon attribute",
            max_value=750,  # Representing 7.5% as an integer, will divide by 100 for any display,
            percent_value=True,
        )

        self.assertEquals(str(gear_modification), gear_modification.gear_modification_name)

    def test_create_gear_attribute(self):
        """Test creating a gear attribute."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "test123",
        )
        gear_attribute_type = gear.GearAttributeType.objects.create(user=user, gear_attribute_type_name="Weapon Attr")

        gear_attribute = gear.GearAttribute.objects.create(
            user=user,
            gear_attribute_type=gear_attribute_type,
            gear_attribute_name="Weapon attribute",
            max_value=750,  # Representing 7.5% as an integer, will divide by 100 for any display,
            percent_value=True,
        )

        self.assertEquals(str(gear_attribute), gear_attribute.gear_attribute_name)

    def test_create_skill(self):
        """Test creating a load-out slot."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "test123",
        )
        skill = skills.Skill.objects.create(
            user=user,
            skill_name="skill name",
        )

        self.assertEquals(str(skill), skill.skill_name)

    def test_create_skill_slot(self):
        """Test creating a load-out slot."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "test123",
        )
        skill = skills.Skill.objects.create(
            user=user,
            skill_name="skill name",
        )

        skill_slot = skills.SkillSlot.objects.create(user=user, skill=skill, skill_slot_name="skill_slot_name")

        self.assertEquals(str(skill_slot), skill_slot.skill_slot_name)

    def test_create_skill_slot_modification_type(self):
        """Test creating a skill slot modification type."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "test123",
        )
        skill_slot_modification_type = skills.SkillSlotModificationType.objects.create(
            user=user,
            skill_slot_modification_type_name="skill slot attr type",
            max_value=750,  # Representing 7.5% as an integer, will divide by 100 for any display,
            percent_value=True,
        )

        self.assertEquals(
            str(skill_slot_modification_type), skill_slot_modification_type.skill_slot_modification_type_name
        )

    def test_create_skill_slot_modification(self):
        """Test creating a skill slot modification type."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "test123",
        )
        skill = skills.Skill.objects.create(
            user=user,
            skill_name="skill name",
        )

        skill_slot = skills.SkillSlot.objects.create(user=user, skill=skill, skill_slot_name="skill_slot_name")

        skill_slot_modification_type = skills.SkillSlotModificationType.objects.create(
            user=user,
            skill_slot_modification_type_name="skill slot attr type",
            max_value=750,  # Representing 7.5% as an integer, will divide by 100 for any display,
            percent_value=True,
        )

        skill_modification = skills.SkillSlotModification.objects.create(
            user=user,
            skill_slot=skill_slot,
            skill_slot_modification_type=skill_slot_modification_type,
        )

        skill_mod = skills.SkillSlotModification.objects.get(pk=1)
        self.assertEquals(
            skill_mod.skill_slot_modification_type.skill_slot_modification_type_name,
            skill_slot_modification_type.skill_slot_modification_type_name,
        )
