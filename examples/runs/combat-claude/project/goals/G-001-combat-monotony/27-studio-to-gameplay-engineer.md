---
kind: handoff
goal: G-001
seq: 27
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 27: studio → gameplay-engineer — Build の記述の確定(やり直し。Handoff 22 を Load に加えた)

## Task

Handoff 22 の変更内容の記述(2.1〜2.4)に、D-009 の規則を 2.1 の 1 文として足し、確定した変更内容の全体を、Handoff 22 を読まなくても分かる形で Findings に書く。

## Context

G-001(戦闘の単調さ)。D-008 により、変更内容を正確に書いた時点で Build は完了する。Handoff 25 は同じ依頼をしたが、Load に Handoff 22 が入っておらず、Handoff 26 で入力の欠落として返された(Studio の Load の漏れ。仕様の問題ではない)。今回は Handoff 22、前提の台帳(Handoff 17)、D-004〜D-006 を Load に加えた。

## Findings

- 規則は決定済み(D-009、`design/combat.md` §4.1、§4.3 の注、V7、V12):
  - 次の波の K と T は、前の波の全員が出現中に入った時点から調べ始める。
  - 出現位置の待ちの敵は「生きている敵」に数えない。
  - 数値・入力・プレイヤー側の値は変わらない。
- Handoff 26 の Findings 2〜4 は、Handoff 22 を見ずに書かれた下書きである。
  - 内容は規則の対応づけ、V7 と V12(a)〜(d)の追跡、模擬上の前提の一覧。
  - 使ってよいが、Handoff 22 の 2.1〜2.4 と台帳(Handoff 17)に照らして確認し、食い違いは Handoff 22 側を正として直す。
  - 台帳の項目番号は Handoff 17 のものを使う。
- 追跡の注意(Handoff 26 の Findings 3): V12(b)で、待ちの間に R の Grub を倒していた場合は、L が出現中に入った時点で波 2 がすぐ出る。Verify はこの場合の期待値を「すぐ出る」と読む。
- `sim/repo-notes.md` にはスポナー・部屋・波・出現位置の記述がない(Handoff 26 の報告)。Handoff 22 や Handoff 17 の台帳が別の答えを持っていないか確認し、答えがない項目は「模擬上の前提」と明記する。実コードで確認済みと書かない。

## Decisions already made

- D-001〜D-006: 戦闘の方向、Grub 突進、技術方針、怯み・接触、予告の視覚。
- D-007: 前提の台帳。
- D-008: Build は記述の完了で完了。判定は模擬ビルドに基づく。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い。

## Constraints

- 規則は決めない。仕様と数値は変えない。新しい入力ボタンなし。
- 欠陥 D の原因を推測して書かない。
- 実コードの変更、ビルド、テストの実行は行わない(D-008)。
- Load の必須ファイルが読めない場合は、推測で補わず、読めないファイル名を挙げて `outcome: question` で返す。同じ欠落での再試行はしない。

## Open questions

- Handoff 22 の記述と D-009 の規則の間に、1 文の統合以外の食い違いはないか。あれば `outcome: question` で返す(規則の変更は `game-designer` の権限)。

## Expected output

- 次の 2 つを含む Handoff 28 を、`to: studio` で書く(`qa` と `art-director` の Verify Handoff を Studio が組み直すため)。
  - Findings に、確定した変更内容の全体(2.1〜2.4、D-009 の 1 文を統合したもの)を自己完結で書く。Handoff 22 や他の Handoff を読まなくても分かること。
  - 模擬上の前提が残る台帳の項目を、Handoff 17 の項目番号で一覧する。
- 自己評価・確信度・疑いは Sender assessment にだけ書く(`qa` には渡されない)。
- 曖昧さや不足があれば `outcome: question`。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: goals/G-001-combat-monotony/22-gameplay-engineer-to-studio.md(変更内容の記述 2.1〜2.4), goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md(台帳 7 項目), design/combat.md, design/grub-charge-telegraph.md, sim/repo-notes.md
- Decisions: decisions/D-004-technical-approach-grub-charge-and-waves.md, decisions/D-005-flinch-contact-and-far-slot-rules.md, decisions/D-006-grub-charge-telegraph-visual.md, decisions/D-007-build-without-code-access-assumption-register.md, decisions/D-008-owner-simulated-build-judgment.md, decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/26-gameplay-engineer-to-studio.md
