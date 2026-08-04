from datetime import date

from pydantic import BaseModel


class Milestone(BaseModel):
    event_title: str        # Maps to title
    event_date: date        # Maps to subtitle
    event_icon: str
    description: str
    color: str

    def to_dict(self):
        return {
            "title": self.event_title,
            "subtitle": self.event_date.strftime("%Y-%m-%d"),
            "icon": self.event_icon,
            "description": self.description,
            "color": self.color
        }
