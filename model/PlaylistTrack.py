from dataclasses import dataclass

@dataclass
class PlaylistTrack():
    PlaylistId:int
    TrackId:int

    def __hash__(self):
        return hash(str(self.PlaylistId)+str(self.TrackId))
