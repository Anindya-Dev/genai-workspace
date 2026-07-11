"""
Knowledge Graph Extractor.

Responsible for converting UnifiedDocument objects
into graph entities and relationships using an LLM.
"""

from backend.normalizer import UnifiedDocument


class GraphExtractor:
    """
    Extracts graph triples from normalized documents.
    """

    def __init__(self):
        pass

    def extract(self, document: UnifiedDocument):
        """
        Extract entities and relationships
        from a UnifiedDocument.

        Returns:
            Graph triples (to be implemented).
        """
        pass