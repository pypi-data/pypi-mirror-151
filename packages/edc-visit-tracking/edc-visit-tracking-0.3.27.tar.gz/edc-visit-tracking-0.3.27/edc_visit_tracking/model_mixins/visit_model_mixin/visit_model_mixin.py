from typing import Any, Optional

from django.db import models
from django.db.models.deletion import PROTECT
from edc_appointment.constants import COMPLETE_APPT, IN_PROGRESS_APPT, MISSED_APPT
from edc_constants.constants import COMPLETE, NO, YES
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_visit_schedule.model_mixins import VisitScheduleModelMixin

from edc_visit_tracking.stubs import SubjectVisitModelStub

from ...constants import MISSED_VISIT, NO_FOLLOW_UP_REASONS
from ...managers import VisitModelManager
from ...reason_updater import SubjectVisitReasonUpdater
from ..previous_visit_model_mixin import PreviousVisitModelMixin
from .visit_model_fields_mixin import VisitModelFieldsMixin


class SubjectVisitMissedError(Exception):
    pass


class VisitModelMixin(
    VisitModelFieldsMixin,
    VisitScheduleModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
    PreviousVisitModelMixin,
    models.Model,
):

    """
    For example:

        class SubjectVisit(VisitModelMixin, CreatesMetadataModelMixin,
                           RequiresConsentModelMixin, BaseUuidModel):

            class Meta(VisitModelMixin.Meta):
                app_label = 'my_app'
    """

    appointment = models.OneToOneField("edc_appointment.appointment", on_delete=PROTECT)

    objects = VisitModelManager()

    def __str__(self) -> str:
        return f"{self.subject_identifier} {self.visit_code}.{self.visit_code_sequence}"

    def save(self: Any, *args, update_fields: Optional[list] = None, **kwargs):
        self.update_document_status_on_save(update_fields)
        self.subject_identifier = self.appointment.subject_identifier
        self.visit_schedule_name = self.appointment.visit_schedule_name
        self.schedule_name = self.appointment.schedule_name
        self.visit_code = self.appointment.visit_code
        self.visit_code_sequence = self.appointment.visit_code_sequence
        self.require_crfs = NO if self.reason == MISSED_VISIT else YES
        if self.appointment.appt_timing == MISSED_APPT and self.reason != MISSED_VISIT:
            reason_updater = SubjectVisitReasonUpdater(appointment=self.appointment)
            reason_updater.update_or_raise()
        super().save(*args, **kwargs)  # type:ignore

    def natural_key(self) -> tuple:
        return (
            self.subject_identifier,
            self.visit_schedule_name,
            self.schedule_name,
            self.visit_code,
            self.visit_code_sequence,
        )

    natural_key.dependencies = ["edc_appointment.appointment"]  # type:ignore

    @property
    def timepoint(self: SubjectVisitModelStub) -> int:
        return self.appointment.timepoint

    @staticmethod
    def get_visit_reason_no_follow_up_choices() -> dict:
        """Returns the visit reasons that do not imply any
        data collection; that is, the subject is not available.
        """
        dct = {}
        for item in NO_FOLLOW_UP_REASONS:
            dct.update({item: item})
        return dct

    def check_appointment_in_progress(self: SubjectVisitModelStub) -> None:
        if self.reason in self.get_visit_reason_no_follow_up_choices():
            if self.appointment.appt_status != COMPLETE_APPT:
                self.appointment.appt_status = COMPLETE_APPT
                self.appointment.save()
        else:
            if self.appointment.appt_status != IN_PROGRESS_APPT:
                self.appointment.appt_status = IN_PROGRESS_APPT
                self.appointment.save()

    def update_document_status_on_save(self, update_fields: Optional[list] = None) -> None:
        """Updates `document_status` as complete unless field is listed
        in update_fields.

        Used when this instance (subject_visit) needs to be updated.
        For example, after being auto-created and before moving on to CRFs.

        See also: edc_subject_dashboard
        """
        if "document_status" not in (update_fields or []):
            self.document_status = COMPLETE

    class Meta:
        abstract = True
        unique_together = (
            (
                "subject_identifier",
                "visit_schedule_name",
                "schedule_name",
                "visit_code",
                "visit_code_sequence",
            ),
            (
                "subject_identifier",
                "visit_schedule_name",
                "schedule_name",
                "report_datetime",  # implies one visit per day!
            ),
        )
        ordering = (
            "subject_identifier",
            "visit_schedule_name",
            "schedule_name",
            "visit_code",
            "visit_code_sequence",
            "report_datetime",
        )

        indexes = [
            models.Index(
                fields=[
                    "subject_identifier",
                    "visit_schedule_name",
                    "schedule_name",
                    "visit_code",
                    "visit_code_sequence",
                    "report_datetime",
                ]
            )
        ]
