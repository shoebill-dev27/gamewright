# Build 0.3: what running it looks like

Only level 1 differs from 0.2. Levels 2 and 3 look and respond exactly as in 0.2. Timings below are as seen in a 60 fps screen recording on a phone or tablet.

## Level 1 at rest (after the opening movement, about 1.6 s after load)

- The scene is sand, one tide pool, a crab and a shell-shaped home. The text bubble near the top still reads "Drag the tide pool!".
- The tide pool is a saturated pastel water blue/teal, clearly bluer and darker than the sand. In a grayscale capture its fill is visibly darker than the sand, at roughly 1.8:1 on the starting colors. The exact ratio depends on the sand's real color and on how the grayscale conversion is done.
- The tide pool is the only object with the darker outline. It pulses continuously and gently, growing from normal size to about 6% larger and back every 2 seconds.
- The crab has the same lighter outline as the other scenery. It no longer bobs and sits still.
- The shell home has the same lighter outline as the other scenery and does not move. Any highlight-style look it had in 0.2 is gone.
- Nothing else on screen has a darker outline than the scenery. There is no timer, countdown or failure message.

## Opening movement (once per load, and again after a restart)

- With no touch, the pool slides about a quarter of the way toward the home over 0.8 s, then slides back over 0.8 s. The idle pulse then starts at the pool's starting spot.
- It does not replay when the device is rotated, and the pulse carries on through the rotation.
- During the slide, the pool can be grabbed where it is drawn.

## Touching the pool

- On touch-down, any opening movement, ease-back or redirect pulse stops at once. The pool grows to about 10% bigger within 0.1 s and a soft shadow appears under it. The idle pulse stops.
- The pool follows the finger 1:1 from where it was drawn, including mid-slide, and cannot leave the play area.
- A second finger placed on a pool that is already held is ignored.
- On release the pool shrinks back to normal size over 0.15 s, the shadow goes, and the idle pulse resumes. The pool stays where it was dropped.
- Dropping on the home finishes the level. Dropping on the crab leaves the pool there, and the crab does not react.
- The touchable area is the pool's normal size. While it pulses larger, a touch on its outer rim can count as a touch on the sand underneath and give the sand response instead.
- Undo after a drop puts the pool back at its previous position. After the first drop, that is the starting spot, not any spot from the opening movement. A second undo does nothing.

## Touching the crab

- Within 0.1 s the crab flips instantly, if needed, to face the side the pool is on, judged from the crab's center. If it already faces that side, it does not flip. It wiggles about ±8° for 0.4 s.
- The pool then does a pulse: it grows to about 15% bigger and back twice, over 0.6 s in total. It starts within 0.2 s of the touch.
- If the finger stays down and moves, the crab does not move. It leans about 10° toward the pool while the finger is down and springs back on release. Only one pool pulse happens, at touch-down.
- While the pool is being dragged, the crab flips to face it whenever the pool crosses to the other side of the crab's center. These flips are instant.

## Touching the home

- Within 0.1 s the home brightens by about 20% and fades back over 0.6 s. The pool does the same pulse as above.
- The home does not move and cannot be dragged.

## Touching empty sand

- Only the pool pulse happens. The sand itself shows nothing.

## Repeated touches

- The pool pulse starts at most once every 1.5 s. Tapping the sand, crab and home quickly for 5 s gives the pool about three or four pulses.
- The crab wiggle and flip, and the home glow, still play on every tap.
- Every touch on the crab, home, sand or pool shows some visible response within 0.2 s.

## Home glow while dragging

- While the pool is held, the home glows steadily whenever the pool's center is within 1.5 pool-widths of the home's center. The width is the pool's normal size, not its enlarged or lifted size.
- The glow ends when the pool moves out of range or is dropped. A pool that is not held never triggers it, including during the opening movement.

## Touching something other than the pool during the opening movement

- The opening movement stops. The pool glides back to its starting spot in 0.15 s, however far along the slide it was.
- The crab flip and wiggle, or the home glow, start at once and play during that glide. For sand there is no object response.
- At 0.15 s the pool lands at its starting spot, the pool pulse starts, if the 1.5 s limit allows, and the idle pulse begins.
- Touching the crab, home or sand during the glide plays that object's response. The glide carries on.
- Touching the pool during the glide makes it follow the finger from where it is drawn.
- After a drop, undo returns the pool to its starting spot, and a second undo does nothing. This is the same whether or not the opening movement was cut short.

## Devices with a reduce-motion setting turned on

- This applies to iOS "Reduce Motion" and Android "Remove animations", where those settings exist. Level 1 checks the setting when it loads.
- The opening movement is skipped.
- The idle pulse, pool pulse, crab wiggle and crab lean are replaced by plain brightness changes lasting about 0.4 s. The crab and the home do not move.
- The darker outline and the color difference between the pool and the sand are still there.
- The pool still grows, gets a shadow, follows the finger and shrinks on release as described above.
- The crab still flips instantly to face the pool.
- On devices without this setting, the full movement above is shown. There is no in-game switch.

## Other

- The level is still finished by dragging the pool onto the home. It can be done by touch alone, with the text bubble hidden or ignored.
- All artwork comes from the existing sprite sheet, with only color, flip, size, rotation, position and brightness changes.
