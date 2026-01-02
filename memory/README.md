# Memory (Phase 5.4)

This directory contains **local, dev-only persistence** for user-owned memory.

## Structure

memory/
└── owners/
    └── <owner_id>/
        ├── memory.json
        └── proposals.json

## Design Principles

- Each memory belongs to exactly one `owner_id`
- No memory is auto-created or auto-consumed
- All writes go through proposal + approval
- This backend is intentionally simple and local
- Safe to delete during development

## Status

- Phase 5.4: owner_id + local persistence
- Not production-ready
- No authentication

