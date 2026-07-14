"""
Knowledge Graph Extractor.

Responsible for converting UnifiedDocument objects
into graph entities and relationships using an LLM.
"""

from backend.normalizer import UnifiedDocument
from backend.schema import GraphExtractionResult


class GraphExtractor:
    """
    Extracts graph triples from normalized documents.
    """

    def __init__(self):
        """
        Initialize the graph extractor.

        TODO:
        - Initialize Groq client
        - Configure LlamaIndex extraction pipeline
        """
        pass

    def extract(self, document: UnifiedDocument) -> GraphExtractionResult:
        """
        Extract graph entities and relationships
        from a normalized document.

        Returns:
            GraphExtractionResult
        """

        # TODO:
        # 1. Build prompt
        # 2. Send prompt to LLM
        # 3. Parse response
        # 4. Validate result

        return GraphExtractionResult()

    def _build_prompt(self, document: UnifiedDocument) -> str:
        """Build the prompt for the LLM."""
        raise NotImplementedError

    def _parse_response(self, response: str) -> GraphExtractionResult:
        """Convert the LLM response into graph objects."""
        raise NotImplementedError

    def _validate_result(
        self,
        result: GraphExtractionResult
    ) -> GraphExtractionResult:
        """Validate extracted entities and relationships."""
        raise NotImplementedError