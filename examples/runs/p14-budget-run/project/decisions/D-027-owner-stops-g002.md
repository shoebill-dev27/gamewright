---
kind: decision
id: D-027
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-23
supersedes: none
---
# D-027: G-002を未達・検証未完了で打ち切る

## Decision

Ownerは85の案Bを選択した。G-002を未達・検証未完了として打ち切り、status: abandonedでCloseする。追加の実装・測定・評価は開かない。予算は123 operationsのままとし、追加継続予算は設定しない。実装の削除・巻戻しは行わない。

Ownerの回答原文：

> 案B。ここで打ち切ってください。理由: 残りに少なくとも 44〜48 operations が要るという見積もりは、この Goal にかけられる費用を超えます。未達・検証未完了のまま、現在の成果（連続ランと部屋 5 の単体ボス、試験 161 件）と、終わっていない検証を Outcome に正直に書いて Close してください。続きが要るかは、別の Goal として後で判断します。

現在の成果と不足をOutcomeに記録する。試験成功を独立QA・体験評価・Goal達成の代用にせず、未実施のReviewを実施済みと扱わない。歴史的一致の確認不能は、未実施・未解消の検証と区別する。

## Rationale

必須残工程の見積もり44〜48 operationsが、OwnerのこのGoalにかけられる費用を超えるため。完成や検証合格による終了ではなく、費用判断による打切りである。

## Alternatives considered

案Aの「Resume時点の実累計＋60 operations」での継続は、Ownerが費用を理由に選択しなかった。必須検証を免除して達成扱いにする案は採用しない。

## Revisit when

Ownerが続きの必要性を別Goalとして判断するとき。再開時は、その時点のビルド・未完了事項・予算を確認し、新たに範囲を定める。
