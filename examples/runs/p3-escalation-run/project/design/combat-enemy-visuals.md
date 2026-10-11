# Enemy combat visuals: telegraphs, charge lane, block and stun (G-002)

Status: visual spec for build 0.4. Written by the Art Director for `design/combat-enemy-depth.md` (authoritative for all timings, damage and ranges; nothing here changes them). It answers open question Q1 of that spec. Scope is the 5-room slice. There are no new inputs and no new UI buttons.

Colors are proposed starting values. They can be adjusted at visual review as long as the rules in section 2 still hold.

## 1. Intent

The player must be able to answer three questions at a glance, in every room including room 5. Who is about to hurt me? Where will it land? When can I no longer change my mind about moving? The cues must also say when an enemy is safe to hit: guard down, stunned, recovering.

One shared cue approach is used for all four attacks: a **threat shape** (outline plus fill), a **lock change**, and an **attacker rim**. Enemies differ by shape, not by bespoke effects.

## 2. Visual language (global rules)

### 2.1 Palette roles
| Role | Proposed value | Used for |
|---|---|---|
| Threat orange | #FF6A1A | Threat shape outline and fill while the attack is still tracking or unlocked |
| Threat red | #E5211B | Threat shape once locked, and Spitter projectiles in flight |
| Lock flash | #FFE9D6 (white-hot) | The 0.1 s flash at the lock moment |
| Safe/opening steel | #BFE6FF (pale cold cyan-white) | Block cue, guard plate, stun cue. Never an attack. |
| Lantern light | #FFC864 at low saturation, soft radial gradient | The player's light only |
| Threat outer edge | #0B0F1A, 1 px dark keyline around every threat outline | Keeps outlines readable on lit floor |

Reserved-color rule: **saturated orange/red appears only on active threats** (a threat shape, the attacker rim, a Spitter projectile). Idle, walking, waiting, recovering and stunned enemies show no orange/red, including in their base sprite accents. This is what makes the cue meaningful (spec 2.2).

### 2.2 Separation from the lantern
- Lantern light is soft, has no hard edge, is amber-yellow and low saturation, and flickers slowly. Threat shapes have a hard outline, are saturated orange/red, and use pulse and lock changes.
- The threat layer is drawn **above the lighting pass and is not darkened by it.** A telegraph stays fully visible in unlit parts of the cave. The shape is drawn under enemies and the player, so sprites stay readable.
- Lantern light never draws outlines or hatching.

### 2.3 Shared threat-shape anatomy
Every damaging attack uses these parts, driven only by elapsed telegraph time (real seconds):
1. **Outline** of the area that can hurt. It must match the real hit area of the attack. Dashed and thin (2 px) while the attack can still change direction. Solid and thick (4 px) once locked.
2. **Fill** inside the outline, in the same color. It grows from the enemy outward to full (for the Charger lane and Spitter line it ramps in alpha instead, because their full length must show from the start). The fill alpha is capped at 35 % so overlapping shapes and the sprites under them remain visible. Fill reaches full at exactly the moment damage can begin, so "fully filled" means "now".
3. **Lock change** (section 2.4).
4. **Attacker rim**: a 2 px outline pulse on the attacking enemy's silhouette in the same color, so the player sees which enemy owns the shape. The pulse is a brightness ramp, not a strobe.
5. **Hold, then clear**: on the damage frame the shape stays for one more rendered frame, then clears. The shape and rim are removed immediately if the enemy dies or the attack is cancelled (spec edge case 4).

Shapes are distinct, so attack types do not rely on hue and can be told apart in grayscale:
| Attack | Shape |
|---|---|
| Grub lunge | Short rectangle with an arrowhead, 2 tiles long, pointing at the lunge direction |
| Spitter shot | Thin line (about 0.25 tile) with a small reticle at its far end |
| Charger charge | Wide lane (1 tile) with moving chevrons and an end-cap bar at the stop point |
| Shieldbearer bash | Wedge/cone, 1.5 tiles |

### 2.4 Lock change
At every lock point, all of these happen together:
- The outline changes from thin and dashed to thick and solid.
- The color shifts from orange to red.
- A white-hot flash of 0.1 s runs along the outline, and the attacker rim flashes once.

The thick solid red state **stays** until the attack ends, so the player who missed the flash still sees the locked state. This also keeps the cue the same at 30 and 60 FPS, because it does not depend on a single frame. The flash is limited to one per attack, so there are no strobing effects.

Lock points (spec values): Spitter at 0.4 s into its 0.6 s telegraph (0.2 s before firing). Charger at 0.5 s into its 0.8 s windup (direction fixed for the last 0.3 s). Grub: direction locks at the end of the telegraph (see note N1). Shieldbearer: the bash area does not turn during the telegraph, so it is drawn locked (thick, solid, red) from the start of the telegraph.

## 3. Per-attack cues

### 3.1 Grub lunge (0.5 s telegraph, lunge 0.15 s, recovery 0.6 s)
- The Grub stops, its rim pulses, and the arrow-rectangle grows from the Grub toward the player over 0.5 s. It follows the player until it locks. The lock change fires at the end of the telegraph, as the lunge starts.
- Recovery (0.6 s): all orange/red is gone and the sprite dims slightly. This tells the player it is safe to swipe.
- Walking Grubs show no cue.

### 3.2 Spitter shot (0.6 s telegraph, aim locks at 0.4 s)
- The thin aim line extends from the Spitter in the aim direction and tracks the player for 0.4 s (dashed, orange). At the lock point it turns solid, red and thick, with the flash, and the reticle snaps.
- The line is drawn to the first obstacle or guard in its path (so a Shieldbearer in front visibly "catches" the line). See Q-A for the range.
- A projectile in flight is a red core with a dark keyline and an orange trailing glow. It carries no shape and no attacker rim, and does not count toward the limit of 2.

### 3.3 Charger charge lane (windup 0.8 s: tracks 0.5 s, locked 0.3 s)
- The lane is drawn for the whole windup: from the Charger along the charge direction, 1 tile wide, ending at the wall or at 8 tiles, whichever comes first. The end-cap bar marks where the charge would stop. During tracking the lane rotates with the Charger and its length updates as the end point changes.
- Tracking (0 to 0.5 s): dashed orange outline, low fill alpha (15 %), slow chevrons moving along the lane toward the end.
- Lock (0.5 s): lock change per 2.4. The fill rises to 35 % red, the chevrons speed up, and the lane stops rotating. The final 0.3 s is the "last chance to leave the lane" window, and it is visually the thick solid red state.
- Charge: the lane stays as the Charger travels and clears on the frame after the charge ends. The Charger body gets a short orange speed streak (this counts as part of the threat rim).
- Charge and lane never overlap in meaning with Spitter lines: the lane is wide with chevrons, the Spitter line is thin with a reticle.

### 3.4 Shieldbearer
- **Guard plate (always visible):** a steel-colored (#BFE6FF) plate on the 120° front arc of the sprite, rotating as the Shieldbearer turns. This is not a threat, so it never uses orange/red. It tells the player where attacks do 0.
- **Bash telegraph (0.6 s):** the wedge shape (1.5 tiles) in front. It does not rotate, so it is drawn locked from the start (thick solid red, outline already solid), with the fill growing outward over 0.6 s. Rim pulses. The plate stays up.
- **Guard down (0.8 s recovery after a bash):** the plate drops. It becomes a dim, low-alpha outline at the front and a clear gap shows on the front arc. All orange/red is gone. This is the "hit it now" signal.
- **Block cue (a swipe landing inside the guard arc, damage 0):** at the contact point on the arc, a steel-white spark ring expands to about 0.75 tile over 0.2 s, and the plate flashes bright for 0.1 s. A distinct short metallic "clank" sound plays (not used for any other hit; see asset flag F3). The Shieldbearer sprite is not pushed or recolored. The block cue is never orange/red and never shows on a hit that deals damage, so the player can tell "blocked" from "hurt".

### 3.5 Charger stun and recovery
- **Wall-stun (1.5 s):** on a wall hit, a short dust/impact puff at the wall. The Charger's sprite tilts and sits low, all orange/red is removed, and 3 steel-white (#BFE6FF) sparks circle its head. The sparks blink faster in the last 0.3 s of the stun so the player knows the opening is ending.
- **Open recovery (0.8 s, no wall hit):** the sprite dims slightly, with a small dust puff and no sparks. This is visually weaker than the stun, so the player can tell "long opening" from "short opening".
- **Cooldown (1.0 s):** back to normal idle visuals, with no orange/red until the next windup starts.

## 4. Readability with multiple enemies (room 5)

Room 5: Shieldbearer, Charger, Spitter, 2 Grubs. At most 2 enemies are in telegraph or attack at once (D-003), so at most 2 threat shapes are on screen. Spitter projectiles in flight are extra and look different (round red core, no outline shape).

- Waiting, approaching, recovering and stunned enemies have no orange/red, so every orange/red shape on screen means "an active threat now".
- Each shape is connected to its owner by the origin point and the rim pulse. Overlapping shapes keep opaque outlines (alpha-capped fills), and the Charger lane is drawn under other shapes and under all sprites.
- If two shapes overlap, the one with the earlier lock moment draws on top, so the most urgent one stays visible.
- The steel colors (guard plate, block, stun) are the only non-threat effects in the scene, and they are cold. The player learns "cold = safe/opening, hot = danger".

## 5. Cost and implementation assumptions (for the Technical Director to check)

- F1: One shared "threat shape" renderer with parameters (shape type, origin, direction, length, progress, locked, color), using 3 masks (rect/arrow, line, wedge) plus a chevron texture. No per-enemy bespoke assets.
- F2: The rim pulse is an outline effect on enemy silhouettes. Check that outline rendering or a shader is available and cheap; fallback is a pre-baked brighter sprite outline.
- F3: The block sound needs one short audio asset. If audio is not available in the slice, the visual block cue alone is acceptable and QA criterion VC7 sound part is dropped.
- F4: The Charger lane can reach 8 tiles and may run across the room. Check draw cost with the lane, up to 2 shapes, and projectiles at 30 FPS.
- F5: Cue states must come from the enemy's state and elapsed time (phase and time in phase), not from animation frame counts. The cue must be on screen for at least one rendered frame before damage (D-003). Visuals must be swappable without logic changes (as the Technical Director plans).
- F6: Enemy base sprites must not use saturated orange/red accents. If existing art does, it needs recoloring (small asset task).
- F7: The lane and wedge outlines must be drawn from the same geometry as the actual hit areas (not a separate approximation).

## 6. Acceptance criteria

### 6.1 Verification (QA) — run at 30 FPS and 60 FPS with the same result
- VC1 Presence: for each of Grub lunge, Spitter shot, Charger charge and Shieldbearer bash, the threat shape and the attacker rim are on screen within 1 rendered frame of the telegraph starting and stay on screen until the attack ends. Visible time before damage is at least 0.4 s and matches the spec durations (±0.05 s).
- VC2 Absence: no orange/red threat shape or rim is visible on idle, walking, waiting, recovering, stunned or dead enemies, and none appears for a third enemy that is waiting for a slot.
- VC3 Lock: the lock change (thick solid red outline plus 0.1 s flash) occurs at 0.4 s ±0.05 s into the Spitter telegraph and at 0.5 s ±0.05 s into the Charger windup, and the locked state stays until the attack ends. The Shieldbearer's bash shape is locked from the start of its telegraph. The Grub's lock change coincides with the start of the lunge.
- VC4 Shape matches hit area: the Charger lane length equals the real charge travel (to the wall or 8 tiles). A player standing inside the shape at damage time is hit, and a player standing outside is not. This holds for the Grub arrow, Spitter line and Shieldbearer wedge as well (±0.25 tile at the outline edge).
- VC5 Lane tracking: during the first 0.5 s of the windup the lane rotates with the Charger. In the last 0.3 s it does not change direction or length.
- VC6 Distinct shapes: in a grayscale capture, the four attack shapes can be told apart by shape alone.
- VC7 Block cue: a swipe inside the guard arc shows the steel spark and plate flash within 1 rendered frame, lasting 0.2 s ±0.05 s (plus the clank sound, if F3 is built). A swipe that deals damage (from the side or back) shows no block cue. The block cue contains no orange/red.
- VC8 Guard down: during the 0.8 s bash recovery the guard plate is lowered and no orange/red is on the Shieldbearer. During the rest of the time the plate is up.
- VC9 Stun: the stun cue (tilted sprite plus steel sparks) lasts 1.5 s ±0.05 s after a wall hit and is absent after an open-field charge (which shows the weaker 0.8 s recovery cue). Sparks blink faster in the last 0.3 s.
- VC10 Contrast: the outline (including its dark keyline) has a contrast ratio of at least 3:1 against both the brightest lit floor tile and the darkest unlit floor tile in the room, measured on captures. The shape is not dimmed by the lighting pass.
- VC11 Limit: in room 5 at no time are more than 2 threat shapes on screen (projectiles excluded).
- VC12 Cleanup: when an enemy dies during its telegraph, its shape and rim are gone by the next rendered frame.
- VC13 Flash safety: no cue flashes more than 3 times in any 1 s period.
- VC14 No new UI: no new buttons or HUD elements are added.

### 6.2 Experience signals (Review and the Art Director's visual review; not for the Playtester's handoff)
- VE1 In room 5 the player can say, in their own words, which enemy was attacking and where the attack would land, without describing it as "everything is flashing".
- VE2 The player can tell the Charger lane from a Spitter line, and can tell "blocked" from "hurt".
- VE3 The player notices the "hit it now" openings (guard down, stun) and uses them.
- VE4 The player does not mistake the lantern glow for a threat, or a threat for the lantern.
- VE5 Hits taken are described as "I saw it and was too slow / chose wrong", not "I did not see it" (pillar 3).

## 7. Notes and questions (nothing here changes a spec value)

- N1 (for `game-designer`): the Grub's direction locks at the **end** of its telegraph and the lunge takes 0.15 s. With a tracking shape until the last instant, the player has almost no reaction time after the lock. The visual cannot fix that. If this is not intended, the Grub may need an earlier lock point (for example 0.2 s before the lunge, like the Spitter). I have drawn it as the spec says, and the lock cue can be moved with no visual change in design. The Studio should route the question to `game-designer`.
- Q-A (game-designer / Technical Director): the Spitter's projectile range is not given. The aim line is drawn to the first obstacle or guard, or to the room edge. Tell me if there is a range limit.
- Q-B (Technical Director / game-designer): the actual widths and angle of the Grub lunge rectangle, the Spitter line and the Shieldbearer bash cone. Cues are drawn from the real hit areas (F7), and the sizes above are visual estimates (Grub about 1 tile wide, cone about 90°). Confirm the real values so the cue matches.
- Q-C: existing hit-feedback visuals are not in this packet. I assume that a damaging hit on the player already has its own feedback and that the block cue is clearly different (steel, no screen shake). Check at visual review.

## 8. Changed documents

New: `design/combat-enemy-visuals.md`. The Studio should link it in the `project.md` Design index with `design/combat-enemy-depth.md`.
