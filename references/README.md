# References and Resource Intake

This directory contains metadata and safe-to-publish reference indexes, not restricted evidence.

## Files
- `source_registry.csv`: canonical source catalog (research sources, standards, models and legacy datasets). Columns added at archival (2026-10-05): `author_or_publisher`, `version_or_date`, `license_or_redistribution`, `sha256`, `project_role`, `cited_in`. "not recorded" means the repository holds no access date; "NOT VERIFIED" means redistribution terms were not established and no reuse right is claimed.
- `resource_intake_log.csv`: operational intake log for files collected by the team.

## Handling rule
Original court records containing sensitive material may be kept in restricted local storage and represented here only by metadata, locator, and hash.

When a new source arrives:
1. assign a new `SRC-###`;
2. preserve original filename;
3. compute SHA-256 locally;
4. record origin and access date;
5. flag sensitive/minor content;
6. do not edit the source file;
7. use a working copy for extraction.
