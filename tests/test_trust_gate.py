"""test_trust_gate.py -- the optional lead-handoff receipt mints + verifies (or degrades cleanly).

Covers both paths: when openagentontology is installed (real Ed25519 + PQ receipt, verifies,
tamper caught) and when it is not (explicit unsigned stub, never a fake signature). The crypto
itself is tested in the openagentontology package; this pins the SalesGPT integration contract.
"""
from __future__ import annotations

import copy

import pytest

from salesgpt.trust_gate import (
    build_handoff_manifest,
    mint_lead_handoff_receipt,
    verify_receipt,
    _oao,
)

LEAD = {
    "lead_id": "acme-123",
    "bant": {"budget": True, "authority": True, "need": True, "timing": "Q3"},
    "meddic_score": 0.72,
    "qualified_by": "salesgpt",
    "conversation": "discovery call notes ...",
}

_HAS_OAO = _oao() is not None


def test_manifest_requires_lead_id():
    with pytest.raises(ValueError):
        build_handoff_manifest({"bant": {}})


def test_manifest_hashes_conversation_not_stores_it():
    m = build_handoff_manifest(LEAD)
    assert m["conversation_hash"].startswith("sha256:")
    assert "discovery call notes" not in str(m)  # raw conversation is not carried in clear


def test_unsigned_stub_when_oao_absent(monkeypatch):
    # force the no-package path and confirm it never fakes a signature
    monkeypatch.setattr("salesgpt.trust_gate._oao", lambda: None)
    r = mint_lead_handoff_receipt(LEAD)
    assert r["signed"] is False
    assert "openagentontology" in r["unsigned_reason"]
    assert "signature_b64" not in r


@pytest.mark.skipif(not _HAS_OAO, reason="openagentontology not installed")
def test_real_receipt_mints_and_verifies():
    r = mint_lead_handoff_receipt(LEAD)
    v = verify_receipt(r)
    assert v["ok"] is True
    assert r["evidence"]["ontology"]["lead_id"] == "acme-123"


@pytest.mark.skipif(not _HAS_OAO, reason="openagentontology not installed")
def test_tamper_breaks_verification():
    r = mint_lead_handoff_receipt(LEAD)
    tampered = copy.deepcopy(r)
    tampered["evidence"]["ontology"]["meddic_score"] = 0.99  # inflate the score after signing
    v = verify_receipt(tampered)
    assert v["ok"] is False


# ---- Quantum Hardening (H4 + H3) -- standing pol.must_do.150 pattern -----------------

@pytest.mark.skipif(not _HAS_OAO, reason="openagentontology not installed")
def test_h4_minted_receipt_carries_kid():
    import hashlib
    r = mint_lead_handoff_receipt(LEAD)
    # 128 bits of identifier -- adversarial collision resistance for offline "same notary?" use
    assert r.get("kid") and len(r["kid"]) == 32
    assert r["kid"] == hashlib.sha256(r["verify_pubkey_b64"].encode("ascii")).hexdigest()[:32]


@pytest.mark.skipif(not _HAS_OAO, reason="openagentontology not installed")
def test_h3_pq_required_rejects_pq_stripped_receipt():
    r = mint_lead_handoff_receipt(LEAD)
    stripped = copy.deepcopy(r)
    for k in ("ml_dsa_signature_b64", "ml_dsa_public_key_b64",
              "slh_dsa_signature_b64", "slh_dsa_public_key_b64"):
        stripped.pop(k, None)
    # default require_pq (env-driven, default True) must REJECT the stripped receipt
    strict = verify_receipt(stripped)
    assert strict["ok"] is False
    assert "PQ-required" in strict["reason"]
    # explicit opt-out preserves the legacy Ed25519 path for archival receipts
    legacy = verify_receipt(stripped, require_pq=False)
    assert legacy["ok"] is True
