from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class PhotoFrame:
    width: int
    height: int

    @property
    def ratio(self) -> float:
        return self.width / self.height
