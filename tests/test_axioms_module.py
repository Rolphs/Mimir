import ecosistema_ia.axioms as axioms


def test_axioms_count():
    assert len(axioms.AXIOMS) == 10
    assert "Axiom I" in axioms.AXIOMS
    assert "Axiom X" in axioms.AXIOMS


def test_modules_import_axioms():
    import ecosistema_ia.config as cfg
    import ecosistema_ia.entorno.territorio as territorio

    assert "AXIOMS" in cfg.__dict__
    assert "AXIOMS" in territorio.__dict__


