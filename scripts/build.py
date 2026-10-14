#!/usr/bin/env python3
"""Regenerates index.html and download.html from the content below.
Run from anywhere: python3 scripts/build.py"""
import html, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_URL = "https://prakritirupa.vercel.app"
BMC = "https://buymeacoffee.com/bipashant"

FORMS = [
    dict(slug="shailaputri", night="१", day="Night 1", name="Shailaputri", deva="शैलपुत्री",
         essence="Daughter of the mountain, steady as stone.",
         attrs="Rides a white bull · holds a trident and a lotus",
         story=["In an earlier life she was Sati, who gave up her body in the fire of her father's sacrifice. She was born again as the daughter of Himavan, king of the Himalaya, and so she is called Shailaputri, the mountain's daughter.",
                "The nine nights begin with her, because every journey needs firm ground under it."],
         mantra="ॐ देवी शैलपुत्र्यै नमः", translit="Om Devi Shailaputryai Namah",
         meaning="Om, I bow to the Goddess Shailaputri."),
    dict(slug="brahmacharini", night="२", day="Night 2", name="Brahmacharini", deva="ब्रह्मचारिणी",
         essence="She who walks the long path with patience.",
         attrs="Walks barefoot · holds prayer beads and a water pot",
         story=["To win Shiva as her husband, the young Parvati gave up every comfort and lived in the forest for years, first on fruit, then on leaves, and at last on nothing at all.",
                "Brahmacharini is that steady, quiet devotion. She carries no weapon, only her prayer beads and a little water."],
         mantra="ॐ देवी ब्रह्मचारिण्यै नमः", translit="Om Devi Brahmacharinyai Namah",
         meaning="Om, I bow to the Goddess Brahmacharini."),
    dict(slug="chandraghanta", night="३", day="Night 3", name="Chandraghanta", deva="चन्द्रघण्टा",
         essence="Grace that is ready for battle.",
         attrs="Rides a lion · ten arms · a bell-shaped half-moon on her brow",
         story=["After she married Shiva, she wore a crescent moon on her forehead shaped like a temple bell, and that is where her name comes from.",
                "She is calm and lovely to look at, yet every one of her ten hands is ready. The sound of her bell is said to drive fear away."],
         mantra="ॐ देवी चन्द्रघण्टायै नमः", translit="Om Devi Chandraghantayai Namah",
         meaning="Om, I bow to the Goddess Chandraghanta."),
    dict(slug="kushmanda", night="४", day="Night 4", name="Kushmanda", deva="कूष्माण्डा",
         essence="Her smile lit the first light of the universe.",
         attrs="Rides a tiger · eight arms · lives at the heart of the sun",
         story=["Before anything existed there was only darkness. Then she smiled, and the whole universe came out of that smile like light out of a seed.",
                "She is said to live inside the sun itself. The warmth we feel each morning is hers."],
         mantra="ॐ देवी कूष्माण्डायै नमः", translit="Om Devi Kushmandayai Namah",
         meaning="Om, I bow to the Goddess Kushmanda."),
    dict(slug="skandamata", night="५", day="Night 5", name="Skandamata", deva="स्कन्दमाता",
         essence="A mother holding the young warrior in her lap.",
         attrs="Sits on a lotus · holds baby Skanda and two lotus flowers",
         story=["Her son Skanda, also called Kartikeya, grew up to lead the army of the gods. Here he is still a child with six small faces, sitting safely in his mother's lap.",
                "She reminds us that great strength often begins with a mother's care."],
         mantra="ॐ देवी स्कन्दमातायै नमः", translit="Om Devi Skandamatayai Namah",
         meaning="Om, I bow to the Goddess Skandamata."),
    dict(slug="katyayani", night="६", day="Night 6", name="Katyayani", deva="कात्यायनी",
         essence="Courage that answers in a single leap.",
         attrs="Rides a lion · holds a sword and a lotus",
         story=["She was born in the hermitage of the sage Katyayana, who had prayed for years that the Goddess would come to him as his daughter.",
                "Old stories tell of the young women of Vrindavan bathing in the Yamuna at dawn and praying to her. She is quick, fearless, and close to anyone who calls on her."],
         mantra="ॐ देवी कात्यायन्यै नमः", translit="Om Devi Katyayanyai Namah",
         meaning="Om, I bow to the Goddess Katyayani."),
    dict(slug="kalaratri", night="७", day="Night 7", name="Kalaratri", deva="कालरात्रि",
         essence="The darkest night, which swallows fear.",
         attrs="Rides a donkey · dark skin, wild hair, fire in her breath",
         story=["Kalaratri means the dark night of time. She is the fiercest of the nine, with flames for breath and nothing soft about her.",
                "Yet she is also called Shubhankari, the one who brings good, because all of her darkness is turned against what frightens us."],
         mantra="ॐ देवी कालरात्र्यै नमः", translit="Om Devi Kalaratryai Namah",
         meaning="Om, I bow to the Goddess Kalaratri."),
    dict(slug="mahagauri", night="८", day="Night 8", name="Mahagauri", deva="महागौरी",
         essence="Pure white light after the long penance.",
         attrs="Rides a white bull · holds a trident and a small drum",
         story=["After her years of penance, Parvati's skin was dark with dust and sun. Shiva washed her in the waters of the Ganga, and she shone as white as the moon and jasmine.",
                "Mahagauri is the calm after the storm, gentle and quick to forgive."],
         mantra="ॐ देवी महागौर्यै नमः", translit="Om Devi Mahagauryai Namah",
         meaning="Om, I bow to the Goddess Mahagauri."),
    dict(slug="siddhidatri", night="९", day="Night 9", name="Siddhidatri", deva="सिद्धिदात्री",
         essence="She who gives everything that is complete.",
         attrs="Sits on a lotus · holds a discus, conch, mace and lotus",
         story=["A siddhi is a perfect power, and she is the one who grants them. Gods, sages and even demons bow before her.",
                "It is said that Shiva himself received his powers from her, and that half of his body became hers. With her, the nine nights are complete."],
         mantra="ॐ देवी सिद्धिदात्र्यै नमः", translit="Om Devi Siddhidatryai Namah",
         meaning="Om, I bow to the Goddess Siddhidatri."),
]
TENTH = dict(slug="mahishasuramardini", night="१०", day="Day 10 · Vijaya Dashami", name="Mahishasuramardini", deva="महिषासुरमर्दिनी",
         essence="The victory of the tenth day.",
         attrs="Rides a lion · ten arms · strikes down the buffalo demon",
         story=["For nine days and nights she fought Mahishasura, a demon who could change from buffalo to man and back again. On the tenth day she struck him down while the gods showered her with flowers.",
                "That day is Vijaya Dashami, the day of victory, and the great day of Dashain."],
         mantra="ॐ महिषासुरमर्दिन्यै नमः", translit="Om Mahishasuramardinyai Namah",
         meaning="Om, I bow to her who defeated Mahishasura.")

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
LOTUS_RULE = '<svg class="lotus-rule" viewBox="0 0 120 18" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M0 9h42M78 9h42"/><path d="M60 2c4 4 5 7 5 9s-2 4-5 5c-3-1-5-3-5-5s1-5 5-9z"/><path d="M52 7c-1 4 1 7 8 9M68 7c1 4-1 7-8 9"/><circle cx="60" cy="10" r="1.4" fill="currentColor"/></svg>'
DIYA = '<svg class="diya" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 6c3 4 4 7 4 9.5a4 4 0 0 1-8 0C20 13 21 10 24 6z" fill="currentColor" fill-opacity=".25"/><path d="M6 26c4 0 7 1 10 2.5 3 1.5 13 1.5 16 0 3-1.5 6-2.5 10-2.5-2 8-9 13-18 13S8 34 6 26z"/><path d="M18 42h12"/></svg>'

VA = '''<script>window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };</script>
  <script defer src="/_vercel/insights/script.js"></script>'''

head_common = f'''<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#130B0C">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="/fonts/rozha-one-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/spectral-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css">
  {VA}'''

DESC = "An illustrated book by Bibek Sharma Chapagain on Durga, the Mother Goddess as nature, and the forms she takes across the nine nights of Navaratri and Dashain. Paintings, stories and Sanskrit mantras with meaning."

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
  <script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"Book","name":"She Who Is Nature","alternateName":"प्रकृतिरूपा","description":DESC,"author":{"@type":"Person","name":"Bibek Sharma Chapagain"},"illustrator":{"@type":"Person","name":"Bibek Sharma Chapagain"},"inLanguage":"en","image":SITE_URL+"/img/og.jpg","url":SITE_URL+"/"}, ensure_ascii=False)}</script>
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
            <a class="btn btn-ghost" href="{BMC}" target="_blank" rel="noopener">{ICON_CUP}Buy me a coffee</a>
          </div>
          <ul class="hero-facts">
            <li>12 illustrated chapters</li>
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

    <section class="feature" id="inside" aria-labelledby="inside-title">
      <div class="wrap">
        <div class="feature-art">
          <img src="/img/prakriti.webp" width="1000" height="1506" loading="lazy" decoding="async" alt="Durga as nature herself: her hair becomes a forested mountain, her sari flows into a river, and terraced mustard fields and a village lie at her feet">
        </div>
        <div class="feature-text">
          <p class="eyebrow">Chapter 1 · The Mother who is nature</p>
          <h2 id="inside-title">The mountain, the river, the field in flower. All of it is her.</h2>
          <p><em>She Who Is Nature</em> tells the story of Durga, the great Mother Goddess, and the forms she takes during the nine nights of Navaratri, celebrated in Nepal as Dashain. In this telling she lives close by, as Prakriti, nature itself: the ground under our feet, the rain and the fire, and the quiet strength inside every living thing.</p>
          <p>Each chapter brings one of her forms to life with a story, a full painting, and her mantra in Sanskrit with simple pronunciation and meaning. You don't need to know anything about Hindu tradition to enjoy it.</p>
          <ul class="inside" aria-label="Inside the book">
            <li><strong>12 illustrated chapters</strong><span>From the birth of the Goddess to her victory on the tenth day.</span></li>
            <li><strong>A painting for every form</strong><span>Rich, oil-style portraits in the spirit of Raja Ravi Varma.</span></li>
            <li><strong>Mantras you can say aloud</strong><span>Each in Sanskrit, with easy pronunciation and a plain English meaning.</span></li>
            <li><strong>Written for everyone</strong><span>Simple words, no background needed, and sources listed at the back.</span></li>
          </ul>
        </div>
      </div>
    </section>

    <section class="feature flip" aria-labelledby="origin-title">
      <div class="wrap">
        <div class="feature-art">
          <img src="/img/origin.webp" width="1000" height="1506" loading="lazy" decoding="async" alt="The gods stand in a circle on a dark mountain as streams of golden light pour from them and join into the ten-armed form of Durga">
        </div>
        <div class="feature-text">
          <p class="eyebrow">Chapter 2 · Born of light</p>
          <h2 id="origin-title">When the gods had nothing left, their light became her.</h2>
          <p>A buffalo demon named Mahishasura had won a promise that no man or god could kill him. He seized heaven and drove the gods out. In their anger, light poured from Brahma, Vishnu, Shiva and all the others, and the streams of light met and became one blaze.</p>
          <p>Out of that blaze stepped a woman with ten arms. Each god placed his own weapon in her hands, and she smiled.</p>
          <p class="note">This story comes from the Devi Mahatmya, an old Sanskrit poem still recited during Dashain.</p>
        </div>
      </div>
    </section>

    <section class="nights" id="nights" aria-labelledby="nights-title">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Navaratri · nine nights</p>
          <h2 id="nights-title">Nine nights, nine forms</h2>
          <p>On each night of Navaratri one form of Durga is honoured, from the daughter of the mountain to the giver of every power. Tap a painting to read her story and her mantra.</p>
        </div>
        <div class="grid">{"".join(cards)}
        </div>
      </div>
    </section>

    <section class="feature tenth" id="{TENTH["slug"]}" data-index="9" aria-labelledby="tenth-title">
      <div class="wrap">
        <div class="feature-art">
          <img src="/img/{TENTH["slug"]}.webp" width="1000" height="1506" loading="lazy" decoding="async" alt="Durga on her lion drives her trident into the buffalo demon as Mahishasura emerges from its mouth, while the gods shower flowers from the clouds">
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
          <div class="offer-main">
            <p class="eyebrow">Read it free</p>
            <h2 id="dl-title">Take her home with you.</h2>
            <p>Download the full book as a PDF and keep it on your phone, tablet or computer. Read it during Dashain, share it with family, send it to a friend who has always wondered who Durga is.</p>
            <div class="actions">
              <a class="btn btn-primary" href="/download">{ICON_DL}Download the PDF</a>
              <span class="small">12 chapters · paintings · mantras</span>
            </div>
          </div>
          <aside class="support" aria-labelledby="support-title">
            {DIYA}
            <h3 id="support-title">Keep the lamp lit</h3>
            <p>Every painting in this book took many hours. If it brought you a little closer to her, you can buy me a coffee. It helps me make the next one.</p>
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
        <p>If the book brings you something, a coffee helps me paint the next one. Thank you for reading.</p>
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

open(os.path.join(ROOT, "index.html"), "w").write(index)
open(os.path.join(ROOT, "download.html"), "w").write(download)
print("ok", len(index), len(download))
