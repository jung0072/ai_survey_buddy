import dspy
import dsp

from app.dspy.signatures.signatures import AssessIntentClassification


# Validation logic: check that the predicted answer is correct.
# Also check that the retrieved context does actually contain that answer.
def validate_context_and_answer(example, pred, trace=None):
    answer_EM = dspy.evaluate.answer_exact_match(example, pred)
    answer_PM = dspy.evaluate.answer_passage_match(example, pred)
    return answer_EM and answer_PM


def validate_intent_classifcation(example, pred, trace=None):
    anthropic_haiku = dsp.Claude(model="claude-3-haiku-20240307")

    with dspy.context(lm=anthropic_haiku):
        pred = dspy.Predict(AssessIntentClassification)(
            gold_intent=example["intent"],
            predicted_intent=pred.intent,
        )

    result = True if pred.is_correct.lower().split(" ")[0].strip() == "true" else False

    return result
