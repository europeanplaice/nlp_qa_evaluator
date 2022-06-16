from evaluator import evaluate, generate_masked_sentences
from evaluator import calc_similarity_of_masked_sentences_emb, serialize


def main():
    qas = []
    with open("config.tsv", "r", encoding="utf-8") as f:
        qas = f.readlines()[1:]
    for i, qa in enumerate(qas):
        splitted: list[str] = qa.split("\t")
        answer_correctness, correct_answer_emb = evaluate(
            correct_answer=splitted[1], answer_from_student=splitted[2]
        )
        masked_sentences_emb, new_tokenized_list = generate_masked_sentences(
            splitted[2]
        )
        token_importances = calc_similarity_of_masked_sentences_emb(
            correct_answer_emb=correct_answer_emb,
            masked_sentences_emb=masked_sentences_emb,
            teacher_student_similality=answer_correctness,
        )

        body = serialize(
            splitted[0],
            splitted[1],
            splitted[2],
            answer_correctness,
            new_tokenized_list,
            token_importances,
        )
        with open(f"result_{i}.txt", "w", encoding="utf-8") as f:
            f.write(body)


if __name__ == "__main__":
    main()
