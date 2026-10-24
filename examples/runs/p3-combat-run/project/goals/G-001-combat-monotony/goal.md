---
kind: goal
id: G-001
project: lantern-depths
status: done
created: 2026-10-11
---
# G-001: Improve monotonous combat

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success condition (qualitative): a player from the project's player profile experiences combat in the current build as varied and engaging rather than repetitive. Playing a run involves meaningful moment-to-moment variation in how the player positions, times and responds to enemies. Numeric thresholds belong to Design; the final verdict belongs to Review.

Constraints that shape any solution:
- Pillar 1 and D-001: combat stays one-button (attack + dash). No new input buttons without Owner approval. Variety must come from positioning, timing and enemy behavior.
- Readable threats (pillar 3) and 30/60 FPS correctness must be preserved.
- Small team: prefer reusing existing systems.

Out of scope: new input buttons or a larger player kit, changes to run length, new biomes or rooms unrelated to combat variety, and non-combat systems. By Owner instruction (D-010), Phase 2 (enemy behavior variants) is also out of scope for this Goal.

Not an immediate escalation: the Goal does not conflict with the vision or D-001. It had to be solved inside them.

## Unknowns

Entry questions from `development-loop.md`:
- Observe: done. The playtester observed the experience problem; QA confirmed a dash-damage defect (handoff 05).
- Diagnose: done (handoff 04): three options.
- Decide: done. D-002 chose B (encounter escalation) first, then A (enemy behaviors); C in reserve. The Owner then decided (D-010) to accept criteria 1 and 2 as "not judged" and to skip Phase 2.
- Design: done for Phase 1 (handoffs 11, 35, 44, 53; D-008, D-009). Phase 2 design exists but was not used.
- Plan: done (handoff 16, D-004). Phase 1 needed no separate Plan.
- Build: done for the dash-damage fix, hit-stun input, Phase 1, the narrow follow-up and the wording update (`sim/build-0.8.md` is the newest build). Phase 2: skipped by the Owner.
- Verify: Phase 1 verified with criteria 1 and 2 open (QA pass 50, Art Director pass 51).
- Play: Phase 1 playtest returned (57) with no counts (text-only dry run).
- Review: done (60), verdict `goal-not-met`.

Skipped: Phase 2 steps (9 to 11), by Owner instruction D-010.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | [01](01-studio-to-playtester.md) → [02](02-playtester-to-game-designer.md) |
| 2a | Diagnose | game-designer | diagnose-experience | done | [02](02-playtester-to-game-designer.md) → [04](04-game-designer-to-game-director.md) |
| 2b | Observe (possible defect: damage during dash) | qa | reproduce-defect | done | [03](03-studio-to-qa.md) → [05](05-qa-to-studio.md) |
| 3a | Decide | game-director | make-decision | done (D-002) | [04](04-game-designer-to-game-director.md) → [07](07-game-director-to-game-designer.md) |
| 3b | Build (fix dash-damage defect) | gameplay-engineer | implement-change | done | [06](06-studio-to-gameplay-engineer.md) → [08](08-gameplay-engineer-to-studio.md) |
| 3c | Build (hit-stun input observable, consistent with D-003) | gameplay-engineer | implement-change | done | [18](18-studio-to-gameplay-engineer.md) → [20](20-gameplay-engineer-to-studio.md) |
| 4a–4a″ | Verify (dash-damage fix), attempts 1 to 4 | qa | verify-change | done, no verdict (`question` each time); superseded by 4a‴ | [09](09-studio-to-qa.md), [12](12-studio-to-qa.md), [23](23-studio-to-qa.md), [28](28-studio-to-qa.md); reports [10](10-qa-to-studio.md), [15](15-qa-to-studio.md), [21](21-qa-to-studio.md), [26](26-qa-to-studio.md), [29](29-qa-to-studio.md) |
| 4c | Verify decision (which build description is current) | owner | — | done (D-007: `sim/build-0.5.md`) | [27](27-studio-to-owner.md) |
| 4a‴ | Verify (attempt 5, against `sim/build-0.5.md`) | qa | verify-change | done: **pass** ([31](31-qa-to-studio.md)) | [30](30-studio-to-qa.md) |
| 4b | Design (Phase 1 in full; Phase 2 as proposed behaviors) | game-designer | write-design-spec | done | [07](07-game-director-to-game-designer.md) → [11](11-game-designer-to-studio.md) |
| 5a | Plan (Phase 2 feasibility and cost) | technical-director | technical-plan | done (D-004) | [13](13-studio-to-technical-director.md) → [16](16-technical-director-to-studio.md) |
| 5b | Design (spawn marker and Phase 2 telegraph visuals) | art-director | write-design-spec | done | [14](14-studio-to-art-director.md) → [17](17-art-director-to-studio.md) |
| 5c | Design (adjust Phase 2 spec) | game-designer | write-design-spec | done (D-005) | [19](19-studio-to-game-designer.md) → [22](22-game-designer-to-studio.md) |
| 5d | Design (realign Lunge Grub visual; hit feedback for flinch-immune enemies) | art-director | write-design-spec | done (D-006) | [24](24-studio-to-art-director.md) → [25](25-art-director-to-studio.md) |
| 6, 6b, 6c | Build Phase 1 | gameplay-engineer / game-designer | implement-change / write-design-spec | done (D-008) | [32](32-studio-to-gameplay-engineer.md) → [33](33-gameplay-engineer-to-studio.md); [34](34-studio-to-game-designer.md) → [35](35-game-designer-to-studio.md); [36](36-studio-to-gameplay-engineer.md) → [37](37-gameplay-engineer-to-studio.md) |
| 7a | Verify (Phase 1, `sim/build-0.6.md`) | qa | verify-change | done, `question` ([40](40-qa-to-studio.md)) | [38](38-studio-to-qa.md) |
| 7b | Verify (visual review of the spawn marker ring) | art-director | visual-review | done: pass ([41](41-art-director-to-studio.md)) | [39](39-studio-to-art-director.md) |
| 7c | Design (judging basis for criteria 1 and 2) | game-designer | write-design-spec | done (D-009) | [42](42-studio-to-game-designer.md) → [44](44-game-designer-to-studio.md) |
| 7d | Verify (visual follow-up) | art-director | visual-review | done | [43](43-studio-to-art-director.md) → [45](45-art-director-to-studio.md) |
| 7f | Build (narrow follow-up) | gameplay-engineer | implement-change | done | [46](46-studio-to-gameplay-engineer.md) → [47](47-gameplay-engineer-to-studio.md) |
| 7e | Verify (narrow re-verify, `sim/build-0.7.md`) | qa | verify-change | done: **pass** ([50](50-qa-to-studio.md)); criteria 1 and 2 "deferred to playtest" | [48](48-studio-to-qa.md) |
| 7g | Verify (re-review of ring dot and S0–S3) | art-director | visual-review | done: **pass** ([51](51-art-director-to-studio.md)) | [49](49-studio-to-art-director.md) |
| 7h | Design (spec wording; neutral record sheet) | game-designer | write-design-spec | done ([53](53-game-designer-to-studio.md)) | [52](52-studio-to-game-designer.md) |
| 7i | Build (wording only) | gameplay-engineer | implement-change | done ([55](55-gameplay-engineer-to-studio.md)); `sim/build-0.8.md` is the newest build | [54](54-studio-to-gameplay-engineer.md) |
| 8 | Play (Phase 1) | playtester | playtest-session | done, no counts ([57](57-playtester-to-studio.md)) | [56](56-studio-to-playtester.md) |
| 8b | Decide (Owner) | owner | — | done (D-010): Option A | [58](58-studio-to-owner.md) |
| 9 | Build (Phase 2: behavior variants) | gameplay-engineer | implement-change | skipped (Owner instruction, D-010) | — |
| 9b | Design (confirm Phase 2 figures) | game-designer | write-design-spec | skipped (depends on 9) | — |
| 10a | Verify (Phase 2) | qa | verify-change | skipped (depends on 9) | — |
| 10b | Verify (Phase 2 visuals) | art-director | visual-review | skipped (depends on 9) | — |
| 11 | Play (Phase 2) | playtester | playtest-session | skipped (depends on 9) | — |
| 12 | Review | game-director | review-outcome | done: `goal-not-met` ([60](60-game-director-to-studio.md)); criteria 1 and 2 not judged | [59](59-studio-to-game-director.md) |

Status: planned | tentative | open | done | skipped.

## Route changes

Earlier Route changes are summarized; the Handoffs carry the details.

- Step 1 found a possible defect, so QA ran in parallel (2b). Diagnose gave three options and D-002 chose B then A.
- Verify of the dash-damage fix took five attempts (build-description and Load gaps); D-007 settled the current description and the fix passed.
- Phase 1 Build handed back once on spec contradictions (D-008). Verify raised that criteria 1 and 2 need counted runs (D-009). Both re-verifications passed (50, 51).
- The Playtester returned no counts, which fired an escalation (58). The Owner chose Option A (D-010): criteria 1 and 2 stay "not judged", Phase 2 is skipped.
- After Review (60, `goal-not-met`): the usual return rule (Review → Diagnose) is not applied, because D-010 says the Goal closes on the Review result. Findings and proposed next Goals go into the Outcome. No escalation trigger fires; the Goal closes.

## Next action

None. G-001 is closed. The Owner decides whether to open the proposed Goals listed in the Outcome.

## Outcome

**結果: 目標は未達成(`goal-not-met`)。ただし「失敗」ではなく「意図の達成が示されていない」という意味です。**

### 実施したこと
- **ダッシュ中のダメージ不具合を修正**し、QA が合格と判定しました(ハンドオフ 31)。
- **Phase 1(エンカウンターの段階的強化)を実装**しました(`sim/build-0.8.md`)。部屋ごとの敵の数・構成・端・ウェーブの違い、敵の出現前の 0.8 秒の予兆リング、決定的なスポーン規則を含みます。
- QA(基準 3、4、5、10 の c・d・g)とアートディレクター(リングの見た目)は、ビルド記述にもとづいて合格としました。
- ビルドは仮想(ドライラン)で、実際の計測プレイは行われていません。

### 判定の根拠
- **基準 1(部屋 4〜5 を一か所に留まったままクリアできないか)**と**基準 2(ダッシュが戦闘で使われるか)**は**「未判定」**です。合格とも不合格とも記録していません。プレイテスト(57)はテキストのみで、回数などの数値が得られませんでした。
- 基準 2 の Phase 2 部分(ダッシュに目的を与える敵の挙動)は、Owner の指示(D-010)によりビルドしていません。そのため、診断で挙げた症状のうち「ダッシュに目的がない」「敵が浅い」は未対応のままです。
- 基準 6(ランの長さ 15〜20 分)は計測されていません。
- 基準 3(部屋ごとの違い)と基準 4(脅威が先に見える)は、記述上は満たされています。これらは必要条件であり、体験そのものの証拠ではありません。
- 確信度: Phase 1 が仕様どおり作られている点は中〜高。目標の意図が達成されたか否かは、どちらの方向にも低い(悪い結果とは言えず、「示されていない」状態)。

### 下した Decision
D-002(エンカウンター強化を先に、次に敵の挙動。案 C は保留)、D-003(ヒットスタン中の入力は無視)、D-004(Phase 2 の技術方針)、D-005、D-006(Phase 2 の敵の仕様と見た目)、D-007(検証対象は `sim/build-0.5.md`)、D-008(Phase 1 のスポーン・ウェーブ規則)、D-009(基準 1・2 は回数にもとづきプレイテストで判定)、D-010(Owner:基準 1・2 を「未判定」として受け入れ、Phase 2 は行わず、Review 結果で終了)。D-001(1ボタン戦闘)は変更していません。

### 次の課題(新しい Goal の提案)
1. **Phase 1 ビルドの計測付きプレイテスト(基準 1・2・6)**: 時計、デバッグログ、コントローラまたはスクリプト入力が使える環境が必要です。部屋 4・5 での位置別の被弾数と死亡数(5 か所 × 5 回)、部屋 1〜5 のダッシュ使用とその理由、実際のラン時間、既存の速度・体力・部屋サイズ・当たり判定、`SPAWN_FALLBACK` の回数、複数 Grub の出現間隔、ウェーブ 2 の早い開始が唐突に感じられるかを記録します。その後で再 Review を行います。基準 1 が不合格なら、次はルーム配置の変更(仕様 3.6)、続いて調整パラメータ(3.5 と第 7 節)を検討します。
2. **Phase 2(予兆付きの敵の挙動バリエーション: Lunge Grub、Fan Spitter)**: ダッシュの目的と敵の深さに対応します。着手前に、突進の確定段階の見た目の再調整とチェック A5(仕様 4.6、D-006)、ビルド側の当たり判定サイズと速度の報告による数値の確認、突進速度を調整する場合のテクニカルディレクターによるサブステップ確認が必要です。Phase 1 の効果を先に知るため、提案 1 の後、または同時に行うのが望ましいです。
3. **次のビルド記述の用語整理**: 同時開始の順序を「テーブル順」と明記、「角から 1.5 タイル」の Spitter の文を部屋 3〜5 に限定、出現ログに予定時刻を含めるか明記、見出し「0.3.3」を実際のビルド番号に修正、部屋 3 の Spitter の角を NE と明記、リングの「solid」表記をアートディレクターが確認。いずれも既存の判定(50、51)は覆さず、提案 1 または 2 に含められます。
4. **案 C(攻撃/ダッシュの報酬ルール)**: Phase 1 と 2 の計測プレイの後も消極的な動きが残る場合のみ。専用の Goal と Decision が必要で、コンボ的な語彙は追加しません。

### Owner への確認事項
- 承認が必要な事項はなく、エスカレーション条件にも該当しません。
- 参考として、元の不満(戦闘が単調)が「改善された」とはまだ示されていません。上記の Goal を開くかどうか、いつ開くかは Owner が決めます。特に「ダッシュの目的」と「敵の深さ」は、提案 2 を選んだ場合にのみ対応されます。
