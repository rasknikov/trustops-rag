from trustops_rag.domain.context_building import BuiltContext, ContextItem
from trustops_rag.domain.reliability import ReliabilityInput, assess_reliability


def test_assess_reliability_returns_supported_high_confidence() -> None:
    built_context = BuiltContext(
        question="vacation policy",
        items=[
            ContextItem(
                chunk_id="chunk-1",
                document_version_id="version-1",
                content="The vacation policy allows employees to request annual leave.",
                position=1,
                citation_label="[1]",
            ),
            ContextItem(
                chunk_id="chunk-2",
                document_version_id="version-1",
                content="Managers must approve annual leave requests in the HR system.",
                position=2,
                citation_label="[2]",
            ),
        ],
        rendered_context="[1] The vacation policy allows employees to request annual leave.\n\n[2] Managers must approve annual leave requests in the HR system.",
    )
    reliability_input = ReliabilityInput(
        question="What does the vacation policy allow?",
        answer_text="The vacation policy allows employees to request annual leave.",
        built_context=built_context,
    )

    assessment = assess_reliability(reliability_input)

    assert assessment.supported is True
    assert assessment.confidence_level == "high"
    assert assessment.contradiction_detected is False
    assert assessment.reliability_reason == "supported_by_context"


def test_assess_reliability_detects_contradiction() -> None:
    built_context = BuiltContext(
        question="device access",
        items=[
            ContextItem(
                chunk_id="chunk-1",
                document_version_id="version-1",
                content="Personal devices are not allowed on the production network.",
                position=1,
                citation_label="[1]",
            )
        ],
        rendered_context="[1] Personal devices are not allowed on the production network.",
    )
    reliability_input = ReliabilityInput(
        question="Are personal devices allowed?",
        answer_text="Personal devices are allowed on the production network.",
        built_context=built_context,
    )

    assessment = assess_reliability(reliability_input)

    assert assessment.supported is False
    assert assessment.contradiction_detected is True
    assert assessment.confidence_level == "low"
    assert assessment.reliability_reason == "contradictory_context"
