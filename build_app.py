import json
import os

print("=== Building index.html for Historic Provinces of Japan (令制国暗記トレーナー) ===")

# Load GeoJSON and Master Data
geojson_path = "G:/AI/historic-provinces-of-Japan/provinces.geojson"
master_path = "G:/AI/historic-provinces-of-Japan/provinces_master.json"

with open(geojson_path, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

with open(master_path, "r", encoding="utf-8") as f:
    master_data = json.load(f)

# Regions definition (五畿七道)
DOH_LIST = [
    {"id": "ALL", "name": "全国 (68国)", "desc": "五畿七道 68国すべてを網羅"},
    {"id": "kinai", "name": "畿内（五畿）", "filter": "畿内", "desc": "山城・大和・河内・和泉・摂津の5国"},
    {"id": "tokaido", "name": "東海道", "filter": "東海道", "desc": "伊賀から常陸まで太平洋側の15国"},
    {"id": "tosando", "name": "東山道", "filter": "東山道", "desc": "近江・信濃から奥羽（陸奥・出羽）の8国"},
    {"id": "hokurikudo", "name": "北陸道", "filter": "北陸道", "desc": "若狭・越前・加賀から越後・佐渡の7国"},
    {"id": "sanindo", "name": "山陰道", "filter": "山陰道", "desc": "丹波・丹後から出雲・石見・隠岐の8国"},
    {"id": "sanyodo", "name": "山陽道", "filter": "山陽道", "desc": "播磨から安芸・長門まで瀬戸内側の8国"},
    {"id": "nankaido", "name": "南海道", "filter": "南海道", "desc": "紀伊・淡路・四国4国の計6国"},
    {"id": "saikaido", "name": "西海道", "filter": "西海道", "desc": "九州各州および壱岐・対馬の11国"},
]

geojson_str = json.dumps(geojson_data, ensure_ascii=False, separators=(',', ':'))
master_str = json.dumps(master_data, ensure_ascii=False, separators=(',', ':'))
doh_str = json.dumps(DOH_LIST, ensure_ascii=False, separators=(',', ':'))

raw_html = '''<!DOCTYPE html>
<html lang="ja" class="h-full bg-slate-950 text-slate-100">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <title>GeoAnki 68 — 全国令制国・旧国名 視覚ベクター暗記トレーナー</title>

  <!-- 基本メタ情報 & SEO -->
  <meta name="description" content="日本の令制国（五畿七道68国：武蔵・信濃・尾張・薩摩など）を美麗な白地図ベクターポリゴンで直感暗記！場所当て・名前当て・タイピング・探索の4大モード＆苦手克服デッキ搭載。GeoGuessr・日本史・地理学習に最適なSPA Webアプリ。" />
  <meta name="keywords" content="GeoGuessr, ジオゲッサー, 旧国名, 令制国, 五畿七道, 暗記, 日本地図, 白地図, 地理, 日本史, Anki" />
  <meta name="author" content="64bitfloat" />
  <meta name="theme-color" content="#38bdf8" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

  <!-- Open Graph Protocol (OGP / Discord / SNS) -->
  <meta property="og:site_name" content="GeoAnki 68" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://64bitfloat.github.io/historic-provinces-of-Japan/" />
  <meta property="og:title" content="GeoAnki 68 — 全国令制国・旧国名 視覚ベクター暗記トレーナー" />
  <meta property="og:description" content="日本の令制国（五畿七道68国）を白地図ベクターポリゴンで直感暗記！場所当て・4択・入力・探索モード＆苦手克服デッキ搭載。GeoGuessrや地理学習特化アプリ。" />
  <meta property="og:image" content="https://opengraph.githubassets.com/1/64bitfloat/historic-provinces-of-Japan" />
  <meta property="og:locale" content="ja_JP" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="GeoAnki 68 — 全国令制国・旧国名 視覚ベクター暗記トレーナー" />
  <meta name="twitter:description" content="五畿七道68国を白地図ベクターポリゴンで直感暗記！GeoGuessr・歴史・地理学習の特訓アプリ。" />

  <!-- ファビコン（和風モダン鳥居風） -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%230284c7'/><text x='50' y='65' font-size='44' font-weight='900' fill='white' text-anchor='middle' font-family='sans-serif'>令</text></svg>" />

  <!-- Tailwind CSS (CDN) -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#f0f9ff',
              100: '#e0f2fe',
              400: '#38bdf8',
              500: '#0ea5e9',
              600: '#0284c7',
            }
          }
        }
      }
    };
  </script>

  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <style>
    html, body {
      height: 100%;
      height: 100dvh;
      overflow: hidden;
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Kaku Gothic ProN", "Yu Gothic UI", Meiryo, sans-serif;
    }
    #map {
      background: #080d1a !important;
    }
    .leaflet-container {
      background: #080d1a !important;
    }
    .leaflet-pane > svg {
      transform: translate3d(0, 0, 0);
      backface-visibility: hidden;
    }
    @keyframes pulse-gold {
      0%, 100% { fill-opacity: 0.95; stroke-width: 3.5px; fill: #fbbf24; stroke: #f59e0b; }
      50% { fill-opacity: 0.35; stroke-width: 5px; fill: #fef08a; stroke: #fbbf24; }
    }
    .polygon-pulse {
      animation: pulse-gold 1.2s infinite ease-in-out;
    }
    .no-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .no-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
    }
    ::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    ::-webkit-scrollbar-track {
      background: #0f172a;
    }
    ::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 3px;
    }
  </style>
</head>
<body class="h-full flex flex-col overflow-hidden bg-slate-950 select-none">

  <!-- ========================================== -->
  <!-- 画面A: 地域・五畿七道セレクト画面 (Hub) -->
  <!-- ========================================== -->
  <div id="screen-hub" class="flex-1 flex flex-col h-full overflow-hidden">
    <!-- Hub ヘッダー -->
    <header class="bg-slate-900/90 backdrop-blur border-b border-slate-800 px-4 py-3 shrink-0 z-10 shadow-lg">
      <div class="max-w-6xl mx-auto flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-sky-500/20 font-black text-white text-base">
            令
          </div>
          <div>
            <h1 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
              GeoAnki 68
              <span class="text-xs font-normal text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded-full border border-sky-500/20">五畿七道</span>
            </h1>
            <p class="text-xs text-slate-400 hidden sm:block">全国68令制国（旧国名）視覚ベクター暗記トレーナー</p>
          </div>
        </div>

        <!-- 総合制覇率サマリー & アクション -->
        <div class="flex items-center gap-3">
          <div class="text-right">
            <div class="text-xs text-slate-400">全国制覇数</div>
            <div class="text-sm sm:text-base font-extrabold text-sky-400">
              <span id="hub-total-cleared">0</span> <span class="text-xs font-normal text-slate-400">/ 68</span>
              <span id="hub-total-pct" class="text-xs font-semibold text-slate-300 ml-1">(0.0%)</span>
            </div>
          </div>
          <button id="btn-show-help" class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition" title="使い方ガイド">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </button>
        </div>
      </div>
    </header>

    <!-- 全国達成度プログレスバー -->
    <div class="w-full bg-slate-900/60 border-b border-slate-800/80 px-4 py-2 shrink-0">
      <div class="max-w-6xl mx-auto flex items-center gap-3">
        <div class="flex-1 bg-slate-800 h-2.5 rounded-full overflow-hidden">
          <div id="hub-progress-bar" class="bg-gradient-to-r from-sky-500 to-cyan-400 h-full w-0 transition-all duration-500"></div>
        </div>
        <div class="text-[11px] text-slate-400 whitespace-nowrap">
          制覇地域: <span id="hub-doh-completed-count" class="text-sky-400 font-bold">0</span> / 8道
        </div>
      </div>
    </div>

    <!-- 地方フィルターピルバー -->
    <div class="bg-slate-900/40 border-b border-slate-800/50 px-4 py-2.5 shrink-0 overflow-x-auto no-scrollbar">
      <div class="max-w-6xl mx-auto flex items-center gap-2" id="hub-filter-chips">
      </div>
    </div>

    <!-- 地域カードグリッド（メインスクロール領域） -->
    <main class="flex-1 overflow-y-auto px-4 py-4 overscroll-contain">
      <div class="max-w-6xl mx-auto space-y-4">
        <!-- 苦手克服クイックバナー（ミス履歴がある場合のみ出現） -->
        <div id="hub-weak-banner" class="hidden bg-gradient-to-r from-rose-950/40 to-slate-900 border border-rose-500/30 rounded-xl p-3.5 flex items-center justify-between gap-3 shadow-lg">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center font-bold text-lg shrink-0">
              ⚡
            </div>
            <div>
              <div class="text-sm font-bold text-white flex items-center gap-2">
                苦手克服特訓デッキ
                <span id="hub-weak-count-badge" class="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 text-xs font-semibold">0国</span>
              </div>
              <p class="text-xs text-slate-400 mt-0.5">直近で間違えた旧国を集中トレーニング</p>
            </div>
          </div>
          <button id="btn-start-weak-all" class="px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs sm:text-sm transition shrink-0 active:scale-95 shadow">
            復習スタート →
          </button>
        </div>

        <!-- カード一覧コンテナ -->
        <div id="hub-cards-container" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
        </div>
      </div>
    </main>
  </div>

  <!-- ========================================== -->
  <!-- 画面B: 学習・クイズ画面 (Spoke) -->
  <!-- ========================================== -->
  <div id="screen-spoke" class="hidden flex-1 flex flex-col h-full overflow-hidden relative">
    <!-- Spoke トップバー -->
    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 px-3 sm:px-4 py-2 shrink-0 z-20 flex items-center justify-between gap-2 shadow-md">
      <div class="flex items-center gap-2 sm:gap-3 min-w-0">
        <button id="btn-back-to-hub" class="p-1.5 sm:p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center gap-1 shrink-0 text-xs sm:text-sm font-bold" title="地域一覧に戻る">
          <svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
          <span class="hidden sm:inline">戻る</span>
        </button>

        <div class="min-w-0">
          <div class="flex items-center gap-1.5">
            <h2 id="spoke-region-title" class="text-sm sm:text-base font-extrabold text-white truncate">東海道</h2>
            <span id="spoke-region-count-badge" class="text-[10px] sm:text-xs font-semibold px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-400 border border-sky-500/30 shrink-0">15国</span>
          </div>
          <div class="flex items-center gap-2 text-[11px] text-slate-400 mt-0.5">
            <span>進捗: <strong id="spoke-progress-text" class="text-slate-200">1 / 15</strong></span>
            <span class="text-slate-600">|</span>
            <span id="spoke-accuracy-tag" class="text-slate-400">正答率: --%</span>
          </div>
        </div>
      </div>

      <!-- 右側アクション（音声トグル・全域リセット・ヒント） -->
      <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
        <button id="btn-sound-toggle" class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sky-400 transition" title="効果音オン/オフ">
          <svg id="icon-sound-on" class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
          <svg id="icon-sound-off" class="w-4 h-4 sm:w-5 sm:h-5 hidden text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z m12 0l-6-6m0 6l6-6"/></svg>
        </button>
        <button id="btn-fit-bounds" class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-semibold transition flex items-center gap-1" title="全体を表示">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/></svg>
          <span class="hidden sm:inline">全域</span>
        </button>
      </div>
    </header>

    <!-- レベル切り替えタブ ＆ モード切り替えバー -->
    <div class="bg-slate-900/90 border-b border-slate-800 px-3 py-1.5 shrink-0 flex flex-wrap items-center justify-between gap-2 z-10">
      <!-- 難易度レベル -->
      <div class="flex items-center gap-1 overflow-x-auto no-scrollbar" id="level-tabs">
        <button data-level="1" class="level-btn px-2.5 py-1 rounded-md text-xs font-bold bg-sky-600 text-white transition">Lv.1</button>
        <button data-level="2" class="level-btn px-2.5 py-1 rounded-md text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700 transition">Lv.2</button>
        <button data-level="3" class="level-btn px-2.5 py-1 rounded-md text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700 transition">Lv.3</button>
        <button data-level="4" class="level-btn px-2.5 py-1 rounded-md text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700 transition">Lv.4</button>
        <button data-level="ALL" class="level-btn px-2.5 py-1 rounded-md text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700 transition">全難易度</button>
        <button data-level="WEAK" class="level-btn px-2.5 py-1 rounded-md text-xs font-bold bg-slate-800 text-rose-400 hover:bg-slate-700 transition flex items-center gap-1">
          <span>苦手</span>
          <span id="level-weak-badge" class="text-[10px] bg-rose-500/20 px-1 rounded-full">0</span>
        </button>
      </div>

      <!-- モード切り替えピル -->
      <div class="flex items-center bg-slate-800/80 p-0.5 rounded-lg border border-slate-700/60" id="mode-pills">
        <button data-mode="locate" class="mode-btn px-2.5 py-1 rounded-md text-xs font-bold bg-sky-500 text-white transition flex items-center gap-1">
          <span>📍 場所当て</span>
        </button>
        <button data-mode="name" class="mode-btn px-2.5 py-1 rounded-md text-xs font-bold text-slate-300 hover:text-white transition flex items-center gap-1">
          <span>🏷️ 名前当て</span>
        </button>
        <button data-mode="type" class="mode-btn px-2.5 py-1 rounded-md text-xs font-bold text-slate-300 hover:text-white transition flex items-center gap-1">
          <span>⌨️ 入力</span>
        </button>
        <button data-mode="explore" class="mode-btn px-2.5 py-1 rounded-md text-xs font-bold text-slate-300 hover:text-white transition flex items-center gap-1">
          <span>🔍 探索</span>
        </button>
      </div>
    </div>

    <!-- 地図コンテナ -->
    <div id="map" class="flex-1 w-full h-full relative"></div>

    <!-- 地図上オーバーレイ：ヒントポップアップ（必要時） -->
    <div id="hint-bubble" class="hidden absolute top-2 left-1/2 -translate-x-1/2 z-[500] max-w-sm w-11/12 bg-slate-900/95 border border-sky-500/40 rounded-xl p-3 shadow-2xl backdrop-blur text-xs sm:text-sm text-slate-200">
      <div class="flex items-center justify-between gap-2 border-b border-slate-800 pb-1.5 mb-1.5">
        <div class="font-bold text-sky-400 flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <span>ヒント情報</span>
        </div>
        <button id="btn-close-hint" class="text-slate-400 hover:text-white text-base leading-none">&times;</button>
      </div>
      <div id="hint-content"></div>
    </div>

    <!-- 下部コントロールパネル（モード毎に出し分け） -->
    <footer class="bg-slate-900/95 backdrop-blur border-t border-slate-800 p-3 sm:p-4 shrink-0 z-20 min-h-[110px] flex flex-col justify-center">
      
      <!-- ① 場所当てモード (locate) -->
      <div id="panel-locate" class="space-y-2">
        <div class="flex items-center justify-between gap-2">
          <div>
            <div class="text-[11px] text-sky-400 font-semibold">【場所当て】地図上の該当エリアをタップしてください</div>
            <div class="text-base sm:text-lg font-black text-white flex items-center gap-2">
              <span id="target-locate-name" class="text-sky-300 text-lg sm:text-xl">武蔵</span>
              <span id="target-locate-kana" class="text-xs sm:text-sm font-normal text-slate-400">（むさし）</span>
            </div>
          </div>
          <button id="btn-toggle-hint" class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-sky-400 hover:text-sky-300 text-xs font-bold transition flex items-center gap-1 border border-slate-700">
            <span>💡 ヒント</span>
          </button>
        </div>
      </div>

      <!-- ② 名前当てモード (name: 4択ボタン) -->
      <div id="panel-name" class="hidden space-y-2">
        <div class="flex items-center justify-between text-xs">
          <div class="text-slate-300 font-semibold flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping inline-block"></span>
            黄色く光っている旧国の名称を選択してください:
          </div>
          <div class="text-slate-400 hidden sm:block">キーボード [1] [2] [3] [4] でも回答可</div>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2" id="choice-buttons-grid">
        </div>
      </div>

      <!-- ③ 入力モード (type) -->
      <div id="panel-type" class="hidden space-y-2">
        <div class="text-xs text-slate-300 font-semibold flex items-center gap-1.5">
          <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping inline-block"></span>
          黄色く光っている旧国の名称（漢字またはひらがな）を入力:
        </div>
        <form id="form-type-answer" class="flex items-center gap-2" onsubmit="return false;">
          <input type="text" id="input-type-answer" placeholder="例: むさし または 武蔵" autocomplete="off" autocorrect="off" spellcheck="false" class="flex-1 bg-slate-800 border border-slate-700 focus:border-sky-500 rounded-xl px-3.5 py-2 text-sm sm:text-base text-white focus:outline-none transition shadow-inner" />
          <button type="submit" id="btn-submit-type" class="px-4 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm transition shrink-0 active:scale-95 shadow">
            決定 ↵
          </button>
        </form>
      </div>

      <!-- ④ 探索モード (explore) -->
      <div id="panel-explore" class="hidden">
        <div id="explore-empty-state" class="text-center py-2 text-xs text-slate-400">
          地図上の旧国ポリゴンをタップすると詳細情報（読み・現在の都道府県・名所）が表示されます
        </div>
        <div id="explore-detail-state" class="hidden flex items-start justify-between gap-3">
          <div class="min-w-0">
            <div class="flex items-center gap-2">
              <span id="explore-name" class="text-lg font-black text-white">武蔵</span>
              <span id="explore-kana" class="text-xs text-slate-400">（むさし）</span>
              <span id="explore-doh-badge" class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-400 border border-sky-500/30">東海道</span>
              <span id="explore-lvl-badge" class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300">Lv.1</span>
            </div>
            <div class="text-xs text-slate-300 mt-1">
              現代の地域: <strong id="explore-pref" class="text-sky-300">東京都・埼玉県・神奈川県北東部</strong>
            </div>
            <div id="explore-desc" class="text-[11px] text-slate-400 mt-0.5 truncate">
              江戸・東京、武蔵野、さいたま
            </div>
          </div>
          <div class="text-right shrink-0" id="explore-status-tag">
          </div>
        </div>
      </div>

      <!-- フィードバックバー（正解/不正解時のオーバーレイ） -->
      <div id="feedback-bar" class="hidden mt-2 p-2.5 rounded-xl border flex items-center justify-between gap-2 shadow-lg transition-all">
        <div id="feedback-content" class="flex-1 text-xs sm:text-sm font-semibold"></div>
      </div>
    </footer>
  </div>

  <!-- ========================================== -->
  <!-- 全問完了モーダル (Stage Complete Popup) -->
  <!-- ========================================== -->
  <div id="modal-stage-complete" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
    <div class="bg-gradient-to-b from-slate-900 to-slate-950 border border-sky-500/40 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-5 text-center relative overflow-hidden">
      <!-- 装飾用背景グロー -->
      <div class="absolute -top-16 -left-16 w-36 h-36 bg-sky-500/15 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -bottom-16 -right-16 w-36 h-36 bg-amber-500/15 rounded-full blur-3xl pointer-events-none"></div>

      <!-- トロフィーアイコン -->
      <div class="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-tr from-amber-500 to-yellow-300 flex items-center justify-center text-3xl shadow-xl shadow-amber-500/25">
        🏆
      </div>

      <!-- タイトル -->
      <div>
        <h3 class="text-xl font-black text-white flex items-center justify-center gap-1.5">
          特訓ステージクリア！
        </h3>
        <p id="complete-modal-subtitle" class="text-xs sm:text-sm text-sky-400 font-semibold mt-1">東海道（Level 1）全問終了！</p>
      </div>

      <!-- 成績カード -->
      <div class="bg-slate-800/70 border border-slate-700/60 rounded-xl p-4 grid grid-cols-2 gap-3 text-left">
        <div>
          <div class="text-[11px] text-slate-400">今回の出題数</div>
          <div class="text-base sm:text-lg font-bold text-white mt-0.5">
            <span id="complete-modal-total-questions">15</span> <span class="text-xs font-normal text-slate-400">国</span>
          </div>
        </div>
        <div>
          <div class="text-[11px] text-slate-400">地域の制覇状況</div>
          <div class="text-base sm:text-lg font-bold text-emerald-400 mt-0.5">
            <span id="complete-modal-region-cleared">15</span> <span class="text-xs font-normal text-slate-400">/ <span id="complete-modal-region-total">15</span></span>
          </div>
        </div>
        <div class="col-span-2 pt-2 border-t border-slate-700/60 flex items-center justify-between">
          <div class="text-[11px] text-slate-400">全国制覇数:</div>
          <div class="text-xs font-bold text-sky-300">
            <span id="complete-modal-total-cleared">0</span> / 68 国 (<span id="complete-modal-total-pct">0.0%</span>)
          </div>
        </div>
      </div>

      <!-- アクションボタン -->
      <div class="space-y-2 pt-1">
        <button id="btn-complete-retry" class="w-full py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm transition shadow-lg shadow-sky-600/20 active:scale-98 flex items-center justify-center gap-2">
          <span>🔄 もう一度特訓する（シャッフル）</span>
        </button>
        <button id="btn-complete-next-level" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white font-bold text-sm transition border border-slate-700 active:scale-98 flex items-center justify-center gap-2">
          <span id="complete-next-level-label">⭐ 次の難易度に進む</span>
        </button>
        <button id="btn-complete-hub" class="w-full py-2 rounded-xl bg-transparent hover:bg-slate-800/60 text-slate-400 hover:text-slate-200 font-semibold text-xs transition">
          ← 地域選択（トップ）に戻る
        </button>
      </div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- ヘルプモーダル -->
  <!-- ========================================== -->
  <div id="modal-help" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-5 shadow-2xl space-y-4 max-h-[85vh] overflow-y-auto">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 class="text-base font-bold text-white flex items-center gap-2">
          <span class="w-6 h-6 rounded-lg bg-sky-500/20 text-sky-400 flex items-center justify-center text-xs font-black">?</span>
          GeoAnki 68 の使い方ガイド
        </h3>
        <button id="btn-close-help" class="text-slate-400 hover:text-white text-xl leading-none">&times;</button>
      </div>

      <div class="space-y-3 text-xs sm:text-sm text-slate-300 leading-relaxed">
        <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700/50">
          <div class="font-bold text-sky-400 mb-1">🏛️ 令制国（旧国名）とは？</div>
          <p class="text-xs text-slate-300">
            日本の律令制に基づいて定められた古代〜幕末までの行政区分です。「五畿七道（68国）」はGeoGuessrでの地域絞り込みや日本史・地理の基礎知識として幅広く活用されています。
          </p>
        </div>

        <div class="space-y-2">
          <div class="font-bold text-white">🎯 4つの学習モード</div>
          <ul class="space-y-1.5 list-disc list-inside text-xs text-slate-300">
            <li><strong class="text-sky-300">📍 場所当てモード:</strong> 出題された国名の位置を、地図上のポリゴンをタップして回答します。</li>
            <li><strong class="text-sky-300">🏷️ 名前当てモード:</strong> 地図上で黄色く点滅する旧国の名称を4択ボタンから選びます（数字キー 1〜4 対応）。</li>
            <li><strong class="text-sky-300">⌨️ 入力モード:</strong> 点滅する旧国名をキーボード（ひらがな/漢字）で入力します。</li>
            <li><strong class="text-sky-300">🔍 探索モード:</strong> 地図を自由にタップして各国の読み、現代の都道府県、名所ヒントを閲覧できます。</li>
          </ul>
        </div>

        <div class="space-y-2">
          <div class="font-bold text-white">⭐ 難易度レベル</div>
          <ul class="space-y-1 text-xs text-slate-300">
            <li><span class="text-sky-400 font-bold">Lv.1</span>: 武蔵・信濃・尾張・薩摩など超有名・必修の15国</li>
            <li><span class="text-sky-400 font-bold">Lv.2</span>: 三河・美濃・伊勢・越前など基本の21国</li>
            <li><span class="text-sky-400 font-bold">Lv.3</span>: 遠江・但馬・備中・肥前など差がつく24国</li>
            <li><span class="text-sky-400 font-bold">Lv.4</span>: 志摩・若狭・隠岐・対馬など難関の8国</li>
          </ul>
        </div>

        <div class="border-t border-slate-800 pt-3">
          <button id="btn-reset-data" class="w-full py-2 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 text-xs font-bold transition">
            ⚠️ 学習記録・制覇データを初期化
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- トースト通知 -->
  <!-- ========================================== -->
  <div id="toast" class="hidden fixed bottom-20 left-1/2 -translate-x-1/2 z-50 bg-slate-900 border border-slate-700 text-white text-xs sm:text-sm px-4 py-2 rounded-xl shadow-2xl pointer-events-none transition-all"></div>

  <!-- ========================================== -->
  <!-- アプリケーションスクリプト -->
  <!-- ========================================== -->
  <script>
    /* ========================================================
       マスターデータ埋め込み
       ======================================================== */
    const GEOJSON_DATA = __GEOJSON_PLACEHOLDER__;
    const PROVINCES = __MASTER_PLACEHOLDER__;
    const DOH_LIST = __DOH_PLACEHOLDER__;

    const PROV_LIST = Object.values(PROVINCES);

    /* ========================================================
       Web Audio API 効果音シンセサイザー
       ======================================================== */
    class SoundFX {
      constructor() {
        this.ctx = null;
        this.enabled = true;
      }
      init() {
        if (!this.ctx) {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          if (AudioContext) {
            try {
              this.ctx = new AudioContext();
            } catch(e) {}
          }
        }
      }
      playCorrect() {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;
        if (this.ctx.state === 'suspended') this.ctx.resume();
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(523.25, now); // C5
        osc.frequency.setValueAtTime(659.25, now + 0.08); // E5
        osc.frequency.setValueAtTime(783.99, now + 0.16); // G5
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.35);
      }
      playWrong() {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;
        if (this.ctx.state === 'suspended') this.ctx.resume();
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(160, now);
        osc.frequency.setValueAtTime(130, now + 0.1);
        gain.gain.setValueAtTime(0.14, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.3);
      }
      playFanfare() {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;
        if (this.ctx.state === 'suspended') this.ctx.resume();
        const now = this.ctx.currentTime;
        const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
        notes.forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(freq, now + idx * 0.1);
          gain.gain.setValueAtTime(0.16, now + idx * 0.1);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.1 + 0.4);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(now + idx * 0.1);
          osc.stop(now + idx * 0.1 + 0.45);
        });
      }
      toggle() {
        this.enabled = !this.enabled;
        return this.enabled;
      }
    }
    const sound = new SoundFX();

    /* ========================================================
       LocalStorage 学習履歴ストア
       ======================================================== */
    const STORAGE_KEY = 'geoanki_provinces_v1';
    class Store {
      static load() {
        try {
          const raw = localStorage.getItem(STORAGE_KEY);
          return raw ? JSON.parse(raw) : { records: {} };
        } catch(e) {
          return { records: {} };
        }
      }
      static save(data) {
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        } catch(e) {}
      }
      static recordAnswer(code, isCorrect) {
        const data = this.load();
        if (!data.records[code]) {
          data.records[code] = { correct: 0, wrong: 0, last: null, ts: Date.now() };
        }
        const r = data.records[code];
        if (isCorrect) {
          r.correct = (r.correct || 0) + 1;
          r.last = 'correct';
        } else {
          r.wrong = (r.wrong || 0) + 1;
          r.last = 'wrong';
        }
        r.ts = Date.now();
        this.save(data);
      }
      static getRecord(code) {
        const data = this.load();
        return data.records[code] || null;
      }
      static getTotalCleared() {
        const data = this.load();
        let c = 0;
        PROV_LIST.forEach(p => {
          const r = data.records[p.code];
          if (r && r.correct > 0) c++;
        });
        return c;
      }
      static getDohCleared(dohName) {
        const data = this.load();
        let c = 0;
        PROV_LIST.filter(p => p.doh === dohName).forEach(p => {
          const r = data.records[p.code];
          if (r && r.correct > 0) c++;
        });
        return c;
      }
      static getWeakList(dohFilter = 'ALL') {
        const data = this.load();
        return PROV_LIST.filter(p => {
          if (dohFilter !== 'ALL' && p.doh !== dohFilter) return false;
          const r = data.records[p.code];
          return r && (r.wrong > 0 && r.last === 'wrong');
        });
      }
      static resetAll() {
        localStorage.removeItem(STORAGE_KEY);
      }
    }

    /* ========================================================
       アプリケーション状態管理
       ======================================================== */
    const state = {
      currentScreen: 'hub', // 'hub' | 'spoke'
      selectedDoh: 'ALL', // 'ALL' or '畿内', '東海道' etc.
      selectedLevel: '1', // '1' | '2' | '3' | '4' | 'ALL' | 'WEAK'
      currentMode: 'locate', // 'locate' | 'name' | 'type' | 'explore'
      activeQuestionList: [],
      currentIndex: 0,
      currentQuestion: null,
      currentChoices: [],
      map: null,
      geoJsonLayer: null,
      provLayerMap: {}, // code -> [layer]
      isAnswering: false,
      feedbackTimer: null,
    };

    /* ========================================================
       Hub 画面 (地域セレクト) ロジック
       ======================================================== */
    function initHub() {
      renderHubHeaderSummary();
      renderFilterChips();
      renderHubCards('ALL');

      // ヘルプモーダル
      const modal = document.getElementById('modal-help');
      document.getElementById('btn-show-help').onclick = () => modal.classList.remove('hidden');
      document.getElementById('btn-close-help').onclick = () => modal.classList.add('hidden');
      modal.onclick = (e) => { if (e.target === modal) modal.classList.add('hidden'); };

      // データリセット
      document.getElementById('btn-reset-data').onclick = () => {
        if (confirm('すべての旧国の正答履歴・制覇記録をリセットしますか？')) {
          Store.resetAll();
          modal.classList.add('hidden');
          renderHubHeaderSummary();
          renderHubCards(state.selectedDoh);
          showToast('学習データを初期化しました');
        }
      };

      // 苦手全問復習ボタン
      document.getElementById('btn-start-weak-all').onclick = () => {
        startStudy('ALL', 'WEAK');
      };
    }

    function renderHubHeaderSummary() {
      const cleared = Store.getTotalCleared();
      const total = 68;
      const pct = ((cleared / total) * 100).toFixed(1);

      document.getElementById('hub-total-cleared').textContent = cleared;
      document.getElementById('hub-total-pct').textContent = '(' + pct + '%)';
      document.getElementById('hub-progress-bar').style.width = pct + '%';

      // 制覇地域カウント
      let dohClearedCount = 0;
      DOH_LIST.filter(d => d.filter).forEach(d => {
        const dTotal = PROV_LIST.filter(p => p.doh === d.filter).length;
        const dCleared = Store.getDohCleared(d.filter);
        if (dTotal > 0 && dCleared === dTotal) dohClearedCount++;
      });
      document.getElementById('hub-doh-completed-count').textContent = dohClearedCount;

      // 苦手バナー
      const weakList = Store.getWeakList('ALL');
      const weakBanner = document.getElementById('hub-weak-banner');
      if (weakList.length > 0) {
        weakBanner.classList.remove('hidden');
        document.getElementById('hub-weak-count-badge').textContent = weakList.length + '国';
      } else {
        weakBanner.classList.add('hidden');
      }
    }

    function renderFilterChips() {
      const container = document.getElementById('hub-filter-chips');
      container.innerHTML = '';

      const filters = [
        { label: 'すべて', val: 'ALL' },
        { label: '畿内', val: '畿内' },
        { label: '東海道', val: '東海道' },
        { label: '東山道', val: '東山道' },
        { label: '北陸道', val: '北陸道' },
        { label: '山陰道', val: '山陰道' },
        { label: '山陽道', val: '山陽道' },
        { label: '南海道', val: '南海道' },
        { label: '西海道', val: '西海道' }
      ];

      filters.forEach(f => {
        const btn = document.createElement('button');
        btn.className = 'filter-chip px-3 py-1.5 rounded-full text-xs font-bold transition whitespace-nowrap ' + 
          (f.val === 'ALL' ? 'bg-sky-500 text-white shadow-md shadow-sky-500/20' : 'bg-slate-800 text-slate-300 hover:bg-slate-700');
        btn.textContent = f.label;
        btn.onclick = () => {
          document.querySelectorAll('.filter-chip').forEach(b => {
            b.classList.remove('bg-sky-500', 'text-white', 'shadow-md', 'shadow-sky-500/20');
            b.classList.add('bg-slate-800', 'text-slate-300');
          });
          btn.classList.add('bg-sky-500', 'text-white', 'shadow-md', 'shadow-sky-500/20');
          btn.classList.remove('bg-slate-800', 'text-slate-300');
          renderHubCards(f.val);
        };
        container.appendChild(btn);
      });
    }

    function renderHubCards(filterVal) {
      const container = document.getElementById('hub-cards-container');
      container.innerHTML = '';

      let list = DOH_LIST;
      if (filterVal !== 'ALL') {
        list = DOH_LIST.filter(d => d.filter === filterVal);
      }

      list.forEach(d => {
        const card = document.createElement('div');
        card.className = 'group bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-sky-500/50 rounded-2xl p-4 transition-all duration-200 cursor-pointer shadow-lg hover:shadow-sky-500/10 flex flex-col justify-between';

        const isAll = d.id === 'ALL';
        const provs = isAll ? PROV_LIST : PROV_LIST.filter(p => p.doh === d.filter);
        const total = provs.length;
        const cleared = isAll ? Store.getTotalCleared() : Store.getDohCleared(d.filter);
        const pct = total > 0 ? ((cleared / total) * 100).toFixed(0) : 0;
        const isComplete = cleared === total && total > 0;

        let chipsHtml = provs.slice(0, 8).map(p => {
          return '<span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800/80 text-slate-300 font-medium">' + p.name + '</span>';
        }).join('');
        if (provs.length > 8) {
          chipsHtml += '<span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800/80 text-slate-500 font-medium">+' + (provs.length - 8) + '国</span>';
        }

        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full ` + (isComplete ? 'bg-emerald-400 ring-2 ring-emerald-500/30' : 'bg-sky-400') + `"></span>
                <h4 class="text-base font-extrabold text-white group-hover:text-sky-300 transition">` + d.name + `</h4>
              </div>
              <span class="text-xs font-bold px-2 py-0.5 rounded-full ` + (isComplete ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-slate-800 text-slate-300') + `">
                ` + cleared + ` / ` + total + ` (` + pct + `%)
              </span>
            </div>
            <p class="text-xs text-slate-400 mt-1">` + d.desc + `</p>
            
            <div class="flex flex-wrap gap-1 mt-3">
              ` + chipsHtml + `
            </div>
          </div>

          <div class="mt-4 pt-3 border-t border-slate-800/80">
            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
              <div class="bg-gradient-to-r ` + (isComplete ? 'from-emerald-500 to-teal-400' : 'from-sky-500 to-cyan-400') + ` h-full transition-all duration-300" style="width: ` + pct + `%"></div>
            </div>
            <div class="mt-2.5 flex items-center justify-between text-xs">
              <span class="text-slate-500 group-hover:text-sky-400 font-semibold transition">特訓を開始する</span>
              <span class="text-slate-400 group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        `;

        card.onclick = () => {
          startStudy(isAll ? 'ALL' : d.filter, '1');
        };

        container.appendChild(card);
      });
    }

    /* ========================================================
       Spoke 画面 (学習・クイズ) ロジック
       ======================================================== */
    function startStudy(dohFilter, initialLevel = '1') {
      state.selectedDoh = dohFilter;
      state.selectedLevel = initialLevel;
      state.currentScreen = 'spoke';

      document.getElementById('screen-hub').classList.add('hidden');
      document.getElementById('screen-spoke').classList.remove('hidden');

      // タイトル更新
      const dohObj = DOH_LIST.find(d => d.filter === dohFilter || (dohFilter === 'ALL' && d.id === 'ALL'));
      const dohTitle = dohObj ? dohObj.name : dohFilter;
      const targetProvs = dohFilter === 'ALL' ? PROV_LIST : PROV_LIST.filter(p => p.doh === dohFilter);

      document.getElementById('spoke-region-title').textContent = dohTitle;
      document.getElementById('spoke-region-count-badge').textContent = targetProvs.length + '国';

      // Leaflet 地図初期化
      if (!state.map) {
        initMap();
      } else {
        setTimeout(() => {
          state.map.invalidateSize();
          fitTargetBounds();
        }, 50);
      }

      setupLevelButtons();
      setupModeButtons();
      loadLevelDeck(state.selectedLevel);
    }

    /* ========================================================
       出題対象判定 & ポリゴンスタイル（出題範囲外グレーアウト）
       ======================================================== */
    function isProvTargetInCurrentStage(code) {
      const p = PROVINCES[code];
      if (!p) return false;
      // 選択中の地域（五畿七道）に含まれない場合は対象外
      if (state.selectedDoh !== 'ALL' && p.doh !== state.selectedDoh) {
        return false;
      }
      // 探索モード または 'ALL' の場合はすべて対象
      if (state.currentMode === 'explore' || state.selectedLevel === 'ALL') {
        return true;
      }
      // 苦手復習（WEAK）の場合
      if (state.selectedLevel === 'WEAK') {
        const weakList = Store.getWeakList(state.selectedDoh);
        return weakList.some(w => w.code === code);
      }
      // Level 1〜4 の場合
      return p.lvl === parseInt(state.selectedLevel, 10);
    }

    function getProvNormalStyle(code) {
      const isTarget = isProvTargetInCurrentStage(code);
      if (!isTarget) {
        // 出題範囲外: 暗いグレーアウト（背景に沈む半透明スレート）
        return {
          fillColor: '#1e293b',
          fillOpacity: 0.35,
          color: '#334155',
          weight: 1.0,
          opacity: 0.45
        };
      }
      // 出題範囲内: 白地図スタイル（清潔な白〜明灰でくっきり浮き立つ）
      return {
        fillColor: '#e2e8f0',
        fillOpacity: 0.92,
        color: '#475569',
        weight: 1.5,
        opacity: 1
      };
    }

    function updateAllPolygonStyles() {
      Object.keys(state.provLayerMap).forEach(code => {
        const layers = state.provLayerMap[code];
        if (!layers) return;
        const style = getProvNormalStyle(code);
        layers.forEach(l => {
          if (l._path) l._path.classList.remove('polygon-pulse');
          l.setStyle(style);
        });
      });
    }

    function initMap() {
      state.map = L.map('map', {
        center: [36.5, 138.0],
        zoom: 6,
        minZoom: 4,
        maxZoom: 12,
        zoomControl: false,
        attributionControl: false
      });

      L.control.zoom({ position: 'topright' }).addTo(state.map);

      // GeoJSON レイヤー描画
      state.provLayerMap = {};
      state.geoJsonLayer = L.geoJSON(GEOJSON_DATA, {
        style: (feature) => getProvNormalStyle(feature.properties.code),
        onEachFeature: (feature, layer) => {
          const p = feature.properties;
          if (!state.provLayerMap[p.code]) {
            state.provLayerMap[p.code] = [];
          }
          state.provLayerMap[p.code].push(layer);

          layer.on({
            mouseover: (e) => onPolygonHover(e, p.code),
            mouseout: (e) => onPolygonOut(e, p.code),
            click: () => onPolygonClick(p.code)
          });
        }
      }).addTo(state.map);

      fitTargetBounds();
    }

    function highlightPolygon(code, type) {
      const layers = state.provLayerMap[code];
      if (!layers) return;

      layers.forEach(l => {
        if (type === 'question') {
          l.setStyle({
            fillColor: '#facc15',
            fillOpacity: 0.88,
            color: '#eab308',
            weight: 3.5,
            opacity: 1
          });
          if (l._path) l._path.classList.add('polygon-pulse');
        } else if (type === 'correct') {
          if (l._path) l._path.classList.remove('polygon-pulse');
          l.setStyle({
            fillColor: '#10b981',
            fillOpacity: 0.9,
            color: '#34d399',
            weight: 3,
            opacity: 1
          });
        } else if (type === 'wrong') {
          if (l._path) l._path.classList.remove('polygon-pulse');
          l.setStyle({
            fillColor: '#ef4444',
            fillOpacity: 0.9,
            color: '#f87171',
            weight: 3,
            opacity: 1
          });
        } else if (type === 'hover') {
          l.setStyle({
            fillColor: '#38bdf8',
            fillOpacity: 0.75,
            color: '#7dd3fc',
            weight: 2.2
          });
        } else {
          if (l._path) l._path.classList.remove('polygon-pulse');
          l.setStyle(getProvNormalStyle(code));
        }
      });
    }

    function resetAllHighlights() {
      Object.keys(state.provLayerMap).forEach(code => {
        highlightPolygon(code, 'reset');
      });
    }

    function onPolygonHover(e, code) {
      if (state.currentMode === 'explore') {
        highlightPolygon(code, 'hover');
      } else if (state.currentMode === 'locate' && !state.isAnswering) {
        if (isProvTargetInCurrentStage(code)) {
          const layers = state.provLayerMap[code];
          if (layers) layers.forEach(l => l.setStyle({ weight: 2.4, color: '#0284c7' }));
        }
      }
    }

    function onPolygonOut(e, code) {
      if (state.currentMode === 'explore') {
        highlightPolygon(code, 'reset');
      } else if (state.currentMode === 'locate' && !state.isAnswering) {
        const layers = state.provLayerMap[code];
        if (layers) layers.forEach(l => l.setStyle(getProvNormalStyle(code)));
      }
    }

    function fitTargetBounds() {
      if (!state.map || !state.geoJsonLayer) return;

      if (state.selectedDoh === 'ALL') {
        state.map.fitBounds(state.geoJsonLayer.getBounds(), { padding: [20, 20] });
      } else {
        const targetProvs = PROV_LIST.filter(p => p.doh === state.selectedDoh);
        const group = new L.FeatureGroup();
        targetProvs.forEach(p => {
          const layers = state.provLayerMap[p.code];
          if (layers) layers.forEach(l => group.addLayer(l));
        });
        if (group.getLayers().length > 0) {
          state.map.fitBounds(group.getBounds(), { padding: [35, 35] });
        } else {
          state.map.fitBounds(state.geoJsonLayer.getBounds(), { padding: [20, 20] });
        }
      }
    }

    /* ========================================================
       レベル ＆ モード切り替え
       ======================================================== */
    function setupLevelButtons() {
      const weakList = Store.getWeakList(state.selectedDoh);
      document.getElementById('level-weak-badge').textContent = weakList.length;

      document.querySelectorAll('.level-btn').forEach(btn => {
        btn.onclick = () => {
          document.querySelectorAll('.level-btn').forEach(b => {
            b.classList.remove('bg-sky-600', 'text-white');
            b.classList.add('bg-slate-800', 'text-slate-300');
          });
          btn.classList.add('bg-sky-600', 'text-white');
          btn.classList.remove('bg-slate-800', 'text-slate-300');

          loadLevelDeck(btn.dataset.level);
        };
      });
    }

    function setupModeButtons() {
      document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.onclick = () => {
          document.querySelectorAll('.mode-btn').forEach(b => {
            b.classList.remove('bg-sky-500', 'text-white');
            b.classList.add('text-slate-300');
          });
          btn.classList.add('bg-sky-500', 'text-white');
          btn.classList.remove('text-slate-300');

          setMode(btn.dataset.mode);
        };
      });
    }

    function setMode(newMode) {
      state.currentMode = newMode;
      resetAllHighlights();
      clearTimeout(state.feedbackTimer);
      state.isAnswering = false;

      document.getElementById('panel-locate').classList.add('hidden');
      document.getElementById('panel-name').classList.add('hidden');
      document.getElementById('panel-type').classList.add('hidden');
      document.getElementById('panel-explore').classList.add('hidden');
      document.getElementById('feedback-bar').classList.add('hidden');
      document.getElementById('hint-bubble').classList.add('hidden');

      updateAllPolygonStyles();

      if (newMode === 'locate') {
        document.getElementById('panel-locate').classList.remove('hidden');
        renderCurrentQuestion();
      } else if (newMode === 'name') {
        document.getElementById('panel-name').classList.remove('hidden');
        renderCurrentQuestion();
      } else if (newMode === 'type') {
        document.getElementById('panel-type').classList.remove('hidden');
        renderCurrentQuestion();
        setTimeout(() => document.getElementById('input-type-answer').focus(), 50);
      } else if (newMode === 'explore') {
        document.getElementById('panel-explore').classList.remove('hidden');
        document.getElementById('explore-empty-state').classList.remove('hidden');
        document.getElementById('explore-detail-state').classList.add('hidden');
      }
    }

    /* ========================================================
       問題デッキ構築 ＆ 出題ループ
       ======================================================== */
    function loadLevelDeck(levelStr) {
      state.selectedLevel = levelStr;
      let pool = state.selectedDoh === 'ALL' ? [...PROV_LIST] : PROV_LIST.filter(p => p.doh === state.selectedDoh);

      if (levelStr === 'WEAK') {
        pool = Store.getWeakList(state.selectedDoh);
        if (pool.length === 0) {
          showToast('苦手な旧国はありません！ 全問正解または未解答です。');
          pool = state.selectedDoh === 'ALL' ? [...PROV_LIST] : PROV_LIST.filter(p => p.doh === state.selectedDoh);
        }
      } else if (levelStr !== 'ALL') {
        const targetLvl = parseInt(levelStr, 10);
        pool = pool.filter(p => p.lvl === targetLvl);
        if (pool.length === 0) {
          pool = state.selectedDoh === 'ALL' ? [...PROV_LIST] : PROV_LIST.filter(p => p.doh === state.selectedDoh);
        }
      }

      pool.sort(() => Math.random() - 0.5);
      state.activeQuestionList = pool;
      state.currentIndex = 0;

      updateAllPolygonStyles();
      renderCurrentQuestion();
    }

    function renderCurrentQuestion() {
      resetAllHighlights();
      clearTimeout(state.feedbackTimer);
      state.isAnswering = false;
      document.getElementById('feedback-bar').classList.add('hidden');
      document.getElementById('hint-bubble').classList.add('hidden');

      if (state.activeQuestionList.length === 0) return;

      // 全問終了チェック：ポップアップを表示して待機
      if (state.currentIndex >= state.activeQuestionList.length) {
        showStageCompleteModal();
        return;
      }

      const target = state.activeQuestionList[state.currentIndex];
      state.currentQuestion = target;

      document.getElementById('spoke-progress-text').textContent = (state.currentIndex + 1) + ' / ' + state.activeQuestionList.length;
      updateAccuracyTag();

      if (state.currentMode === 'locate') {
        document.getElementById('target-locate-name').textContent = target.name;
        document.getElementById('target-locate-kana').textContent = '（' + target.kana + '）';
      } else if (state.currentMode === 'name') {
        highlightPolygon(target.code, 'question');
        generateChoiceButtons(target);
      } else if (state.currentMode === 'type') {
        highlightPolygon(target.code, 'question');
        const input = document.getElementById('input-type-answer');
        input.value = '';
        setTimeout(() => input.focus(), 50);
      }
    }

    /* ========================================================
       全問完了ポップアップ制御
       ======================================================== */
    function showStageCompleteModal() {
      sound.playFanfare();

      const modal = document.getElementById('modal-stage-complete');
      const dohObj = DOH_LIST.find(d => d.filter === state.selectedDoh || (state.selectedDoh === 'ALL' && d.id === 'ALL'));
      const dohTitle = dohObj ? dohObj.name : state.selectedDoh;

      let lvlName = '全難易度';
      if (state.selectedLevel === 'WEAK') lvlName = '苦手克服';
      else if (state.selectedLevel !== 'ALL') lvlName = 'Level ' + state.selectedLevel;

      document.getElementById('complete-modal-subtitle').textContent = dohTitle + '（' + lvlName + '）全問終了！';

      const totalQ = state.activeQuestionList.length;
      document.getElementById('complete-modal-total-questions').textContent = totalQ;

      // 地域の制覇状況
      const regProvs = state.selectedDoh === 'ALL' ? PROV_LIST : PROV_LIST.filter(p => p.doh === state.selectedDoh);
      const regCleared = state.selectedDoh === 'ALL' ? Store.getTotalCleared() : Store.getDohCleared(state.selectedDoh);
      document.getElementById('complete-modal-region-cleared').textContent = regCleared;
      document.getElementById('complete-modal-region-total').textContent = regProvs.length;

      // 全国制覇数
      const totalCleared = Store.getTotalCleared();
      const totalPct = ((totalCleared / 68) * 100).toFixed(1);
      document.getElementById('complete-modal-total-cleared').textContent = totalCleared;
      document.getElementById('complete-modal-total-pct').textContent = totalPct + '%';

      // 次の難易度ラベル
      const nextBtnLabel = document.getElementById('complete-next-level-label');
      if (state.selectedLevel === '1') nextBtnLabel.textContent = '⭐ Level 2 に挑戦する';
      else if (state.selectedLevel === '2') nextBtnLabel.textContent = '⭐ Level 3 に挑戦する';
      else if (state.selectedLevel === '3') nextBtnLabel.textContent = '⭐ Level 4 に挑戦する';
      else nextBtnLabel.textContent = '⭐ 全難易度（ALL）に挑戦する';

      modal.classList.remove('hidden');
    }

    function hideStageCompleteModal() {
      document.getElementById('modal-stage-complete').classList.add('hidden');
    }

    function updateAccuracyTag() {
      const cleared = Store.getTotalCleared();
      document.getElementById('spoke-accuracy-tag').textContent = '全国制覇: ' + cleared + ' / 68';
    }

    /* ========================================================
       回答処理
       ======================================================== */
    function onPolygonClick(clickedCode) {
      if (state.currentMode === 'explore') {
        showExploreDetails(clickedCode);
        return;
      }

      // 4択問題・入力問題ではポリゴンクリックによる回答は受け付けない
      if (state.currentMode === 'name' || state.currentMode === 'type') return;

      // 出題範囲外の旧国をタップしたときの救済通知
      if (!isProvTargetInCurrentStage(clickedCode)) {
        const cp = PROVINCES[clickedCode];
        if (cp) {
          showToast('『' + cp.name + '』は Lv.' + cp.lvl + '（' + cp.doh + '）です（現在のLevelでは出題対象外）');
        }
        return;
      }

      if (state.currentMode !== 'locate' || state.isAnswering) return;
      state.isAnswering = true;

      const target = state.currentQuestion;
      const isCorrect = clickedCode === target.code;

      Store.recordAnswer(target.code, isCorrect);
      showFeedback(isCorrect, target, clickedCode);
    }

    function generateChoiceButtons(target) {
      const pool = state.selectedDoh === 'ALL' ? PROV_LIST : PROV_LIST.filter(p => p.doh === state.selectedDoh);
      let dummies = pool.filter(p => p.code !== target.code).sort(() => Math.random() - 0.5).slice(0, 3);
      if (dummies.length < 3) {
        dummies = PROV_LIST.filter(p => p.code !== target.code).sort(() => Math.random() - 0.5).slice(0, 3);
      }

      const choices = [target, ...dummies].sort(() => Math.random() - 0.5);
      state.currentChoices = choices;

      const grid = document.getElementById('choice-buttons-grid');
      grid.innerHTML = '';

      choices.forEach((c, idx) => {
        const btn = document.createElement('button');
        btn.className = 'choice-btn p-2 sm:p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs sm:text-sm border border-slate-700 transition active:scale-95 text-center truncate shadow flex flex-col items-center justify-center';
        btn.innerHTML = `
          <div class="flex items-center gap-1">
            <span class="text-[10px] text-slate-400 font-mono hidden sm:inline">[` + (idx + 1) + `]</span>
            <span class="truncate">` + c.name + `</span>
          </div>
          <span class="text-[10px] font-normal text-slate-400 truncate">` + c.kana + `</span>
        `;
        btn.onclick = () => handleChoiceAnswer(c.code, btn);
        grid.appendChild(btn);
      });
    }

    function handleChoiceAnswer(selectedCode, clickedBtn) {
      if (state.isAnswering) return;
      state.isAnswering = true;

      const target = state.currentQuestion;
      const isCorrect = selectedCode === target.code;

      Store.recordAnswer(target.code, isCorrect);
      showFeedback(isCorrect, target);
    }

    document.getElementById('form-type-answer').onsubmit = (e) => {
      e.preventDefault();
      if (state.isAnswering || state.currentMode !== 'type') return;

      const input = document.getElementById('input-type-answer');
      const ans = input.value.trim().toLowerCase();
      if (!ans) return;

      state.isAnswering = true;
      const target = state.currentQuestion;

      const isCorrect = ans === target.name.toLowerCase() || ans === target.kana.toLowerCase() || ans === (target.name + '国').toLowerCase();

      Store.recordAnswer(target.code, isCorrect);
      showFeedback(isCorrect, target);
    };

    function showFeedback(isCorrect, target, clickedCode = null) {
      const bar = document.getElementById('feedback-bar');
      const content = document.getElementById('feedback-content');
      bar.classList.remove('hidden', 'bg-emerald-950/80', 'border-emerald-500/50', 'bg-rose-950/80', 'border-rose-500/50');

      if (isCorrect) {
        sound.playCorrect();
        highlightPolygon(target.code, 'correct');

        bar.classList.add('bg-emerald-950/80', 'border-emerald-500/50');
        content.innerHTML = `
          <div class="flex items-center justify-between gap-2">
            <div class="flex items-center gap-2 text-emerald-400">
              <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
              <span>正解！ <strong>` + target.name + `</strong>（` + target.kana + `）</span>
              <span class="text-[11px] text-emerald-300/80 hidden sm:inline">【現代: ` + target.pref + `】</span>
            </div>
            <button id="btn-next-fast" class="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition">次へ ↵</button>
          </div>
        `;
        document.getElementById('btn-next-fast').onclick = () => nextQuestion();

        state.feedbackTimer = setTimeout(() => nextQuestion(), 1100);
      } else {
        sound.playWrong();
        highlightPolygon(target.code, 'wrong');

        let clickedInfo = '';
        if (clickedCode && PROVINCES[clickedCode]) {
          const cp = PROVINCES[clickedCode];
          clickedInfo = '（タップしたのは『' + cp.name + '』）';
        }

        bar.classList.add('bg-rose-950/80', 'border-rose-500/50');
        content.innerHTML = `
          <div class="flex items-center justify-between gap-2">
            <div class="text-rose-300">
              <span class="font-bold text-rose-400">不正解！</span> 正解は<strong>『` + target.name + `』</strong>（` + target.kana + `）` + clickedInfo + `
              <div class="text-[11px] text-slate-300 mt-0.5">現代の地域: ` + target.pref + ` | ` + target.desc + `</div>
            </div>
            <button id="btn-next-manual" class="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs transition shrink-0 shadow">次へ ↵</button>
          </div>
        `;
        document.getElementById('btn-next-manual').onclick = () => nextQuestion();
      }
    }

    function nextQuestion() {
      clearTimeout(state.feedbackTimer);
      state.currentIndex++;
      renderCurrentQuestion();
    }

    /* ========================================================
       探索モード 詳細カード
       ======================================================== */
    function showExploreDetails(code) {
      const p = PROVINCES[code];
      if (!p) return;

      resetAllHighlights();
      highlightPolygon(code, 'question');

      document.getElementById('explore-empty-state').classList.add('hidden');
      document.getElementById('explore-detail-state').classList.remove('hidden');

      document.getElementById('explore-name').textContent = p.name;
      document.getElementById('explore-kana').textContent = '（' + p.kana + '）';
      document.getElementById('explore-doh-badge').textContent = p.doh;
      document.getElementById('explore-lvl-badge').textContent = 'Lv.' + p.lvl;
      document.getElementById('explore-pref').textContent = p.pref;
      document.getElementById('explore-desc').textContent = p.desc;

      const rec = Store.getRecord(code);
      const tag = document.getElementById('explore-status-tag');
      if (rec && rec.correct > 0) {
        tag.innerHTML = '<span class="text-xs text-emerald-400 font-bold">✓ 制覇済 (' + rec.correct + '回正解)</span>';
      } else if (rec && rec.wrong > 0) {
        tag.innerHTML = '<span class="text-xs text-rose-400 font-bold">✕ 要復習 (' + rec.wrong + '回ミス)</span>';
      } else {
        tag.innerHTML = '<span class="text-xs text-slate-500">未挑戦</span>';
      }
    }

    /* ========================================================
       ヒント表示 & ユーティリティ
       ======================================================== */
    document.getElementById('btn-toggle-hint').onclick = () => {
      const bubble = document.getElementById('hint-bubble');
      if (!state.currentQuestion) return;
      const target = state.currentQuestion;

      document.getElementById('hint-content').innerHTML = `
        <div class="space-y-1">
          <div>現代の都道府県: <strong class="text-sky-300">` + target.pref + `</strong></div>
          <div class="text-slate-400 text-xs">特徴・名所: ` + target.desc + `</div>
          <div class="text-slate-400 text-xs">五畿七道: ` + target.doh + ` （Lv.` + target.lvl + `）</div>
        </div>
      `;
      bubble.classList.remove('hidden');
    };
    document.getElementById('btn-close-hint').onclick = () => {
      document.getElementById('hint-bubble').classList.add('hidden');
    };

    document.getElementById('btn-fit-bounds').onclick = () => fitTargetBounds();

    document.getElementById('btn-sound-toggle').onclick = () => {
      const on = sound.toggle();
      document.getElementById('icon-sound-on').classList.toggle('hidden', !on);
      document.getElementById('icon-sound-off').classList.toggle('hidden', on);
      showToast(on ? '効果音: ON' : '効果音: OFF');
    };

    document.getElementById('btn-back-to-hub').onclick = () => {
      clearTimeout(state.feedbackTimer);
      hideStageCompleteModal();
      state.currentScreen = 'hub';
      document.getElementById('screen-spoke').classList.add('hidden');
      document.getElementById('screen-hub').classList.remove('hidden');
      renderHubHeaderSummary();
      renderHubCards(state.selectedDoh);
    };

    // 全問完了モーダルのボタンイベント
    document.getElementById('btn-complete-retry').onclick = () => {
      hideStageCompleteModal();
      state.currentIndex = 0;
      state.activeQuestionList.sort(() => Math.random() - 0.5);
      renderCurrentQuestion();
    };

    document.getElementById('btn-complete-next-level').onclick = () => {
      hideStageCompleteModal();
      let nextLvl = 'ALL';
      if (state.selectedLevel === '1') nextLvl = '2';
      else if (state.selectedLevel === '2') nextLvl = '3';
      else if (state.selectedLevel === '3') nextLvl = '4';
      else nextLvl = 'ALL';

      // レベルボタンスタイル更新
      document.querySelectorAll('.level-btn').forEach(b => {
        const isMatch = b.dataset.level === nextLvl;
        b.classList.toggle('bg-sky-600', isMatch);
        b.classList.toggle('text-white', isMatch);
        b.classList.toggle('bg-slate-800', !isMatch);
        b.classList.toggle('text-slate-300', !isMatch);
      });

      loadLevelDeck(nextLvl);
    };

    document.getElementById('btn-complete-hub').onclick = () => {
      hideStageCompleteModal();
      document.getElementById('btn-back-to-hub').click();
    };

    window.addEventListener('keydown', (e) => {
      if (state.currentScreen !== 'spoke') return;

      // 完了モーダル表示中のEnterキー（再挑戦）
      const completeModal = document.getElementById('modal-stage-complete');
      if (completeModal && !completeModal.classList.contains('hidden')) {
        if (e.key === 'Enter') {
          document.getElementById('btn-complete-retry').click();
        } else if (e.key === 'Escape') {
          hideStageCompleteModal();
        }
        return;
      }

      if (e.key === 'Enter') {
        const btnFast = document.getElementById('btn-next-fast');
        const btnManual = document.getElementById('btn-next-manual');
        if (btnFast && !btnFast.closest('#feedback-bar').classList.contains('hidden')) {
          btnFast.click();
        } else if (btnManual && !btnManual.closest('#feedback-bar').classList.contains('hidden')) {
          btnManual.click();
        }
      }

      if (state.currentMode === 'name' && !state.isAnswering) {
        const keyIdx = parseInt(e.key, 10) - 1;
        if (keyIdx >= 0 && keyIdx < 4) {
          const btns = document.querySelectorAll('.choice-btn');
          if (btns[keyIdx]) btns[keyIdx].click();
        }
      }
    });

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.remove('hidden');
      setTimeout(() => t.classList.add('hidden'), 2200);
    }

    window.addEventListener('DOMContentLoaded', () => {
      initHub();
    });
  </script>
</body>
</html>
'''

# Replace placeholders
final_html = raw_html.replace('__GEOJSON_PLACEHOLDER__', geojson_str)
final_html = final_html.replace('__MASTER_PLACEHOLDER__', master_str)
final_html = final_html.replace('__DOH_PLACEHOLDER__', doh_str)

output_html_path = "G:/AI/historic-provinces-of-Japan/index.html"
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(final_html)

size = os.path.getsize(output_html_path)
print(f"Successfully generated index.html ({size / 1024:.1f} KB)")
