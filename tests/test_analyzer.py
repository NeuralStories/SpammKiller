import pytest
import sys
import os
import asyncio

# Append engine to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'engine'))

from post_call_analyzer import PostCallAnalyzer

@pytest.mark.asyncio
async def test_analyzer_classification():
    analyzer = PostCallAnalyzer()
    
    # Test text
    transcript = [
        {"speaker": "spammer", "text": "Hola le llamo de su distribuidora de luz, tiene un problema en la factura."}
    ]
    
    result = await analyzer.analyze("test_id", transcript, "+34912345678", 60)
    
    assert result["scam_type"] == "energia"
    assert result["scam_confidence"] > 0.0

def test_data_redaction():
    analyzer = PostCallAnalyzer()
    
    text_with_dni = "Mi DNI es 12345678X y mi teléfono es +34912345678."
    redacted = analyzer.redact_sensitive_data(text_with_dni)
    
    assert "12345678X" not in redacted
    assert "[DNI_REDACTADO]" in redacted
    assert "+34912345678" not in redacted
    assert "[TELÉFONO_REDACTADO]" in redacted