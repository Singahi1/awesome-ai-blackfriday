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
TODAY = date(2026, 11, 25)

# category order used by the site
CATEGORIES = [
    "AI Chat & Assistants",
    "Coding & Agents",
    "Meetings & Automation",
    "Image & Design",
    "Video",
    "Voice & Audio",
    "Writing & Docs",
    "Research & PDF",
    "SEO & Marketing",
    "Hosting & Infra",
    "Security & Compliance",
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
    deal="60% off Lifetime Premium — $79.20 once instead of $198, no subscription",
    discount=60, price_before="$198 one-time", price_after="$79.20 one-time",
    code="BLACKFRIDAY2026", ends="2026-12-15",
    ends_note="Vendor docs say Dec 15; some trackers report Nov 30 — confirm at checkout",
    audience="New customers", tags=["lifetime"],
    url="https://www.typingmind.com/buy",
    source="https://docs.typingmind.com/resources/ai-black-friday-deals",
    verified="2026-11-25")

add(name="Google AI Pro", category="AI Chat & Assistants",
    what="Gemini 4, 5 TB storage, higher Antigravity limits",
    deal="Up to 50% off select Google AI annual plans for existing AI / storage subscribers; some see AI Pro at $99.99 for year one. New-subscriber offers start Nov 27.",
    discount=50, price_before="$199.99/yr", price_after="from $99.99/yr (targeted)",
    ends="2026-11-26", ends_note="Member early access through Nov 26; exact offer depends on current plan",
    audience="Existing Google AI / storage subscribers first",
    tags=["targeted", "annual"], renewal="Renews at $199.99/yr unless cancelled",
    url="https://one.google.com/about/plans",
    source="https://whichaicoder.com/ai-coding-black-friday-deals/",
    verified="2026-11-25")

add(name="Microsoft 365 Premium", category="AI Chat & Assistants",
    what="Office apps plus Copilot in Word, Excel and Outlook",
    deal="30% off the first month ($13.99) or first year ($139.99)",
    discount=30, price_before="$19.99/mo or $199.99/yr", price_after="$13.99 first month / $139.99 first year",
    ends="2026-11-28", ends_note="Microsoft Store Black Friday window Nov 19–28; offer while advertised",
    status="live", renewal="Full price after the intro period",
    url="https://www.microsoft.com/en-us/microsoft-365/buy/compare-all-microsoft-365-products",
    source="https://www.microsoft.com/en-us/store/b/black-friday", verified="2026-11-25")

add(name="Perplexity Pro", category="AI Chat & Assistants",
    what="Answer engine with research modes",
    deal="No price cut — adds $40 of Computer credits (Max adds $450)",
    discount=None, price_before="$17/mo billed yearly", price_after="$17/mo + credits",
    ends=None, ends_note="'Limited time', undated", status="perk",
    tags=["perk"], url="https://www.perplexity.ai/pro",
    source="https://www.zemith.com/en/contents/ai-black-friday-deals", verified="2026-11-24")

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
    source="https://whichaicoder.com/ai-coding-black-friday-deals/", verified="2026-11-24")

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
    deal="Up to 69% off premium plans in the Nov 24 wave — Plus $30/mo billed yearly (was $59). Separate Black Friday Market add-ons are up to 75% off through Nov 30.",
    discount=69, ends="2026-11-25", ends_note="Plan wave ends 00:00 UTC Nov 25; add-on Market ends Nov 30",
    tags=["flash"], renewal="Renews at plan list price",
    url="https://higgsfield.ai/pricing",
    source="https://higgsfield.ai/", verified="2026-11-25")

add(name="Krea", category="Image & Design",
    what="Real-time image generation and upscaling",
    deal="Up to 70% off yearly plans",
    discount=70, ends=None, ends_note="No end date printed", tags=["annual"],
    url="https://www.krea.ai/pricing",
    source="https://www.prompthackers.co/ai-tools/black-friday-deals", verified="2026-11-24")

add(name="Recraft", category="Image & Design",
    what="Vector and brand-consistent image generation",
    deal="40% off any yearly plan, from $6/mo billed annually",
    discount=40, price_before="Yearly list", price_after="from $6/mo",
    ends="2026-12-01", audience="New plans only",
    url="https://www.recraft.ai/pricing",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-24")

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
    deal="Up to 67% off — Studio Collection $299/yr (was $499), Topaz Photo $169 (was $199); daily deals rotate",
    discount=67, price_before="$499/yr", price_after="$299/yr",
    ends=None, ends_note="Vendor prints a countdown, not a written end date; daily deal prices rotate",
    tags=["bundle"],
    url="https://topazlabs.com/pricing/",
    source="https://topazlabs.com/pricing/", verified="2026-11-25")

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
    deal="[Expired October campaign] Basic $0.29 for the first month (renews $15/mo); Standard $21.60 first month",
    discount=98, price_before="$15/mo", price_after="$0.29 first month",
    ends="2026-10-30", ends_note="October 21–30 campaign ended; residual sale banners are stale",
    status="expired", tags=["first-month", "expired"],
    renewal="Renews at $15/mo — the steepest cliff on this list",
    url="https://dreamina.capcut.com/ai-video/dreamina-october-offer-faq-2026",
    source="https://dreamina.capcut.com/ai-video/dreamina-october-offer-faq-2026", verified="2026-11-25")

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
    deal="Pro $19 for the first month (then $89/mo), or $44/mo billed yearly ($528/yr, was $59/mo); up to 51% off",
    discount=51, price_before="$89/mo monthly / $59/mo yearly", price_after="$19 first month / $44/mo yearly",
    ends="2026-12-07",
    ends_note="Nov 23 16:00 GMT – Dec 7 07:59 GMT; excludes Japan",
    audience="New customers and free-plan upgrades",
    url="https://www.synthesia.io/pricing",
    source="https://www.synthesia.io/pricing", verified="2026-11-25")

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
    source="https://join.elevenlabs.io/bfcm/terms", verified="2026-11-25")

add(name="Krisp", category="Voice & Audio",
    what="AI noise cancellation and meeting notes",
    deal="55% off annual plans",
    discount=55, code="KRISPBF2026", ends=None, ends_note="No end date printed",
    url="https://krisp.ai/pricing/",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-24")

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
    source="https://www.prompthackers.co/ai-tools/black-friday-deals", verified="2026-11-24")

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
    source="https://www.greatfrontend.com/blog/black-friday-deals-for-front-end-developers-2026", verified="2026-11-24")

add(name="Hostinger AI Builder", category="Hosting & Infra",
    what="AI website builder plus hosting",
    deal="Site-wide banner: up to 85% off",
    discount=85, ends=None, ends_note="No end date printed",
    url="https://www.hostinger.com/ai-builder",
    source="https://buildstacktools.com/guides/black-friday-ai-dev-tool-deals-2026.html", verified="2026-11-24")

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
    ("CapCut", "Pro $19.99/mo or $179.99/yr, Ultra $79/mo. No seasonal offer on the pricing page.", "https://www.capcut.com/pricing", "2026-11-14"),
    ("Leonardo.Ai", "Essential $12, Premium $30, Ultimate $60/mo; yearly is 20% off year-round. No 2026 sale.", "https://leonardo.ai/pricing", "2026-11-22"),
    ("Ideogram", "Plus $20/mo, Pro $60/mo; 'up to 33% off' is the standing annual discount, not an event.", "https://ideogram.ai/pricing", "2026-11-22"),
    ("Playground AI", "20% off annual billing is the standing term; no Black Friday label.", "https://playground.com/pricing", "2026-11-22"),
    ("Speechify", "No 2026 offer on the pricing page, and no verified 2025 offer to fall back on.", "https://speechify.com/pricing/", "2026-11-21"),
    ("Murf AI", "No 2026 offer. 2025 ran 33% off annual — not repeated so far.", "https://murf.ai/pricing", "2026-11-21"),
    ("QuillBot", "No 2026 offer found. 2025 ran 40% off annual with BFCMDEAL.", "https://quillbot.com/premium", "2026-11-21"),
    ("Descript", "Hobbyist $16, Creator $24, Business $50 per person/mo. No 2026 offer.", "https://www.descript.com/pricing", "2026-11-21"),
    ("OpusClip", "No 2026 offer. 2025 ran 65% off annual.", "https://www.opus.pro/pricing", "2026-11-21"),
    ("Figma", "Professional $20/seat/mo monthly, $16 annual. No seasonal sale; education plan is the real saving.", "https://www.figma.com/pricing/", "2026-11-22"),
    ("Zapier", "Professional from $29.99/mo monthly, $19.99 yearly. No Black Friday offer.", "https://zapier.com/pricing", "2026-11-22"),
    ("Loom", "Business $18/user/mo, Business + AI $24. Annual saves 17%; no seasonal offer.", "https://www.loom.com/pricing", "2026-11-22"),
    ("Motion", "Pro AI $49/mo, Business AI $69/mo; $29/$39 on annual. No Black Friday offer.", "https://www.usemotion.com/pricing", "2026-11-22"),
    ("Wix / Webflow", "No sale banner on either pricing page. Webflow nonprofits get 50% off year-round.", "https://webflow.com/pricing", "2026-11-22"),
]

WATCHLIST = [
    ("Framer", "Black Friday page says the sale starts Nov 27 at 9am CET, but no discount or terms were published when checked.", "https://www.framer.com/black-friday/"),
    ("TradingView", "Black Friday page is live but 'launches in' — countdown points to Nov 23, 08:00 UTC.", "https://www.tradingview.com/black-friday/"),
    ("Surfer SEO", "Deal lands Nov 27; terms not published yet.", "https://surferseo.com/pricing/"),
    ("Emergent / Bolt bundle", "A tracker reports a one-year bundle for $69, but it is not on Bolt's pricing page — unconfirmed.", "https://bolt.new/pricing"),
]

ALWAYS_ON = [
    ("Google AI Pro for students", "Free for 12 months for US college students 18+, verified with SheerID. Worth $239.88 at the monthly price. Redeem by Dec 31; a card is required and it renews at $19.99 unless cancelled.", "https://one.google.com/ai-student", "Student"),
    ("GitHub Copilot Student", "Free Copilot Pro while you remain eligible (verified student status). Copilot Free is also free for individuals.", "https://education.github.com/pack", "Student"),
    ("JetBrains", "40% off personal subscriptions for former students; 50% off IDEs and JetBrains AI for startups for up to 5 years.", "https://www.jetbrains.com/store/", "Standing"),
    ("Modal", "$30/month of free compute credits on the Starter plan, plus up to $10k for academics.", "https://modal.com/pricing", "Free tier"),
    ("Lambda", "Up to $5,000 in cloud credits for qualifying researchers, by application.", "https://lambda.ai/pricing", "Research"),
    ("RunPod", "Referral credit of $5–$500 after a first $10 spend, plus $1k–$25k in startup credits by application.", "https://www.runpod.io/pricing", "Referral"),
    ("DigitalOcean", "$200 in credit for the first 60 days on a new account.", "https://www.digitalocean.com/pricing", "Standing"),
    ("n8n", "Startup plan: 50% off Business for companies under 20 employees.", "https://n8n.io/pricing/", "Standing"),
    ("Ideogram / Leonardo / Playground / Midjourney / Suno", "Up to 33%, 20%, 20%, 20% and 20% off respectively for paying annually — not a Black Friday deal, but it never expires.", "https://www.midjourney.com/plans", "Standing"),
    ("Otter.ai / Fireflies / Fathom", "Annual billing is the discount here: 51%, 44% and 25% respectively, charged every day of the year.", "https://otter.ai/pricing", "Standing"),
]

# ================================================================ batch 2
# harvested from tracker tables published 20–23 Nov 2026; every row keeps the
# tracker URL as `source` and the date its vendor page was read
AID = "https://aideals.app/deals/black-friday"
WURD = "https://wurd.ai/blog/ai-black-friday-deals"
MEET = "https://aiincontext.com/articles/bf2026-ai-meeting-notes-tools"
IMG = "https://aiincontext.com/articles/bf2026-ai-image-tools"
TP = "https://taskpanel.io/deals/discounts"

# ---------------------------------------------------------------- meetings
add(name="tl;dv", category="Meetings & Automation",
    what="Records, transcribes and summarises Zoom, Meet and Teams calls",
    deal="45% off the Business annual plan — $29/seat/mo drops to about $15.95 (500 coupons only)",
    discount=45, price_before="$348/yr per seat", price_after="~$191/yr per seat",
    code="BLACKFRIDAY45", ends=None, ends_note="No end date; capped at 500 coupons",
    renewal="Renews at $29/seat/mo", audience="Business annual plan",
    url="https://tldv.io/pricing/", source=MEET, verified="2026-11-21")

add(name="Otter.ai", category="Meetings & Automation",
    what="Live transcription, summaries and action items",
    deal="50% off Pro or Business annual (Black Friday window); a separate Cyber Monday window runs through Dec 6",
    discount=50, price_before="$16.99/mo Pro", price_after="50% off annual",
    ends="2026-11-29", ends_note="Black Friday window ends Nov 29; Cyber Monday window ends Dec 6",
    renewal="Year two at list price",
    url="https://otter.ai/black-friday",
    source="https://otter.ai/black-friday", verified="2026-11-25")

add(name="MeetGeek", category="Meetings & Automation",
    what="Meeting recorder with AI summaries and CRM sync",
    deal="30% off Pro and Business for 12 months, monthly or annual",
    discount=30, code="BLACKFRIDAY2026", ends=None, ends_note="No end date printed",
    audience="New subscriptions",
    url="https://meetgeek.ai/pricing", source=AID, verified="2026-11-21")

add(name="Noota", category="Meetings & Automation",
    what="AI meeting notes and recruiting interviews",
    deal="40% off a new annual Pro or Business plan for the first year",
    discount=40, ends="2026-11-30", audience="New annual plans",
    url="https://noota.io/pricing", source=AID, verified="2026-11-21")

add(name="Sembly AI", category="Meetings & Automation",
    what="Meeting assistant with team-wide searchable notes",
    deal="20% off any plan, any billing period, for 12 months",
    discount=20, code="BF2026", ends=None, ends_note="No end date printed",
    url="https://www.sembly.ai/pricing/", source=AID, verified="2026-11-21")

add(name="Voibe", category="Meetings & Automation",
    what="Local-first voice dictation for Mac",
    deal="25% off every plan — monthly, annual and lifetime",
    discount=25, code="BFCM26", ends=None, ends_note="No end date printed",
    url="https://voibe.app/pricing", source=AID, verified="2026-11-21")

add(name="MeetingDebrief", category="Meetings & Automation",
    what="Turns recordings into structured debriefs",
    deal="35% off the one-time licence, any number of devices",
    discount=35, code="BFCM2026", ends=None, ends_note="No end date printed",
    tags=["lifetime"], url="https://meetingdebrief.com/", source=AID, verified="2026-11-21")

add(name="Landbot", category="Meetings & Automation",
    what="No-code chatbot builder for web and WhatsApp",
    deal="50% off the first year of an annual Starter, Professional or WhatsApp plan",
    discount=50, ends="2026-11-30", ends_note="Runs Nov 10–30",
    audience="Accounts without an active paid subscription",
    url="https://landbot.io/pricing", source=AID, verified="2026-11-21")

add(name="Tidio", category="Meetings & Automation",
    what="AI live chat and support automation",
    deal="20% off the first payment on Starter or Growth, monthly or annual, with code BF2026; add-ons excluded (except Shopify)",
    discount=20, code="BF2026", ends="2026-12-08",
    ends_note="Official window Nov 25 – Dec 8, 2026; vendor timezone",
    renewal="Full price after the first payment",
    url="https://www.tidio.com/black-friday/",
    source="https://www.tidio.com/black-friday/", verified="2026-11-25")

add(name="Botsify", category="Meetings & Automation",
    what="White-label AI agents for agencies",
    deal="Founding Partner lifetime licence at $499 one-time, with white-label access",
    discount=None, price_before="Subscription pricing", price_after="$499 lifetime",
    ends=None, ends_note="No end date printed", tags=["lifetime"],
    url="https://botsify.com/pricing", source=WURD, verified="2026-11-21")

add(name="HelpJet", category="Meetings & Automation",
    what="Support chatbot trained on your docs",
    deal="Double the monthly replies on annual plans (1,000 → 2,000), applied automatically",
    discount=None, price_before="1,000 replies/mo", price_after="2,000 replies/mo",
    ends=None, ends_note="No end date printed", status="perk", tags=["perk"],
    url="https://helpjet.ai/pricing", source=WURD, verified="2026-11-21")

# ---------------------------------------------------------------- coding
add(name="TinyCommand", category="Coding & Agents",
    what="AI ops agent for cloud infrastructure",
    deal="90% off the first year on yearly plans — pay one month, get twelve",
    discount=90, ends="2026-12-07", ends_note="Runs Nov 14 – Dec 7",
    renewal="Full annual price in year two",
    url="https://tinycommand.com/pricing", source=AID, verified="2026-11-21")

add(name="Perch", category="Coding & Agents",
    what="AI coding-agent monitor for Mac",
    deal="40% off a one-time Mac licence, solo or per team seat (first 500 orders)",
    discount=40, code="BLACKFRIDAY2026", ends=None, ends_note="No end date; 500-order cap",
    tags=["lifetime"], url="https://perch.dev/", source=AID, verified="2026-11-21")

add(name="DevIntern", category="Coding & Agents",
    what="AI coding agent that works like a junior developer",
    deal="40% off the first invoice of Team or Business, or the one-time Supporter licence",
    discount=40, code="BLACKFRIDAY26", ends=None, ends_note="No end date printed",
    url="https://devintern.dev/pricing", source=AID, verified="2026-11-21")

add(name="Slashspace", category="Coding & Agents",
    what="Team workspace for AI coding sessions",
    deal="51% off the yearly plan",
    discount=51, code="BF2026", ends=None, ends_note="No end date printed",
    url="https://slashspace.app/pricing", source=AID, verified="2026-11-21")

add(name="Enconvo", category="Coding & Agents",
    what="AI agent launcher for macOS with MCP support",
    deal="30% off lifetime licences, plus the first month or year of Cloud plans",
    discount=30, ends=None, ends_note="No end date printed", tags=["lifetime"],
    url="https://enconvo.com/pricing", source=AID, verified="2026-11-21")

add(name="Layerwise", category="Coding & Agents",
    what="AI review layer for pull requests",
    deal="20% off any plan for 12 months, monthly or annual",
    discount=20, code="BLACKFRIDAY2026", ends=None, ends_note="No end date printed",
    url="https://layerwise.dev/pricing", source=AID, verified="2026-11-21")

add(name="Aikeedo", category="Coding & Agents",
    what="Self-hosted AI SaaS starter kit",
    deal="Up to 50% off the Core plan (first 12 months), the commercial licence and every add-on",
    discount=50, ends="2026-12-01", ends_note="Runs Nov 24 – Dec 1",
    url="https://aikeedo.com/pricing", source=AID, verified="2026-11-21")

add(name="Vinaa", category="Coding & Agents",
    what="AI assistant for Mac with local model support",
    deal="Up to 45% off lifetime licences for 1, 2 or 3 Macs",
    discount=45, ends=None, ends_note="No end date printed", tags=["lifetime"],
    url="https://vinaa.app/pricing", source=AID, verified="2026-11-21")

add(name="Fluent", category="Coding & Agents",
    what="Mac AI assistant that works inside any app",
    deal="25% off Basic, Standard and Team lifetime licences — Basic $49 → $36.75",
    discount=25, price_before="$49 one-time", price_after="$36.75 one-time",
    code="BF2026", ends="2026-12-01", tags=["lifetime"],
    url="https://fluentmac.app/buy", source=AID, verified="2026-11-21")

add(name="Kveeky", category="Coding & Agents",
    what="AI app builder with credit-based pricing",
    deal="35% off paid plans, applied at checkout",
    discount=35, code="BF2026", ends=None, ends_note="No end date printed",
    url="https://kveeky.com/pricing", source=AID, verified="2026-11-21")

add(name="Flowith", category="AI Chat & Assistants",
    what="Canvas-style AI workspace with multi-model threads",
    deal="Up to 31% off Black Pass plans — Go from $9.99/mo",
    discount=31, price_before="Black Pass list", price_after="from $9.99/mo",
    ends="2026-11-30", ends_note="Runs Nov 20–30",
    url="https://flowith.io/pricing", source=AID, verified="2026-11-21")

# ---------------------------------------------------------------- writing / research
add(name="Lara Translate", category="Writing & Docs",
    what="Document, image and audio translation in 200+ languages",
    deal="50% off one year of Pro or Team (tiers 1–3), billed annually",
    discount=50, code="BLCKFRDY2026", ends=None, ends_note="No end date printed",
    audience="Annual billing, tiers 1–3",
    url="https://laratranslate.com/pricing", source=WURD, verified="2026-11-21")

add(name="Trinka AI", category="Writing & Docs",
    what="Academic grammar and style checker with AI detection",
    deal="40% off all annual plans, applied automatically",
    discount=40, ends="2026-11-30", ends_note="Auto-applied at checkout",
    url="https://www.trinka.ai/pricing", source=WURD, verified="2026-11-21")

add(name="YouMind", category="Writing & Docs",
    what="AI workspace that turns research into articles and slides",
    deal="50% off the Max plan",
    discount=50, ends=None, ends_note="No end date printed",
    url="https://youmind.com/pricing", source=WURD, verified="2026-11-21")

add(name="Upplai", category="Writing & Docs",
    what="AI resume tailoring for applicant tracking systems",
    deal="20% off resume packages of $20 and up",
    discount=20, code="CYBER20", ends=None, ends_note="Announced by the vendor, no date",
    status="announced", tags=["announced"],
    url="https://upplai.com/pricing", source=WURD, verified="2026-11-21")

# ---------------------------------------------------------------- image
add(name="NightCafe", category="Image & Design",
    what="Community image generation with credit packs",
    deal="Double credits in the first month plus 5 free Kling 4.0 videos per $10 spent",
    discount=None, price_before="400 credits/mo", price_after="800 credits first month",
    ends="2026-11-30", ends_note="11:59 PM PT on Cyber Monday",
    renewal="Credits return to normal from month two",
    url="https://creator.nightcafe.studio/pricing", source=IMG, verified="2026-11-21")

add(name="Magnific (ex-Freepik)", category="Image & Design",
    what="Upscaling and AI image tools plus stock assets",
    deal="40% off credits on individual subscriptions — Premium $14.50/mo (was $20)",
    discount=27, price_before="$20/mo", price_after="$14.50/mo",
    ends="2026-12-10", audience="Individual subscriptions, not labelled Black Friday",
    url="https://www.magnific.ai/pricing", source=AID, verified="2026-11-21")

add(name="Dzine", category="Image & Design",
    what="Design and image generation canvas",
    deal="40% off the first year of individual annual plans",
    discount=40, code="BF40", ends=None, ends_note="No end date printed",
    audience="New subscribers and current monthly subscribers",
    url="https://www.dzine.ai/pricing", source=AID, verified="2026-11-21")

# ---------------------------------------------------------------- video
add(name="Pictory", category="Video",
    what="Turns scripts, URLs and decks into short videos",
    deal="70% off Professional annual — $17.50/mo instead of $59; Starter $12.50 and Teams $59.50 also on sale",
    discount=70, price_before="$59/mo", price_after="$17.50/mo",
    code="BLACKFRIDAY2026", ends=None, ends_note="Labelled 'Black Friday Offer', no written end date",
    renewal="Renews at the annual list price",
    url="https://pictory.ai/pricing/",
    source="https://pictory.ai/pricing/", verified="2026-11-25")

add(name="quso.ai", category="Video",
    what="Long video to short clips, formerly Vidyo.ai",
    deal="50% off new yearly Lite, Essential and Growth plans — kept at every renewal",
    discount=50, ends="2026-12-01", tags=["recurring"],
    renewal="Discount is permanent on this plan", audience="New yearly plans",
    url="https://quso.ai/pricing", source=AID, verified="2026-11-21")

add(name="BlitzReels", category="Video",
    what="Short-form video generator",
    deal="60% off the first year on annual Starter, Growth or Agency versus paying monthly",
    discount=60, ends=None, ends_note="No end date printed",
    url="https://blitzreels.com/pricing", source=AID, verified="2026-11-21")

add(name="Vid.AI", category="Video",
    what="Text-to-video and avatar videos",
    deal="Up to 60% off the first month, or 40% off the first year",
    discount=60, ends=None, ends_note="No end date printed", audience="New customers",
    url="https://vid.ai/pricing", source=AID, verified="2026-11-21")

add(name="ClipUGC", category="Video",
    what="UGC-style ad videos with AI actors",
    deal="50% off the first 2 months of monthly Professional or Business",
    discount=50, ends="2026-12-06",
    url="https://clipugc.com/pricing", source=AID, verified="2026-11-21")

add(name="Vadoo AI", category="Video",
    what="AI video generator with subtitles and dubbing",
    deal="30% off the Pro or Advance annual plan",
    discount=30, code="BF30", ends=None, ends_note="No end date printed",
    url="https://vadoo.tv/pricing", source=AID, verified="2026-11-21")

# ---------------------------------------------------------------- voice
add(name="LALAL.AI", category="Voice & Audio",
    what="Stem splitting and vocal removal",
    deal="40% off annual Pro for the first year, plus top-ups",
    discount=40, ends=None, ends_note="No written expiry on the vendor page",
    url="https://www.lalal.ai/pricing/", source=AID, verified="2026-11-21")

add(name="Narration Box", category="Voice & Audio",
    what="Text-to-speech narration for videos and podcasts",
    deal="55% off annual Plus, Pro and Scale plans for the first year",
    discount=55, ends="2026-12-02",
    url="https://narrationbox.com/pricing", source=AID, verified="2026-11-21")

add(name="Verbatik AI", category="Voice & Audio",
    what="Text-to-speech with 140+ languages",
    deal="30% off the first 12 months of any plan, plus prepaid credit packs",
    discount=30, code="BFCM26", ends=None, ends_note="No end date printed",
    url="https://verbatik.com/pricing", source=AID, verified="2026-11-21")

# ---------------------------------------------------------------- marketing
add(name="GetGenie", category="SEO & Marketing",
    what="AI SEO writing assistant for WordPress",
    deal="Up to 50% off, applied automatically (45% while the sale is pending)",
    discount=50, ends=None, ends_note="No end date printed",
    url="https://getgenie.ai/pricing/", source=WURD, verified="2026-11-21")

add(name="TrueRanker", category="SEO & Marketing",
    what="Rank tracking plus AI-visibility monitoring",
    deal="50% off Starter, Pro and Agency annual plans for the first year, or 25% off monthly for 12 months",
    discount=50, ends=None, ends_note="Announced by the vendor, no date",
    status="announced", tags=["announced"],
    url="https://trueranker.com/pricing", source=WURD, verified="2026-11-21")

add(name="Predis.ai", category="SEO & Marketing",
    what="AI social media post and ad generator",
    deal="Up to 50% off annual plans (Rise 50%, Core 40%, Enterprise+ 15%)",
    discount=50, ends=None, ends_note="No end date printed",
    url="https://predis.ai/pricing/", source=AID, verified="2026-11-21")

add(name="PostNitro", category="SEO & Marketing",
    what="Carousel and social post generator",
    deal="Up to 40% off Creator+ and Team+ — 40% off annual (BF26A), 16.7% off monthly (BF26M), recurring",
    discount=40, code="BF26A (annual) / BF26M (monthly)", ends=None,
    ends_note="No end date printed", tags=["recurring"],
    url="https://postnitro.ai/pricing", source=AID, verified="2026-11-21")

add(name="Reply.io", category="SEO & Marketing",
    what="Cold outreach and AI SDR platform",
    deal="40% off Reply plans; 25% off annual Jason AI SDR plans",
    discount=40, code="BF26REPLY / BF26JASON (AI SDR)", ends=None,
    ends_note="No end date printed",
    url="https://reply.io/pricing/", source=AID, verified="2026-11-21")

add(name="Ocoya", category="SEO & Marketing",
    what="AI social media management",
    deal="30% off Starter, Team and Agency plans, billed monthly",
    discount=30, ends=None, ends_note="No end date printed",
    url="https://www.ocoya.com/pricing", source=AID, verified="2026-11-21")

add(name="ContentStudio", category="SEO & Marketing",
    what="Social media scheduling with AI content generation",
    deal="Up to 50% off yearly plans (Standard 34%, Advanced 39%, Agency Unlimited 50%)",
    discount=50, price_before="$29/mo", price_after="$19/mo",
    ends=None, ends_note="No end date printed",
    url="https://contentstudio.io/pricing", source=WURD, verified="2026-11-21")

add(name="Supergrow", category="SEO & Marketing",
    what="LinkedIn content and scheduling with AI",
    deal="50% off all annual plans for the first year",
    discount=50, code="BF50", ends=None, ends_note="No end date printed",
    audience="New customers and monthly subscribers switching to annual",
    url="https://www.supergrow.ai/pricing", source=AID, verified="2026-11-21")

add(name="Tagshop AI", category="SEO & Marketing",
    what="Turns product catalogues into social video ads",
    deal="Up to 51% off yearly Starter, Growth and Pro plans",
    discount=51, ends=None, ends_note="No end date printed",
    url="https://tagshop.ai/pricing", source=AID, verified="2026-11-21")

add(name="Decktopus", category="SEO & Marketing",
    what="AI presentation and carousel maker",
    deal="66% off the first year of Pro and Business annual — Pro $40.76 for the year",
    discount=66, price_before="$120/yr", price_after="$40.76/yr",
    code="BF26", ends=None, ends_note="No end date printed",
    renewal="Renews at the annual list price",
    url="https://www.decktopus.com/pricing", source=WURD, verified="2026-11-21")

add(name="EngageBay", category="SEO & Marketing",
    what="All-in-one CRM with marketing automation",
    deal="40% off all plans plus 50,000 free email credits and free HubSpot migration",
    discount=40, ends=None, ends_note="No end date printed",
    url="https://www.engagebay.com/pricing", source=WURD, verified="2026-11-21")

add(name="Groupboss", category="SEO & Marketing",
    what="Turns Facebook group joins into leads",
    deal="40% off the first year of a yearly plan — Basic $47.40",
    discount=40, code="GBCM40", ends=None, ends_note="No end date printed",
    url="https://groupboss.io/pricing", source=WURD, verified="2026-11-21")

add(name="Two Minute Reports", category="SEO & Marketing",
    what="Client reporting for marketing agencies",
    deal="50% off the first year of any annual plan",
    discount=50, ends=None, ends_note="New customers only, no end date printed",
    url="https://twominutereports.com/pricing", source=WURD, verified="2026-11-21")

add(name="FeedBoss", category="SEO & Marketing",
    what="Connects ChatGPT, Claude and Grok to LinkedIn",
    deal="50% off all plans",
    discount=50, code="BFCM2026", ends=None, ends_note="Announced by the vendor, no date",
    status="announced", tags=["announced"], audience="New customers",
    url="https://feedboss.io/pricing", source=WURD, verified="2026-11-21")

add(name="Onethread", category="SEO & Marketing",
    what="Project management for small teams",
    deal="30% off annual plans, no code needed",
    discount=30, ends=None, ends_note="Announced by the vendor, no date",
    status="announced", tags=["announced"],
    url="https://onethread.com/pricing", source=WURD, verified="2026-11-21")

add(name="Salesmate", category="SEO & Marketing",
    what="CRM with built-in marketing automation",
    deal="An extra 10% off annual subscriptions on all plans",
    discount=10, code="BLACKFRIDAY26", ends=None, ends_note="Announced by the vendor, no date",
    status="announced", tags=["announced"],
    url="https://www.salesmate.io/pricing/", source=WURD, verified="2026-11-21")

add(name="Agency Handy", category="SEO & Marketing",
    what="Client portal and agency management with an AI agent",
    deal="Up to 70% off yearly plans — Freelancer $109/yr",
    discount=70, price_before="$363/yr", price_after="$109/yr",
    code="YEARLY70", ends=None, ends_note="No end date printed",
    url="https://agencyhandy.com/pricing", source=WURD, verified="2026-11-21")

add(name="Leadpages", category="Hosting & Infra",
    what="Landing pages and lead capture",
    deal="Up to 60% off the first year of annual plans (60% Pro and Business, 40% Grow)",
    discount=60, ends=None, ends_note="No end date printed",
    url="https://www.leadpages.com/pricing", source=AID, verified="2026-11-21")

# ---------------------------------------------------------------- infra
add(name="Together AI", category="Hosting & Infra",
    what="Inference API and GPU clusters",
    deal="18% off B200 post-training — $9.00/GPU-hour instead of $11.00",
    discount=18, price_before="$11.00/GPU-hr", price_after="$9.00/GPU-hr",
    ends="2026-12-14", ends_note="Post-training only",
    url="https://www.together.ai/pricing", source=TP, verified="2026-11-23")

add(name="Novita AI", category="Hosting & Infra",
    what="GPU instances and 200+ model APIs",
    deal="50% off batch inference tokens",
    discount=50, ends=None, ends_note="No end date printed", tags=["usage-only"],
    url="https://novita.ai/pricing", source=TP, verified="2026-11-23")

# ---------------------------------------------------------------- scan 2026-11-25
add(name="SiteData", category="SEO & Marketing",
    what="Research website traffic, SEO keywords, competitor ads and AdSense publisher networks",
    deal="50% off annual plans or 30% off monthly for the life of the subscription, auto-applied at Stripe checkout — Starter $49.50/yr (was $99) or $20.30/mo (was $29)",
    discount=50, price_before="$99/yr or $29/mo", price_after="$49.50/yr or $20.30/mo",
    ends="2026-11-30", ends_note="Ends Nov 30 at 24:00 UTC+8 (16:00 UTC)",
    audience="New and existing customers", tags=["recurring"],
    renewal="Same discounted rate on renewals while the subscription stays active",
    url="https://sitedata.dev/black-friday",
    source="https://sitedata.dev/black-friday", verified="2026-11-25")

add(name="Suno", category="Voice & Audio",
    what="AI music and lyric video generation",
    deal="30% off the first year of annual Pro, Premier or Platinum plans — web only; monthly plans and credits excluded",
    discount=30, price_before="$96/yr Pro", price_after="$67.20/yr Pro",
    ends="2026-11-30", ends_note="Official FAQ: through Nov 30; first year only",
    renewal="Renews at the standard annual price",
    url="https://suno.com/pricing",
    source="https://help.suno.com/en/articles/14878337", verified="2026-11-25")

add(name="VEED", category="Video",
    what="AI video editing, avatars, dubbing and subtitles",
    deal="30% off the full first year of any annual paid plan, or 30% off the first month on monthly; Enterprise excluded",
    discount=30, code="BLACKFRIDAY30", ends="2026-12-02",
    ends_note="Official window Nov 24 – Dec 2, 2026; one code per subscription",
    renewal="Annual: standard price in year two; monthly: full price after month one",
    url="https://www.veed.io/tools/black-friday",
    source="https://www.veed.io/tools/black-friday", verified="2026-11-25")

add(name="neuroflash", category="Writing & Docs",
    what="AI writing and marketing content with digital twins",
    deal="25% off annual Essential and Pro plans, or 20% off monthly, with code 9C94CXA6",
    discount=25, code="9C94CXA6", ends="2026-11-30",
    ends_note="Through Cyber Monday, Nov 30 at 23:59 (vendor timezone)",
    renewal="Regular price from Dec 1",
    url="https://neuroflash.com/black-friday",
    source="https://neuroflash.com/black-friday", verified="2026-11-25")

add(name="Later", category="SEO & Marketing",
    what="Social media scheduling, analytics and content planning",
    deal="6 months free in total on an annual Growth or Scale plan: 3 included with annual billing + 3 extra with the code",
    discount=25, price_before="Growth $37.50/mo", price_after="3 extra months free on first annual term",
    code="LATERBF26", ends="2026-12-04",
    ends_note="New annual purchases Nov 1 – Dec 4, 2026; later.com only, not the iOS app",
    audience="New customers only; no upgrades or monthly-to-annual switches",
    renewal="Standard annual rate after the first term",
    url="https://later.com/black-friday-sale/",
    source="https://later.com/black-friday-sale/", verified="2026-11-25")

# ---------------------------------------------------------------- partner
# Listing published by the site's sponsor. Kept visually distinct and marked
# `sponsored` so it never reads as independently verified like the rows above.
add(name="Singahi", category="Security & Compliance",
    what="ISO 27001 / SOC 2 compliance, penetration testing and managed security for growing companies",
    deal="30% off all services — compliance, assessment and managed security engagements",
    discount=30, price_before="List price", price_after="30% off",
    ends=None, ends_note="Partner offer — mention the list when you enquire",
    status="live", audience="Companies that need to prove security to customers, investors or regulators",
    tags=["partner"], sponsored=True,
    url="https://singahi.com", source="https://singahi.com", verified="2026-11-23")

# ---------------------------------------------------------------- usefulness
# Default ordering is usefulness to a reader, not headline percentage. The score
# is how many people can act on the deal x how good the price is x how little
# friction (no code hunting, no enterprise gate, no first-month teaser).
CATEGORY_WEIGHT = {
    "AI Chat & Assistants": 12,
    "Coding & Agents": 9,
    "Writing & Docs": 7,
    "Research & PDF": 5,
    "Image & Design": 5,
    "Video": 4,
    "Meetings & Automation": 3,
    "Voice & Audio": 2,
    "SEO & Marketing": 0,
    "Hosting & Infra": -3,
    "Security & Compliance": 0,
}

# tools a broad audience either already pays for or actively wants
BRAND = {
    "ElevenLabs": 26, "Adobe Creative Cloud Pro": 24, "Adobe Firefly": 16,
    "TypingMind": 20, "GitHub Copilot": 18, "Google AI Pro": 18,
    "Perplexity Pro": 12, "Microsoft 365 Premium": 14, "Canva Pro": 14,
    "ProWritingAid": 12, "Krisp": 12, "Notion AI": 10, "Cursor": 10,
    "tl;dv": 9, "Otter.ai": 9, "Pictory": 8, "invideo": 8, "Synthesia": 7,
    "Higgsfield": 7, "Recraft": 6, "Krea": 6, "Topaz Labs": 6,
    "PDF Pals": 5, "BoltAI": 6, "MindPal": 5, "LALAL.AI": 5,
    "Cloudways": 6, "Kinsta": 5, "Hostinger AI Builder": 6, "Together AI": 4,
    "NightCafe": 4, "Craft": 5, "Trinka AI": 4, "Lara Translate": 5,
}

# hand-set scores that override the formula where editorial judgement differs
USEFUL_OVERRIDE = {
    "ElevenLabs": 96, "Adobe Creative Cloud Pro": 93, "TypingMind": 90,
    "Google AI Pro": 88, "GitHub Copilot": 84, "Adobe Firefly": 83,
    "ProWritingAid": 80, "Canva Pro": 79, "Krisp": 78, "Perplexity Pro": 77,
    "tl;dv": 76, "Pictory": 75, "Microsoft 365 Premium": 74, "Otter.ai": 73,
    "Recraft": 71, "Krea": 70, "Topaz Labs": 68, "Higgsfield": 67,
    "PDF Pals": 66, "BoltAI": 65, "invideo": 64, "Synthesia": 63,
    "Craft": 62, "Cloudways": 61, "MindPal": 60, "LALAL.AI": 59,
    "NightCafe": 58, "Trinka AI": 57, "Lara Translate": 56, "Kinsta": 55,
    "Filmora": 54, "Hostinger AI Builder": 53, "Podwise": 52,
    "NotebookLM Tools": 51, "BoltAI": 65, "Bito": 50,
    "Suno": 69, "VEED": 66, "neuroflash": 55, "Later": 58, "SiteData": 59,
    "Singahi": 72,
}


def usefulness(d):
    if d["name"] in USEFUL_OVERRIDE:
        return USEFUL_OVERRIDE[d["name"]]
    s = 46 + CATEGORY_WEIGHT.get(d["category"], 0) + BRAND.get(d["name"], 0)
    if isinstance(d.get("discount"), int):
        s += min(d["discount"], 60) * 0.30
    tags = d.get("tags") or []
    if "lifetime" in tags:
        s += 7
    if d.get("status") == "announced":
        s -= 10
    if "first-month" in tags:
        s -= 16
    if d.get("status") == "perk":
        s -= 12
    if d.get("sponsored"):
        s = USEFUL_OVERRIDE.get(d["name"], s)
    return max(5, min(95, round(s)))


for _d in D:
    _d["useful"] = usefulness(_d)

payload = {
    "meta": {
        "title": "Awesome AI Black Friday Deals",
        "black_friday": "2026-11-27",
        "cyber_monday": "2026-11-30",
        "generated": TODAY.isoformat(),
        "checked_window": "2026-11-09 to 2026-11-25",
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
