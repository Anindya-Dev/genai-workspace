"""
Graph schema definitions for ChronoGraph.

Defines all supported entity types and relationship types
used during knowledge graph extraction.
"""

from enum import Enum


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