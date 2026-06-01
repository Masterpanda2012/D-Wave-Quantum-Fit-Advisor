# Outreach email — D-Wave Systems (deliverability-safe)

Use the **plain-text body** below in Gmail/Outlook (paste as plain text, not from a rich doc). Do not attach files on the first message. Send to **one named person** when possible, not a bulk alias.

---

## Before you send (reduces spam folder risk)

1. **Recipient** — Prefer a real contact (DevRel, solutions engineer, hiring manager) from LinkedIn or the company site. Avoid `info@`, `hello@`, `contact@`, and long CC lists on the first send.
2. **From address** — Send from your normal mailbox (e.g. school or personal Gmail you already use for real mail). Do not use a brand-new address for cold outreach.
3. **Authentication** — If you use a custom domain, confirm SPF, DKIM, and DMARC are set in DNS (Google Workspace / Cloudflare docs). Gmail accounts already have this handled.
4. **Format** — Plain text only for v1. No HTML newsletter layout, no images, no tracking links, no URL shorteners (bit.ly, etc.).
5. **Links** — **One link** in the body (GitHub repo). Put run instructions in the README, not in the email.
6. **Subject** — Short, specific, no ALL CAPS, no exclamation marks, no “FREE” / “URGENT” / “ACT NOW”.
7. **Volume** — One company, one person, one email. Wait for a reply before wide follow-ups.
8. **Optional** — Send Tuesday–Thursday morning in the recipient’s time zone. Add 2–3 prior emails in the same thread only if you already talked to that person.

---

## Subject line (pick one)

Best default:

    Question on quantum adoption tooling (student project)

Alternatives:

    Student-built prototype: when to use quantum vs classical
    Feedback request: problem qualification wizard (open source)

Avoid:

    Open-source prototype — “should I use quantum?” …   (quotes + em dash can hurt on some filters)
    AMAZING opportunity / internship / partnership

---

## Plain-text body (copy from here)

Hi [First name],

I built a small open-source side project inspired by D-Wave’s adoption story: helping engineers decide whether an optimization problem is worth classical solvers, hybrid Leap workflows, or a quantum POC—without needing a PhD first.

It is called Quantum Fit Advisor: a FastAPI backend and React wizard. You describe the problem (routing, scheduling, portfolio, etc.), and it returns a conservative recommendation (classical, hybrid, or quantum) with a short rationale, five transparent fit scores, a QUBO/BQM sketch, and links to relevant Ocean docs. It defaults to classical when scale or structure does not justify quantum, on purpose.

I am not pitching a product or asking for a job in this note—only whether the framing matches how your team actually qualifies opportunities. If it is off base, a one-line redirect would be enough.

Repo (README has run steps): https://github.com/Masterpanda2012/D-Wave-Quantum-Fit-Advisor

Thank you for your time,

Nikhil Avin
[Your school or program, optional one line]
[City, optional]

---

## What we removed vs the rich draft (and why)

| Removed from email | Why |
|--------------------|-----|
| Markdown bold/headers | Many clients send HTML; heavy formatting looks like marketing mail |
| Code blocks / localhost URLs | Filters flag shell snippets and non-public hosts |
| Multiple doc links | Link-heavy messages score higher as promotional |
| “Lead qualification” / “sales funnel” | B2B spam lexicon |
| Long bullet lists | Fine on GitHub README; in email, keep under ~150 words if possible |

The README on GitHub can stay detailed; the email should be a short human intro plus one link.

---

## If it still lands in spam

- Ask a friend to send a test to you and check headers (Gmail: Show original → SPF/DKIM pass).
- Reply from your regular contacts first that day so the mailbox has normal activity.
- If using school Outlook, send from web client once (not a broken SMTP app).
- Follow up once after 5–7 business days with a shorter note in the **same thread**, still plain text, no new links.

---

## Rich reference draft (do not send as-is)

Keep the long markdown version for your own notes only, or turn it into a GitHub Discussion / README section—not the first email.
