"""
SEO builder for Simultala Cab Service.

Run after changing SITE_URL below or PHONE in js/main.js:
    python build_seo.py

It (re)generates:
  - one landing page per location  (e.g. deoghar-taxi-service.html)
  - sitemap.xml, robots.txt, site.webmanifest
  - assets/og-image.png, assets/icon-192.png, assets/icon-512.png, assets/apple-touch-icon.png
  - SEO tags, schema and the location links inside index.html
  - the phone number everywhere (taken from js/main.js)
"""
import json
import re
from datetime import date
from html import escape
from pathlib import Path

# ===== Apni website ka domain yahan likhein (aakhir mein / nahi) =====
SITE_URL = "https://simultallacab.com"
# =====================================================================

ROOT = Path(__file__).parent
PHONE = re.search(r'const PHONE = "(\d{10})"', (ROOT / "js/main.js").read_text(encoding="utf-8")).group(1)
PHONE_PRETTY = f"{PHONE[:5]} {PHONE[5:]}"
TODAY = date.today().isoformat()
BRAND = "Simultala Cab Service"
BRAND_HI = "सिमुलतला कैब सर्विस"

# en, hi, district, state, approx road km from Simultala, stations, places to see, local note (hi)
LOCATIONS = [
    ("Simultala", "सिमुलतला", "Jamui", "Bihar", 0, ["Simultala"], ["लट्टू पहाड़", "हल्दिया झरना", "सनसेट पॉइंट"],
     "सिमुलतला हमारा घर है। पहाड़ों और जंगल से घिरे इस छोटे हिल स्टेशन के हर मोहल्ले और गाँव तक हमारी गाड़ी पहुँचती है।"),
    ("Jhajha", "झाझा", "Jamui", "Bihar", 25, ["Jhajha Junction"], ["मिंटो टावर, गिद्धौर", "लट्टू पहाड़, सिमुलतला"],
     "झाझा जंक्शन पर दिन-रात ट्रेनें रुकती हैं। लेट ट्रेन हो या रात 2 बजे की ट्रेन, हमारी गाड़ी स्टेशन पर मिलेगी।"),
    ("Jamui", "जमुई", "Jamui", "Bihar", 55, ["Jamui"], ["लछुआड़ जैन मंदिर", "मिंटो टावर, गिद्धौर"],
     "जमुई ज़िला मुख्यालय है &ndash; कचहरी, सदर अस्पताल, कॉलेज और बाज़ार के लिए रोज़ हमारी गाड़ियाँ चलती हैं।"),
    ("Gidhaur", "गिद्धौर", "Jamui", "Bihar", 45, ["Gidhaur"], ["मिंटो टावर", "दुर्गा मंदिर, गिद्धौर"],
     "गिद्धौर का मिंटो टावर और पुराना राजमहल देखने आने वालों के लिए आसान टैक्सी।"),
    ("Sikandra", "सिकंदरा", "Jamui", "Bihar", 75, [], ["लछुआड़ जैन मंदिर", "क्षत्रियकुंड"],
     "सिकंदरा से लछुआड़ और क्षत्रियकुंड जाने वाले जैन यात्रियों के लिए हम खास टूर कराते हैं।"),
    ("Chakai", "चकाई", "Jamui", "Bihar", 30, [], ["लट्टू पहाड़, सिमुलतला", "बाबा धाम, देवघर"],
     "चकाई से देवघर और गिरिडीह दोनों तरफ़ के रास्ते हमारे ड्राइवरों के जाने-पहचाने हैं।"),
    ("Kiul", "किऊल", "Lakhisarai", "Bihar", 90, ["Kiul Junction"], ["अशोकधाम मंदिर", "शृंगी ऋषि आश्रम"],
     "किऊल जंक्शन पर उतरिए, हमारी गाड़ी आपको किसी भी गाँव या शहर तक पहुँचाएगी।"),
    ("Lakhisarai", "लखीसराय", "Lakhisarai", "Bihar", 95, ["Lakhisarai", "Kiul Junction"], ["अशोकधाम मंदिर", "शृंगी ऋषि आश्रम"],
     "लखीसराय से देवघर, पटना और भागलपुर के लिए लोकल और आउटस्टेशन टैक्सी।"),
    ("Munger", "मुंगेर", "Munger", "Bihar", 110, ["Munger", "Jamalpur Junction"], ["मुंगेर किला", "कष्टहरणी घाट", "बिहार योग विद्यालय"],
     "मुंगेर किला, गंगा घाट और योग विद्यालय आने वालों के लिए आरामदायक गाड़ी।"),
    ("Jamalpur", "जमालपुर", "Munger", "Bihar", 105, ["Jamalpur Junction"], ["मुंगेर किला", "कष्टहरणी घाट"],
     "जमालपुर जंक्शन से पिकअप और ड्रॉप, किसी भी समय।"),
    ("Sultanganj", "सुल्तानगंज", "Bhagalpur", "Bihar", 85, ["Sultanganj"], ["अजगैबीनाथ मंदिर", "उत्तरवाहिनी गंगा"],
     "श्रावणी मेले में सुल्तानगंज से जल उठाकर देवघर जाने वाले कांवरियों के लिए गाड़ी और ग्रुप वाहन।"),
    ("Bhagalpur", "भागलपुर", "Bhagalpur", "Bihar", 110, ["Bhagalpur Junction"], ["विक्रमशिला", "मंदार पर्वत", "अजगैबीनाथ"],
     "भागलपुर से देवघर, बासुकीनाथ और मंदार पर्वत के लिए टैक्सी और टूर पैकेज।"),
    ("Banka", "बांका", "Banka", "Bihar", 60, ["Banka"], ["मंदार पर्वत, बौंसी", "ओढ़नी डैम"],
     "बांका से मंदार पर्वत और देवघर के लिए एक दिन का टूर।"),
    ("Katoria", "कटोरिया", "Banka", "Bihar", 25, [], ["बाबा धाम, देवघर", "मंदार पर्वत"],
     "कटोरिया से देवघर बहुत पास है &ndash; दर्शन के लिए सुबह-सुबह निकलें, शाम तक घर।"),
    ("Deoghar", "देवघर", "Deoghar", "Jharkhand", 50, ["Baidyanath Dham", "Jasidih Junction", "Deoghar Airport"],
     ["बाबा बैद्यनाथ धाम", "नौलखा मंदिर", "तपोवन", "त्रिकूट पर्वत", "सत्संग आश्रम"],
     "बाबा धाम दर्शन, देवघर एयरपोर्ट, AIIMS देवघर और होटल तक &ndash; देवघर में हमारी गाड़ियाँ रोज़ चलती हैं।"),
    ("Jasidih", "जसीडीह", "Deoghar", "Jharkhand", 40, ["Jasidih Junction"], ["बाबा बैद्यनाथ धाम", "तपोवन", "त्रिकूट पर्वत"],
     "जसीडीह जंक्शन पर उतरकर सीधे बाबा धाम या होटल &ndash; स्टेशन पर ड्राइवर नाम का बोर्ड लेकर मिलेगा।"),
    ("Madhupur", "मधुपुर", "Deoghar", "Jharkhand", 65, ["Madhupur Junction"], ["पत्थरचपटी", "बाबा धाम, देवघर"],
     "मधुपुर जंक्शन से देवघर, गिरिडीह और सिमुलतला के लिए टैक्सी।"),
    ("Giridih", "गिरिडीह", "Giridih", "Jharkhand", 90, ["Giridih"], ["उसरी फॉल", "खंडोली डैम", "पारसनाथ / मधुबन"],
     "गिरिडीह से उसरी फॉल, खंडोली और पारसनाथ (शिखरजी) के लिए टूर।"),
    ("Basukinath", "बासुकीनाथ", "Dumka", "Jharkhand", 85, [], ["बासुकीनाथ धाम", "बाबा धाम, देवघर"],
     "बाबा धाम के बाद बासुकीनाथ दर्शन &ndash; एक ही गाड़ी में दोनों धाम।"),
    ("Dumka", "दुमका", "Dumka", "Jharkhand", 110, ["Dumka"], ["मसानजोर डैम", "बासुकीनाथ धाम"],
     "दुमका से देवघर, बासुकीनाथ और मसानजोर के लिए टैक्सी।"),
    ("Jamtara", "जामताड़ा", "Jamtara", "Jharkhand", 100, ["Jamtara", "Karmatanr"], ["बाबा धाम, देवघर"],
     "जामताड़ा और करमाटांड़ से देवघर, धनबाद और आसनसोल के लिए गाड़ी।"),
    ("Godda", "गोड्डा", "Godda", "Jharkhand", 90, [], ["बाबा धाम, देवघर", "बासुकीनाथ धाम"],
     "गोड्डा से देवघर, भागलपुर और सिमुलतला के लिए टैक्सी।"),
]

# Deoghar se 100 km ke andar ki aur jagahen (doori geo_cache.json se nikalti hai)
DB, JH, WB = "बाबा धाम, देवघर", "Jharkhand", "West Bengal"
LOCATIONS += [
    ("Hansdiha", "हंसडीहा", "Dumka", JH, None, [], ["बासुकीनाथ धाम", DB],
     "हंसडीहा चौक NH-133 पर है &ndash; यहाँ से देवघर, दुमका, गोड्डा और भागलपुर चारों तरफ़ के लिए हमारी गाड़ी मिलती है।"),
    ("Sarath", "सारठ", "Deoghar", JH, None, [], [DB, "तपोवन"],
     "सारठ से देवघर, मधुपुर और चितरा के लिए लोकल और रिज़र्व टैक्सी।"),
    ("Palojori", "पालोजोरी", "Deoghar", JH, None, [], [DB, "मसानजोर डैम"],
     "पालोजोरी से देवघर, जामताड़ा और दुमका जाने के लिए आरामदायक गाड़ी।"),
    ("Mohanpur", "मोहनपुर", "Deoghar", JH, None, [], [DB, "त्रिकूट पर्वत", "तपोवन"],
     "देवघर शहर से सटे मोहनपुर से बाबा धाम, जसीडीह स्टेशन और एयरपोर्ट तक टैक्सी।"),
    ("Sarwan", "सरवां", "Deoghar", JH, None, [], [DB, "नौलखा मंदिर"],
     "सरवां से बाबा धाम दर्शन और जसीडीह स्टेशन के लिए गाड़ी, दिन हो या रात।"),
    ("Karon", "करौं", "Deoghar", JH, None, [], [DB, "पत्थरचपटी, मधुपुर"],
     "करौं से देवघर, मधुपुर और जामताड़ा के लिए टैक्सी।"),
    ("Devipur", "देवीपुर", "Deoghar", JH, None, [], [DB, "AIIMS देवघर"],
     "AIIMS देवघर देवीपुर में है &ndash; मरीज़ों और उनके परिवार के लिए 24 घंटे टैक्सी, स्टेशन और घर तक।"),
    ("Margomunda", "मारगोमुंडा", "Deoghar", JH, None, [], [DB, "उसरी फॉल, गिरिडीह"],
     "मारगोमुंडा से मधुपुर, देवघर और गिरिडीह के लिए गाड़ी।"),
    ("Jarmundi", "जरमुंडी", "Dumka", JH, None, [], ["बासुकीनाथ धाम", DB],
     "बासुकीनाथ धाम जरमुंडी में ही है &ndash; बासुकीनाथ और बाबा धाम, दोनों दर्शन एक ही गाड़ी में।"),
    ("Saraiyahat", "सरैयाहाट", "Dumka", JH, None, [], ["बासुकीनाथ धाम", DB],
     "सरैयाहाट से देवघर, हंसडीहा और दुमका के लिए टैक्सी।"),
    ("Shikaripara", "शिकारीपाड़ा", "Dumka", JH, None, [], ["मलूटी मंदिर", "मसानजोर डैम"],
     "मलूटी के प्राचीन मंदिर देखने और दुमका, देवघर जाने के लिए गाड़ी।"),
    ("Masalia", "मसलिया", "Dumka", JH, None, [], ["मसानजोर डैम", "बासुकीनाथ धाम"],
     "मसलिया से दुमका, जामताड़ा और देवघर के लिए टैक्सी।"),
    ("Jama", "जामा", "Dumka", JH, None, [], ["बासुकीनाथ धाम", DB],
     "जामा से दुमका, बासुकीनाथ और देवघर के लिए गाड़ी।"),
    ("Mihijam", "मिहिजाम", "Jamtara", JH, None, ["Chittaranjan"], ["कल्याणेश्वरी मंदिर", DB],
     "मिहिजाम और चित्तरंजन स्टेशन से देवघर, जामताड़ा और आसनसोल के लिए टैक्सी।"),
    ("Karmatanr", "करमाटांड़", "Jamtara", JH, None, ["Vidyasagar (Karmatanr)"], ["विद्यासागर का नंदन कानन", DB],
     "विद्यासागर स्टेशन (करमाटांड़) पर पिकअप, और देवघर, जामताड़ा के लिए गाड़ी।"),
    ("Nala", "नाला", "Jamtara", JH, None, [], [DB, "मसानजोर डैम"],
     "नाला से जामताड़ा, दुमका और देवघर के लिए टैक्सी।"),
    ("Kundahit", "कुंडहित", "Jamtara", JH, None, [], [DB],
     "कुंडहित से जामताड़ा, देवघर और आसनसोल के लिए गाड़ी।"),
    ("Narayanpur", "नारायणपुर", "Jamtara", JH, None, [], [DB],
     "नारायणपुर से जामताड़ा, देवघर और धनबाद के लिए टैक्सी।"),
    ("Mahagama", "महगामा", "Godda", JH, None, [], ["मंदार पर्वत", DB],
     "महगामा से गोड्डा, भागलपुर और देवघर के लिए टैक्सी।"),
    ("Pathargama", "पथरगामा", "Godda", JH, None, [], [DB, "बासुकीनाथ धाम"],
     "पथरगामा से गोड्डा, हंसडीहा और देवघर के लिए गाड़ी।"),
    ("Poreyahat", "पोड़ैयाहाट", "Godda", JH, None, [], [DB, "बासुकीनाथ धाम"],
     "पोड़ैयाहाट से हंसडीहा, गोड्डा और देवघर के लिए टैक्सी।"),
    ("Sundarpahari", "सुंदरपहाड़ी", "Godda", JH, None, [], [DB],
     "सुंदरपहाड़ी से गोड्डा, दुमका और देवघर के लिए गाड़ी।"),
    ("Boarijor", "बोआरीजोर", "Godda", JH, None, [], [DB],
     "बोआरीजोर से गोड्डा, भागलपुर और देवघर के लिए टैक्सी।"),
    ("Pakur", "पाकुड़", "Pakur", JH, None, ["Pakur"], [DB, "बासुकीनाथ धाम"],
     "पाकुड़ से देवघर, दुमका और बासुकीनाथ के लिए आउटस्टेशन टैक्सी।"),
    ("Jamua", "जमुआ", "Giridih", JH, None, [], ["पारसनाथ / मधुबन", DB],
     "जमुआ से गिरिडीह, देवघर और कोडरमा के लिए टैक्सी।"),
    ("Bengabad", "बेंगाबाद", "Giridih", JH, None, [], [DB, "उसरी फॉल"],
     "बेंगाबाद से गिरिडीह, मधुपुर और देवघर के लिए गाड़ी।"),
    ("Gandey", "गांडेय", "Giridih", JH, None, [], ["उसरी फॉल", DB],
     "गांडेय से गिरिडीह और देवघर के लिए टैक्सी।"),
    ("Tisri", "तिसरी", "Giridih", JH, None, [], ["पारसनाथ / मधुबन", DB],
     "तिसरी से गिरिडीह, देवघर और जमुई के लिए गाड़ी।"),
    ("Deori", "देवरी", "Giridih", JH, None, [], ["पारसनाथ / मधुबन", DB],
     "देवरी से गिरिडीह, चकाई और देवघर के लिए टैक्सी।"),
    ("Madhuban", "मधुबन (पारसनाथ)", "Giridih", JH, None, ["Parasnath"], ["सम्मेद शिखरजी", "पारसनाथ पहाड़"],
     "सम्मेद शिखरजी (पारसनाथ) की यात्रा &ndash; जैन तीर्थ यात्रियों के लिए देवघर, गिरिडीह और पारसनाथ स्टेशन से गाड़ी।"),
    ("Dhanbad", "धनबाद", "Dhanbad", JH, None, ["Dhanbad Junction"], ["मैथन डैम", "पंचेत डैम", DB],
     "धनबाद जंक्शन से देवघर, बाबा धाम और गिरिडीह के लिए one-way और round trip टैक्सी।"),
    ("Nirsa", "निरसा", "Dhanbad", JH, None, [], ["मैथन डैम", "कल्याणेश्वरी मंदिर"],
     "निरसा और मैथन से देवघर, धनबाद और आसनसोल के लिए गाड़ी।"),
    ("Chittaranjan", "चित्तरंजन", "Paschim Bardhaman", WB, None, ["Chittaranjan"], ["कल्याणेश्वरी मंदिर", DB],
     "चित्तरंजन स्टेशन से देवघर, जामताड़ा और आसनसोल के लिए टैक्सी।"),
    ("Asansol", "आसनसोल", "Paschim Bardhaman", WB, None, ["Asansol Junction"], ["कल्याणेश्वरी मंदिर", "मैथन डैम", DB],
     "आसनसोल जंक्शन से बाबा धाम देवघर और बासुकीनाथ के लिए one-way और round trip टैक्सी।"),
    ("Bounsi", "बौंसी", "Banka", "Bihar", None, [], ["मंदार पर्वत", DB],
     "मंदार पर्वत बौंसी में है &ndash; मंदार दर्शन और देवघर, भागलपुर के लिए गाड़ी।"),
    ("Amarpur", "अमरपुर", "Banka", "Bihar", None, [], ["मंदार पर्वत", "अजगैबीनाथ, सुल्तानगंज"],
     "अमरपुर से बांका, भागलपुर और देवघर के लिए टैक्सी।"),
    ("Belhar", "बेलहर", "Banka", "Bihar", None, [], [DB, "मंदार पर्वत"],
     "बेलहर से बांका, सुल्तानगंज और देवघर के लिए गाड़ी।"),
    ("Chandan", "चांदन", "Banka", "Bihar", None, [], [DB, "मंदार पर्वत"],
     "चांदन से कटोरिया, देवघर और बांका के लिए टैक्सी।"),
    ("Dhoraiya", "धोरैया", "Banka", "Bihar", None, [], ["मंदार पर्वत", DB],
     "धोरैया से बांका, भागलपुर और देवघर के लिए गाड़ी।"),
    ("Tarapur", "तारापुर", "Munger", "Bihar", None, [], ["अजगैबीनाथ, सुल्तानगंज", DB],
     "तारापुर से सुल्तानगंज, मुंगेर और देवघर के लिए टैक्सी।"),
    ("Sono", "सोनो", "Jamui", "Bihar", None, [], ["लट्टू पहाड़, सिमुलतला", DB],
     "सोनो से झाझा, जमुई, चकाई और देवघर के लिए गाड़ी।"),
    ("Khaira", "खैरा", "Jamui", "Bihar", None, [], ["लछुआड़ जैन मंदिर", "मिंटो टावर, गिद्धौर"],
     "खैरा से जमुई, सिकंदरा और देवघर के लिए टैक्सी।"),
    ("Laxmipur", "लक्ष्मीपुर", "Jamui", "Bihar", None, [], ["लट्टू पहाड़, सिमुलतला", DB],
     "लक्ष्मीपुर से जमुई, झाझा और देवघर के लिए गाड़ी।"),
    ("Barhat", "बरहट", "Jamui", "Bihar", None, [], ["लछुआड़ जैन मंदिर", DB],
     "बरहट से जमुई, लखीसराय और देवघर के लिए टैक्सी।"),
]
GEO = json.loads((ROOT / "geo_cache.json").read_text(encoding="utf-8"))
STATE_HI = {"Bihar": "बिहार", "Jharkhand": "झारखंड", "West Bengal": "पश्चिम बंगाल"}


def km_between(a, b):
    import math
    (la1, lo1), (la2, lo2) = [tuple(map(math.radians, GEO[x][:2])) for x in (a, b)]
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def nearest(en, n=14):
    return sorted((l for l in LOCATIONS if l[0] != en), key=lambda l: km_between(en, l[0]))[:n]

SERVICES = [
    ("लोकल टैक्सी", "local taxi"),
    ("रेलवे स्टेशन पिकअप / ड्रॉप", "railway station pickup and drop"),
    ("एयरपोर्ट टैक्सी (देवघर, पटना, राँची)", "airport taxi"),
    ("बाबा धाम देवघर दर्शन", "Baba Dham darshan cab"),
    ("आउटस्टेशन कैब (one-way / round trip)", "outstation cab"),
    ("टूर पैकेज", "tour packages"),
    ("होटल बुकिंग", "hotel booking"),
    ("शादी और बारात की गाड़ी", "wedding car rental"),
]
ROUTE_TARGETS = [("Deoghar", "देवघर"), ("Patna", "पटना"), ("Ranchi", "राँची"), ("Kolkata", "कोलकाता"),
                 ("Bhagalpur", "भागलपुर"), ("Dhanbad", "धनबाद"), ("Gaya", "गया"), ("Jasidih", "जसीडीह")]


def slug(en):
    return f"{en.lower()}-taxi-service.html"


def url(path=""):
    return f"{SITE_URL}/{path}"


def tel():
    return f"tel:+91{PHONE}"


def wa():
    return f"https://wa.me/91{PHONE}"


def business_ld(area=None, page_url=None):
    data = {
        "@context": "https://schema.org",
        "@type": "TaxiService",
        "@id": f"{SITE_URL}/#business",
        "name": BRAND,
        "alternateName": BRAND_HI,
        "url": page_url or url(),
        "logo": url("assets/icon-512.png"),
        "image": url("assets/og-image.png"),
        "telephone": f"+91{PHONE}",
        "priceRange": "₹1500+",
        "foundingDate": "2016",
        "slogan": "10+ years of experience, 50+ cabs, 1,00,000+ trips completed",
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59",
        },
        "address": {"@type": "PostalAddress", "addressLocality": "Simultala", "addressRegion": "Bihar",
                    "postalCode": "811316", "addressCountry": "IN"},
        "hasMap": "https://share.google/q4A3YEuAPNPlMQWhH",
        "sameAs": ["https://www.google.com/search?kgmid=/g/11zy8x69f1"],
        "geo": {"@type": "GeoCoordinates", "latitude": 24.70, "longitude": 86.57},
        "areaServed": area or [{"@type": "City", "name": f"{l[0]}, {l[3]}"} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Taxi services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": en}} for _, en in SERVICES]},
    }
    return data


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a).replace("&ndash;", "–")}}
        for q, a in faqs]}


def ld_script(*objs):
    return "\n".join(
        f'  <script type="application/ld+json">\n{json.dumps(o, ensure_ascii=False, indent=2)}\n  </script>' for o in objs)


def common_head(title, desc, keywords, canonical, css_prefix=""):
    return f'''  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="hi-IN" href="{canonical}">
  <link rel="alternate" hreflang="en-IN" href="{canonical}">
  <link rel="alternate" hreflang="x-default" href="{canonical}">
  <meta name="geo.region" content="IN-BR">
  <meta name="geo.placename" content="Simultala, Jamui, Bihar">
  <meta name="geo.position" content="24.70;86.57">
  <meta name="ICBM" content="24.70, 86.57">
  <meta name="theme-color" content="#0E3B2E">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="hi_IN">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{url('assets/og-image.png')}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{url('assets/og-image.png')}">
  <link rel="icon" type="image/svg+xml" href="{css_prefix}assets/logo.svg">
  <link rel="icon" type="image/png" sizes="192x192" href="{css_prefix}assets/icon-192.png">
  <link rel="apple-touch-icon" href="{css_prefix}assets/apple-touch-icon.png">
  <link rel="manifest" href="{css_prefix}site.webmanifest">'''


# ---------------------------------------------------------------- location pages
def load_template():
    """Pieces shared with index.html (read after index.html is patched)."""
    global HEADER, SPRITE, TAIL, WA_BTN
    t = (ROOT / "index.html").read_text(encoding="utf-8")
    HEADER = t[t.index('  <header class="topbar">'):t.index('  <main id="top">')]
    HEADER = HEADER.replace('href="#top"', 'href="index.html"')
    for sec in ["services", "packages", "outstation", "hotel", "area", "book"]:
        HEADER = HEADER.replace(f'href="#{sec}"', f'href="index.html#{sec}"')
    SPRITE = t[t.index('  <!-- Car drawings'):t.index('  <header class="topbar">')]
    TAIL = t[t.index('  <footer class="footer">'):]
    WA_BTN = re.search(r'<a class="btn btn--wa" data-wa.*?</a>', t, flags=re.S).group(0)

def location_page(loc):
    en, hi, district, state, km, stations, sights, note = loc
    state_hi = STATE_HI[state]
    canonical = url(slug(en))
    title = f"{en} Taxi Service | {hi} टैक्सी सर्विस, Cab Booking ₹1500 से – {BRAND}"
    desc = (f"{en} taxi service – {hi} में 24 घंटे टैक्सी: लोकल, स्टेशन पिकअप, Deoghar darshan, airport, "
            f"outstation cab, tour package, hotel booking. 10+ years, 50+ cabs, 1,00,000+ trips. किराया ₹1500 से शुरू। "
            f"Call {PHONE_PRETTY}.")
    keywords = ", ".join([
        f"{en} taxi", f"{en} taxi service", f"{en} cab", f"{en} cab service", f"{en} cab booking",
        f"{en} car rental", f"{en} taxi number", f"taxi in {en}", f"cab in {en}", f"{hi} टैक्सी", f"{hi} कैब",
        f"{hi} टैक्सी सर्विस", f"{hi} गाड़ी बुकिंग", f"{en} to Deoghar taxi", f"{en} to Patna taxi",
        f"{en} to Ranchi taxi", f"{en} outstation cab", f"{en} railway station taxi", f"{district} taxi",
        f"{en} wedding car", f"{en} tour and travels", f"{en} tour package", f"{en} to Basukinath taxi",
        f"{en} to Jasidih taxi", f"{en} to Simultala taxi", f"{hi} से देवघर टैक्सी", "Simultala Cab Service"])
    if km:
        dist_line = f"सिमुलतला से {hi} की दूरी लगभग {km} km है।"
    else:
        dist_line = f"देवघर से {hi} लगभग {max(5, round(km_between('Deoghar', en) / 5) * 5)} km (सीधी दूरी) पर है।"
    stations_line = (f"स्टेशन पिकअप: {', '.join(stations)}।" if stations else "")
    faqs = [
        (f"{hi} में टैक्सी का किराया कितना है?",
         f"{hi} में टैक्सी का किराया ₹1500 से शुरू होता है। सही किराया दूरी, गाड़ी और समय देखकर फ़ोन पर बताया जाता है &ndash; कॉल करें {PHONE_PRETTY}।"),
        (f"क्या {hi} में बाबा धाम दर्शन के लिए पूरे दिन की टैक्सी मिलेगी?" if en in ("Deoghar", "Jasidih")
         else f"क्या {hi} से देवघर बाबा धाम के लिए टैक्सी मिलेगी?",
         f"हाँ। {hi} से बाबा बैद्यनाथ धाम, बासुकीनाथ, तपोवन और त्रिकूट के लिए one-way, round trip और पूरे दिन का दर्शन पैकेज मिलता है।"),
        (f"क्या रात में {hi} से टैक्सी मिलती है?",
         f"हाँ, {BRAND} 24 घंटे चलती है। रात की ट्रेन, सुबह की फ्लाइट या इमरजेंसी के लिए कभी भी कॉल करें।"),
        (f"{hi} से आउटस्टेशन कैब कहाँ-कहाँ जाती है?",
         f"{hi} से पटना, राँची, कोलकाता, गया, धनबाद, भागलपुर, वाराणसी और देश में कहीं भी one-way या round trip कैब मिलती है।"),
    ]
    services = "".join(
        f'<li><a data-call href="{tel()}"><strong>{shi}</strong><span>{en} {sen}</span></a></li>' for shi, sen in SERVICES)
    routes = "".join(f'''
            <li><a class="sign" data-call href="{tel()}">
              <span class="sign__to">{thi}</span>
              <span class="sign__en">{en} to {ten} taxi</span>
              <svg class="sign__arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h14M12 5l7 7-7 7"/></svg>
            </a></li>''' for ten, thi in ROUTE_TARGETS if ten != en)
    sights_html = "".join(f"<li>{s}</li>" for s in sights)
    others = "".join(f'<li><a href="{slug(l[0])}">{l[0]} Taxi</a></li>' for l in nearest(en)) + (
        '<li><a href="deoghar-tour-package.html">Deoghar Tour Package</a></li><li><a href="index.html#area">सभी शहर</a></li>')
    faq_html = "".join(f'''
          <details>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>''' for q, a in faqs)
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": BRAND, "item": url()},
        {"@type": "ListItem", "position": 2, "name": f"{en} Taxi Service", "item": canonical}]}
    area = [{"@type": "City", "name": f"{en}, {state}"}, {"@type": "AdministrativeArea", "name": f"{district} district, {state}"}]
    biz = business_ld(area=area, page_url=canonical)
    biz["name"] = f"{BRAND} – {en}"

    return f'''<!DOCTYPE html>
<html lang="hi">
<head>
{common_head(title, desc, keywords, canonical)}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Mukta:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
{ld_script(biz, breadcrumb, faq_ld(faqs))}
</head>
<body>

{SPRITE}{HEADER}  <main id="top">
    <section class="hero loc-hero">
      <div class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">{BRAND}</a> <span aria-hidden="true">/</span> {en} Taxi</nav>
        <p class="hero__place">{district}, {state_hi} <span class="hero__badge">10+ साल, 50+ गाड़ियाँ, 1,00,000+ सफ़र</span></p>
        <h1>{hi} टैक्सी सर्विस</h1>
        <p class="loc-hero__en">{en} Taxi &amp; Cab Service &ndash; 24 hours</p>
        <p class="hero__lede">{note} {dist_line}</p>
        <a class="plate" data-call href="{tel()}" aria-label="कॉल करें">
          <span class="plate__label">{hi} के लिए कॉल करें</span>
          <span class="plate__num" data-phone-text>{PHONE_PRETTY}</span>
        </a>
        <div class="hero__row">
          {WA_BTN.replace('data-wa ', f'data-wa data-msg="{en} टैक्सी" ', 1)}
          <p class="hero__price">किराया <strong>₹1500</strong> से शुरू<sup>*</sup></p>
        </div>
        <p class="hero__note">* पूरा किराया दूरी और गाड़ी देखकर फ़ोन पर बताया जाता है।</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="head">
          <h2>{hi} में हमारी सेवाएँ</h2>
          <p>Every service is available in {en} and all villages around it. {stations_line}</p>
        </div>
        <ul class="loc-services">{services}</ul>
      </div>
    </section>

    <section class="section section--mist">
      <div class="wrap">
        <div class="head">
          <h2>{hi} से कहाँ जाना है?</h2>
          <p>Popular cab routes from {en}. बोर्ड दबाइए, किराया पूछिए।</p>
        </div>
        <ul class="signs">{routes}
        </ul>
        <h3 class="signs__title">{hi} के पास घूमने की जगहें</h3>
        <ul class="loc-sights">{sights_html}</ul>
      </div>
    </section>

    <section class="section" id="faq">
      <div class="wrap faq">
        <div class="head">
          <h2>{hi} टैक्सी: सवाल-जवाब</h2>
          <p>{en} taxi FAQs</p>
        </div>
        <div class="faq__list">{faq_html}
        </div>
      </div>
    </section>

    <section class="section section--mist">
      <div class="wrap">
        <div class="head">
          <h2>आस-पास के शहरों में भी टैक्सी</h2>
          <p>{BRAND} covers every town within 100 km of Simultala.</p>
        </div>
        <ul class="loc-links">{others}</ul>
      </div>
    </section>

    <section class="final">
      <div class="wrap final__in">
        <h2>{hi} में गाड़ी चाहिए? अभी कॉल कीजिए।</h2>
        <a class="plate plate--dark" data-call href="{tel()}" aria-label="कॉल करें">
          <span class="plate__label">कॉल करें</span>
          <span class="plate__num" data-phone-text>{PHONE_PRETTY}</span>
        </a>
      </div>
    </section>
  </main>

{TAIL}'''


# ---------------------------------------------------------------- tour package page
TOUR_SLUG = "deoghar-tour-package.html"


def tour_page():
    t = (ROOT / "index.html").read_text(encoding="utf-8")
    packages = re.search(r'        <ul class="packages">.*?\n        </ul>', t, flags=re.S).group(0)
    canonical = url(TOUR_SLUG)
    title = "Deoghar Tour Package | देवघर टूर पैकेज, बाबा धाम दर्शन टैक्सी – Simultala Cab Service"
    desc = ("Deoghar tour package – बाबा धाम दर्शन, देवघर + बासुकीनाथ, पूरा देवघर टूर (होटल सहित), सिमुलतला प्रकृति दर्शन, "
            "मंदार पर्वत और पारसनाथ जैन यात्रा। गाड़ी, ड्राइवर, पेट्रोल शामिल, ₹1500 से शुरू। "
            f"Call {PHONE_PRETTY}.")
    keywords = ", ".join([
        "Deoghar tour package", "Baba Dham tour package", "Baidyanath Dham tour package", "Deoghar Basukinath tour package",
        "Deoghar sightseeing taxi", "Deoghar local sightseeing", "Deoghar darshan taxi", "Deoghar one day tour",
        "Deoghar 2 days tour package", "Deoghar tour package with hotel", "Basukinath tour package", "Trikut Parvat taxi",
        "Tapovan Deoghar taxi", "Shravani Mela taxi", "Kanwar yatra taxi Sultanganj to Deoghar", "Simultala tour package",
        "Mandar Parvat tour", "Parasnath tour package", "Shikharji tour package", "Jasidih to Deoghar taxi",
        "देवघर टूर पैकेज", "बाबा धाम टूर पैकेज", "देवघर दर्शन टैक्सी", "बासुकीनाथ टूर", "देवघर घूमने के लिए गाड़ी",
        "श्रावणी मेला टैक्सी", "Simultala Cab Service"])
    faqs = [
        ("देवघर टूर पैकेज में क्या-क्या शामिल है?",
         "गाड़ी, ड्राइवर और पेट्रोल शामिल है। पूरा रूट पहले से तय होता है और दर्शन के समय ड्राइवर इंतज़ार करता है। होटल किसी भी पैकेज में जोड़ा जा सकता है।"),
        ("एक दिन में देवघर में क्या-क्या घूम सकते हैं?",
         "बाबा बैद्यनाथ धाम, नौलखा मंदिर, तपोवन, त्रिकूट पर्वत और सत्संग आश्रम एक दिन में आराम से हो जाते हैं। बासुकीनाथ जोड़ना हो तो पूरा दिन लगता है।"),
        ("देवघर टूर पैकेज की कीमत क्या है?",
         f"पैकेज ₹1500 से शुरू होते हैं। सही कीमत दिन, गाड़ी और होटल देखकर फ़ोन पर बताई जाती है &ndash; कॉल करें {PHONE_PRETTY}।"),
        ("क्या जसीडीह स्टेशन या देवघर एयरपोर्ट से पिकअप मिलेगा?",
         "हाँ। जसीडीह जंक्शन, देवघर एयरपोर्ट, मधुपुर, झाझा या सिमुलतला &ndash; जहाँ उतरें, वहीं से टूर शुरू होता है।"),
    ]
    faq_html = "".join(f'''
          <details>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>''' for q, a in faqs)
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": BRAND, "item": url()},
        {"@type": "ListItem", "position": 2, "name": "Deoghar Tour Package", "item": canonical}]}
    biz = business_ld(area=[{"@type": "City", "name": "Deoghar, Jharkhand"}], page_url=canonical)
    from_links = "".join(f'<li><a href="{slug(l[0])}">{l[0]} Taxi</a></li>' for l in nearest("Deoghar", 20))
    return f'''<!DOCTYPE html>
<html lang="hi">
<head>
{common_head(title, desc, keywords, canonical)}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Mukta:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
{ld_script(biz, breadcrumb, faq_ld(faqs))}
</head>
<body>

{SPRITE}{HEADER}  <main id="top">
    <section class="hero loc-hero">
      <div class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">{BRAND}</a> <span aria-hidden="true">/</span> Deoghar Tour Package</nav>
        <p class="hero__place">देवघर, झारखंड <span class="hero__badge">10+ साल, 50+ गाड़ियाँ, 1,00,000+ सफ़र</span></p>
        <h1>देवघर टूर पैकेज</h1>
        <p class="loc-hero__en">Deoghar Tour Package &amp; Baba Dham Darshan Taxi</p>
        <p class="hero__lede">बाबा बैद्यनाथ धाम, बासुकीनाथ, तपोवन, त्रिकूट और नौलखा मंदिर &ndash; पूरा रूट हम तय करते हैं, ड्राइवर हर जगह इंतज़ार करता है। होटल भी साथ में बुक हो जाता है।</p>
        <a class="plate" data-call href="{tel()}" aria-label="कॉल करें">
          <span class="plate__label">पैकेज के लिए कॉल करें</span>
          <span class="plate__num" data-phone-text>{PHONE_PRETTY}</span>
        </a>
        <div class="hero__row">
          {WA_BTN.replace('data-wa ', 'data-wa data-msg="देवघर टूर पैकेज" ', 1)}
          <p class="hero__price">पैकेज <strong>₹1500</strong> से शुरू<sup>*</sup></p>
        </div>
        <p class="hero__note">* पूरी कीमत दिन, गाड़ी और होटल देखकर फ़ोन पर बताई जाती है।</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="head">
          <h2>सभी टूर पैकेज</h2>
          <p>Car, driver and fuel included. Hotel can be added to any package.</p>
        </div>
{packages}
      </div>
    </section>

    <section class="section section--mist" id="faq">
      <div class="wrap faq">
        <div class="head">
          <h2>देवघर टूर: सवाल-जवाब</h2>
          <p>Deoghar tour package FAQs</p>
        </div>
        <div class="faq__list">{faq_html}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="head">
          <h2>कहीं से भी टूर शुरू करें</h2>
          <p>Pickup from any town within 100 km of Deoghar and Simultala.</p>
        </div>
        <ul class="loc-links">{from_links}<li><a href="index.html#area">सभी शहर</a></li></ul>
      </div>
    </section>

    <section class="final">
      <div class="wrap final__in">
        <h2>देवघर घूमना है? अभी कॉल कीजिए।</h2>
        <a class="plate plate--dark" data-call href="{tel()}" aria-label="कॉल करें">
          <span class="plate__label">कॉल करें</span>
          <span class="plate__num" data-phone-text>{PHONE_PRETTY}</span>
        </a>
      </div>
    </section>
  </main>

{TAIL}'''


# ---------------------------------------------------------------- index.html
def patch_index():
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    places = ", ".join(l[0] for l in LOCATIONS[1:13])
    title = "Simultala Cab Service | Deoghar Taxi Service, Simultala Taxi, Hansdiha Taxi &amp; Deoghar Tour Package"
    desc = ("Simultala Cab Service – देवघर और सिमुलतला से 100 km तक हर जगह टैक्सी। Deoghar taxi service, Simultala taxi, "
            "Hansdiha, Jasidih, Jhajha, Jamui, Basukinath, Dumka, Giridih, Dhanbad taxi। Deoghar tour package, बाबा धाम दर्शन, "
            f"station pickup, airport, outstation cab, hotel booking. 10+ साल, 50+ गाड़ियाँ। ₹1500 से। Call {PHONE_PRETTY}.")
    kw_match = re.search(r'<meta name="keywords" content="(.*?)">', s)
    keywords = [k.strip() for k in (kw_match.group(1) if kw_match else "").split(",") if k.strip()]
    extra = ["Deoghar taxi service", "Simultala taxi service", "Hansdiha taxi service", "Deoghar cab service",
             "Deoghar tour package", "Baba Dham tour package", "Deoghar Basukinath tour package", "Deoghar sightseeing taxi",
             "Deoghar airport taxi", "AIIMS Deoghar taxi", "Jasidih to Deoghar taxi", "Deoghar to Basukinath taxi",
             "Deoghar to Patna taxi", "Deoghar to Ranchi taxi", "Deoghar to Kolkata taxi", "Deoghar to Dhanbad taxi",
             "Shravani Mela taxi", "Simultala tour package", "Parasnath tour package",
             "देवघर टैक्सी सर्विस", "सिमुलतला टैक्सी सर्विस", "हंसडीहा टैक्सी सर्विस", "देवघर टूर पैकेज", "बाबा धाम टूर पैकेज"]
    extra += [f"{l[0]} taxi service" for l in LOCATIONS] + [f"{l[1]} टैक्सी" for l in LOCATIONS]
    keywords = ", ".join(dict.fromkeys(keywords + extra))
    head_new = common_head(title, desc, keywords, url())

    start = s.index("<head>") + len("<head>\n")
    end = s.index('  <link rel="preconnect" href="https://fonts.googleapis.com">')
    s = s[:start] + head_new + "\n" + s[end:]

    # schema: business + FAQ + website
    faqs = re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", s, flags=re.S)
    website = {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "alternateName": BRAND_HI, "url": url(),
               "inLanguage": ["hi-IN", "en-IN"]}
    old = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S).group(1))
    area = old.get("areaServed") or []
    names = {a["name"].split(",")[0] for a in area}
    area += [{"@type": "Place", "name": f"{l[0]}, {l[3]}"} for l in LOCATIONS if l[0] not in names]
    biz = business_ld(area=area)
    biz["description"] = old.get("description", "")
    ld = ld_script(biz, faq_ld(faqs), website)
    s = re.sub(r'(  <script type="application/ld\+json">.*?</script>\n)+', lambda m: ld + "\n", s, count=1, flags=re.S)

    # location page links (inside coverage section)
    groups = {}
    for l in LOCATIONS:
        groups.setdefault((l[2], l[3]), []).append(l)
    links = "".join(
        f'\n          <div class="loc-group"><h4>{d} <small>{STATE_HI[st]}</small></h4><ul class="loc-links">'
        + "".join(f'<li><a href="{slug(l[0])}">{l[0]} Taxi</a></li>' for l in ls) + "</ul></div>"
        for (d, st), ls in groups.items())
    block = (f'<!-- LOC-LINKS:START -->\n        <h3 class="districts__title">देवघर और सिमुलतला से 100 km तक: शहर के हिसाब से टैक्सी</h3>\n'
             f'        <p class="loc-tour"><a class="btn btn--ink" href="{TOUR_SLUG}">देवघर टूर पैकेज देखें</a></p>\n'
             f'        <div class="loc-groups">{links}\n        </div>\n        <!-- LOC-LINKS:END -->')
    if "<!-- LOC-LINKS:START -->" in s:
        s = re.sub(r"<!-- LOC-LINKS:START -->.*?<!-- LOC-LINKS:END -->", lambda m: block, s, flags=re.S)
    else:
        s = s.replace('        <p class="loc-note">', f'        {block}\n        <p class="loc-note">', 1)

    s = phone_fix(s)
    if 'src="js/main.js" defer' not in s:
        s = s.replace('<script src="js/main.js"></script>', '<script src="js/main.js" defer></script>')
    p.write_text(s, encoding="utf-8")


def phone_fix(s):
    s = re.sub(r"tel:\+91\d{10}", tel(), s)
    s = re.sub(r"https://wa\.me/91\d{10}", wa(), s)
    s = re.sub(r'"telephone": "\+91\d{10}"', f'"telephone": "+91{PHONE}"', s)
    s = re.sub(r"(data-phone-text>)\d{5} \d{5}", rf"\g<1>{PHONE_PRETTY}", s)
    return s


# ---------------------------------------------------------------- images
def build_images():
    from PIL import Image, ImageDraw, ImageFont
    fonts = Path("C:/Windows/Fonts")
    bold = lambda n: ImageFont.truetype(str(fonts / "segoeuib.ttf"), n)
    reg = lambda n: ImageFont.truetype(str(fonts / "segoeui.ttf"), n)
    forest, taxi, hill = (14, 59, 46), (255, 198, 26), (26, 94, 71)

    def milestone(d, x, y, w):
        h = int(w * 1.15)
        r = w // 2
        d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill="white")
        d.pieslice([x, y, x + w, y + w], 180, 360, fill=taxi)
        d.rectangle([x, y + r, x + w, y + int(r * 1.25)], fill=taxi)
        d.polygon([(x, y + h), (x, y + int(h * .78)), (x + w * .35, y + h * .64), (x + w * .6, y + h * .74),
                   (x + w, y + h * .66), (x + w, y + h)], fill=hill)

    # social share image
    img = Image.new("RGB", (1200, 630), forest)
    d = ImageDraw.Draw(img)
    d.ellipse([940, 220, 1140, 420], fill=taxi)
    d.polygon([(0, 470), (200, 360), (420, 440), (640, 330), (900, 420), (1200, 340), (1200, 630), (0, 630)], fill=hill)
    d.rectangle([0, 540, 1200, 600], fill=(43, 47, 51))
    for x in range(0, 1200, 60):
        d.rectangle([x, 567, x + 34, 573], fill="white")
    milestone(d, 70, 60, 90)
    d.text((180, 62), "Simultala Cab Service", font=bold(64), fill="white")
    d.text((182, 140), "Taxi within 100 km  |  Deoghar  |  Jhajha  |  Jamui  |  Jasidih", font=reg(30), fill=(220, 232, 226))
    d.text((70, 230), "10+ years   50+ cabs   1,00,000+ trips", font=bold(44), fill=taxi)
    d.rounded_rectangle([70, 320, 600, 470], radius=14, fill=taxi, outline="black", width=6)
    d.text((100, 334), "Call now  |  Fare from \u20b91500", font=bold(30), fill="black")
    d.text((98, 372), PHONE_PRETTY, font=bold(72), fill="black")
    img.save(ROOT / "assets/og-image.png", optimize=True)

    # app icons
    for size, name in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")]:
        ic = Image.new("RGB", (size, size), forest)
        di = ImageDraw.Draw(ic)
        w = int(size * .56)
        milestone(di, (size - w) // 2, int(size * .14), w)
        f = bold(int(size * .13))
        tw = di.textlength("SCS", font=f)
        di.text(((size - tw) / 2, int(size * .2)), "SCS", font=f, fill=forest)
        ic.save(ROOT / "assets" / name, optimize=True)


# ---------------------------------------------------------------- run
def main():
    patch_index()
    load_template()
    pages = []
    for loc in LOCATIONS:
        (ROOT / slug(loc[0])).write_text(phone_fix(location_page(loc)), encoding="utf-8")
        pages.append(slug(loc[0]))

    (ROOT / TOUR_SLUG).write_text(phone_fix(tour_page()), encoding="utf-8")
    entries = [(url(), "1.0", "daily"), (url(TOUR_SLUG), "0.9", "weekly")] + [(url(p), "0.8", "weekly") for p in pages]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc_url, prio, freq in entries:
        sitemap.append(f"  <url>\n    <loc>{escape(loc_url)}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
                       f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>")
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {url('sitemap.xml')}\n", encoding="utf-8")

    manifest = {"name": BRAND, "short_name": "Simultala Cab", "start_url": "/", "display": "standalone",
                "background_color": "#0E3B2E", "theme_color": "#0E3B2E", "lang": "hi",
                "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}
    (ROOT / "site.webmanifest").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    build_images()
    print(f"Done: index.html + {len(pages)} location pages, sitemap.xml, robots.txt, images. Phone {PHONE}, site {SITE_URL}")


if __name__ == "__main__":
    main()
