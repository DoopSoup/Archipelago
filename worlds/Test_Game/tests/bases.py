from test.bases import WorldTestBase

from ..world import APTestGame_World

class APTestGame_Test(WorldTestBase):
    game = "APTestGame"
    world: APTestGame_World # type: ignore