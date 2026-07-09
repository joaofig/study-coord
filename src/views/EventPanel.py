from nicegui import ui

from viewmodels.ViewModel import ViewModel
from viewmodels.EventViewModel import EventViewModel
from views.EventGrid import EventGrid
from views.View import View
from views.dialogs.DeleteWarningDialog import DeleteWarningDialog
from views.dialogs.EventDialog import EventDialog


class EventPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study_id = 0
        self.patient_id = 0
        self.subscribe(channel="study",
                       message="selected",
                       handler=self._study_selected)
        self.subscribe(channel="patient",
                       message="selected",
                       handler=self._patient_selected)

    async def _study_selected(self, **kwargs):
        if "study_id" in kwargs:
            self.study_id = kwargs["study_id"]
            self.patient_id = 0

    async def _patient_selected(self, **kwargs):
        if "patient_id" in kwargs:
            self.patient_id = kwargs["patient_id"]
        if "study_id" in kwargs:
            self.study_id = kwargs["study_id"]

    async def _new_event_dialog(self):
        event_vm = EventViewModel()
        await event_vm.load_patients(self.study_id)
        event_vm.patient_id = self.patient_id
        await event_vm.call("load_patient", patient_id=self.patient_id)
        dialog = EventDialog(event_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load", study_id=self.study_id, patient_id=self.patient_id)
            await self.broadcast("study_list", "load")

    async def _on_delete_event(self):
        dialog = DeleteWarningDialog("Are you sure you want to delete this event?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            event_id = self.vm.get("event_id")
            if event_id:
                await self.vm.call("delete", event_id=event_id)
            await self.broadcast("study_list", "load")

    def show(self):
        with ui.row().classes("w-full h-full"):

            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add", on_click=self._new_event_dialog) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Add Event")

                with ui.button(icon="delete", on_click=self._on_delete_event) \
                        .classes("text-xs") \
                        .bind_enabled(self.vm, "event_id") \
                        .props("color=red padding=xs"):
                    ui.tooltip("Delete Event")

                with ui.button(icon="table_view") \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                EventGrid(self.vm).show()
