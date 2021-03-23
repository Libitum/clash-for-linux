import gettext

_t = gettext.translation("clashtk", fallback=True)
_ = _t.gettext


def change_language(lang=None):
    _t.install()
