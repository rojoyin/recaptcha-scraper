from typing import Protocol


class ChallengeSolver(Protocol):
    async def solve(self, url):
        pass
