from src.logging import get_logger
from typing import List, Optional

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    SentenceTransformer = None
    cosine_similarity = None


class SemanticMemory:
    def __init__(self, memory, settings):
        self.memory = memory
        self.cfg = settings
        self.semantic_model = None
        self.logger = get_logger(__name__)
        if SentenceTransformer:
            try:
                self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
                self.logger.info(
                    "SentenceTransformer model loaded for semantic search."
                )
            except Exception as e:
                self.logger.warning(
                    f"Failed to load SentenceTransformer model: {e}. "
                    "Semantic fact recall will be degraded."
                )
                self.semantic_model = None

    def embed_fact(self, fact_text: str) -> Optional[List[float]]:
        if self.semantic_model:
            return self.semantic_model.encode(fact_text).tolist()
        return None

    def recall_facts(self, topic: Optional[str] = None) -> str:
        facts_dict = self.memory.data.get("learned_facts", {})
        if not facts_dict:
            return "I haven't learned any specific facts yet."
        all_fact_texts = [
            fact_data["text"]
            for fact_data in facts_dict.values()
            if fact_data.get("text")
        ]
        if not all_fact_texts:
            return "I haven't learned any specific facts yet."
        if topic and isinstance(topic, str) and topic.strip():
            topic_lower = topic.lower()
            relevant_facts = []
            if self.semantic_model and cosine_similarity:
                topic_embedding = self.semantic_model.encode(topic_lower)
                facts_with_embeddings = {
                    k: v for k, v in facts_dict.items() if v.get("embedding")
                }
                if facts_with_embeddings:
                    fact_embeddings = [
                        fact_data["embedding"]
                        for fact_data in facts_with_embeddings.values()
                    ]
                    fact_texts_with_embeddings = [
                        fact_data["text"]
                        for fact_data in facts_with_embeddings.values()
                    ]
                    similarities = cosine_similarity(
                        topic_embedding.reshape(1, -1), fact_embeddings
                    )[0]
                    sorted_indices = similarities.argsort()[::-1]
                    for i in sorted_indices:
                        if similarities[i] > 0.5:
                            relevant_facts.append(fact_texts_with_embeddings[i])
                        if len(relevant_facts) >= 3:
                            break
            else:
                relevant_facts = [
                    text for text in all_fact_texts if topic_lower in text.lower()
                ]
            if relevant_facts:
                return (
                    "Here are some facts I remember related to that: \n- "
                    + "\n- ".join(relevant_facts)
                )
            return (
                "I don't have any specific facts about '"
                + str(topic)
                + "'"
            )
        return (
            "Here are some facts I remember: \n- "
            + "\n- ".join(all_fact_texts[:1])
            + ("\n- " + "\n- ".join(all_fact_texts[1:]) if len(all_fact_texts) > 1 else "")
        ) 