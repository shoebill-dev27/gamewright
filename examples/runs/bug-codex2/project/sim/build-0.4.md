# Build 0.4 — what playing it looks like

Build identifier: 0.3-G001-15.

The following behavior applies on desktop with keyboard or gamepad, at both 30 and 60 FPS.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. Outside protected periods, you take damage if three arrive at once.
- Room 3: Spitter projectiles are slow; a single step sideways avoids them. You can walk up and defeat a Spitter with two swipes.
- Room 4–5: backing into a corner, facing the Grubs and swiping remains effective. Stepping aside avoids projectiles.
- Dashing is rarely necessary to clear rooms. Holding position and swiping remains effective throughout a run.

## Dash and damage

A dash covers four tiles over 0.25 seconds on an unobstructed straight path. Walls still stop movement. Grub contact and Spitter projectile hits cost no hearts throughout the dash, including its early and late portions.

Without protection from a dash or recent damage, either kind of hit removes one heart and prevents input for 0.3 seconds. Input then recovers, while further hits remain harmless until 0.8 seconds after the damaging hit.

Dashing as soon as input recovers does not expose you to damage during the dash. Ending that dash does not cut short the remaining protection from the earlier hit.

For example, after taking damage at 0 seconds:

- If you begin a dash around 0.70 seconds, a contact or projectile hit around 0.85 seconds costs no additional hearts while you are still dashing. A hit around 1.10 seconds removes one heart, provided you have not started another dash or taken another damaging hit.
- If you begin a dash around 0.34 seconds, a hit around 0.70 seconds costs no additional hearts even though the dash has ended. A hit around 0.95 seconds removes one heart under the same conditions.
- Without another dash, contacts around 0.15, 0.45 and 0.70 seconds cost no additional hearts. Input is unavailable during the first 0.3 seconds and available afterward.

These timings describe hits that actually connect strictly before or after the stated boundaries.

Harmless hits do not start another period of input loss or postpone when damage can occur again. Multiple harmless contacts or projectile hits have the same result. With no preceding damage, hits during a dash leave hearts unchanged, and a hit 0.40 seconds after dash start removes one heart once that dash has ended. Projectile disappearance on impact remains unchanged.

## Other controls and timing

An attack pressed during a dash waits until the dash ends, then occurs once. Dash reuse remains restricted by the existing 0.6-second cooldown. Attack, dash and pause remain the available action buttons.

At 60 FPS, 0.25 seconds spans 15 frame intervals. At 30 FPS, it falls between seven and eight frame intervals; the dash ending is visible on an updated frame rather than at a separately displayed halfway point. The exact displayed ending frame and the outcome of a hit coinciding precisely with dash start or end are not established here. The protection behavior above applies to hits clearly inside the dash or clearly within the protection following damage at either frame rate.
