---
kind: handoff
goal: G-001
seq: 44
from: game-director
to: studio
stage: Review
outcome: goal-met
---
# 44: game-director → studio — G-001 の Review 結果(模擬ビルド 0.6 に基づく判定: 達成)

## Task

Goal G-001(戦闘の単調さの改善)の意図が満たされたかの判定を受け取り、Close に進む。次の課題は、新しい Goal の提案として扱う。

## Context

Handoff 43 の依頼による Review。**この判定はすべて「模擬ビルド 0.6(`sim/build-0.6.md`)の記述」と、それに基づく Verify・Play の報告に基づく(D-008)。実機で確かめた判定ではない。** Playtester の観察(Handoff 42)も、記述を読んで思い描いた体験であり、実際の手応えではない。

## Findings

### 判定

**`goal-met`(模擬ビルドに基づく。確信度は中程度)**。判断は D-010 に記録した。

### 成功条件との照合

成功条件(`goal.md`): 戦闘中に、同じ行動の繰り返しではなく、位置取り・タイミング・敵の挙動への対応といった判断を実感できること。

| 成功条件の要素 | 模擬ビルド 0.6 での証拠 |
|---|---|
| 位置取り | 部屋 2・4・5 で、隅に立って振るだけの戦い方は通用しない(レーンが出て約 0.7 秒後に突進される)。部屋 3 は Spitter が止まる戦い方を許さない。Playtester は「見てから横に動く」場面が自然に生まれると報告 |
| タイミング | 突進の接触の瞬間の 0.25 秒前からのダッシュで抜ける。Recovery(0.8 秒)が反撃の機会になる。突進は同時に 1 体、再突進は約 3.3 秒以上あと |
| 敵の挙動への対応 | 予告(レーン、沈み込み、熾火)を読む。背中の隆起で突進型を先に見分けられる。部屋 4・5 では弾と突進を同時に処理する |
| 進行 | 部屋 1(基本)→ 2(突進)→ 3(Spitter)→ 4(組み合わせ)→ 5(全部)の筋があり、Grub 速度と Spitter 間隔も段階的に上がる |

補足: Verify は `qa`(Handoff 38)と `art-director`(Handoff 40)がともに pass。新しいボタンもなく、D-001 に抵触しない。見た目の混同(S1、S2、Recovery の誤読)も、「0.7 秒では足りない」も、Play では報告されなかった。

### 問題 A〜F の扱い(Open questions 2〜3 への答え)

| # | 判断 | 理由 |
|---|---|---|
| A 部屋 1・3 に変化が少ない | D-002、D-003 の範囲内で許容する設計の帰結 | 突進を部屋 2・4・5 に限ったのは D-003 の決定。部屋 1 は基本を覚える部屋、部屋 3 は Spitter が役割。5 部屋中 3 部屋で型が変わり、進行も付いた。今回は変えない |
| B 張り付き・離れすぎで突進を見ずに済む | 達成を妨げない。次の課題 | 未検証(Playtester は試していない)。新しい単調さを生む恐れがあるので、実機で確認する。確認前に開始条件の数値(3.0〜6.0 タイル)は変えない |
| C 突進中のスワイプの手応え | 次の課題(実機の感触の確認に含める) | フィードバック(白い光、火花)は仕様どおりある。感触は実機要 |
| D 出現待ちが伝わるか | 次の課題 | D-009 の Revisit when の条件に近いが、まだ発動していない |
| E 欠陥 D(被弾直後のダッシュ中のダメージ) | 達成を覆さない。次の課題の最優先 | 以前からある挙動で、記述上は「ときどき」。実際の頻度は未確認。ただし突進を避けるダッシュの信頼を損ねうる |
| F 部屋 5 の突進順序 | 次の課題(実機で確認) | 公平な難しさか運任せかは、記述からは判断できない |

欠陥 D が判定に与える影響(Open question 3): 達成の判定を変えるほどの証拠はない。ただし、実際に起きて突進回避を成立させないなら、この判定は見直す(D-010 の Revisit when)。

### 実機で確認できていない点(Outcome の「確認できない点」に残すもの。Open question 4 への答え)

判定に**実質的に影響する**もの:
- 0.7 秒の予告を読んでダッシュまで入力できるか(ゲームパッド、小さい画面)。足りなければ、単調さの改善の主役である突進が成立しない。
- 張り付き戦法(問題 B)が実際に成立し、突進を無意味にするか。
- 欠陥 D の実際の頻度と、突進回避への影響。
- 全体として、実時間で遊んだとき飽きにくくなったか(最終的な成功条件そのもの)。

判定への影響は小さいが、**残す**もの:
- Handoff 38: V3 の窓の端の数値(0.05 秒外れると被弾)、30/60 FPS の実測、等距離の位置でのログによる FL の確認。
- Handoff 40: 暗い床での 35% のレーンの読み取り(A5)、レーンと弾・ランタンの光の区別、Recovery の誤読、かすりの感触、抜けた合図の過剰(S1)、解決後も残るレーンの誤読(S2)、出現中と Recovery の青の近さ(S3)、小さい画面での尾根の差、色覚の差。
- ビルド記述の欠落 G1〜G5(Charge 中の尾根、倒されたときの点灯の消去、シェブロンの静止、弾の見た目、数値の許容差)。
- H1〜H4(ゲームパッドの操作感、各部屋の実時間、音と演出、敵の速度と弾速)。

### 次の課題(新しい Goal の提案。この Goal の範囲は広げない)

優先度順:

1. **欠陥 D の再現と規則の決定**(最優先)。`qa` による再現(`reproduce-defect`)。Owner の元の報告文が必要で、入力にないため、Owner に原文を求める。再現後に `game-designer` が規則を書く(現行の指示どおり)。
2. **実機での確認(H1〜H4 と上の影響する点)**。実際のコードベースが用意された場合に、Build と Verify を実コードでやり直すかを Owner に確認する(D-008 の Revisit when)。
3. **張り付き戦法(問題 B)と部屋 5 の突進順序(問題 F)の検証**。実機または Play で、成立するかを見る。成立するなら、開始条件の調整を `game-designer` に診断させる(D-003 の Revisit when にも関わる)。
4. **出現待ちの伝わり(問題 D)**。画面でそれと分かるかを確認する。伝わらないなら見た目の合図を `art-director` が検討する(D-009 の Revisit when)。
5. **部屋 1・3 の変化(問題 A)**。D-002 の Revisit when(まだ型が単調と感じられる場合)に当たると実機で分かった場合に限り、Spitter の変化などを別の判断として扱う。今は着手しない。

### Decisions to revisit

Revisit 条件に達したものはない。次の条件は監視する: D-002(型がまだ単調なら Spitter の変化などを検討)、D-003(張り付きで突進が無意味になる場合)、D-009(出現待ちで波を引き延ばせると分かった場合)。D-010 は上記の Revisit 条件を持つ。

## Decisions already made

- D-001、D-002、D-003、D-005、D-006、D-008、D-009 は変更しない。
- D-010(新規、`game-director`): 模擬ビルドに基づく達成の判定、問題 A の許容、B・F・欠陥 D の扱い。

## Constraints

- この判定は模擬ビルドに基づく。実機の証拠として扱わない。Outcome にもそう書く。
- 欠陥 D の規則は決めていない。

## Open questions

1. 欠陥 D の元の報告文を Owner から得られるか(次の課題 1)。Owner の項目として Outcome に書く。
2. 実際のコードベースが用意される見込みがあるか(次の課題 2)。D-008 の Revisit when に当たるため、Owner の判断。

## Expected output

Studio は次の Route で Close を行う。Outcome は `owner_language`(日本語)で書き、次を含める。

- 結果: 模擬ビルド 0.6 に基づく達成。実機の証拠ではない。
- Decisions: D-002、D-003、D-005、D-006、D-008、D-009、D-010。
- 次の課題(上記の 1〜5)と、Owner の項目(欠陥 D の原文、実コードの用意)。
- 実機で確認できない点(上記の一覧)。

Owner のエスカレーションは不要。D-001 の変更、新しい入力ボタン、ビジョンの柱の変更、スコープの拡大のいずれにも当たらない。

## Sender assessment

- 確信度は中程度。成功条件は「実感」という質的なもので、証拠は記述から思い描いた体験にとどまる。この限界のため、最終的な「飽きにくくなったか」は実機でしか言えない。
- `goal-not-met` にしなかった理由は D-010 に書いた。問題 A・B・F のどれも、成功条件を満たさない証拠にはなっていない。B と欠陥 D は、実機で逆の結果が出れば判定を覆しうるため、Revisit 条件に入れた。
- 欠陥 D を後回しにしていない。達成の判定とは別に、次の課題の先頭に置いた。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md、studio/skills/make-decision.md
- Project: project.md#vision、project.md#player-profile、project.md#constraints、design/combat.md、design/grub-charge-telegraph.md、sim/build-0.6.md、goals/G-001-combat-monotony/goal.md、goals/G-001-combat-monotony/38-qa-to-studio.md、goals/G-001-combat-monotony/40-art-director-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md、decisions/D-002-combat-direction-rooms-and-grub-charge.md、decisions/D-003-grub-charge-and-room-rules.md、decisions/D-008-owner-simulated-build-judgment.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md、decisions/D-010-g001-review-goal-met-simulated.md
- Previous handoff: goals/G-001-combat-monotony/43-studio-to-game-director.md
