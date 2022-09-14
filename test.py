from radon.complexity import cc_rank, SCORE
from radon.cli import Config
from radon.cli.harvest import CCHarvester

paths = ["."]

config = Config(
    exclude=None,
    ignore=None,
    order=SCORE,
    no_assert=False,
    show_closures=False,
    show_complexity=True,
    min='A',
    max='F',
)

harv = CCHarvester(paths, config)
results = harv._to_dicts()

breakpoint()



