"""Tests for tactic_engine.py"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'engine'))

from tactic_engine import TacticEngine


class TestTacticEngine:
    """Test suite for TacticEngine."""

    @pytest.fixture
    def persona(self):
        return {
            'name': 'carmen',
            'tactics': [
                'buscar_papeles', 'consulta_hijo', 'problema_auditivo',
                'duda_seguridad', 'peticion_identificacion', 'burocracia_ligera'
            ],
            'silence_response_ms': 4000,
            'max_silence_loops': 5
        }

    @pytest.fixture
    def engine(self, persona):
        return TacticEngine(persona)

    def test_engine_initialization(self, engine):
        """Test engine initializes with correct attributes."""
        assert engine.persona['name'] == 'carmen'
        assert len(engine.tactics) == 6
        assert engine.last_tactic is None

    def test_select_tactic_random(self, engine):
        """Test random tactic selection after turns."""
        engine.turns_since_tactic = 10
        tactic = engine.select_tactic("random text", 10, [])
        assert tactic is not None
        assert "[APLICAR TÁCTICA:" in tactic

    def test_select_tactic_trigger_contrato(self, engine):
        """Test triggered tactic for 'contrato'."""
        tactic = engine.select_tactic(
            "quiero que firmes el contrato ahora",
            1,
            []
        )
        assert tactic is not None
        assert "buscar_papeles" in tactic or "burocracia_ligera" in tactic

    def test_select_tactic_trigger_banco(self, engine):
        """Test triggered tactic for 'banco'."""
        tactic = engine.select_tactic(
            "esto es del banco oficial",
            1,
            []
        )
        assert tactic is not None
        assert "duda_seguridad" in tactic

    def test_pressure_situation(self, engine):
        """Test response to pressure situation."""
        tactic = engine.select_tactic(
            "tienes que hacerlo ahora mismo urgentemente",
            1,
            []
        )
        assert tactic is not None  # Should use defensive tactic

    def test_no_repeat_same_tactic(self, engine):
        """Test that same tactic doesn't repeat consecutively."""
        engine.last_tactic = "consulta_hijo"
        engine.tactics = ["consulta_hijo", "buscar_papeles", "problema_auditivo"]
        tactic = engine._select_random_tactic()
        assert tactic != "consulta_hijo" or len(engine.tactics) == 1

    def test_silence_response(self, engine):
        """Test silence response generation."""
        engine.silence_count = 1
        response = engine.get_silence_response()
        assert response != ""
        assert "¿" in response or "Ay" in response

    def test_silence_max_loops(self, engine):
        """Test max silence loops triggers warning."""
        engine.silence_count = 10
        response = engine.get_silence_response()
        assert "[POSIBLE COLGAR]" in response

    def test_reset_silence_count(self, engine):
        """Test silence count reset."""
        engine.silence_count = 5
        engine.reset_silence_count()
        assert engine.silence_count == 0

    def test_tactics_summary(self, engine):
        """Test tactics summary after use."""
        engine.tactic_history = ['buscar_papeles', 'consulta_hijo', 'buscar_papeles']
        summary = engine.get_tactics_summary()
        assert summary['buscar_papeles'] == 2
        assert summary['consulta_hijo'] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])