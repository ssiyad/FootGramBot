from threading import Timer

from FootGramBot import FGM, COMPETITIONS


def update_matches():
    MATCH_LIST = []
    for comp in COMPETITIONS:
        _matches = FGM.matches(comp)
        if 'matches' in _matches:
            _matches = _matches['matches']
            for match in _matches:
                match['comp'] = comp
                MATCH_LIST.append(match)

    if MATCH_LIST:
        FGM.save_data(MATCH_LIST)


def timer_func():
    Timer(60.0, timer_func).start()
    update_matches()


timer_func()
