---
kind: decision
id: D-022
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-022: V1補足の確定（旧経路表示、弾ID・消滅理由、長時間観測）

## Decision

詳細は`design/final-boss-and-continuous-run.md`§11。D-017の契約、第1〜4部屋、共有戦闘規則は変更しない。

1. 旧経路のボス表示：現行manualの注記を受け入れる。§6の完全表示は公開ドライバの経路に適用し、旧経路を委譲しない（旧60秒挙動を保つ）。旧経路`room 5`のplayer viewだけに誤認防止の注記1行を先頭に出す。
2. 弾IDと消滅理由：trace viewと公開ドライバのイベントログに限り要求する。ID `S<n>`、消滅は弾1個につき1回、理由は`lifetime`／`edge`／`hit`／`absorbed`／`cleared`。player viewの文言は変更しない。
3. 長時間観測：`view-every`と`trace-every <seconds>`で周期出力の間隔を指定でき、既定は変更しない。終了時に要約を出す。周期出力の行数に上限を置く。間隔指定は結果に影響しない。

## Rationale

最小の変更でD-017とG-002の検証要求を満たす。旧経路を変えるとD-017／D-021で承認した範囲外の挙動変更になる。ボスの弾は最大1個で、player viewでは数と既存メッセージで足りるため、IDは検証用のtraceに限る。20分の実行では0.5秒周期の描画が大量になるため、間隔指定で量を制限する。

## Alternatives considered

- 旧経路にも完全なボス表示を出す：旧60秒挙動とPlayer.describeを変えるため不採択。
- 注記なしで現状維持：旧経路でボス部屋を見た利用者が表示の欠落を契約違反と誤認するため不採択。
- player viewにIDと消滅文言を出す：読み取りを増やさず、既存文言の保持（step94）を乱すため不採択。
- 長時間は`trace-every frame`のみ：20分では出力が膨大で検証に使えないため不採択。

## Revisit when

旧経路でボスを観測する利用が多く、注記では不足とわかった場合。独立QAでIDや消滅理由の不足が出た場合。20分実行で周期間隔の指定だけでは出力が扱えない場合。
