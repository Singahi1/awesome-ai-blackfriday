#!/usr/bin/env python3
"""Curated dataset for awesome-ai-blackfriday.

Single source of truth is data/deals.json, generated from this file by
`python3 scripts/build.py`. Every row carries the URL where the offer was read
and the date it was checked, because a deal without a source is a rumour.
"""
import json
import os
from datetime import date, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date(2026, 11, 23)

# category order used by the site
CATEGORIES = [
    "AI Chat & Assistants",
    "Coding & Agents",
    "Image & Design",
    "Video",
    "Voice & Audio",
    "Writing & Docs",
    "Research & PDF",
    "SEO & Marketing",
    "Hosting & Infra",
]

D = []


def add(**kw):
    kw.setdefault("code", None)
    kw.setdefault("tags", [])
    kw.setdefault("renewal", None)
    kw.setdefault("status", "live")
    kw.setdefault("audience", None)
    kw.setdefault("ends_note", None)
    kw.setdefault("discount", None)
    kw["id"] = kw["name"].lower().replace(" ", "-").replace(".", "").replace("/", "-")
    D.append(kw)


# ---------------------------------------------------------------- AI chat
add(name="TypingMind", category="AI Chat & Assistants",
    what="Bring-your-own-key chat client for GPT, Claude, Gemini + 20 more",
    deal="60% off Lifetime Premium — about $79 once, no subscription",
    discount=60, price_before="$199 one-time", price_after="~$79 one-time",
    code="BLACKFRIDAY2026", ends="2026-12-15", status="live",
    audience="New customers", tags=["lifetime"],
    url="https://www.typingmind.com/buy",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals",
    verified="2026-11-20")

add(name="Google AI Pro", category="AI Chat & Assistants",
    what="Gemini 4, 5 TB storage, higher Antigravity limits",
    deal="Up to 50% off select Google AI annual plans (member early access; some accounts see AI Pro at $4.99/mo for 3 months)",
    discount=50, price_before="$19.99/mo", price_after="from $4.99/mo",
    ends="2026-11-26", ends_note="Subscriber early access; public offers from Nov 27",
    audience="Existing Google AI / storage subscribers first",
    tags=["targeted", "annual"], renewal="Renews at $19.99/mo unless cancelled",
    url="https://one.google.com/about/plans",
    source="https://whichaicoder.com/ai-coding-black-friday-deals/",
    verified="2026-11-20")

add(name="Microsoft 365 Premium", category="AI Chat & Assistants",
    what="Office apps plus Copilot in Word, Excel and Outlook",
    deal="30% off the first month or first year",
    discount=30, price_before="$19.99/mo", price_after="$13.99 first month",
    ends=None, ends_note="No end date printed", status="live",
    renewal="Full price after the intro period",
    url="https://www.microsoft.com/en-us/microsoft-365/buy/compare-all-microsoft-365-products",
    source="https://geotoolbox.ai/blog/black-friday-ai-deals", verified="2026-11-16")

add(name="Perplexity Pro", category="AI Chat & Assistants",
    what="Answer engine with research modes",
    deal="No price cut — adds $40 of Computer credits (Max adds $450)",
    discount=None, price_before="$17/mo billed yearly", price_after="$17/mo + credits",
    ends=None, ends_note="'Limited time', undated", status="perk",
    tags=["perk"], url="https://www.perplexity.ai/pro",
    source="https://www.zemith.com/en/contents/ai-black-friday-deals", verified="2026-11-18")

add(name="Grok / X Premium", category="AI Chat & Assistants",
    what="X subscription tiers that share the Cursor plan family",
    deal="50% off the first month on monthly plans — Premium $30 → $15",
    discount=50, price_before="$30/mo", price_after="$15 first month",
    ends=None, ends_note="Standing promo, no end date", status="standing",
    url="https://grok.com/plans",
    source="https://geotoolbox.ai/blog/black-friday-ai-deals", verified="2026-11-16")

add(name="Canva Pro", category="Image & Design",
    what="Design suite with Magic Studio AI tools",
    deal="50% off the first 3 months — $9/mo instead of $18",
    discount=50, price_before="$18/mo", price_after="$9/mo for 3 months",
    ends=None, ends_note="No end date printed",
    audience="New monthly subscriptions", renewal="Renews at $18/mo",
    url="https://www.canva.com/pricing/",
    source="https://howtoai.com/ai-black-friday-deals/", verified="2026-11-21")

# ---------------------------------------------------------------- coding / agents
add(name="GitHub Copilot", category="Coding & Agents",
    what="AI pair programmer in VS Code, JetBrains, CLI",
    deal="30% off Copilot Fusion model usage on paid plans (plan price unchanged: Pro $10, Pro+ $39, Max $100)",
    discount=30, price_before="Fusion usage at list price", price_after="30% off usage",
    ends="2026-11-30", status="live", tags=["usage-only"],
    renewal="Discount ends; usage returns to list price",
    url="https://github.com/features/copilot/plans",
    source="https://whichaicoder.com/ai-coding-black-friday-deals/", verified="2026-11-20")

add(name="BoltAI", category="Coding & Agents",
    what="Native Mac AI client for coding and writing with your own keys",
    deal="Up to $160 off — Pro $59 (was $99), Pro+ $119 (was $199), Lifetime $239 (was $399)",
    discount=40, price_before="$99 / $199 / $399", price_after="$59 / $119 / $239",
    code="BFCM2026", ends=None, ends_note="No end date printed", tags=["lifetime"],
    url="https://boltai.com/pricing",
    source="https://thoughtcook.github.io/verified-black-friday/", verified="2026-11-23")

add(name="Coderick AI (SiteGround)", category="Coding & Agents",
    what="AI site builder bundled with SiteGround hosting",
    deal="50% off all annual plans — Essential $50 first year (was $100)",
    discount=50, price_before="$100/yr", price_after="$50/yr",
    ends="2026-11-28", ends_note="Countdown to 06:00 UTC",
    renewal="Renews at $100/yr", audience="New customers",
    url="https://www.siteground.com/coderick-ai",
    source="https://thoughtcook.github.io/verified-black-friday/", verified="2026-11-23")

add(name="Wasmer Pro", category="Coding & Agents",
    what="Serverless WebAssembly runtime",
    deal="50% off Wasmer Pro for 12 months — $5/mo, then $10/mo",
    discount=50, price_before="$10/mo", price_after="$5/mo for 12 months",
    code="BLACKFRIDAY26", ends=None, ends_note="No end date printed",
    audience="First-time customers", renewal="Then $10/mo",
    url="https://wasmer.io/black-friday-2026",
    source="https://thoughtcook.github.io/verified-black-friday/", verified="2026-11-20")

add(name="Meku", category="Coding & Agents",
    what="Prompt-to-web-app builder that outputs code you own",
    deal="30% off all yearly plans",
    discount=30, code="BLFCM2026", ends="2026-12-01",
    price_before="Yearly list price", price_after="30% off year one",
    url="https://meku.dev/pricing",
    source="https://blackfridaydeals.dev/blog/black-friday-ai-tools-deals", verified="2026-11-17")

add(name="PageAI", category="Coding & Agents",
    what="Generates a production-ready marketing site in one shot",
    deal="37% off",
    discount=37, code="BF26", ends=None, ends_note="No end date printed",
    url="https://pageai.pro/pricing",
    source="https://blackfridaydeals.dev/blog/black-friday-ai-tools-deals", verified="2026-11-17")

add(name="DocuWriter.ai", category="Coding & Agents",
    what="Generates code docs, tests and refactors from source files",
    deal="50% off Pro and Enterprise (monthly)",
    discount=50, code="BLACKFRIDAY26", ends="2026-12-02",
    url="https://www.docuwriter.ai/pricing",
    source="https://blackfridaydeals.dev/blog/black-friday-ai-tools-deals", verified="2026-11-17")

add(name="Thunkable", category="Coding & Agents",
    what="No-code mobile app builder with AI blocks",
    deal="50% off Builder, Advanced and Monthly Accelerator plans",
    discount=50, ends=None, ends_note="No end date printed",
    audience="New plans only",
    url="https://thunkable.com/pricing",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-20")

add(name="TeleportHQ", category="Coding & Agents",
    what="Visual builder that exports React/Next.js code",
    deal="25% off Premium — $20.99/mo against $28",
    discount=25, price_before="$28/mo", price_after="$20.99/mo",
    ends=None, ends_note="No end date printed",
    url="https://teleporthq.io/pricing",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-20")

add(name="MindPal", category="Coding & Agents",
    what="Build multi-agent workflows for teams and clients",
    deal="60% off the first year of any annual plan — Pro $16/mo (was $39), Advanced $60/mo (was $149)",
    discount=60, price_before="$39/mo", price_after="$16/mo",
    code="BLACKFRIDAY2026", ends="2026-12-11", status="live",
    renewal="Renews at full annual price from year two",
    url="https://mindpal.space/pricing",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

add(name="Pabbly Plus", category="Coding & Agents",
    what="Automation bundle: Connect, Subscriptions, Email, Forms",
    deal="All-app bundle at $828/yr against $1,428/yr",
    discount=42, price_before="$1,428/yr", price_after="$828/yr",
    ends=None, ends_note="No end date printed",
    url="https://www.pabbly.com/pricing/",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-20")

# ---------------------------------------------------------------- image / design
add(name="Adobe Creative Cloud Pro", category="Image & Design",
    what="Photoshop, Illustrator, Premiere and Firefly in one plan",
    deal="57% off the first year — $29.99/mo instead of $69.99 (students $15.99, teams $44.99/licence)",
    discount=57, price_before="$69.99/mo", price_after="$29.99/mo",
    ends="2026-11-27", ends_note="Official terms: Nov 13–27, 2026",
    audience="First-time subscribers, 12-month commitment",
    renewal="Year two returns to $69.99/mo — set a reminder",
    url="https://www.adobe.com/creativecloud/plans.html",
    source="https://www.prompthackers.co/ai-tools/black-friday-deals", verified="2026-11-18")

add(name="Adobe Firefly", category="Image & Design",
    what="Generative image, video and vector models from Adobe",
    deal="Pro $9.99/mo (50% off) and Pro Plus $19.99/mo (60% off) for 6 months, 4,000 credits/mo",
    discount=60, price_before="$19.99 / $49.99/mo", price_after="$9.99 / $19.99/mo",
    ends="2026-12-06", audience="First-time subscribers, one per customer",
    renewal="Then $19.99 / $49.99 per month",
    url="https://www.adobe.com/products/firefly/plans.html",
    source="https://howtoai.com/ai-black-friday-deals/", verified="2026-11-21")

add(name="Higgsfield", category="Image & Design",
    what="AI video and image studio (cinematic camera controls)",
    deal="Up to 70% off premium plans — earlier 63% window closed, new flash window opened Nov 23",
    discount=70, ends="2026-11-24", ends_note="00:00 UTC — a 24-hour window",
    tags=["flash"], renewal="Renews at plan list price",
    url="https://higgsfield.ai/pricing",
    source="https://thoughtcook.github.io/verified-black-friday/", verified="2026-11-23")

add(name="Krea", category="Image & Design",
    what="Real-time image generation and upscaling",
    deal="Up to 70% off yearly plans",
    discount=70, ends=None, ends_note="No end date printed", tags=["annual"],
    url="https://www.krea.ai/pricing",
    source="https://www.prompthackers.co/ai-tools/black-friday-deals", verified="2026-11-18")

add(name="Recraft", category="Image & Design",
    what="Vector and brand-consistent image generation",
    deal="40% off any yearly plan, from $6/mo billed annually",
    discount=40, price_before="Yearly list", price_after="from $6/mo",
    ends="2026-12-01", audience="New plans only",
    url="https://www.recraft.ai/pricing",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-20")

add(name="Kavel", category="Image & Design",
    what="Image and video generation credits",
    deal="2× credits on every new plan — a full extra year of credits on yearly plans",
    discount=None, price_before="Standard credits", price_after="2× credits",
    ends="2026-12-01", ends_note="Starter $100/yr ($8.33/mo)",
    url="https://kavel.ai/pricing",
    source="https://thoughtcook.github.io/verified-black-friday/", verified="2026-11-23")

add(name="OpenArt", category="Image & Design",
    what="Stable Diffusion workflows, training and upscaling",
    deal="Up to 40% off annual plans — Starter $11/mo (was $14), Pro $36/mo (was $56); up to 50% off select models",
    discount=40, price_before="$14 / $56/mo", price_after="$11 / $36/mo",
    ends="2026-11-30", ends_note="Model discount ends Nov 30; plans undated",
    audience="New annual subscribers, first billing period",
    url="https://openart.ai/pricing",
    source="https://www.prompthackers.co/ai-tools/black-friday-deals", verified="2026-11-18")

add(name="Topaz Labs", category="Image & Design",
    what="Photo and video upscaling, denoise, sharpening",
    deal="Up to 67% off — Studio Collection $299/yr (was $499), Topaz Photo $169 (was $199)",
    discount=67, price_before="$499/yr", price_after="$299/yr",
    ends=None, ends_note="No end date printed", tags=["bundle"],
    url="https://topazlabs.com/pricing/",
    source="https://www.prompthackers.co/ai-tools/black-friday-deals", verified="2026-11-18")

add(name="Luminar (Skylum)", category="Image & Design",
    what="One-time-purchase AI photo editor",
    deal="Up to 77% off Desktop, All Platforms and Max licences",
    discount=77, price_before="List price", price_after="up to 77% off",
    ends=None, ends_note="No end date printed", audience="New buyers",
    tags=["lifetime"], url="https://skylum.com/luminar",
    source="https://www.prompthackers.co/ai-tools/black-friday-deals", verified="2026-11-18")

add(name="ON1 Photo RAW 2027", category="Image & Design",
    what="RAW editor with AI masking and upscaling",
    deal="One-time $59.99 (was $99.99); MAX $129.99 (was $169.99); subscriptions up to 22% off",
    discount=40, price_before="$99.99", price_after="$59.99",
    ends="2026-11-27", ends_note="11:59 PM PT", tags=["lifetime"],
    url="https://www.on1.com/landing/black-friday/",
    source="https://thoughtcook.github.io/verified-black-friday/", verified="2026-11-13")

add(name="Dreamina", category="Image & Design",
    what="ByteDance image and video generator",
    deal="Basic $0.29 for the first month (renews $15/mo); Standard $21.60 first month",
    discount=98, price_before="$15/mo", price_after="$0.29 first month",
    ends=None, ends_note="No end date printed", tags=["first-month"],
    renewal="Renews at $15/mo — the steepest cliff on this list",
    url="https://dreamina.capcut.com/pricing",
    source="https://www.zemith.com/en/contents/ai-black-friday-deals", verified="2026-11-18")

# ---------------------------------------------------------------- video
add(name="invideo", category="Video",
    what="Script-to-video with AI voiceover and stock footage",
    deal="Up to 75% off — pay for 12 months, get 24; Ultra $40/seat/mo for 2 years",
    discount=75, price_before="$160/seat/mo", price_after="$40/seat/mo (24 mo)",
    ends=None, ends_note="Countdown only, no printed date",
    renewal="Renews at list from year three",
    url="https://invideo.io/pricing/",
    source="https://blackfridaydeals.dev/blog/black-friday-ai-tools-deals", verified="2026-11-17")

add(name="Synthesia", category="Video",
    what="AI avatar videos from text or slides",
    deal="Up to 50% off yearly plans (Black Friday / Cyber Week)",
    discount=50, ends="2026-12-07",
    ends_note="Runs Nov 23 10:00 GMT – Dec 7", audience="New customers and free-plan upgrades",
    url="https://www.synthesia.io/pricing",
    source="https://howtoai.com/ai-black-friday-deals/", verified="2026-11-21")

add(name="Colossyan", category="Video",
    what="Training videos from documents and slides",
    deal="40% off the first year of Professional — $35.40/mo (was $59)",
    discount=40, price_before="$59/mo", price_after="$35.40/mo",
    code="BLACKFRIDAY40", ends="2026-11-30", ends_note="Runs Nov 23–30",
    url="https://www.colossyan.com/pricing",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

add(name="Framov", category="Video",
    what="AI video editing and repurposing",
    deal="50% off annual plans — Basic $179.40/yr (was $358.80)",
    discount=50, price_before="$358.80/yr", price_after="$179.40/yr",
    ends=None, ends_note="Countdown only, no printed date",
    url="https://framov.com/pricing",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-20")

add(name="Filmora", category="Video",
    what="Desktop video editor with AI captions and cutouts",
    deal="Up to 30% off — Premium Yearly $79.99 (was $99.99), Advanced 10% off",
    discount=20, price_before="$99.99/yr", price_after="$79.99/yr",
    ends="2026-12-08", url="https://filmora.wondershare.com/shop/buy/buy-video-editor.html",
    source="https://blackfridaydeals.dev/blog/black-friday-ai-tools-deals", verified="2026-11-17")

add(name="Kling", category="Video",
    what="AI video generation (Kling 4.0)",
    deal="35% off for 3 months, or 50% off the first year — Standard $60 first year (then $79.20)",
    discount=50, price_before="$79.20/yr", price_after="$60/yr",
    ends="2026-11-30", ends_note="Model promo runs to Nov 30",
    renewal="Year two at $79.20",
    url="https://kling.ai/pricing",
    source="https://www.zemith.com/en/contents/ai-black-friday-deals", verified="2026-11-18")

add(name="Fliki", category="Video",
    what="Turns scripts and blog posts into narrated videos",
    deal="50% off annual Standard and Premium (price shows at checkout)",
    discount=50, code="FLIKIBFCM50", ends=None, ends_note="No end date printed",
    url="https://fliki.ai/pricing",
    source="https://www.prompthackers.co/ai-tools/black-friday-deals", verified="2026-11-18")

add(name="Mubert", category="Voice & Audio",
    what="Royalty-free AI music generation",
    deal="Up to 50% off annual plans for the first year",
    discount=50, ends=None, ends_note="Countdown only, no printed date",
    url="https://mubert.com/render/pricing",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-20")

# ---------------------------------------------------------------- voice
add(name="ElevenLabs", category="Voice & Audio",
    what="Text-to-speech, voice cloning, dubbing, music and agents",
    deal="Up to 55% off the first year — Creator $99 (was $220), Pro $445.50 (was $990)",
    discount=55, price_before="$220/yr", price_after="$99/yr",
    ends="2026-12-01", ends_note="11:59 PM ET; offer ran Nov 16 – Dec 1",
    audience="New and upgrading subscribers, direct web only",
    renewal="Renews at the regular annual price from year two",
    tags=["editor-pick"],
    url="https://elevenlabs.io/pricing",
    source="https://elevenlabs.io/black-friday-promo", verified="2026-11-21")

add(name="Krisp", category="Voice & Audio",
    what="AI noise cancellation and meeting notes",
    deal="55% off annual plans",
    discount=55, code="KRISPBF2026", ends=None, ends_note="No end date printed",
    url="https://krisp.ai/pricing/",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-20")

add(name="Leelo", category="Voice & Audio",
    what="AI voice studio for narration, videos and podcasts",
    deal="Lifetime Pro $149 (was $199) with 80,000 credits/mo; 50% more credits on every pack",
    discount=25, price_before="$199 one-time", price_after="$149 one-time",
    ends="2026-12-01", ends_note="Runs Nov 24 – Dec 1", tags=["lifetime"],
    url="https://leelo.ai/pricing",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

add(name="Podwise", category="Voice & Audio",
    what="Podcast transcripts, summaries and mind maps",
    deal="40% off Standard ($42.48/yr) and Pro ($85.68/yr) — renewals stay discounted",
    discount=40, code="BF2026", ends=None, ends_note="No end date printed",
    url="https://podwise.ai/pricing",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

# ---------------------------------------------------------------- writing
add(name="ProWritingAid", category="Writing & Docs",
    what="Grammar, style and readability editor",
    deal="50% off yearly ($60 vs $120) and lifetime ($199.50 vs $399); 25% off Story Credits",
    discount=50, price_before="$120/yr", price_after="$60/yr",
    ends="2026-11-29", ends_note="11:59 PM PT — the vendor blog says Dec 4, go by the pricing page",
    tags=["lifetime"], url="https://prowritingaid.com/pricing",
    source="https://www.prompthackers.co/ai-tools/black-friday-deals", verified="2026-11-18")

add(name="Craft", category="Writing & Docs",
    what="Docs and notes with built-in AI",
    deal="Up to 40% off Plus and Family — 40% off yearly, 20% off monthly",
    discount=40, code="BLACKFRIDAY26-A (yearly), BLACKFRIDAY26-M (monthly)",
    ends=None, ends_note="No end date printed",
    url="https://www.craft.do/pricing",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-20")

add(name="dochost", category="Writing & Docs",
    what="Publish docs sites with AI drafting",
    deal="30% off the first year of Pro or Max (yearly only)",
    discount=30, code="BLACKFRIDAY30", ends="2026-12-06", ends_note="Los Angeles time",
    url="https://dochost.io/pricing",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-20")

add(name="RewriteBar", category="Writing & Docs",
    what="Grammar, rewrite and translate inside any Mac app",
    deal="50% off — Standard lifetime $14.50 instead of $29",
    discount=50, price_before="$29 one-time", price_after="$14.50 one-time",
    code="BF2026", ends="2026-12-03", tags=["lifetime"],
    url="https://rewritebar.com/",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

add(name="Refine", category="Writing & Docs",
    what="Offline AI grammar checker for Mac",
    deal="35% off — $24.70 instead of $38 for one Mac",
    discount=35, price_before="$38 one-time", price_after="$24.70 one-time",
    ends="2026-11-30", tags=["lifetime", "offline"],
    url="https://refine.app/",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

add(name="DuoTyping", category="Writing & Docs",
    what="Inline AI typing assistant",
    deal="50% off the first payment of Pro — $4.95 instead of $9.90",
    discount=50, price_before="$9.90/mo", price_after="$4.95 first month",
    code="BFCM2026", ends=None, ends_note="No end date printed",
    url="https://duotyping.com/pricing",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

add(name="SeoWriting.AI", category="SEO & Marketing",
    what="SEO article generation with WordPress auto-publish",
    deal="40% off yearly plans, stacked on the usual 25% annual discount — Starter $8.40/mo (was $19)",
    discount=40, price_before="$19/mo", price_after="$8.40/mo",
    code="BLACKFRIDAY40", ends="2026-12-07", audience="Yearly plans only",
    url="https://seowriting.ai/pricing",
    source="https://blackfridaydeals.dev/blog/black-friday-ai-tools-deals", verified="2026-11-17")

add(name="Scalenut", category="SEO & Marketing",
    what="AI writer plus keyword research",
    deal="60% off annual plans — Starter $24/mo (was $59)",
    discount=60, price_before="$59/mo", price_after="$24/mo",
    ends=None, ends_note="Labelled 'limited offer' with no deadline — check checkout",
    url="https://www.scalenut.com/pricing",
    source="https://geotoolbox.ai/blog/black-friday-ai-deals", verified="2026-11-16")

add(name="SE Ranking", category="SEO & Marketing",
    what="Rank tracking, audits and competitor research",
    deal="20% off annual plans, on top of the usual annual discount",
    discount=20, ends="2026-12-04", audience="New customers",
    url="https://seranking.com/pricing.html",
    source="https://www.prompthackers.co/ai-tools/black-friday-deals", verified="2026-11-18")

# ---------------------------------------------------------------- research
add(name="PDF Pals", category="Research & PDF",
    what="Chat with PDFs on Mac using local models",
    deal="Lifetime $149 (was $249) for 4 Macs; or 20% off Basic and Plus",
    discount=40, price_before="$249 one-time", price_after="$149 one-time",
    ends="2026-12-01", tags=["lifetime", "offline"],
    url="https://pdfpals.com/buy",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

add(name="NotebookLM Tools", category="Research & PDF",
    what="Add-on features for Google NotebookLM",
    deal="30% off one-month ($4.90) and one-year ($20.30) passes",
    discount=30, code="BLACKFRIDAY2026", ends="2026-12-02",
    url="https://notebooklmtools.com/pricing",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

add(name="EvidenceLens", category="Research & PDF",
    what="Summarise videos, articles and PDFs, then fact-check claims",
    deal="40% off Plus Lifetime — $29.40",
    discount=40, code="BW2026", ends="2026-12-01", tags=["lifetime"],
    url="https://evidencelens.com/pricing",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

add(name="AI Toolbox", category="Research & PDF",
    what="Folders, full-text search and export for ChatGPT/Claude chats",
    deal="50% off Lifetime ($49.50) and All Access Lifetime ($99.50)",
    discount=50, code="BLACKFRIDAY", ends="2026-11-30", tags=["lifetime"],
    url="https://aitoolbox.app/pricing",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

add(name="Carry", category="Research & PDF",
    what="Saves AI chats as Markdown into Obsidian or a folder",
    deal="Lifetime $59 instead of $79",
    discount=25, price_before="$79 one-time", price_after="$59 one-time",
    code="BLACKFRIDAY20", ends=None, ends_note="No end date printed", tags=["lifetime"],
    url="https://carry.md/",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals", verified="2026-11-20")

# ---------------------------------------------------------------- infra (adjacent)
add(name="Cloudways", category="Hosting & Infra",
    what="Managed cloud hosting for WordPress/Laravel/Node, incl. AI agents",
    deal="80% off the first 2 months of a new account (capped at $200/mo) — AI Website Builder $1.60/mo",
    discount=80, code="BFCM802", ends="2026-12-04", ends_note="11:59 PM ET to sign up",
    audience="New accounts", url="https://www.cloudways.com/en/black-friday-offer.php",
    source="https://geotoolbox.ai/blog/black-friday-ai-deals", verified="2026-11-18")

add(name="Kinsta", category="Hosting & Infra",
    what="Managed WordPress and app hosting",
    deal="50% off monthly plans for 3 months, or 3 months free on annual plans",
    discount=50, ends="2026-12-01", audience="New customers",
    url="https://kinsta.com/pricing/",
    source="https://www.greatfrontend.com/blog/black-friday-deals-for-front-end-developers-2026", verified="2026-11-19")

add(name="Hostinger AI Builder", category="Hosting & Infra",
    what="AI website builder plus hosting",
    deal="Site-wide banner: up to 85% off",
    discount=85, ends=None, ends_note="No end date printed",
    url="https://www.hostinger.com/ai-builder",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-20")

add(name="Static.run", category="Hosting & Infra",
    what="Static site hosting with analytics and one-click deploy",
    deal="30% off all plans, recurring",
    discount=30, code="BLFCM2026", ends="2026-12-01", ends_note="Runs Nov 16 – Dec 1",
    url="https://static.run/pricing",
    source="https://uideck.com/blog/black-friday-deals-for-developer", verified="2026-11-09")

# ---------------------------------------------------------------- no deals (verified)
NO_DEAL = [
    ("ChatGPT Plus", "OpenAI's pricing page lists Go, Plus and Pro with no promotion. Coupon-site '50% off ChatGPT' pages are not OpenAI offers.", "https://openai.com/chatgpt/pricing/", "2026-11-18"),
    ("Claude Pro", "Claude Pro is $20/mo, or $17/mo billed annually ($200 up front). No sale on the pricing page.", "https://www.claude.com/pricing", "2026-11-19"),
    ("Cursor", "Plus $8, Premium $30, Super $100, Ultra $200 — no promo on the pricing page. The 50%-off-first-month Grok offer lives on grok.com, not Cursor.", "https://cursor.com/pricing", "2026-11-20"),
    ("Midjourney", "Basic $10/mo, or $96/yr (the standing 20% annual discount). No seasonal offer.", "https://www.midjourney.com/plans", "2026-11-18"),
    ("Notion AI", "Plus $10 and Business $20 per seat/mo on annual billing. No seasonal offer; AI is metered at $10 per 1,000 credits.", "https://www.notion.com/pricing", "2026-11-14"),
    ("Grammarly", "A 50%-off banner is still up, but its button leads to an expired-offer page. Treat it as last year's sale.", "https://www.grammarly.com/plans", "2026-11-18"),
    ("Jasper", "Pro is $59/seat/mo billed yearly, $69 monthly. No Black Friday wording.", "https://www.jasper.ai/pricing", "2026-11-16"),
    ("Lovable", "No Black Friday offer. Verified students get up to 50% off Pro year-round.", "https://lovable.dev/pricing", "2026-11-20"),
    ("Replit", "Core $20/mo, Pro $100/mo. Annual billing only; no Black Friday offer.", "https://replit.com/pricing", "2026-11-20"),
    ("Devin / Windsurf", "No Black Friday offer on the pricing page.", "https://windsurf.com/pricing", "2026-11-20"),
    ("Runway", "No Black Friday label; standard annual discount only.", "https://runwayml.com/pricing", "2026-11-18"),
    ("HeyGen", "Creator $29/mo ($24 annual). No Black Friday offer.", "https://www.heygen.com/pricing", "2026-11-09"),
    ("Semrush", "No seasonal sale — SEO Toolkit is $117.33/mo billed annually. Ahrefs states it never discounts seasonally either.", "https://www.semrush.com/pricing/", "2026-10-29"),
    ("Obsidian Sync", "No promo; Sync is $4/user/mo billed annually.", "https://obsidian.md/pricing", "2026-11-17"),
    ("Vercel / Supabase / Cloudflare / PostHog", "No Black Friday offers on any of these pricing pages — free tiers only.", "https://vercel.com/pricing", "2026-11-19"),
]

WATCHLIST = [
    ("TradingView", "Black Friday page is live but 'launches in' — countdown points to Nov 23, 08:00 UTC.", "https://www.tradingview.com/black-friday/"),
    ("Surfer SEO", "Deal lands Nov 27; terms not published yet.", "https://surferseo.com/pricing/"),
    ("Emergent / Bolt bundle", "A tracker reports a one-year bundle for $69, but it is not on Bolt's pricing page — unconfirmed.", "https://bolt.new/pricing"),
]

ALWAYS_ON = [
    ("Google AI Pro for students", "Free for 12 months for US college students 18+, verified with SheerID. Worth $239.88 at the monthly price. Redeem by Dec 31; a card is required and it renews at $19.99 unless cancelled.", "https://one.google.com/ai-student", "Student"),
    ("GitHub Copilot Student", "Free Copilot Pro while you remain eligible (verified student status).", "https://education.github.com/pack", "Student"),
    ("JetBrains", "40% off personal subscriptions for former students; 50% off IDEs and JetBrains AI for startups for up to 5 years.", "https://www.jetbrains.com/store/", "Standing"),
    ("DigitalOcean", "$200 in credit for the first 60 days on a new account.", "https://www.digitalocean.com/pricing", "Standing"),
    ("n8n", "Startup plan: 50% off Business for companies under 20 employees.", "https://n8n.io/pricing/", "Standing"),
    ("Midjourney / Suno / Claude / Perplexity", "20% off for paying annually — not a Black Friday deal, but it is the discount that never expires.", "https://www.midjourney.com/plans", "Standing"),
]

payload = {
    "meta": {
        "title": "Awesome AI Black Friday Deals",
        "black_friday": "2026-11-27",
        "cyber_monday": "2026-11-30",
        "generated": TODAY.isoformat(),
        "checked_window": "2026-11-09 to 2026-11-23",
        "count": len(D),
    },
    "categories": CATEGORIES,
    "deals": D,
    "no_deal": [
        {"name": n, "note": note, "url": u, "checked": d} for n, note, u, d in NO_DEAL
    ],
    "watchlist": [{"name": n, "note": note, "url": u} for n, note, u in WATCHLIST],
    "always_on": [{"name": n, "note": note, "url": u, "kind": k} for n, note, u, k in ALWAYS_ON],
}

os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
with open(os.path.join(ROOT, "data", "deals.json"), "w") as f:
    json.dump(payload, f, indent=2)
    f.write("\n")

print(f"wrote {len(D)} deals, {len(NO_DEAL)} no-deal rows")
from collections import Counter
print(Counter(d["category"] for d in D))
missing = [d["name"] for d in D if not d.get("source") or not d.get("verified")]
print("missing source:", missing)

# mirror the dataset as a classic script so the site also works when index.html
# is opened straight from disk (file:// blocks fetch)
with open(os.path.join(ROOT, "data", "deals.js"), "w") as f:
    f.write("/* generated from data/deals.json — do not edit */\nwindow.DEALS = ")
    json.dump(payload, f, indent=2)
    f.write(";\n")
print("wrote data/deals.js fallback")
