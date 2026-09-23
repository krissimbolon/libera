# References and Resource Intake

This directory contains metadata and safe-to-publish reference indexes, not restricted evidence.

## Files
- `source_registry.csv`: canonical source catalog used in the research design.
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
