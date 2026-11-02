import urllib.request
import urllib.parse
import json
import math
import os

print("=== Downloading and preparing Japanese Provinces (令制国) dataset ===")

# Master metadata for 68 historic provinces (五畿七道)
PROVINCES_META = {
    # 畿内 (5)
    "山城": {"kana": "やましろ", "doh": "畿内", "pref": "京都府南部", "lvl": 1, "desc": "平安京、宇治抹茶、伏見稲荷"},
    "大和": {"kana": "やまと", "doh": "畿内", "pref": "奈良県", "lvl": 1, "desc": "平城京、法隆寺、吉野千本桜"},
    "河内": {"kana": "かわち", "doh": "畿内", "pref": "大阪府東部", "lvl": 3, "desc": "百舌鳥・古市古墳群、東大阪の町工場"},
    "和泉": {"kana": "いずみ", "doh": "畿内", "pref": "大阪府南西部", "lvl": 3, "desc": "堺刃物、岸和田だんじり祭、関西空港"},
    "摂津": {"kana": "せっつ", "doh": "畿内", "pref": "大阪府北部・兵庫県南東部", "lvl": 2, "desc": "大坂城、神戸港、有馬温泉、甲子園"},

    # 東海道 (15)
    "伊賀": {"kana": "いが", "doh": "東海道", "pref": "三重県北西部", "lvl": 4, "desc": "伊賀流忍者、伊賀上野城、松尾芭蕉生誕地"},
    "伊勢": {"kana": "いせ", "doh": "東海道", "pref": "三重県中北部", "lvl": 2, "desc": "伊勢神宮、鈴鹿サーキット、松阪牛"},
    "志摩": {"kana": "しま", "doh": "東海道", "pref": "三重県志摩半島", "lvl": 4, "desc": "リアス式海岸、伊勢志摩サミット、真珠養殖"},
    "尾張": {"kana": "おわり", "doh": "東海道", "pref": "愛知県西部", "lvl": 1, "desc": "織田信長、名古屋城、熱田神宮"},
    "三河": {"kana": "みかわ", "doh": "東海道", "pref": "愛知県東部", "lvl": 2, "desc": "徳川家康生誕の地、岡崎城、トヨタ自動車"},
    "遠江": {"kana": "とおとうみ", "doh": "東海道", "pref": "静岡県西部", "lvl": 3, "desc": "浜名湖、うなぎ、楽器・バイク産業"},
    "駿河": {"kana": "するが", "doh": "東海道", "pref": "静岡県中部・東部", "lvl": 2, "desc": "駿府城、富士山南麓、三保松原"},
    "伊豆": {"kana": "いず", "doh": "東海道", "pref": "静岡県伊豆半島・伊豆諸島", "lvl": 2, "desc": "熱海・伊東温泉、浄蓮の滝、下田開国"},
    "甲斐": {"kana": "かい", "doh": "東海道", "pref": "山梨県", "lvl": 1, "desc": "武田信玄、甲府盆地、富士五湖、ぶどう・ほうとう"},
    "相模": {"kana": "さがみ", "doh": "東海道", "pref": "神奈川県（横浜・川崎除く大部分）", "lvl": 1, "desc": "鎌倉幕府、湘南海岸、箱根温泉、小田原城"},
    "武蔵": {"kana": "むさし", "doh": "東海道", "pref": "東京都・埼玉県・神奈川県北東部", "lvl": 1, "desc": "江戸・東京、武蔵野、さいたま"},
    "安房": {"kana": "あわ", "doh": "東海道", "pref": "千葉県南部", "lvl": 4, "desc": "房総半島南端、館山城、白浜海岸"},
    "上総": {"kana": "かずさ", "doh": "東海道", "pref": "千葉県中部", "lvl": 3, "desc": "房総半島中部、東京湾アクアライン、養老渓谷"},
    "下総": {"kana": "しもうさ", "doh": "東海道", "pref": "千葉県北部・茨城県南西部", "lvl": 3, "desc": "成田国際空港、利根川流域、下総台地"},
    "常陸": {"kana": "ひたち", "doh": "東海道", "pref": "茨城県（南西部除く大部分）", "lvl": 2, "desc": "水戸偕楽園、筑波山、霞ヶ浦、日立製作所"},

    # 東山道 (8)
    "近江": {"kana": "おうみ", "doh": "東山道", "pref": "滋賀県", "lvl": 1, "desc": "日本最大の湖・琵琶湖、彦根城、近江商人"},
    "美濃": {"kana": "みの", "doh": "東山道", "pref": "岐阜県南部", "lvl": 2, "desc": "織田信長の岐阜城、関ヶ原の戦い、美濃焼"},
    "飛騨": {"kana": "ひだ", "doh": "東山道", "pref": "岐阜県北部", "lvl": 3, "desc": "白川郷合掌造り、飛騨高山の古い町並み、下呂温泉"},
    "飛弾": {"kana": "ひだ", "doh": "東山道", "pref": "岐阜県北部", "lvl": 3, "desc": "白川郷合掌造り、飛騨高山（表記ゆれ：飛騨）"},
    "信濃": {"kana": "しなの", "doh": "東山道", "pref": "長野県", "lvl": 1, "desc": "信州、日本アルプス、善光寺、国宝松本城、信州そば"},
    "上野": {"kana": "こうずけ", "doh": "東山道", "pref": "群馬県", "lvl": 2, "desc": "上州、草津・伊香保温泉、富岡製糸場、上毛三山"},
    "下野": {"kana": "しもつけ", "doh": "東山道", "pref": "栃木県", "lvl": 2, "desc": "世界遺産日光東照宮、那須高原、宇都宮餃子"},
    "陸奥": {"kana": "むつ", "doh": "東山道", "pref": "青森・岩手・宮城・福島県", "lvl": 1, "desc": "奥州藤原氏平泉、伊達政宗仙台城、松島、十和田湖"},
    "出羽": {"kana": "でわ", "doh": "東山道", "pref": "山形県・秋田県", "lvl": 2, "desc": "出羽三山、鳥海山、最上川、庄内平野、秋田米"},

    # 北陸道 (7)
    "若狭": {"kana": "わかさ", "doh": "北陸道", "pref": "福井県南部", "lvl": 4, "desc": "若狭湾のリアス海岸、御食国小浜、三方五湖"},
    "越前": {"kana": "えちぜん", "doh": "北陸道", "pref": "福井県北部", "lvl": 2, "desc": "越前ガニ、東尋坊、曹洞宗大本山永平寺、丸岡城"},
    "加賀": {"kana": "かが", "doh": "北陸道", "pref": "石川県南部", "lvl": 1, "desc": "加賀百万石前田家、金沢兼六園、山中・山代温泉"},
    "能登": {"kana": "のと", "doh": "北陸道", "pref": "石川県能登半島", "lvl": 3, "desc": "能登半島、輪島塗、白米千枚田、見附島"},
    "越中": {"kana": "えっちゅう", "doh": "北陸道", "pref": "富山県", "lvl": 2, "desc": "富山湾の寒ブリ、立山黒部アルペンルート、売薬"},
    "越後": {"kana": "えちご", "doh": "北陸道", "pref": "新潟県本土", "lvl": 1, "desc": "上杉謙信の越後、魚沼産コシヒカリ、日本酒、雪国"},
    "佐渡": {"kana": "さど", "doh": "北陸道", "pref": "新潟県佐渡島", "lvl": 3, "desc": "世界遺産佐渡金山、朱鷺（トキ）の生息地、たらい舟"},

    # 山陰道 (8)
    "丹波": {"kana": "たんば", "doh": "山陰道", "pref": "京都府中部・兵庫県東部", "lvl": 3, "desc": "丹波黒豆・丹波栗、明智光秀の丹波攻め、篠山城"},
    "丹後": {"kana": "たんご", "doh": "山陰道", "pref": "京都府北部", "lvl": 3, "desc": "日本三景天橋立、伊根の舟屋、丹後ちりめん"},
    "但馬": {"kana": "たじま", "doh": "山陰道", "pref": "兵庫県北部", "lvl": 3, "desc": "但馬牛、城崎温泉、天空の城竹田城跡、コウノトリ"},
    "因幡": {"kana": "いなば", "doh": "山陰道", "pref": "鳥取県東部", "lvl": 3, "desc": "因幡の白兎伝説、鳥取砂丘、鳥取城"},
    "伯耆": {"kana": "ほうき", "doh": "山陰道", "pref": "鳥取県西部", "lvl": 3, "desc": "名峰伯耆大山、水木しげるロード境港、三朝温泉"},
    "出雲": {"kana": "いずも", "doh": "山陰道", "pref": "島根県東部", "lvl": 1, "desc": "縁結びの出雲大社、国宝松江城、宍道湖夕日"},
    "石見": {"kana": "いわみ", "doh": "山陰道", "pref": "島根県西部", "lvl": 3, "desc": "世界遺産石見銀山、伝統芸能石見神楽、津和野"},
    "隠岐": {"kana": "おき", "doh": "山陰道", "pref": "島根県隠岐諸島", "lvl": 4, "desc": "隠岐ユネスコ世界ジオパーク、後鳥羽上皇配流の地"},

    # 山陽道 (8)
    "播磨": {"kana": "はりま", "doh": "山陽道", "pref": "兵庫県南西部", "lvl": 2, "desc": "世界遺産国宝姫路城、明石海峡・明石焼き、播州織"},
    "美作": {"kana": "みまさか", "doh": "山陽道", "pref": "岡山県北部", "lvl": 4, "desc": "宮本武蔵生誕地、桜の名所津山城、湯原温泉"},
    "備前": {"kana": "びぜん", "doh": "山陽道", "pref": "岡山県南東部", "lvl": 2, "desc": "国宝級日本刀と備前焼、岡山城、日本三名園後楽園"},
    "備中": {"kana": "びっちゅう", "doh": "山陽道", "pref": "岡山県西部", "lvl": 3, "desc": "倉敷美観地区、現存天守の備中松山城、吹屋ふるさと村"},
    "備後": {"kana": "びんご", "doh": "山陽道", "pref": "広島県東部", "lvl": 3, "desc": "坂と文学の街尾道、鞆の浦、福山城、備後絣"},
    "安芸": {"kana": "あき", "doh": "山陽道", "pref": "広島県西部", "lvl": 1, "desc": "世界遺産厳島神社（宮島）、原爆ドーム、毛利元就"},
    "周防": {"kana": "すおう", "doh": "山陽道", "pref": "山口県東部・中部", "lvl": 3, "desc": "名橋錦帯橋（岩国）、防府天満宮、大内氏文化の山口"},
    "長門": {"kana": "ながと", "doh": "山陽道", "pref": "山口県西部", "lvl": 2, "desc": "明治維新の萩城下町・松下村塾、角島大橋、下関フグ"},

    # 南海道 (6)
    "紀伊": {"kana": "きい", "doh": "南海道", "pref": "和歌山県・三重県南部", "lvl": 2, "desc": "世界遺産熊野古道・高野山、和歌山城、有田みかん"},
    "淡路": {"kana": "あわじ", "doh": "南海道", "pref": "兵庫県淡路島", "lvl": 3, "desc": "国生み神話の島、鳴門の渦潮、淡路島玉ねぎ"},
    "阿波": {"kana": "あわ", "doh": "南海道", "pref": "徳島県", "lvl": 2, "desc": "阿波おどり、鳴門の渦潮、祖谷のかずら橋、すだち"},
    "讃岐": {"kana": "さぬき", "doh": "南海道", "pref": "香川県", "lvl": 2, "desc": "讃岐うどん、こんぴらさん（金刀比羅宮）、栗林公園"},
    "伊予": {"kana": "いよ", "doh": "南海道", "pref": "愛媛県", "lvl": 2, "desc": "日本最古の名湯道後温泉、松山城、しまなみ海道"},
    "土佐": {"kana": "とさ", "doh": "南海道", "pref": "高知県", "lvl": 1, "desc": "坂本龍馬、桂浜、高知城、カツオのたたき、四万十川"},

    # 西海道 (11)
    "筑前": {"kana": "ちくぜん", "doh": "西海道", "pref": "福岡県西部・北部", "lvl": 2, "desc": "太宰府天満宮、博多商人、糸島、福岡城"},
    "筑後": {"kana": "ちくご", "doh": "西海道", "pref": "福岡県南部", "lvl": 3, "desc": "柳川の川下り、久留米ラーメン、筑後川"},
    "豊前": {"kana": "ぶぜん", "doh": "西海道", "pref": "福岡県東部・大分県北部", "lvl": 3, "desc": "小倉城、門司港レトロ、福澤諭吉の中津城下町"},
    "豊後": {"kana": "ぶんご", "doh": "西海道", "pref": "大分県中部・南部", "lvl": 3, "desc": "おんせん県別府・湯布院温泉、国宝臼杵石仏"},
    "肥前": {"kana": "ひぜん", "doh": "西海道", "pref": "佐賀県・長崎県本土", "lvl": 3, "desc": "吉野ヶ里遺跡、有田焼、長崎出島・グラバー園"},
    "肥後": {"kana": "ひご", "doh": "西海道", "pref": "熊本県", "lvl": 2, "desc": "加藤清正の熊本城、世界最大級のカルデラ阿蘇山"},
    "日向": {"kana": "ひゅうが", "doh": "西海道", "pref": "宮崎県", "lvl": 3, "desc": "神話の里高千穂峡、青島・日南海岸、チキン南蛮"},
    "大隅": {"kana": "おおすみ", "doh": "西海道", "pref": "鹿児島県東部・奄美・種子島・屋久島", "lvl": 3, "desc": "種子島宇宙センター、世界遺産屋久島、大隅半島"},
    "薩摩": {"kana": "さつま", "doh": "西海道", "pref": "鹿児島県西部", "lvl": 1, "desc": "西郷隆盛、桜島、薩摩切子、サツマイモ・黒豚"},
    "壱岐": {"kana": "いき", "doh": "西海道", "pref": "長崎県壱岐島", "lvl": 4, "desc": "古代一支国の原の辻遺跡、辰ノ島、壱岐牛・麦焼酎"},
    "対馬": {"kana": "つしま", "doh": "西海道", "pref": "長崎県対馬", "lvl": 4, "desc": "国境の島、古代山城金田城、ツシマヤマネコ"}
}

# Fetch GeoJSON from ArcGIS FeatureServer
url = "https://services.arcgis.com/wlVTGRSYTzAbjjiC/arcgis/rest/services/old_boundary/FeatureServer/0/query?" + urllib.parse.urlencode({
    "where": "1=1",
    "outFields": "OBJECTID,国名",
    "returnGeometry": "true",
    "outSR": "4326",
    "f": "geojson"
})

print("Fetching GeoJSON from ArcGIS Online...")
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as res:
    raw_geojson = json.loads(res.read().decode("utf-8"))

print(f"Downloaded {len(raw_geojson.get('features', []))} features.")

# Simplify coordinates (round to 4 decimal places approx 11m) and enrich properties
def round_coords(coords):
    if isinstance(coords[0], (int, float)):
        return [round(coords[0], 4), round(coords[1], 4)]
    return [round_coords(c) for c in coords]

def calc_centroid(coords):
    # Flatten all points and get bounding box center
    flat = []
    def extract(c):
        if isinstance(c[0], (int, float)):
            flat.append((c[0], c[1]))
        else:
            for sub in c:
                extract(sub)
    extract(coords)
    if not flat:
        return [0, 0]
    avg_lng = sum(p[0] for p in flat) / len(flat)
    avg_lat = sum(p[1] for p in flat) / len(flat)
    return [round(avg_lat, 4), round(avg_lng, 4)]

cleaned_features = []
master_dict = {}

# Code mapping index
prov_id = 1

for feat in raw_geojson.get("features", []):
    raw_name = feat["properties"].get("国名", "").strip()
    # Normalize name (飛弾 -> 飛騨)
    name = "飛騨" if raw_name == "飛弾" else raw_name
    
    meta = PROVINCES_META.get(name, PROVINCES_META.get(raw_name, {}))
    if not meta:
        print(f"Warning: meta not found for {name}")
        continue
    
    geom = feat["geometry"]
    geom["coordinates"] = round_coords(geom["coordinates"])
    lat_lng = calc_centroid(geom["coordinates"])

    code = f"P{prov_id:02d}"
    prov_id += 1

    properties = {
        "code": code,
        "name": name,
        "kana": meta.get("kana", ""),
        "doh": meta.get("doh", ""),
        "pref": meta.get("pref", ""),
        "lvl": meta.get("lvl", 2),
        "desc": meta.get("desc", ""),
        "lat": lat_lng[0],
        "lng": lat_lng[1]
    }

    feat["properties"] = properties
    cleaned_features.append(feat)

    master_dict[code] = properties

output_geojson = {
    "type": "FeatureCollection",
    "features": cleaned_features
}

# Save output files
with open("G:/AI/historic-provinces-of-Japan/provinces.geojson", "w", encoding="utf-8") as f:
    json.dump(output_geojson, f, ensure_ascii=False, separators=(',', ':'))

with open("G:/AI/historic-provinces-of-Japan/provinces_master.json", "w", encoding="utf-8") as f:
    json.dump(master_dict, f, ensure_ascii=False, indent=2)

file_size = os.path.getsize("G:/AI/historic-provinces-of-Japan/provinces.geojson")
print(f"Successfully processed {len(cleaned_features)} provinces.")
print(f"GeoJSON size: {file_size / 1024:.1f} KB")
