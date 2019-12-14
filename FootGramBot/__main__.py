import importlib

from FootGramBot import updater
from FootGramBot.modules import ALL_MODULES

IMPORTED = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("FootGramBot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__
    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")


def main():
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
