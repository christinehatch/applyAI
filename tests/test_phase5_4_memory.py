import pytest


def test_proposal_before_write_creates_no_memory_item():
    """
    Invariant A: Proposal-before-write
    - proposing memory must not create a stored MemoryItem
    - only approval creates MemoryItem
    """
    from phase5.memory import (
        InMemoryMemoryStore,
        InMemoryMemoryProposalService,
        MemorySource,
        MemoryKind,
    )

    store = InMemoryMemoryStore()
    svc = InMemoryMemoryProposalService(store)

    owner_id = "user-1"
    source = MemorySource(source_type="phase3_reflection", source_id="r1", note="After Phase 3 summary")

    proposal = svc.propose(
        owner_id=owner_id,
        proposed_text="I prefer learning by building small prototypes.",
        kind=MemoryKind.PREFERENCE,
        source=source,
    )

    assert store.list(owner_id) == []

    item = svc.approve(
        owner_id=owner_id,
        proposal_id=proposal.proposal_id,
        final_text="I prefer learning by building small prototypes.",
    )

    items = store.list(owner_id)
    assert len(items) == 1
    assert items[0].id == item.id
    assert items[0].text == "I prefer learning by building small prototypes."
    assert items[0].owner_id == owner_id


def test_decline_has_no_side_effects_and_cannot_be_approved_later():
    """
    Invariant D: Decline has no side effects
    - declining creates no MemoryItem
    - declined proposals cannot later be approved
    """
    from phase5.memory import (
        InMemoryMemoryStore,
        InMemoryMemoryProposalService,
        MemorySource,
        MemoryKind,
    )

    store = InMemoryMemoryStore()
    svc = InMemoryMemoryProposalService(store)

    owner_id = "user-1"
    source = MemorySource(source_type="phase3_reflection", source_id="r1", note="After Phase 3 summary")

    proposal = svc.propose(
        owner_id=owner_id,
        proposed_text="I want to remember that I enjoy ambiguity.",
        kind=MemoryKind.SELF_OBSERVATION,
        source=source,
    )

    svc.decline(owner_id=owner_id, proposal_id=proposal.proposal_id)

    assert store.list(owner_id) == []

    with pytest.raises(Exception):
        svc.approve(
            owner_id=owner_id,
            proposal_id=proposal.proposal_id,
            final_text="I want to remember that I enjoy ambiguity.",
        )


def test_delete_means_non_use_and_is_excluded_from_selection_context():
    """
    Invariant E + F:
    - deleted memory items are excluded from ledger list
    - deleted memory IDs are not resolvable into selection context
    """
    from phase5.memory import (
        InMemoryMemoryStore,
        InMemoryMemoryProposalService,
        MemorySelectionContextBuilder,
        MemorySource,
        MemoryKind,
    )

    store = InMemoryMemoryStore()
    svc = InMemoryMemoryProposalService(store)
    selector = MemorySelectionContextBuilder(store)

    owner_id = "user-1"
    source = MemorySource(source_type="phase5_3_interpretation", source_id="i1", note="After resonance: resonates")

    proposal = svc.propose(
        owner_id=owner_id,
        proposed_text="I want to keep projects small and iterative.",
        kind=MemoryKind.CONSTRAINT,
        source=source,
    )
    item = svc.approve(
        owner_id=owner_id,
        proposal_id=proposal.proposal_id,
        final_text="I want to keep projects small and iterative.",
    )

    assert len(store.list(owner_id)) == 1

    store.delete(owner_id=owner_id, memory_id=item.id)

    assert store.list(owner_id) == []

    ctx = selector.build(owner_id=owner_id, selected_memory_ids=[item.id])
    assert ctx.selected_memory_ids == [item.id]
    assert ctx.resolved_texts == []  # deleted items must not resolve


def test_validator_blocks_identity_clinical_and_authoritative_language():
    """
    Validator enforcement (Invariant C):
    - identity-locking phrases are blocked
    - clinical/diagnostic terms are blocked
    - authoritative/prescriptive language is blocked
    """
    from phase5.memory import (
        InMemoryMemoryStore,
        InMemoryMemoryProposalService,
        MemorySource,
        MemoryKind,
        MemoryValidationError,
    )

    store = InMemoryMemoryStore()
    svc = InMemoryMemoryProposalService(store)

    owner_id = "user-1"
    source = MemorySource(source_type="phase3_reflection", source_id="r1", note="After Phase 3 summary")

    proposal = svc.propose(
        owner_id=owner_id,
        proposed_text="placeholder",
        kind=MemoryKind.SELF_OBSERVATION,
        source=source,
    )

    bad_texts = [
        "You are a person who always overthinks.",  # identity-locking (matches 'you are a ')
        "This is a diagnosis of ADHD.",             # clinical/diagnostic
        "You should definitely do this next.",      # authoritative ('you should')
    ]

    for bad in bad_texts:
        with pytest.raises(MemoryValidationError):
            svc.approve(
                owner_id=owner_id,
                proposal_id=proposal.proposal_id,
                final_text=bad,
            )

    # Ensure validator failure never writes memory
    assert store.list(owner_id) == []


def test_empty_selection_does_not_auto_consume_memory_and_has_no_attribution():
    """
    No auto-consumption (Invariant F):
    - even if memory exists, passing empty selected IDs returns empty resolved_texts
    - attribution should only appear when memory is actually used
    """
    from phase5.memory import (
        InMemoryMemoryStore,
        InMemoryMemoryProposalService,
        MemorySelectionContextBuilder,
        MemorySource,
        MemoryKind,
    )

    store = InMemoryMemoryStore()
    svc = InMemoryMemoryProposalService(store)
    selector = MemorySelectionContextBuilder(store)

    owner_id = "user-1"
    source = MemorySource(source_type="phase5_3_interpretation", source_id="i1", note="After resonance: resonates")

    proposal = svc.propose(
        owner_id=owner_id,
        proposed_text="I prefer learning by building small prototypes.",
        kind=MemoryKind.PREFERENCE,
        source=source,
    )
    svc.approve(
        owner_id=owner_id,
        proposal_id=proposal.proposal_id,
        final_text="I prefer learning by building small prototypes.",
    )

    assert len(store.list(owner_id)) == 1  # memory exists

    ctx = selector.build(owner_id=owner_id, selected_memory_ids=[])

    assert ctx.selected_memory_ids == []
    assert ctx.resolved_texts == []
    assert ctx.attribution_line == ""  # no attribution if nothing was used
