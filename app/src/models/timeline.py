from src.dtos.milestone import Milestone
from src.models.patient import PatientModel
from src.models.study import StudyModel
from src.tools.observability import GridList


class TimelineModel:
    def __init__(self):
        self.milestones = GridList()

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
                self.milestones.append(ms.to_dict())

    async def _add_patients(self, study_id: int):
        model = PatientModel()
        patients = await model.list(study_id)
        for patient in patients:
            ms = Milestone(
                event_title=f"Patient: {patient.name} started",
                event_date=patient.start_date,
                event_icon="user_plus",
                description=patient.comments or "",
                color="orange"
            )
            self.milestones.append(ms.to_dict())

            if patient.exit_date:
                ms = Milestone(
                    event_title=f"Patient: {patient.name} exited",
                    event_date=patient.exit_date,
                    event_icon="user_minus",
                    description=patient.comments or "",
                    color="red"
                )
                self.milestones.append(ms.to_dict())

    async def load(self, study_id: int):
        await self._add_study(study_id)
        await self._add_patients(study_id)

