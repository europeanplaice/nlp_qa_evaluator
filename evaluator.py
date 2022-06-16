import tensorflow_hub as hub
import numpy as np
import tensorflow_text
import tensorflow as tf
from transformers import AutoTokenizer
from scipy.stats import rankdata

embed = hub.load(
    "https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3"
)


def evaluate(correct_answer: str, answer_from_student: str) -> tuple[float, tf.Tensor]:
    correct_answer_emb = embed([correct_answer])
    answer_from_student_emb = embed([answer_from_student])
    similarity = np.inner(correct_answer_emb, answer_from_student_emb)
    return similarity[0][0], correct_answer_emb


def generate_masked_sentences(sentence: str) -> tuple[tf.Tensor, list[str]]:
    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

    tokenized_list: list[int] = tokenizer.tokenize(sentence)
    encoded_list: list[int] = tokenizer.convert_tokens_to_ids(tokenized_list)
    new_tokenized_list: list[str] = []
    masked_sentence_list: list[str] = []
    for i in range(len(encoded_list)):
        if i == len(encoded_list) - 3:
            break
        encoded_list_copy = encoded_list.copy()
        encoded_list_copy[i] = tokenizer.mask_token_id
        encoded_list_copy[i + 1] = tokenizer.mask_token_id
        encoded_list_copy[i + 2] = tokenizer.mask_token_id
        encoded_list_copy[i + 3] = tokenizer.mask_token_id
        masked_sentence: str = tokenizer.decode(encoded_list_copy)
        masked_sentence_list.append(masked_sentence)
        new_tokenized_list.append(tokenizer.decode(encoded_list[i: i + 4]))
    masked_sentences_emb = embed(masked_sentence_list)
    return masked_sentences_emb, new_tokenized_list


def calc_similarity_of_masked_sentences_emb(
    correct_answer_emb: tf.Tensor,
    masked_sentences_emb: tf.Tensor,
    teacher_student_similality: float,
) -> list[float]:
    token_importances: list[float] = []
    for masked_sentence_emb in masked_sentences_emb:
        masked_similarity: float = np.inner(
            correct_answer_emb, [masked_sentence_emb])[0][0]
        token_importance: float = teacher_student_similality - masked_similarity
        token_importances.append(token_importance)
    return token_importances


def serialize(
    question: str,
    correct_answer: str,
    students_answer: str,
    answer_correctness: float,
    tokenized_list: list[str],
    token_importances: list[float],
) -> str:
    rank = len(token_importances) - rankdata(token_importances).astype(int) + 1
    body = f"question: {question}\ncorrect_answer: {correct_answer}\nstudents_answer: {students_answer}\n"
    body += f"correctness: {answer_correctness}\n"
    for token, token_importance, r in zip(tokenized_list, token_importances, rank):
        body += f"rank: {int(r)} -> {token_importance}, {token}\n"
    return body
