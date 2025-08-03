from dataclasses import dataclass, asdict
import uuid
from typing import List, Tuple

@dataclass
class BoxAnnotation:
    id: str
    image_path: str
    x1: int
    y1: int
    x2: int
    y2: int
    label: str = "default"
    type: str = "box"

    @staticmethod
    def create(image_path: str, x1: int, y1: int, x2: int, y2: int, label: str="default"):
        return BoxAnnotation(
            id=str(uuid.uuid4()),
            image_path=image_path,
            x1=x1, y1=y1,
            x2=x2, y2=y2,
            label=label
        )

    def to_dict(self) -> dict:
        d = asdict(self)
        d["type"] = "box"
        return d

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            id=d["id"],
            image_path=d["image_path"],
            x1=d["x1"], y1=d["y1"],
            x2=d["x2"], y2=d["y2"],
            label=d.get("label", "default")
        )

@dataclass
class PolygonAnnotation:
    id: str
    image_path: str
    points: List[Tuple[int,int]]
    label: str = "default"
    type: str = "polygon"

    @staticmethod
    def create(image_path: str, points: List[Tuple[int,int]], label: str="default"):
        return PolygonAnnotation(
            id=str(uuid.uuid4()),
            image_path=image_path,
            points=points.copy(),
            label=label
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "image_path": self.image_path,
            "points": self.points,
            "label": self.label,
            "type": "polygon"
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            id=d["id"],
            image_path=d["image_path"],
            points=[tuple(pt) for pt in d["points"]],
            label=d.get("label", "default")
        )

