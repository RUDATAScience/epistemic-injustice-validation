# Informational Health Stress Tests: 限界状況下のシグナル消失とP値の妄想

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

本リポジトリは、アンケートや大規模データ収集における「社会的望ましさバイアス（忖度）」がもたらす情報の破壊について、極限状況の境界条件を設定した「ストレステスト」を実行するPythonシミュレーションです。

「不満が軽微であれば検知できるのではないか」「専門家のような強い確信があれば同調圧力に勝てるのではないか」「サンプル数が多ければ統計的に有意な差が見えるのではないか」というデータサイエンスの希望的観測を、数理的に完全に反証します。

## 📌 背景と問題意識 (Background)

既存のデータ分析では、マイノリティの声や異常値は「統計的ノイズ」として処理されるか、あるいは「サンプル数(N)を増やして有意差(P値)を出せば解決する」と信じられています。しかし、データ生成プロセスそのものが社会的同調圧力（忖度）で歪んでいる場合、この常識は致命的なエラーを引き起こします。

本シミュレーションは、以下の3つの絶望的な事実（ストレステスト結果）を定量的に証明します。

1. **近接シグナルの早期消滅 (Validation G)**:
   最悪の評価(1)よりも、やや不満(2)のようなマジョリティに近い「微細な問題」の方が、忖度の引力によって圧倒的に早く不可視化される。
2. **専門家の叫びの無効化 (Validation H)**:
   マイノリティが極めて高い確信度（専門家）を持ち、マジョリティが付和雷同（低い確信度）であったとしても、社会的重力が一定を超えればその声は統計的に完全に沈黙する。
3. **P値の妄想マップ (Validation I)**:
   サンプル数(N)が巨大化するほど、極微小な忖度による「歪み」であっても、既存の統計検定（t検定）はそれを「高度に有意な成功（P < 0.001）」として誤検知してしまう。

## 🧮 数理モデル (Mathematical Model)

個人の最終的な効用（U_total）を、内発的な「本音（U_true）」と外発的な「忖度（U_sontaku）」の線形結合として定義し、Softmax関数を通じて選択確率を算出します。

U_total = (1 - v2) * U_true + v2 * U_sontaku

* v2: 社会的望ましさ（忖度）の重み。0で完全な本音、1で完全な同調。
* Beta: 回答者の確信度。Softmax関数の鋭敏さを制御。Validation Hでは、マイノリティとマジョリティに非対称な確信度（Beta=10 vs Beta=2）を適用しています。

## 📊 出力される分析結果 (Outputs)

スクリプトを実行すると `harsh_stress_test_results` ディレクトリが作成され、以下の高解像度グラフ（PNG）と生データ（CSV）が生成されます。

* **Fig G: How Subtle Signals Disappear Faster**
  * 評価1（深刻な問題）と評価2（微細な問題）の消失速度の比較。微細なシグナルほど早期にマジョリティに吸収されるプロセスを可視化。
* **Fig H: Certainty (Beta=10) cannot prevent Signal Collapse**
  * 専門家集団（Beta=10）であっても、社会的圧力（v2=0.5）を超えた瞬間にシグナルが崩壊するパラドックスの証明。
* **Fig I: The Zone of Statistical Delusion (N vs v2 Heatmap)**
  * サンプルサイズNと忖度v2の二次元空間における「P値の妄想マップ」。Nが大きくなるほど、微細なバイアスを「有意な改善」として捉えてしまう統計学の欠陥を示すヒートマップ。

## 🚀 実行方法 (Usage)

本コードは **Google Colaboratory** または ローカルのPython環境で実行可能です。

1. `stress_test_sim.py`（または Jupyter Notebook形式）を実行します。
2. 計算完了後、グラフとCSVを格納した `harsh_stress_test_archive.zip` が生成されます。

### ローカル環境での実行に関する注意
ローカルのPython環境（VSCode, JupyterLab等）で実行する場合は、スクリプト内の `from google.colab import files` および、末尾のコメントアウトされている `files.download(...)` は使用せず、そのままスクリプトを実行してください。カレントディレクトリにZIPファイルが生成されます。

```bash
# 依存ライブラリのインストール
pip install -r requirements.txt

# スクリプトの実行
python stress_test_sim.py
