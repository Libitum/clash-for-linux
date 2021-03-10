import gettext

_t = gettext.translation("clashtk", fallback=True)


def change_language(lang=None):
    _t.install()
