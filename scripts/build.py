#!/usr/bin/env python3
"""Regenerates index.html and download.html from the content below.
Run from anywhere: python3 scripts/build.py"""
import html, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_URL = "https://prakritirupa.vercel.app"
BMC = "https://buymeacoffee.com/bipashant"
KINDLE = "https://www.amazon.com/dp/B0HN3JPRBT"
# Kindle books are sold per country store: a reader must use the store that matches their Amazon account.
KINDLE_STORES = [
    ("United States", "Amazon.com", "https://www.amazon.com/dp/B0HN3JPRBT"),
    ("Australia", "Amazon.com.au", "https://www.amazon.com.au/dp/B0HN3JPRBT"),
]

FORMS = [
    dict(slug="shailaputri", night="१", day="Night 1", name="Shailaputri", deva="शैलपुत्री",
         essence="Daughter of the mountain, steady as stone.",
         attrs="Rides a white bull · holds a trident and a lotus · a half-moon in her hair",
         story=["In an earlier life she was Sati. When her father, King Daksha, mocked Shiva in front of everyone at his great sacred fire, she let her body go. She was born again to Himavat, king of the Himalaya, and his queen Mena, who named her Parvati, the mountain's daughter.",
                "She has already lost everything once, and she has come back smiling. The nine forms begin with her: with a mountain, and a return."],
         mantra="ॐ देवी शैलपुत्र्यै नमः", translit="Om Devi Shailaputryai Namah",
         meaning="Om, I bow to the Goddess Shailaputri."),
    dict(slug="brahmacharini", night="२", day="Night 2", name="Brahmacharini", deva="ब्रह्मचारिणी",
         essence="She who walks the path of discipline.",
         attrs="Walks barefoot · holds prayer beads and a water pot",
         story=["Shiva was still grieving for Sati and noticed no one, so the young Parvati set out to become as strong in spirit as he was. She sat between fires in summer and stood in icy water on winter nights. She ate only fruit, then fallen leaves, then not even leaves, and people called her Aparna, “the one without even a leaf.”",
                "At last a young student came to mock Shiva, and she angrily sent him away. He smiled and showed his true face. It was Shiva himself: “From today, I am yours.”"],
         mantra="ॐ देवी ब्रह्मचारिण्यै नमः", translit="Om Devi Brahmacharinyai Namah",
         meaning="Om, I bow to the Goddess Brahmacharini."),
    dict(slug="chandraghanta", night="३", day="Night 3", name="Chandraghanta", deva="चन्द्रघण्टा",
         essence="Grace that is ready for battle.",
         attrs="Rides a lion · ten arms · a bell-shaped half-moon on her brow",
         story=["Her name means “moon bell,” for the bell-shaped half-moon on her forehead. No old story carries her name, so the tales told about her are newer ones. In one, Shiva arrives at the wedding with ghosts and wild hermits, and Parvati's mother faints. Parvati takes this fierce form on her lion and stands between her family and the wedding party until Shiva agrees to come as a bridegroom should.",
                "In another, the ring of her moon bell scatters an army of giant bats. Her face stays calm, almost gentle. She is ready for battle; she just isn't angry about it."],
         mantra="ॐ देवी चन्द्रघण्टायै नमः", translit="Om Devi Chandraghantayai Namah",
         meaning="Om, I bow to the Goddess Chandraghanta."),
    dict(slug="kushmanda", night="४", day="Night 4", name="Kushmanda", deva="कूष्माण्डा",
         essence="Her smile lit the first light of the universe.",
         attrs="Rides a tiger · eight arms · lives at the heart of the sun",
         story=["Her name is often read as ku, little, ushma, warmth, and anda, egg: the little warm egg the whole universe grew from. Before anything existed there was only darkness. Then she smiled, and the light of that smile broke the warm egg of the world open into stars and planets and suns.",
                "Ever since, they say, she has lived at the heart of the sun. When the sun warms your face on a cold morning, you could think of it as her smile, still reaching you."],
         mantra="ॐ देवी कूष्माण्डायै नमः", translit="Om Devi Kushmandayai Namah",
         meaning="Om, I bow to the Goddess Kushmanda."),
    dict(slug="skandamata", night="५", day="Night 5", name="Skandamata", deva="स्कन्दमाता",
         essence="A mother holding the young warrior in her lap.",
         attrs="Sits on a lotus · a lion resting beside her · holds baby Skanda and two lotus flowers",
         story=["Only a son of Shiva could defeat the demon Taraka. That son, Skanda, also called Kartikeya or Murugan, was carried into the world by fire, by the river Ganga and by six star-maidens, the Pleiades, and grew six faces to drink from all six. Then Parvati lifted him onto her lap and fed him as her own.",
                "When he was grown, she gave him a spear called Shakti, her own power in the shape of a weapon, and with it he set the heavens free. She gave him more than milk. She gave him her strength."],
         mantra="ॐ देवी स्कन्दमातायै नमः", translit="Om Devi Skandamatayai Namah",
         meaning="Om, I bow to the Goddess Skandamata."),
    dict(slug="katyayani", night="६", day="Night 6", name="Katyayani", deva="कात्यायनी",
         essence="Courage that answers in a single leap.",
         attrs="Rides a lion · holds a crescent sword and a lotus",
         story=["Her name means “daughter of Katyayana,” a wise old hermit. Some say she appeared in his forest home; others say she took his name because he was the first to pray to her. In one telling she is the goddess born from the gods' anger. When the buffalo demon asked to marry her, she told him to beat her in battle first, then leapt from her lion onto his back and struck him down.",
                "Her other story is gentler. In a village by the river Yamuna, girls in love with Krishna bathed in the cold river before dawn for a whole month and prayed to her to make him their husband. Young women still pray to her when they hope to find the right person to marry."],
         mantra="ॐ देवी कात्यायन्यै नमः", translit="Om Devi Katyayanyai Namah",
         meaning="Om, I bow to the Goddess Katyayani."),
    dict(slug="kalaratri", night="७", day="Night 7", name="Kalaratri", deva="कालरात्रि",
         essence="The darkest night, which swallows fear.",
         attrs="Rides a donkey · dark skin, wild hair, fire in her breath",
         story=["Kala means both black and time, and ratri means night, so she is the Black Night, the Night of Time. She is the form people fear most, and she means to be. In a story long told about her, she drinks every drop of the demon Raktabija's blood before it can touch the ground and rise up as another demon.",
                "Yet she is also called Shubhankari, “the one who brings good.” Two of her four hands bless and say “don't be afraid.” She never harms those who come to her. She only frightens the things that frighten them."],
         mantra="ॐ देवी कालरात्र्यै नमः", translit="Om Devi Kalaratryai Namah",
         meaning="Om, I bow to the Goddess Kalaratri."),
    dict(slug="mahagauri", night="८", day="Night 8", name="Mahagauri", deva="महागौरी",
         essence="Pure white light after the long penance.",
         attrs="Rides a white bull · holds a trident and a small drum",
         story=["Three stories tell how she became so bright, and they don't agree. The one most people tell today is the simplest: after years of hard practice in the sun, rain and dust, Parvati's body had turned dark. When Shiva finally accepted her, he washed her with water from the river Ganga, and her skin shone white as lightning.",
                "She comes after the long dark of Kalaratri and feels like rest, like the first clear morning after the rains, when everything looks new."],
         mantra="ॐ देवी महागौर्यै नमः", translit="Om Devi Mahagauryai Namah",
         meaning="Om, I bow to the Goddess Mahagauri."),
    dict(slug="siddhidatri", night="९", day="Night 9", name="Siddhidatri", deva="सिद्धिदात्री",
         essence="She who gives every gift away.",
         attrs="Sits on a lotus · a lion beside her · holds a discus, conch, mace and lotus",
         story=["A siddhi is a perfection, a mastery that comes after long practice. She holds them all and gives them away. Sages, heavenly musicians, forest spirits and even demons gather around her with folded hands, and nobody is turned away.",
                "When Shiva asked her for the power to create, she gave him every gift she had, and then became half of him. That is Ardhanarishvara, “the lord who is half woman.” With her, the nine nights are complete."],
         mantra="ॐ देवी सिद्धिदात्र्यै नमः", translit="Om Devi Siddhidatryai Namah",
         meaning="Om, I bow to the Goddess Siddhidatri."),
]
TENTH = dict(slug="mahishasuramardini", night="१०", day="Day 10 · Vijaya Dashami", name="Mahishasuramardini", deva="महिषासुरमर्दिनी",
         essence="The victory of the tenth day.",
         attrs="Rides a lion · ten arms · strikes down the buffalo demon",
         story=["Mahishasura could become anything: a buffalo, a lion, a man with a sword, an elephant. She did not chase every shape. She held him still, and when his true face came crawling half out of the buffalo, she ended it, while flowers fell from the clouds.",
                "That victory is celebrated on the tenth day, Vijaya Dashami, the great day of Dashain. Before she left, she made a promise: whenever you need me, call, and I will come."],
         mantra="ॐ दुं दुर्गायै नमः", translit="Om Dum Durgayai Namah",
         meaning="Om, Dum, I bow to Durga. Dum is a seed syllable, a sacred sound that carries her power.")

e = html.escape

def detail(f):
    paras = "".join(f"<p>{e(p)}</p>" for p in f["story"])
    return (f'<div class="detail" hidden>'
            f'<p class="eyebrow">{e(f["day"])}</p>'
            f'<h3>{e(f["name"])}<span class="deva" lang="sa">{f["deva"]}</span></h3>'
            f'<p class="attrs">{e(f["attrs"])}</p>{paras}'
            f'<div class="mantra"><span class="label">Her mantra</span>'
            f'<span class="sanskrit" lang="sa">{f["mantra"]}</span>'
            f'<span class="translit">{e(f["translit"])}</span>'
            f'<span class="meaning">{e(f["meaning"])}</span></div></div>')

cards = []
for i, f in enumerate(FORMS):
    cards.append(f'''
        <article class="card" id="{f["slug"]}" data-index="{i}">
          <button type="button" aria-haspopup="dialog" aria-label="Read the story of {e(f["name"])}">
            <span class="art"><img src="/img/{f["slug"]}.webp" alt="{e(f["name"])}: {e(f["attrs"].replace(" · ", ", ").lower())}" width="1000" height="1506" loading="lazy" decoding="async"></span>
            <span class="night"><span class="num" lang="sa">{f["night"]}</span>{e(f["day"])}</span>
            <h3>{e(f["name"])}<span class="deva" lang="sa">{f["deva"]}</span></h3>
            <span class="essence">{e(f["essence"])}</span>
            <span class="more">Her story and mantra</span>
          </button>
          {detail(f)}
        </article>''')

ICON_DL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M5 21h14"/></svg>'
ICON_CUP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9h12v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V9z"/><path d="M16 11h1.5a2.5 2.5 0 0 1 0 5H16"/><path d="M8 3c0 1.5 1 1.5 1 3M12 3c0 1.5 1 1.5 1 3"/></svg>'
ICON_KINDLE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="2.5" width="14" height="19" rx="2"/><path d="M8.5 7h7M8.5 10.5h7M8.5 14h4"/></svg>'
def god_art(name):
    """Inline one of the Trimurti line drawings from img/gods, scaled by its own height so the faces match."""
    svg = open(os.path.join(ROOT, "img", "gods", f"{name}.svg")).read().strip()
    h = re.search(r'viewBox="0 0 [\d.]+ ([\d.]+)"', svg).group(1)
    return svg.replace("<svg ", f'<svg class="god-art" style="--h:{h}" ', 1)

LOTUS_RULE = '<svg class="lotus-rule" viewBox="0 0 120 18" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M0 9h42M78 9h42"/><path d="M60 2c4 4 5 7 5 9s-2 4-5 5c-3-1-5-3-5-5s1-5 5-9z"/><path d="M52 7c-1 4 1 7 8 9M68 7c1 4-1 7-8 9"/><circle cx="60" cy="10" r="1.4" fill="currentColor"/></svg>'
DIYA = '<svg class="diya" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 6c3 4 4 7 4 9.5a4 4 0 0 1-8 0C20 13 21 10 24 6z" fill="currentColor" fill-opacity=".25"/><path d="M6 26c4 0 7 1 10 2.5 3 1.5 13 1.5 16 0 3-1.5 6-2.5 10-2.5-2 8-9 13-18 13S8 34 6 26z"/><path d="M18 42h12"/></svg>'

VA = '''<script>window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };</script>
  <script defer src="/_vercel/insights/script.js"></script>
  <script>window.si = window.si || function () { (window.siq = window.siq || []).push(arguments); };</script>
  <script defer src="/_vercel/speed-insights/script.js"></script>'''

head_common = f'''<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#130B0C">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="/fonts/rozha-one-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/spectral-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css">
  {VA}'''

DESC = "An illustrated book by Bibek Sharma Chapagain on Durga, the Mother Goddess as nature, and the forms she takes across the nine nights of Navaratri and Dashain. Images, stories and Sanskrit mantras with meaning."

index = f'''<!doctype html>
<html lang="en">
<head>
  {head_common}
  <title>She Who Is Nature · Durga and Her Nine Forms</title>
  <meta name="description" content="{e(DESC)}">
  <link rel="canonical" href="{SITE_URL}/">
  <meta property="og:type" content="book">
  <meta property="og:title" content="She Who Is Nature · Durga and Her Nine Forms">
  <meta property="og:description" content="{e(DESC)}">
  <meta property="og:url" content="{SITE_URL}/">
  <meta property="og:image" content="{SITE_URL}/img/og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="The cover face of She Who Is Nature: half Kalaratri in fire, half Mahagauri in pearls">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preload" href="/img/hero-split-face.webp" as="image" type="image/webp">
  <script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"Book","name":"She Who Is Nature","alternateName":"प्रकृतिरूपा","description":DESC,"author":{"@type":"Person","name":"Bibek Sharma Chapagain"},"illustrator":{"@type":"Person","name":"Bibek Sharma Chapagain"},"inLanguage":"en","image":SITE_URL+"/img/og.jpg","url":SITE_URL+"/","workExample":{"@type":"Book","name":"She Who Is Nature (Kindle edition)","bookFormat":"https://schema.org/EBook","url":KINDLE}}, ensure_ascii=False)}</script>
</head>
<body>
  <header class="topbar">
    <div class="wrap">
      <a class="mark" href="/" lang="sa" aria-label="She Who Is Nature, home">प्रकृतिरूपा</a>
      <nav class="topnav" aria-label="Sections">
        <a class="link" href="#inside">Inside the book</a>
        <a class="link" href="#nights">The nine forms</a>
        <a class="link" href="#support">Support</a>
        <a class="btn btn-primary" href="/download">{ICON_DL}Download</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero" aria-labelledby="title">
      <canvas id="embers" aria-hidden="true"></canvas>
      <div class="hero-deva" lang="sa" aria-hidden="true">प्रकृतिरूपा</div>
      <div class="wrap hero-inner">
        <div class="hero-face">
          <img src="/img/hero-split-face.webp" width="1200" height="1805" alt="One face split down the middle: on the left Kalaratri, dark-skinned and wreathed in fire; on the right Mahagauri, fair and crowned with pearls" fetchpriority="high">
        </div>
        <div class="hero-copy">
          <p class="eyebrow">An illustrated book</p>
          <h1 id="title">She Who Is Nature</h1>
          <p class="sub">Durga and Her Nine Forms &nbsp;·&nbsp; <span class="deva" lang="sa">प्रकृतिरूपा</span></p>
          <p class="by">By Bibek Sharma Chapagain</p>
          <div class="hero-cta">
            <a class="btn btn-primary" href="/download">{ICON_DL}Download the book</a>
            <a class="btn btn-ghost" href="/kindle">{ICON_KINDLE}Get it on Kindle</a>
          </div>
          <ul class="hero-facts">
            <li>14 chapters</li>
            <li>Sanskrit mantras with meaning</li>
            <li>Free PDF</li>
          </ul>
        </div>
      </div>
      <div class="edge edge-bottom" aria-hidden="true"></div>
    </section>

    <section class="verse" aria-label="Opening verse">
      <div class="wrap">
        {LOTUS_RULE}
        <p class="sanskrit" lang="sa">या देवी सर्वभूतेषु शक्तिरूपेण संस्थिता।<br>नमस्तस्यै नमस्तस्यै नमस्तस्यै नमो नमः॥</p>
        <p class="translit">Ya devi sarvabhuteshu shakti-rupena samsthita, namas tasyai namas tasyai namas tasyai namo namah.</p>
        <p class="meaning">To the Goddess who lives in every being as strength, I bow to her, I bow to her, again and again I bow.</p>
        <p class="source">From the Devi Mahatmya</p>
      </div>
    </section>

    <section class="prelude" aria-labelledby="prelude-title">
      <div class="wrap">
        <p class="eyebrow">Before the nine forms</p>
        <h2 id="prelude-title">A World Full of Gods</h2>
        <p>Hindu tradition honours countless gods, of rivers and mountains, of sun and rain and strength. The idea underneath is simple: a god is anything that made you what you are. Water to drink. Soil to grow food. The sun that wakes you, the fire that warms you. So people learned to bow to them, the way you'd thank anyone who kept you alive.</p>
        <ul class="trinity" aria-label="The three great movements">
          <li>{god_art("brahma")}<strong>Brahma</strong><span>creates</span></li>
          <li>{god_art("vishnu")}<strong>Vishnu</strong><span>sustains</span></li>
          <li>{god_art("shiva")}<strong>Shiva</strong><span>lets end, to make way</span></li>
        </ul>
        <p>Someone who longs to sing bows to Saraswati. Someone who wants to grow strong and steady prays to Hanuman. They aren't asking for a gift from far away. They are waking that same energy in themselves. <em>Durga</em> is one of her best-loved faces.</p>
      </div>
    </section>

    <section class="feature" id="inside" aria-labelledby="inside-title">
      <div class="wrap">
        <div class="feature-art">
          <img src="/img/prakriti.webp" width="1000" height="1506" loading="lazy" decoding="async" alt="Durga as nature herself: her hair becomes a forested mountain, her sari flows into a river, and terraced mustard fields and a village lie at her feet">
        </div>
        <div class="feature-text">
          <p class="eyebrow">Chapter 1 · She Who Is Nature</p>
          <h2 id="inside-title">The mountain, the river, the field in flower. All of it is her.</h2>
          <p><em>She Who Is Nature</em> tells the story of Durga, the great Mother Goddess, and the forms she takes during the nine nights of Navaratri, celebrated in Nepal as Dashain. In this telling she lives close by, as Prakriti, nature itself: the ground under our feet, the rain and the fire, and the quiet strength inside every living thing.</p>
          <p>Each chapter brings one of her forms to life with a story, an image of her, and her mantra in Sanskrit with simple pronunciation and meaning. You don't need to know anything about Hindu tradition to enjoy it.</p>
          <ul class="inside" aria-label="Inside the book">
            <li><strong>14 chapters</strong><span>From nature herself to her victory on the tenth day, and the old hymn that finds her in all beings.</span></li>
            <li><strong>An image for every form</strong><span>Her visual representation, full of old signs, with a short guide at the back to reading them.</span></li>
            <li><strong>Mantras you can say aloud</strong><span>Each in Sanskrit, with easy pronunciation and a plain English meaning.</span></li>
            <li><strong>Written for everyone</strong><span>Simple words, no background needed, and sources listed at the back.</span></li>
          </ul>
        </div>
      </div>
    </section>

    <section class="feature flip" aria-labelledby="origin-title">
      <div class="wrap">
        <div class="feature-art">
          <img src="/img/origin.webp" width="1000" height="1506" loading="lazy" decoding="async" alt="The gods stand in a circle on a dark mountain as streams of golden light pour from them and join into the many-armed, fiery form of Durga">
        </div>
        <div class="feature-text">
          <p class="eyebrow">Chapter 2 · A Mountain of Fire Becomes a Woman</p>
          <h2 id="origin-title">When the gods had nothing left, their light became her.</h2>
          <p>After a war of a hundred years, the buffalo demon Mahishasura threw Indra off the throne of heaven and drove the gods out to wander the earth. When Vishnu and Shiva heard, their faces darkened with anger. A great light poured from Vishnu's face, then from Brahma, from Shiva and from everyone there, and it all flowed together like rivers running to the sea.</p>
          <p>The light became a mountain of fire, and slowly the fire took a woman's shape. Shiva gave her a trident, Vishnu a discus, Indra his thunderbolt, and the king of the mountains a lion. She laughed, and the mountains shook.</p>
          <p class="note">This story comes from the Devi Mahatmya, an old Sanskrit poem still recited during Dashain.</p>
        </div>
      </div>
    </section>

    <section class="nights" id="nights" aria-labelledby="nights-title">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Navaratri · nine nights</p>
          <h2 id="nights-title">Nine nights, nine forms</h2>
          <p>Her nine names come from a short old prayer, the Devi Kavacham, said to have been spoken by Brahma himself. Over the nine nights of Navaratri they are honoured one at a time, like lamps lit one after another, from the daughter of the mountain to the giver of every gift. Tap an image to read her story and her mantra.</p>
        </div>
        <div class="grid">{"".join(cards)}
        </div>
      </div>
    </section>

    <section class="feature tenth" id="{TENTH["slug"]}" data-index="9" aria-labelledby="tenth-title">
      <div class="wrap">
        <div class="feature-art">
          <img src="/img/{TENTH["slug"]}.webp" width="1000" height="1506" loading="lazy" decoding="async" alt="Durga stands on the buffalo demon and drives her trident into it as Mahishasura crawls out of its mouth, her lion biting its back, while flowers fall from the clouds">
        </div>
        <div class="feature-text">
          <p class="eyebrow">The tenth day · Vijaya Dashami</p>
          <h2 id="tenth-title">Mahishasuramardini<span class="deva" lang="sa">महिषासुरमर्दिनी</span></h2>
          <p>{e(TENTH["story"][0])}</p>
          <p>{e(TENTH["story"][1])}</p>
          <div class="actions">
            <button type="button" class="btn btn-ink" data-open="9">Her mantra</button>
            <a class="btn btn-primary" href="/download">{ICON_DL}Download the book</a>
          </div>
        </div>
        {detail(TENTH)}
      </div>
    </section>

    <section class="night-band" id="support" aria-labelledby="dl-title">
      <div class="edge edge-top" aria-hidden="true"></div>
      <div class="wrap">
        <div class="offer">
          <div class="book3d">
            <div class="book">
              <span class="book-cover"><img src="/img/cover.webp" width="800" height="1200" loading="lazy" decoding="async" alt="The cover of She Who Is Nature: half Kalaratri in fire, half Mahagauri in pearls and jasmine, with the title in gold"></span>
            </div>
          </div>
          <div class="offer-main">
            <p class="eyebrow">Read it free</p>
            <h2 id="dl-title">Take her home with you.</h2>
            <p>Download the full book as a PDF and keep it on your phone, tablet or computer. Read it during Dashain, share it with family, send it to a friend who has always wondered who Durga is. Reading on a Kindle? It's on Amazon too.</p>
            <div class="actions">
              <a class="btn btn-primary" href="/download">{ICON_DL}Download the PDF</a>
              <a class="btn btn-ghost" href="/kindle">{ICON_KINDLE}Get it on Kindle</a>
            </div>
            <span class="small">14 chapters · images · mantras</span>
          </div>
          <aside class="support" aria-labelledby="support-title">
            {DIYA}
            <h3 id="support-title">Keep the lamp lit</h3>
            <p>These stories have been passed down for thousands of years, and I wanted to learn them and share them freely. If this book brought you a little closer to her, you can buy me a coffee. It helps me make the next one.</p>
            <a class="btn btn-ghost" href="{BMC}" target="_blank" rel="noopener">{ICON_CUP}Buy me a coffee</a>
          </aside>
        </div>
        <footer class="footer">
          <p class="deva" lang="sa">या देवी सर्वभूतेषु शक्तिरूपेण संस्थिता॥</p>
          <p>She Who Is Nature · Durga and Her Nine Forms</p>
          <p>© 2026 Bibek Sharma Chapagain · <a href="{BMC}" target="_blank" rel="noopener">buymeacoffee.com/bipashant</a></p>
        </footer>
      </div>
    </section>
  </main>

  <dialog class="viewer" id="viewer" aria-labelledby="viewer-title">
    <button type="button" class="viewer-close" data-close aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
    <div class="viewer-body">
      <div class="viewer-art"><img id="viewer-img" src="" alt="" width="1000" height="1506"></div>
      <div class="viewer-text">
        <div id="viewer-content"></div>
        <div class="viewer-nav">
          <button type="button" data-step="-1" aria-label="Previous form"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg></button>
          <button type="button" data-step="1" aria-label="Next form"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg></button>
          <span class="pos" id="viewer-pos"></span>
        </div>
      </div>
    </div>
  </dialog>

  <script src="/main.js" defer></script>
</body>
</html>
'''

download = f'''<!doctype html>
<html lang="en">
<head>
  {head_common}
  <title>Download · She Who Is Nature</title>
  <meta name="description" content="Download She Who Is Nature: Durga and Her Nine Forms, by Bibek Sharma Chapagain.">
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{SITE_URL}/download">
</head>
<body class="dl-page">
  <header class="topbar">
    <div class="wrap">
      <a class="mark" href="/" lang="sa" aria-label="She Who Is Nature, home">प्रकृतिरूपा</a>
      <nav class="topnav" aria-label="Sections"><a class="link" href="/">Back to the book</a></nav>
    </div>
  </header>
  <main class="dl-hero">
    <div class="wrap dl-grid">
      <img class="dl-face" src="/img/hero-split-face.webp" width="1200" height="1805" alt="The split face of Kalaratri and Mahagauri from the book's cover">
      <div class="dl-text">
        <p class="eyebrow">She Who Is Nature</p>
        <h1 id="dl-heading">Your copy is on its way.</h1>
        <p class="dl-status" id="dl-status" role="status"><span class="spinner" aria-hidden="true"></span><span>Starting your download…</span></p>
        <p id="dl-help">If nothing happens in a few seconds, use the button below. On a phone the book may open in a new tab, where you can save it or share it.</p>
        <div class="actions">
          <a class="btn btn-primary" id="dl-link" href="/she-who-is-nature.pdf" download="She-Who-Is-Nature-Bibek-Sharma-Chapagain.pdf">{ICON_DL}Download the PDF</a>
          <a class="btn btn-ghost" href="{BMC}" target="_blank" rel="noopener">{ICON_CUP}Buy me a coffee</a>
        </div>
        <p>Reading on a Kindle? <a class="kindle" href="/kindle">Get the Kindle edition on Amazon.</a></p>
        <p>If the book brings you something, a coffee helps me make the next one. Thank you for reading.</p>
        <p><a class="back" href="/">← Back to the book</a></p>
      </div>
    </div>
  </main>
  <script>
  (function () {{
    var link = document.getElementById("dl-link");
    var status = document.getElementById("dl-status");
    var help = document.getElementById("dl-help");
    function setStatus(text, done) {{
      status.innerHTML = (done ? "" : '<span class="spinner" aria-hidden="true"></span>') + "<span></span>";
      status.lastChild.textContent = text;
    }}
    // Check the file is there before starting, so a missing PDF never looks like a broken site.
    fetch(link.getAttribute("href"), {{ method: "HEAD", cache: "no-store" }}).then(function (r) {{
      if (!r.ok) throw new Error("missing");
      setTimeout(function () {{
        link.click();
        setStatus("Your download has started.", true);
      }}, 1200);
    }}).catch(function () {{
      setStatus("The PDF is being prepared. Please check back soon.", true);
      document.getElementById("dl-heading").textContent = "Almost ready.";
      help.textContent = "The book will be available to download here very soon.";
      link.hidden = true;
    }});
  }})();
  </script>
</body>
</html>
'''

store_btns = "".join(
    f'<a class="btn btn-ghost" href="{u}" target="_blank" rel="noopener">{ICON_KINDLE}{e(c)} <span class="small">{e(d)}</span></a>'
    for c, d, u in KINDLE_STORES)
kindle = f'''<!doctype html>
<html lang="en">
<head>
  {head_common}
  <title>Get it on Kindle · She Who Is Nature</title>
  <meta name="description" content="Get the Kindle edition of She Who Is Nature: Durga and Her Nine Forms, by Bibek Sharma Chapagain.">
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{SITE_URL}/kindle">
</head>
<body class="dl-page">
  <header class="topbar">
    <div class="wrap">
      <a class="mark" href="/" lang="sa" aria-label="She Who Is Nature, home">प्रकृतिरूपा</a>
      <nav class="topnav" aria-label="Sections"><a class="link" href="/">Back to the book</a></nav>
    </div>
  </header>
  <main class="dl-hero">
    <div class="wrap dl-grid">
      <img class="dl-face" src="/img/hero-split-face.webp" width="1200" height="1805" alt="The split face of Kalaratri and Mahagauri from the book's cover">
      <div class="dl-text">
        <p class="eyebrow">Kindle edition</p>
        <h1>Choose your Amazon store.</h1>
        <p>Kindle books can only be bought from the store that matches the country of your Amazon account. Pick yours below.</p>
        <div class="actions">{store_btns}</div>
        <p>Not listed? The free PDF works anywhere. <a class="kindle" href="/download">Download the PDF.</a></p>
        <p><a class="back" href="/">← Back to the book</a></p>
      </div>
    </div>
  </main>
</body>
</html>
'''

# Short plain-English notes for names and Sanskrit words, shown as tooltips on first use in each section.
GLOSSARY = {
    "Durga": "The Mother Goddess. Her name means “hard to reach,” like a fort high on a mountain.",
    "Prakriti": "Sanskrit for nature: the living world, in all its moods.",
    "Navaratri": "“Nine nights.” An autumn festival honouring the Goddess, one form each night.",
    "Dashain": "Nepal's biggest festival. It is the same festival as Navaratri and Vijaya Dashami, and ends in victory on the tenth day.",
    "Vijaya Dashami": "“Victory tenth.” The tenth day of the festival, when Durga's victory is celebrated.",
    "Devi Mahatmya": "An old Sanskrit poem in praise of the Goddess, still recited during Dashain.",
    "Devi Kavacham": "“Armor of the Goddess.” A short protective prayer that names the nine forms.",
    "Brahma": "The creator god, one of the three great gods of the Hindu tradition.",
    "Vishnu": "The god who keeps the world going, one of the three great gods.",
    "Shiva": "The god of endings that make way for new beginnings, and Parvati's husband.",
    "Parvati": "“She of the mountain.” Daughter of the Himalaya and wife of Shiva, and the Goddess in a human story.",
    "Sati": "Shiva's first wife, who gave up her life. She is later born again as Parvati.",
    "Indra": "King of the gods, ruler of heaven.",
    "Skanda": "A young warrior god, son of Shiva and Parvati. Also called Kartikeya or Murugan.",
    "Kartikeya": "Another name for Skanda, the young warrior god.",
    "Murugan": "Another name for Skanda, loved especially in South India.",
    "Krishna": "A beloved god, shown as a cowherd boy who plays the flute.",
    "Mahishasura": "The shape-shifting buffalo demon who took over heaven.",
    "Himavat": "The king of the mountains, father of Parvati. The Himalaya itself.",
    "Ganga": "The Ganges, India's most sacred river, itself honoured as a goddess.",
    "Yamuna": "A sacred river in northern India, beside the village where Krishna grew up.",
    "Ardhanarishvara": "“The lord who is half woman.” Shiva shown half man, half woman, joined down the middle.",
    "Shakti": "Divine power. Also a name for the Goddess herself.",
    "Raktabija": "A demon whose every drop of blood became another demon.",
    "Taraka": "A demon who could be defeated only by a son of Shiva.",
    "Saraswati": "Goddess of music, learning and wisdom.",
    "Hanuman": "The monkey god of strength and devotion, a loyal friend to Rama.",
    "Siddhi": "A perfection or mastery, earned after long practice.",
}
_SKIP = ("h1", "h2", "h3", "button", "a", "script", "style", "title", "dialog", "noscript")
_RESET = re.compile(r'<(?:section|article|aside)\b|class="detail"')

def add_tooltips(doc):
    """Wrap glossary words in text (never in headings, links, buttons or attributes)."""
    names = sorted(GLOSSARY, key=len, reverse=True)
    word = re.compile(r'(?<![\w-])(' + "|".join(re.escape(n) for n in names) + r')(?![\w-])')
    out, seen, skip, i = [], set(), 0, 0
    for part in re.split(r'(<[^>]+>)', doc):
        if part.startswith("<"):
            m = re.match(r'<(/?)([a-zA-Z0-9]+)', part)
            if m and m.group(2).lower() in _SKIP and not part.endswith("/>"):
                skip += -1 if m.group(1) else 1
                skip = max(skip, 0)
            if _RESET.search(part):
                seen = set()
            out.append(part)
        elif skip or not part.strip():
            out.append(part)
        else:
            def wrap(mo):
                n = mo.group(1)
                if n in seen:
                    return n
                seen.add(n)
                tip = e(GLOSSARY[n])
                return (f'<span class="term" tabindex="0">{n}'
                        f'<span class="tip" role="tooltip">{tip}</span></span>')
            out.append(word.sub(wrap, part))
    return "".join(out)

index = add_tooltips(index)
open(os.path.join(ROOT, "index.html"), "w").write(index)
open(os.path.join(ROOT, "kindle.html"), "w").write(kindle)
open(os.path.join(ROOT, "download.html"), "w").write(download)
print("ok", len(index), len(download))
