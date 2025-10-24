# tests/test_supervisor.py

import pytest
from brains.supervisor import Supervisor

@pytest.fixture
def supervisor():
    return Supervisor()

def test_route_to_emergency(supervisor):
    query = "Qué hago en un paro cardíaco"
    assert 'c1_emergency' in supervisor.route(query)

def test_route_to_non_emergency(supervisor):
    query = "Me corté con un papel"
    assert 'c2_non_emergency' in supervisor.route(query)

def test_route_to_psychological(supervisor):
    query = "Mi amigo está teniendo un ataque de pánico"
    assert 'c3_psychological' in supervisor.route(query)

def test_route_to_resources(supervisor):
    query = "Cuál es el hospital más cercano"
    assert 'c5_resources' in supervisor.route(query)

def test_route_to_default(supervisor):
    query = "dime algo"
    # Debería enrutar a no emergencia por defecto y siempre a idioma
    expected_brains = {'c2_non_emergency', 'c6_language'}
    assert set(supervisor.route(query)) == expected_brains
