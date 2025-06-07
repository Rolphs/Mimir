import pytest

import ecosistema_ia.config as cfg


def test_config_no_unused_constants():
    assert not hasattr(cfg, "CICLOS_INICIALES")
    assert not hasattr(cfg, "NUM_AGENTES_INICIALES")
