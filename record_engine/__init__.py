"""Observation-first clinical record engine.

Extraction records what each document says (observations). Code decides what is true (facts),
using one generic reconciliation algorithm and a readable policy file. Questions compile to a
small query language that code executes with scenario arithmetic; answers cite fact and result
IDs so they can be checked by lookup.
"""

# Bumped whenever a change alters what a build or an answer produces; the service rebuilds
# records made with another version and does not answer over them.
VERSION = "record-engine-0.3"
