from webster.utils import telegram_utils


def test__parse_args():
    parsed_args = ["snes classic", "snes", "nintendo"]

    args = "snes classic, snes, nintendo".split(" ")
    assert telegram_utils.parse_args(args, sep=",") == parsed_args

    args = "snes classic , snes , nintendo".split(" ")
    assert telegram_utils.parse_args(args, sep=",") == parsed_args

    args = "snes classic,snes,nintendo".split(" ")
    assert telegram_utils.parse_args(args, sep=",") == parsed_args

    args = "snes classic/snes/nintendo".split(" ")
    assert telegram_utils.parse_args(args, sep="/") == parsed_args

    parsed_args = ["snes classic", "", "nintendo"]
    args = "snes classic,,nintendo".split(" ")
    assert telegram_utils.parse_args(args, sep=",") == parsed_args

    parsed_args = ["snes classic", "snes", ""]
    args = "snes classic,snes,".split(" ")
    assert telegram_utils.parse_args(args, sep=",") == parsed_args
