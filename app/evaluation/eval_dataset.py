from typing import List, Dict

EvaluationSample = Dict[str, object]

EVAL_DATASET: List[EvaluationSample] = [
    {
        "id": "return_policy_1",
        "question": "What is the return policy?",
        "expected_facts": [
            "30 days",
            "good condition",
            "original packaging",
            "refund within 5 business days"
        ],
        "expected_doc_ids": [
            "return_policy"
        ],
    },
    {
        "id": "return_policy_2",
        "question": "How long does it take to get a refund?",
        "expected_facts": [
            "5 business days"
        ],
        "expected_doc_ids": [
            "return_policy"
        ],
    },
    {
        "id": "return_policy_3",
        "question": "Which items cannot be returned?",
        "expected_facts": [
            "personal care products",
            "final sale",
            "digital products",
            "custom-made"
        ],
        "expected_doc_ids": [
            "return_policy"
        ],
    },
    {
        "id": "shipping_policy_1",
        "question": "What are the shipping options?",
        "expected_facts": [
            "free standard shipping",
            "orders above $50",
            "express shipping",
            "1-2 days"
        ],
        "expected_doc_ids": [
            "shipping_policy"
        ],
    },
    {
        "id": "shipping_policy_2",
        "question": "How long does order processing take?",
        "expected_facts": [
            "1-2 business days",
            "up to 3 days during peak"
        ],
        "expected_doc_ids": [
            "shipping_policy"
        ],
    },
]
