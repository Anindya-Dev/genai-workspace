"""
Graph schema definitions for ChronoGraph.

Defines all supported entity types and relationship types
used during knowledge graph extraction.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


class EntityType(str, Enum):
    PERSON = "Person"
    TECHNOLOGY = "Technology"
    ORGANIZATION = "Organization"
    CONCEPT = "Concept"
    PROJECT = "Project"


class RelationshipType(str, Enum):
    ADVOCATED_FOR = "ADVOCATED_FOR"
    ARGUED_AGAINST = "ARGUED_AGAINST"
    MIGRATED_FROM = "MIGRATED_FROM"
    MIGRATED_TO = "MIGRATED_TO"
    COMMITTED_CODE = "COMMITTED_CODE"
    WORKS_ON = "WORKS_ON"



@dataclass
class GraphEntity:
    """
    Represents a node in the knowledge graph.
    """

    id: str
    name: str
    type: EntityType


@dataclass
class GraphRelationship:
    """
    Represents a relationship (edge) between two entities.
    """

    source: str
    target: str
    type: RelationshipType

    document_id: Optional[str] = None
    timestamp: Optional[datetime] = None


@dataclass
class GraphExtractionResult:
    """
    Output returned by the graph extractor.
    """

    entities: list[GraphEntity] = field(default_factory=list)
    relationships: list[GraphRelationship] = field(default_factory=list)