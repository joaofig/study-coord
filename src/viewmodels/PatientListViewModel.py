from models.patient import PatientList
from viewmodels.ViewModel import ViewModel


class PatientListViewModel(ViewModel):
    patients: list[dict] = []

    def __post_init__(self):
        super().__init__()

    async def handle_command(self, msg: str, data: Any = None):
        match msg:
            case "load_patients":
                study_id = int(data)
                await PatientList().load_from_study(study_id)
        return None

