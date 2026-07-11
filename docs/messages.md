
# Messages

This document contains the complete list of messages that the application sends.

| Channel | Message | Parameters | Description |
|---------|---------|------------|-------------|
| study | selected | study_id: int | A study has been selected. |
| study | study_saved | study: Study | A study has been saved. |
| study_list | load | - | Request to reload the study list. |
| patient | selected | patient_id: int | A patient has been selected. |
| patient | saved | - | A patient has been saved. |
| researcher | researcher_selected | researcher: dict, researcher_id: int | A researcher has been selected. |
| researcher_list | load | - | Request to reload the researcher list. |
| study_researcher | saved | - | A study researcher association has been saved. |
| study_researcher | deleted | - | A study researcher association has been deleted. |
| study_researcher | study_researcher_selected | study_id: int | A study researcher has been selected. |
| event | saved | - | A clinical event has been saved. |
| visit | saved | - | A study visit has been saved. |
| reports | load | - | Request to reload reports. |
| protocol_list | load | study_id: int | Request to reload the protocol deviation list for a study. |
