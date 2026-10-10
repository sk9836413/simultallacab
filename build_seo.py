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
        "hasMap": "https://www.google.com/maps/search/?api=1&query=Simultala%2C+Jamui%2C+Bihar+811316",
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
    state_hi = "बिहार" if state == "Bihar" else "झारखंड"
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
        f"{en} wedding car", f"{en} tour and travels", "Simultala Cab Service"])
    dist_line = (f"सिमुलतला से {hi} की दूरी लगभग {km} km है।" if km else "")
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
    others = "".join(f'<li><a href="{slug(l[0])}">{l[0]} Taxi</a></li>' for l in LOCATIONS if l[0] != en)
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


# ---------------------------------------------------------------- index.html
def patch_index():
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    places = ", ".join(l[0] for l in LOCATIONS[1:13])
    title = f"Simultala Cab Service | सिमुलतला टैक्सी सर्विस – Jhajha, Jamui, Deoghar, Jasidih Taxi ₹1500 से"
    desc = ("Simultala Cab Service – 10+ साल, 50+ गाड़ियाँ, 1,00,000+ सफ़र। सिमुलतला से 100 km तक हर जगह टैक्सी: "
            f"{places}, Giridih, Basukinath, Dumka, Jamtara, Godda। Deoghar darshan, station pickup, airport, outstation cab, "
            f"tour package, hotel booking. किराया ₹1500 से शुरू। Call {PHONE_PRETTY}.")
    kw_match = re.search(r'<meta name="keywords" content="(.*?)">', s)
    keywords = kw_match.group(1) if kw_match else ""
    head_new = common_head(title, desc, keywords, url())

    start = s.index("<head>") + len("<head>\n")
    end = s.index('  <link rel="preconnect" href="https://fonts.googleapis.com">')
    s = s[:start] + head_new + "\n" + s[end:]

    # schema: business + FAQ + website
    faqs = re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", s, flags=re.S)
    website = {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "alternateName": BRAND_HI, "url": url(),
               "inLanguage": ["hi-IN", "en-IN"]}
    old = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S).group(1))
    biz = business_ld(area=old.get("areaServed"))
    biz["description"] = old.get("description", "")
    ld = ld_script(biz, faq_ld(faqs), website)
    s = re.sub(r'(  <script type="application/ld\+json">.*?</script>\n)+', lambda m: ld + "\n", s, count=1, flags=re.S)

    # location page links (inside coverage section)
    links = "".join(f'<li><a href="{slug(l[0])}">{l[0]} Taxi Service</a></li>' for l in LOCATIONS)
    block = (f'<!-- LOC-LINKS:START -->\n        <h3 class="districts__title">शहर के हिसाब से टैक्सी</h3>\n'
             f'        <ul class="loc-links">{links}</ul>\n        <!-- LOC-LINKS:END -->')
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

    entries = [(url(), "1.0", "daily")] + [(url(p), "0.8", "weekly") for p in pages]
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
