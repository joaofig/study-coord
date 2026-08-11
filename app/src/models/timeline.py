
from src.dtos.milestone import Milestone
from src.models.adverse_event import AdverseEventModel
from src.models.patient import PatientModel
from src.models.protocol import ProtocolModel
from src.models.study import StudyModel
from src.models.visit import VisitModel


class TimelineModel:
    def __init__(self):
        self.milestones = []

    async def _add_study(self, study_id: int):
        model = StudyModel()
        study = await model.load(study_id)
        if study:
            ms = Milestone(
                event_title=f"Study: {study.name} started",
                event_date=study.start_date,
                event_icon="start",
                description=study.comments or "",
                color="green"
            )
            self.milestones.append(ms.to_dict())

            if study.end_date:
                ms = Milestone(
                    event_title=f"Study: {study.name} ended",
                    event_date=study.end_date,
                    event_icon="stop_circle",
                    description=study.comments or "",
                    color="blue"
                )
                self.milestones.insert(0, ms.to_dict())

    async def _add_patients(self, study_id: int):
        model = PatientModel()
        patients = await model.list(study_id)
        for patient in patients:
            ms = Milestone(
                event_title=f"Patient {patient.number} started",
                event_date=patient.start_date,
                event_icon="user_plus",
                description=patient.comments or "",
                color="orange"
            )
            self.milestones.append(ms.to_dict())

            if patient.exit_date:
                ms = Milestone(
                    event_title=f"Patient {patient.number} left the study",
                    event_date=patient.exit_date,
                    event_icon="user_minus",
                    description=patient.comments or "",
                    color="red"
                )
                self.milestones.append(ms.to_dict())

    async def _add_visits(self, study_id: int):
        # Placeholder for adding visits to the timeline
        model = VisitModel()
        visits = await model.list(study_id)
        for visit in visits:
            ms = Milestone(
                event_title=f"Visit: {visit.visit_id} for Patient: {visit.patient_id}",
                event_date=visit.visit_date,
                event_icon="calendar_check",
                description=visit.comments or "",
                color="purple"
            )
            self.milestones.append(ms.to_dict())

    async def _add_protocol_violations(self, study_id: int):
        # Placeholder for adding protocol violations to the timeline
        model = ProtocolModel()
        patient_model = PatientModel()
        violations = await model.list(study_id)
        for violation in violations:
            patient = await patient_model.load(violation.patient_id)
            ms = Milestone(
                event_title=f"Protocol Violation for Patient: {patient.name}",
                event_date=violation.event_date,
                event_icon="alert_circle",
                description=violation.description or "",
                color="red"
            )
            self.milestones.append(ms.to_dict())

    async def _add_adverse_events(self, study_id: int):
        # Placeholder for adding adverse events to the timeline
        model = AdverseEventModel()
        patient_model = PatientModel()
        patients = await patient_model.list(study_id)

        for patient in patients:
            events = await model.list(study_id, patient_id=patient.patient_id)
            for event in events:
                ms = Milestone(
                    event_title=f"Adverse Event for Patient: {patient.name}",
                    event_date=event.event_date,
                    event_icon="alert_octagon",
                    description=event.description or "",
                    color="yellow"
                )
                self.milestones.append(ms.to_dict())

    async def load(self, study_id: int) -> list:
        self.milestones = []
        await self._add_patients(study_id)
        await self._add_visits(study_id)
        await self._add_protocol_violations(study_id)
        await self._add_adverse_events(study_id)
        self.milestones.sort(key=lambda x: x["subtitle"], reverse=True)
        await self._add_study(study_id)
        return self.milestones
