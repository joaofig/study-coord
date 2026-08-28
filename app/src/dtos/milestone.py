from datetime import date

from pydantic import BaseModel


class Milestone(BaseModel):
    event_title: str  # Maps to title
    event_date: date  # Maps to subtitle
    event_icon: str
    description: str
    color: str

    def to_dict(self):
        return {
            "event_title": self.event_title,
            "event_date": self.event_date.strftime("%Y-%m-%d"),
            "event_icon": self.event_icon,
            "description": self.description,
            "color": self.color,
        }
