from typing import List


def parse_args(args: List[str], sep: str = ",") -> List[str]:
    return [p.strip() for p in " ".join(args).split(sep)]
