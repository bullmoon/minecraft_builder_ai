# Project Tasks — Minecraft Builder

**Last updated:** 2026-10-31

## Current Phase: Architecture Review

The project has accepted three architectural decisions (DEC-001, DEC-002, DEC-003).

The immediate goal is to review the existing implementation and prepare a migration plan before modifying source code.

## 1. Architecture Review

- [ ] Inspect the current implementation of `build.py`, `builder.py`, and `minecraft_rcon.py`.
- [ ] Review existing configuration files and tests.
- [ ] Compare the current implementation with DEC-001, DEC-002, and DEC-003.
- [ ] Identify code that can be reused.
- [ ] Identify code that should be replaced or removed.
- [ ] Design shared building-volume coordinate calculation.
- [ ] Design full-volume clearing.
- [ ] Define error handling when positioning, clearing, or construction fails.
- [ ] Prepare a phased implementation plan.

## 2. Implementation Tasks

To be scheduled after the architecture review is accepted:

- [ ] Implement player-relative building-volume calculation.
- [ ] Support all four cardinal directions.
- [ ] Support even and odd structure widths.
- [ ] Implement building-volume validation.
- [ ] Implement complete building-volume clearing.
- [ ] Respect Minecraft command limits by splitting large clearing operations when necessary.
- [ ] Ensure construction starts only after successful clearing.
- [ ] Update `build_gate()` to comply with DEC-001.
- [ ] Migrate existing structure builders to the shared workflow.
- [ ] Review the need for `find_ground()` and remove obsolete logic only after its responsibilities have been replaced.
- [ ] Update configuration validation and examples.

## 3. Testing and Verification

- [ ] Add coordinate-calculation tests for all four cardinal directions.
- [ ] Add tests for even and odd widths.
- [ ] Add tests for building-volume boundaries.
- [ ] Add tests for clearing volumes of different sizes.
- [ ] Test behavior when a clearing command fails.
- [ ] Verify that no blocks outside the defined volume are modified.
- [ ] Test that construction does not start after a failed preparation step.
- [ ] Run the complete unit test suite.
- [ ] Perform an in-game test on the Paper server.

## 4. Review Findings from 2026-10-31

- **DEF-01:** Gate wall above lintel is incomplete. Address through DEC-001.
- **DEF-02:** Current ground detection does not recognize many player-built foundations. Reassess because DEC-002 and DEC-003 change the positioning and preparation model.
- **DEF-03:** Gate configuration permits a width that leaves no pillar on one side. Reassess and fix during configuration validation.
- **DEF-04:** Gate opening is not cleared. Address through the shared full-volume clearing mechanism in DEC-002.
- **PERF-01:** Ground detection may generate excessive synchronous RCON calls. Reassess after deciding whether `find_ground()` remains necessary.

## 5. Current Status

**Current phase:** Architecture Review  
**Next action:** Obtain an independent architecture analysis from Claude.  
**Implementation status:** No changes have been made based on the second-pass review yet.

## 6. Completion Policy

A task is complete only when:

1. The implementation is reviewed.
2. Relevant automated tests pass.
3. The Project Owner verifies the result.
4. Documentation is updated where necessary.
5. The Project Owner accepts the change.
