---
kind: decision
id: D-005
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-005: Phase 2 enemies are flinch-immune during their actions; Lunge Grub damages only through the lunge; dash window is defined relative to contact

## Decision

1. **Flinch.**
   - The Lunge Grub is flinch-immune during Wind-up, Lunge and Recovery. Player hits still deal damage but do not interrupt, delay, restart or shorten anything. In Chase it keeps the existing 0.2 s Flinch.
   - The Fan Spitter is flinch-immune in all states.
   - A kill cancels the action at once.
   - Grub and Spitter (Phase 1) keep the existing Flinch unchanged.
   - Technical mechanism: the per-state flinch-immune flag proposed by the Technical Director (handoff 16).
2. **Contact damage.** The Lunge Grub damages only through the lunge (one hit per lunge, and the first overlap uses it up even if the player is invulnerable then) and a Chase bite that wins over the 3.5-tile trigger. No damage in Wind-up or Recovery, including when a lunge ends on the player.
3. **Dash window.** The spec 4.1 text ("a dash between 0.35 s and lunge start covers the hit") is corrected. A dash covers the lunge hit if it starts within 0.25 s up to and including contact (`tc − 0.25 < td ≤ tc`). A dash starting at lunge start or later (up to contact) always covers it for any trigger distance. No lunge or dash timing was changed.
4. **Fan Spitter confirmed** over the repositioning Spitter (consistent with D-004).

Limits: Phase 1 enemies are not changed. No stagger or knockback (D-002 scope). The visual committed stage must be realigned by the Art Director (the dash window moved).

## Rationale

- Without immunity, one swipe cancels the telegraph and resets the Grub indefinitely, and recovery shrinks from 0.8 s to about 0.2 s. That defeats both the readable telegraph (pillar 3) and the dash's purpose.
- Immunity during Recovery keeps the 0.8 s punish window, and 2 swipes (0.7 s) fit in it. Ending Recovery early on a hit would punish the player for attacking.
- Damage only through the lunge keeps every hit tied to a telegraph. A bite during Wind-up or Recovery would be a hit with no readable warning.
- Defining the window relative to contact holds for any hitbox size and speed, which Build has not reported yet. The rule changes no timing, so it stays within D-004's sub-step design.
- The window is inherently 0.25 s (about 7 frames at 30 FPS), but anticipating a known 0.6 s telegraph is timing and not reaction, which fits "depth through timing" (D-001).

## Alternatives considered

- **Keep the existing Flinch on Phase 2 states:** cancels telegraphs and recovery. Rejected.
- **Hit ends Recovery early:** shortens the punish window and punishes attacking. Rejected.
- **Bite on contact during Wind-up or Recovery:** damage without a telegraph, against pillar 3. Rejected.
- **Retime the lunge or dash so the old 0.35 s window holds:** needs hitbox sizes and speeds not yet known, changes the D-004 sub-step basis, and the window would still depend on distance. Kept as tuning knobs if playtest says the window is too tight.
- **Let a lunge hit again after dash invulnerability ends:** a possible double-hit through one overlap. Rejected for readability.
- **Repositioning Spitter:** rejected on cost (D-004).

## Revisit when

- Playtest shows the 0.25 s dash window is too tight (first knob: lunge 0.4 s).
- Build's report of hitbox sizes and speeds changes the contact range materially.
- Players cannot tell hits landed on flinch-immune enemies, even with hit feedback.
- Option C is reconsidered, or Phase 1 enemies' Flinch causes a problem.
