"""
Venture Quest — Build & Validate
================================
An interactive classroom game that teaches venture creation, ideation and
validation using lean-startup / customer-development principles.

Students run one startup idea through five decision rounds:
  1. Frame the opportunity   (customer + problem / jobs-to-be-done)
  2. Find the riskiest assumption   (desirability / feasibility / viability)
  3. Customer discovery interview   (the "Mom Test")
  4. Design an experiment / MVP   (right test + a falsifiable success metric)
  5. Read the evidence & decide   (pivot / persevere / kill)

Scored out of 100 with teaching feedback after every choice.

Author: Dr Ash Najmaei — classroom activity
Run locally:  streamlit run streamlit_app.py
"""

import random
import streamlit as st

# --------------------------------------------------------------------------- #
#  PAGE CONFIG & STYLING
# --------------------------------------------------------------------------- #
st.set_page_config(
    page_title="Venture Quest — Build & Validate",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .vq-hero {
          background: linear-gradient(135deg,#4338ca 0%,#7c3aed 55%,#db2777 100%);
          padding: 1.6rem 1.8rem; border-radius: 18px; color: #fff;
          margin-bottom: 1.2rem;
      }
      .vq-hero h1 { color:#fff; margin:0 0 .3rem 0; font-size:1.9rem; }
      .vq-hero p  { color:#eef; margin:0; font-size:1.02rem; }
      .vq-card {
          background:#f8fafc; border:1px solid #e2e8f0; border-left:5px solid #6366f1;
          padding:1rem 1.2rem; border-radius:12px; margin:.6rem 0;
      }
      .vq-good { border-left-color:#16a34a; background:#f0fdf4; }
      .vq-bad  { border-left-color:#dc2626; background:#fef2f2; }
      .vq-warn { border-left-color:#d97706; background:#fffbeb; }
      .vq-pill {
          display:inline-block; padding:.15rem .6rem; border-radius:999px;
          font-size:.75rem; font-weight:600; margin-right:.35rem;
      }
      .vq-pill-d { background:#dbeafe; color:#1e40af; }   /* desirability */
      .vq-pill-f { background:#fef3c7; color:#92400e; }   /* feasibility  */
      .vq-pill-v { background:#dcfce7; color:#166534; }   /* viability    */
      .stButton>button { border-radius:10px; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
#  SCENARIO CONTENT
#  Each scenario is self-contained so the game is replayable across a class.
# --------------------------------------------------------------------------- #
SCENARIOS = [
    {
        "id": "campuseats",
        "title": "CampusEats",
        "tagline": "An app delivering cheap, healthy meals to uni students.",
        "founder_hook": (
            "You noticed friends surviving on instant noodles during exams. "
            "Your idea: an app that delivers affordable, healthy, ready-to-eat "
            "meals to students on campus."
        ),
        # -- Round 1: pick the sharpest customer + problem framing -----------
        "segments": [
            {
                "label": "Time-poor students in exam period living on campus",
                "score": 20,
                "feedback": "Sharp and specific. A narrow, reachable segment with an urgent, "
                            "recurring pain is exactly what you want early on — it makes the "
                            "problem testable and the first customers findable.",
            },
            {
                "label": "Everyone who eats food",
                "score": 4,
                "feedback": "Far too broad. 'Everyone' is nobody — you can't interview them, "
                            "message them, or reason about their job-to-be-done. Narrow to a "
                            "beachhead you can actually reach.",
            },
            {
                "label": "Health-conscious young professionals in the CBD",
                "score": 10,
                "feedback": "A real segment, but it drifts from the insight that sparked the idea "
                            "(students). You'd be validating a different business. Start where your "
                            "evidence is strongest.",
            },
        ],
        "problems": [
            {
                "label": "\"When I'm slammed with study, I struggle to eat well without wasting "
                         "time or money.\" (a job-to-be-done)",
                "score": 20,
                "feedback": "Excellent — framed as the customer's struggle and desired progress, "
                            "not your solution. Problem-first framing keeps you honest about whether "
                            "the pain is real.",
            },
            {
                "label": "\"Students don't have a food-delivery app built just for them.\"",
                "score": 6,
                "feedback": "This is a solution in disguise ('they lack my app'). Absence of your "
                            "product is not evidence of a problem. Describe the underlying struggle "
                            "instead.",
            },
            {
                "label": "\"Students want lower prices on everything.\"",
                "score": 9,
                "feedback": "True but generic — it doesn't isolate a job you can serve better than "
                            "alternatives. Tie the problem to a specific context and moment.",
            },
        ],
        # -- Round 2: riskiest assumption ------------------------------------
        "assumptions": [
            {
                "text": "Enough students feel the meal problem strongly enough to change habits "
                        "and pay for a fix.",
                "type": "D",
                "riskiest": True,
                "feedback": "Correct. This is the leap-of-faith assumption: if students don't "
                            "actually care enough to change behaviour, nothing else matters. Test "
                            "desirability first — it's the cheapest thing to be wrong about early.",
            },
            {
                "text": "We can cook and deliver a meal for under $8.",
                "type": "V",
                "riskiest": False,
                "feedback": "Viability matters, but modelling unit economics before you know anyone "
                            "wants the meal is optimising a business that may not exist. Park it.",
            },
            {
                "text": "We can build the ordering app on time.",
                "type": "F",
                "riskiest": False,
                "feedback": "Feasibility of building software is rarely the true risk for this idea — "
                            "the market risk (do they want it?) is far larger and cheaper to test.",
            },
        ],
        "context_noun": "students",
        # -- Round 4: MVP options --------------------------------------------
        "mvp_options": [
            {
                "label": "Concierge test: hand-deliver meals to 10 students for a week and "
                         "take real orders + payment.",
                "score": 20,
                "feedback": "Ideal for a desirability test. It puts a real offer in front of real "
                            "customers with real money on the line — no app required. Manual, "
                            "unscalable, and maximally informative.",
            },
            {
                "label": "Build the full app with payments, menus and driver routing, then launch.",
                "score": 5,
                "feedback": "Classic over-build. You'd spend months to learn what a week of manual "
                            "delivery teaches. Big MVPs hide the risk you most need to expose.",
            },
            {
                "label": "Post a poll asking 'Would you use a healthy meal app? Y/N'.",
                "score": 8,
                "feedback": "A poll measures opinions, not behaviour. 'Would you' answers are "
                            "notoriously unreliable — people say yes and never buy. Prefer a test "
                            "where they act.",
            },
        ],
        # -- Round 5: results & decision -------------------------------------
        "result_line": "You hand-delivered to 10 students for a week. 7 ordered at least once; "
                       "4 re-ordered and pre-paid for the next week; average spend $9.20.",
        "decisions": [
            {
                "label": "Persevere — strong pull; move to a slightly larger, still-manual test.",
                "score": 20,
                "feedback": "Right call. Re-orders and pre-payment are strong behavioural signals of "
                            "desirability. Persevere, but keep it manual and widen the test before "
                            "you build anything.",
            },
            {
                "label": "Pivot immediately to corporate catering.",
                "score": 6,
                "feedback": "The evidence points toward persevering, not pivoting. Pivot when data "
                            "says the current path is failing — here it's working. Don't abandon a "
                            "signal you fought to get.",
            },
            {
                "label": "Kill it — 3 of 10 didn't order.",
                "score": 7,
                "feedback": "Too harsh. A 70% trial and 40% pre-paying re-order rate at this stage is "
                            "encouraging. Judge against a threshold you set beforehand, not against "
                            "perfection.",
            },
        ],
    },
    {
        "id": "fitmates",
        "title": "FitMates",
        "tagline": "A marketplace matching gym-goers with compatible workout partners.",
        "founder_hook": (
            "You keep skipping the gym when you go alone. Your idea: an app that "
            "matches people with a nearby workout partner at a similar level and "
            "schedule."
        ),
        "segments": [
            {
                "label": "New gym members in their first 90 days who quit from lack of accountability",
                "score": 20,
                "feedback": "Great beachhead. New members have the strongest, most urgent pain "
                            "(low motivation, high drop-off) and are reachable through gyms. Urgency "
                            "+ reachability = testable.",
            },
            {
                "label": "All gym-goers worldwide",
                "score": 4,
                "feedback": "Too broad to interview, reach, or serve. Marketplaces especially need a "
                            "dense niche first, or you get empty listings on both sides.",
            },
            {
                "label": "Competitive powerlifters",
                "score": 9,
                "feedback": "A passionate niche, but they often already have training partners and "
                            "structures. The pain is weaker here than for wobbling newcomers.",
            },
        ],
        "problems": [
            {
                "label": "\"When I start at a new gym, I lose motivation training alone and quietly "
                         "quit.\" (a job-to-be-done)",
                "score": 20,
                "feedback": "Strong — an emotional, recurring struggle tied to a specific moment. "
                            "That's a job someone will 'hire' a solution for.",
            },
            {
                "label": "\"There's no good app to find gym partners.\"",
                "score": 6,
                "feedback": "Solution-shaped, not problem-shaped. The lack of your product isn't a "
                            "customer problem. Describe the struggle behind it.",
            },
            {
                "label": "\"People want to be fitter.\"",
                "score": 8,
                "feedback": "True but generic and non-specific. It doesn't point to a moment, a "
                            "trigger, or a job you can uniquely serve.",
            },
        ],
        "assumptions": [
            {
                "text": "People will actually meet and train with a stranger the app matches them to.",
                "type": "D",
                "riskiest": True,
                "feedback": "Correct — this is the leap of faith. Matching software is easy; getting "
                            "strangers to show up and train together is the behaviour the whole "
                            "business rests on. Test that first.",
            },
            {
                "text": "The matching algorithm can pair people by level and schedule.",
                "type": "F",
                "riskiest": False,
                "feedback": "Feasible and not the core risk. You can match people manually for the "
                            "first tests — don't let engineering hide the market question.",
            },
            {
                "text": "We can charge a monthly subscription.",
                "type": "V",
                "riskiest": False,
                "feedback": "Pricing/viability comes after you know people will meet and value it. "
                            "Don't optimise revenue on an unproven behaviour.",
            },
        ],
        "context_noun": "gym members",
        "mvp_options": [
            {
                "label": "Wizard-of-Oz: manually match 15 people via a group chat and see how many "
                         "pairs actually train together this week.",
                "score": 20,
                "feedback": "Perfect for the risk. You fake the 'algorithm' by hand and measure the "
                            "one behaviour that matters — do they show up together? Learn in days, "
                            "not months.",
            },
            {
                "label": "Build the matching app with profiles, chat and scheduling, then launch.",
                "score": 5,
                "feedback": "Over-building before the behaviour is proven. If strangers won't meet, "
                            "no feature set saves you. Fake it before you make it.",
            },
            {
                "label": "Run a survey: 'Would you use an app to find a gym buddy?'",
                "score": 8,
                "feedback": "Measures stated intent, not action. Marketplace behaviour must be seen, "
                            "not surveyed. Design a test where people actually turn up.",
            },
        ],
        "result_line": "You hand-matched 15 people into 7 pairs. Only 1 pair trained together more "
                       "than once — most ghosted after an awkward first message. But 9 of the 15 kept "
                       "using the little daily check-in you'd added on the side, and 4 asked if they "
                       "could just get solo reminders and streaks.",
        "decisions": [
            {
                "label": "Pivot — partner-matching flopped, but solo accountability shows real pull; "
                         "refocus on a solo streak / check-in app.",
                "score": 20,
                "feedback": "Right. Your riskiest assumption (strangers will train together) was "
                            "disconfirmed — but a stronger, unexpected signal appeared: people stuck "
                            "with the solo check-in. That's a textbook pivot: keep the traction, "
                            "change the concept.",
            },
            {
                "label": "Persevere — 1 pair is a start; the matching just needs a better algorithm.",
                "score": 6,
                "feedback": "This blames the tool to avoid the evidence. The behaviour clearly says "
                            "people won't train with strangers — grinding harder on a failed "
                            "assumption while ignoring the solo signal is sunk-cost thinking.",
            },
            {
                "label": "Kill it — barely anyone trained together.",
                "score": 8,
                "feedback": "Too final. The partner idea failed, but there IS live pull on the solo "
                            "check-in. When one door shows real behaviour, you pivot toward it rather "
                            "than shut everything down.",
            },
        ],
    },
    {
        "id": "ledgerlite",
        "title": "LedgerLite",
        "tagline": "Dead-simple invoicing & expense tracking for solo tradies.",
        "founder_hook": (
            "Your uncle, an electrician, does his invoicing on paper and dreads tax "
            "time. Your idea: a stripped-back invoicing + expense app for solo "
            "tradespeople who find accounting software overwhelming."
        ),
        "segments": [
            {
                "label": "Solo tradies (1-person businesses) who currently invoice on paper or texts",
                "score": 20,
                "feedback": "Sharp beachhead: a specific, reachable group with an acute, recurring "
                            "pain and clear willingness to pay to avoid tax-time stress.",
            },
            {
                "label": "All small and medium businesses",
                "score": 5,
                "feedback": "Too broad — SMBs span wildly different needs and already-entrenched "
                            "tools. You can't credibly serve or test 'all SMBs' at once.",
            },
            {
                "label": "Large construction firms with finance teams",
                "score": 6,
                "feedback": "These already run full accounting suites and have staff for it. The pain "
                            "your idea targets (overwhelm, no time) barely exists here.",
            },
        ],
        "problems": [
            {
                "label": "\"At tax time I panic because my invoices and receipts are scattered and "
                         "I'm not a numbers person.\" (a job-to-be-done)",
                "score": 20,
                "feedback": "Excellent — an emotional, high-stakes, recurring struggle in a concrete "
                            "moment. That's a job people pay to get done.",
            },
            {
                "label": "\"Tradies don't use a simple enough invoicing app.\"",
                "score": 6,
                "feedback": "Solution-shaped again. 'They don't use my product' is not a problem "
                            "statement. Capture the struggle, not the missing tool.",
            },
            {
                "label": "\"Small businesses want to save money on software.\"",
                "score": 8,
                "feedback": "Generic and weakly connected to the trigger. It won't guide a good "
                            "first test. Anchor to the tax-time panic.",
            },
        ],
        "assumptions": [
            {
                "text": "Tradies are frustrated enough with their current method to switch and pay "
                        "for a new one.",
                "type": "D",
                "riskiest": True,
                "feedback": "Correct. Switching costs and habit are the real enemy. If the pain "
                            "isn't strong enough to overcome inertia, the product dies regardless of "
                            "how good it is. Test desirability + willingness to switch first.",
            },
            {
                "text": "We can integrate with the tax office's e-filing system.",
                "type": "F",
                "riskiest": False,
                "feedback": "A feasibility detail for later. It doesn't need solving before you know "
                            "tradies will switch at all.",
            },
            {
                "text": "We can price it at $15/month and stay profitable.",
                "type": "V",
                "riskiest": False,
                "feedback": "Viability is downstream of desirability here. First learn if they'll "
                            "adopt; then refine price.",
            },
        ],
        "context_noun": "tradies",
        "mvp_options": [
            {
                "label": "Concierge: offer to do 5 tradies' invoicing for them for a month using a "
                         "spreadsheet, and ask them to pre-pay a small fee.",
                "score": 20,
                "feedback": "Ideal desirability + willingness-to-pay test. You deliver the outcome "
                            "manually, watch whether they hand over their messy receipts, and see if "
                            "they'll pay — all without building software.",
            },
            {
                "label": "Develop the full app with bank feeds and tax integration, then sell it.",
                "score": 5,
                "feedback": "Heavy build before the switching behaviour is proven. If inertia wins, "
                            "the features are wasted. Test the human behaviour first.",
            },
            {
                "label": "Ask tradies to rate 'How likely are you to try a new invoicing app?' 1-10.",
                "score": 8,
                "feedback": "Intent scores are weak evidence — high ratings rarely convert to "
                            "switching. Design a test where they actually act (and ideally pay).",
            },
        ],
        "result_line": "You offered to run invoicing for 8 tradies. 5 accepted and handed over their "
                       "receipts; 3 pre-paid a $20 setup fee; 2 said they'd 'do it themselves later' "
                       "and never sent anything.",
        "decisions": [
            {
                "label": "Persevere — real switching + pre-payment; expand the concierge test.",
                "score": 20,
                "feedback": "Right. Handing over receipts and pre-paying are strong signals that the "
                            "pain beats the inertia. Persevere manually, then automate the parts "
                            "that hurt most.",
            },
            {
                "label": "Pivot to serving large firms instead.",
                "score": 6,
                "feedback": "The signal is in the tradie segment you just validated — pivoting away "
                            "discards it. Pivot on failure, not on early success.",
            },
            {
                "label": "Kill it — 3 of 8 didn't follow through.",
                "score": 7,
                "feedback": "Too pessimistic. 5 of 8 switching and 3 pre-paying at this stage is a "
                            "healthy early signal. Set a threshold in advance and judge against it.",
            },
        ],
    },
    {
        "id": "ecothreads",
        "title": "EcoThreads",
        "tagline": "A monthly subscription box of sustainable, ethically-made clothing.",
        "founder_hook": (
            "You care deeply about sustainable fashion and the waste of fast fashion. "
            "Your idea: a monthly subscription that curates and ships ethically-made "
            "clothing to eco-conscious shoppers."
        ),
        "segments": [
            {
                "label": "Eco-conscious 25-35s who already pay a premium for sustainable brands",
                "score": 20,
                "feedback": "Sharp beachhead — reachable, and they've already shown they'll pay more "
                            "for values-aligned products. Existing paying behaviour is gold.",
            },
            {
                "label": "Anyone who buys clothes",
                "score": 4,
                "feedback": "Far too broad to reach, interview, or serve. 'Everyone' hides the fact "
                            "that most shoppers won't pay a sustainability premium.",
            },
            {
                "label": "Trend-driven teens on tight budgets",
                "score": 8,
                "feedback": "A real group, but budget- and trend-led — they pull against the "
                            "premium, curated positioning. The pain-to-pay match is weak.",
            },
        ],
        "problems": [
            {
                "label": "\"I want my wardrobe to match my values, but finding ethical clothes I "
                         "actually like eats hours I don't have.\" (a job-to-be-done)",
                "score": 20,
                "feedback": "Strong — a values-driven struggle with a concrete time cost. That's a "
                            "job people will pay to have done for them.",
            },
            {
                "label": "\"There's no good sustainable-clothing subscription box.\"",
                "score": 6,
                "feedback": "Solution-shaped. The absence of your box is not a customer problem — "
                            "describe the underlying struggle instead.",
            },
            {
                "label": "\"People want cheaper clothes.\"",
                "score": 8,
                "feedback": "Generic, and it actually fights your premium model. Cheapness isn't the "
                            "job your eco-shopper is hiring you for.",
            },
        ],
        "assumptions": [
            {
                "text": "Enough people will pay a recurring premium for curated ethical clothing they "
                        "can't see or try on first.",
                "type": "D",
                "riskiest": True,
                "feedback": "Correct. Recurring premium payment for un-tried physical goods is the "
                            "leap of faith. Enthusiasm and sign-ups are cheap; paying for a box "
                            "sight-unseen is the behaviour that makes or breaks this.",
            },
            {
                "text": "We can source enough ethical suppliers to fill a box every month.",
                "type": "F",
                "riskiest": False,
                "feedback": "A feasibility question for later. Solving sourcing before anyone pays is "
                            "building the engine for a car nobody's bought.",
            },
            {
                "text": "We can keep shipping and returns cheap enough to profit.",
                "type": "V",
                "riskiest": False,
                "feedback": "Viability matters eventually, but modelling margins before proving "
                            "willingness-to-pay optimises a business that may not exist.",
            },
        ],
        "context_noun": "eco-conscious shoppers",
        "mvp_options": [
            {
                "label": "Smoke-test + pre-sale: a landing page that takes real pre-orders with "
                         "payment for the first box.",
                "score": 20,
                "feedback": "Best test. It forces the one signal that counts — money up front — "
                            "before you hold a single item of stock.",
            },
            {
                "label": "Build inventory, shoot a full catalogue, launch the store, then see who buys.",
                "score": 5,
                "feedback": "Over-build. You'd sink cash into stock and photography before knowing "
                            "anyone will pay. The risk is demand, not catalogue polish.",
            },
            {
                "label": "Post the concept on social and count likes and email sign-ups.",
                "score": 8,
                "feedback": "Measures interest, not purchase. Likes and emails are free to give and "
                            "notoriously fail to predict paying behaviour.",
            },
        ],
        # -- VANITY-METRIC TRAP: the tempting 'persevere' answer is wrong ------
        "result_line": "Your landing page half went viral: 12,000 views and 1,500 email sign-ups in a "
                       "week. But of those 1,500, only 6 clicked through to pre-order — and just 1 "
                       "actually entered payment details when asked to pay up front.",
        "decisions": [
            {
                "label": "Don't scale — sign-ups without pre-orders are a vanity metric; rework the "
                         "offer or stop until you see real willingness to pay.",
                "score": 20,
                "feedback": "Right, and this is the trap most people fall into. 1,500 sign-ups FEELS "
                            "like success, but the only behaviour that matters — paying — happened "
                            "once in 1,500. That's a vanity metric. Find why payment collapsed and "
                            "re-test, or walk away.",
            },
            {
                "label": "Persevere — 1,500 sign-ups is huge; start manufacturing the first batch.",
                "score": 5,
                "feedback": "This is the vanity-metric trap. Sign-ups are free and non-committal; "
                            "manufacturing on a ~0.07% pay rate would burn cash on unproven demand. "
                            "Never scale on a number that doesn't involve payment.",
            },
            {
                "label": "Pivot to selling one-off items on a marketplace instead.",
                "score": 8,
                "feedback": "A pivot might come later, but this one is arbitrary — you have zero "
                            "evidence people will pay in ANY format yet. First learn why payment "
                            "collapsed before leaping elsewhere.",
            },
        ],
    },
    {
        "id": "shiftpal",
        "title": "ShiftPal",
        "tagline": "An app for hospitality staff to swap shifts without the group-chat chaos.",
        "founder_hook": (
            "You waited tables through uni and still remember the mess of swapping "
            "shifts over chaotic group chats. Your idea: an app where hospitality "
            "staff post and claim each other's shifts in a tap."
        ),
        "segments": [
            {
                "label": "Casual hospitality staff at busy venues juggling changing rosters",
                "score": 20,
                "feedback": "Specific, reachable, and the pain is frequent and concrete. A dense, "
                            "well-defined beachhead you can actually test in one venue.",
            },
            {
                "label": "All shift workers everywhere (nurses, retail, factories…)",
                "score": 5,
                "feedback": "Too broad — every industry has different rules, systems and cultures. "
                            "You can't serve or test them as one group.",
            },
            {
                "label": "Salaried office workers on fixed 9-5 schedules",
                "score": 4,
                "feedback": "They don't swap shifts — there's essentially no pain here. Wrong "
                            "customer for this job entirely.",
            },
        ],
        "problems": [
            {
                "label": "\"When I can't make a shift, sorting a swap over group chats is stressful "
                         "and things slip through the cracks.\" (a job-to-be-done)",
                "score": 20,
                "feedback": "Excellent — a recurring, stressful struggle in a specific moment, with a "
                            "clear cost when it goes wrong.",
            },
            {
                "label": "\"Venues don't have a dedicated shift-swap app.\"",
                "score": 6,
                "feedback": "Solution-shaped. The lack of your app isn't the problem — the swap "
                            "stress is. Frame the struggle, not the missing tool.",
            },
            {
                "label": "\"Hospitality workers want more flexibility.\"",
                "score": 8,
                "feedback": "True but generic — it doesn't isolate a testable moment or job you can "
                            "serve better than the group chat.",
            },
        ],
        "assumptions": [
            {
                "text": "Workers will open a dedicated app to post and claim swaps instead of just "
                        "messaging their mates.",
                "type": "D",
                "riskiest": True,
                "feedback": "Correct. The whole product rests on workers dropping an ingrained habit "
                            "(the group chat). If they won't change that behaviour, no feature saves "
                            "it — test this first.",
            },
            {
                "text": "We can sync with the venues' existing rostering software.",
                "type": "F",
                "riskiest": False,
                "feedback": "A feasibility detail for later. Integrations don't matter until you know "
                            "workers will actually use a swap tool at all.",
            },
            {
                "text": "Venues will pay a monthly fee per location.",
                "type": "V",
                "riskiest": False,
                "feedback": "Viability comes after adoption. Pricing an unproven behaviour is "
                            "premature.",
            },
        ],
        "context_noun": "hospitality workers",
        "mvp_options": [
            {
                "label": "Wizard-of-Oz: run swaps for ONE venue's staff by hand for two weeks via a "
                         "shared board, and watch what they actually use.",
                "score": 20,
                "feedback": "Ideal. You test the real adoption behaviour at a single venue with no "
                            "build — the fastest way to learn whether people will switch from the "
                            "group chat.",
            },
            {
                "label": "Build the full app (rosters, notifications, venue accounts) then pitch venues.",
                "score": 5,
                "feedback": "Over-build before the core behaviour is proven. If workers won't switch, "
                            "the whole app is wasted effort.",
            },
            {
                "label": "Email hospitality workers a survey asking if they'd use a shift-swap app.",
                "score": 8,
                "feedback": "Stated intent, not behaviour. People say yes to surveys and keep using "
                            "the group chat. Watch what they do, not what they claim.",
            },
        ],
        # -- PIVOT: worker adoption fails, but a paying signal appears elsewhere
        "result_line": "Over two weeks at one café, only 3 of 20 staff ever used your swap board — "
                       "most stuck to the group chat out of habit. But the manager used the board "
                       "constantly to spot roster gaps, fixed shortfalls faster, and asked whether "
                       "you could build 'the manager view' as a paid tool for her three venues.",
        "decisions": [
            {
                "label": "Pivot — worker adoption didn't stick, but the manager has real, paying "
                         "pull; refocus on a manager scheduling tool.",
                "score": 20,
                "feedback": "Right. Your riskiest assumption (worker adoption) was disconfirmed, but a "
                            "stronger signal — including willingness to pay — appeared on the manager "
                            "side. Keep the insight, change who you serve.",
            },
            {
                "label": "Persevere — 3 of 20 is a start; push harder to get workers to adopt.",
                "score": 6,
                "feedback": "The evidence is clear: workers won't leave the group chat. Grinding on a "
                            "failed assumption while ignoring a paying manager is sunk-cost, not grit.",
            },
            {
                "label": "Kill it — only 3 of 20 workers used it.",
                "score": 8,
                "feedback": "Too final. The worker path failed, but there's a live, paying signal from "
                            "the manager. When one door shows real pull, pivot toward it.",
            },
        ],
    },
]

# --------------------------------------------------------------------------- #
#  MOM-TEST INTERVIEW BANK (Round 3) — applied to whichever scenario is active
# --------------------------------------------------------------------------- #
INTERVIEW_QUESTIONS = [
    {
        "q": "\"Walk me through the last time you faced this — what happened, step by step?\"",
        "quality": "good",
        "feedback": "Gold-standard. It asks about a specific past event, so you get facts and "
                    "real behaviour instead of opinions or predictions.",
    },
    {
        "q": "\"Would you use an app that solved this? Be honest!\"",
        "quality": "bad",
        "feedback": "A hypothetical about the future — people are terrible at predicting their own "
                    "behaviour and tend to be polite. This tells you almost nothing.",
    },
    {
        "q": "\"Don't you think a cheaper, faster option would be amazing?\"",
        "quality": "bad",
        "feedback": "Leading + pitching. You've fished for a 'yes' and biased the answer. You "
                    "learn about your ego, not their life.",
    },
    {
        "q": "\"How are you dealing with this problem today, and what does it cost you "
         "(time / money / stress)?\"",
        "quality": "good",
        "feedback": "Excellent. It surfaces the current workaround and the real cost of the "
                    "problem — the size of the pain and whether it's worth solving.",
    },
    {
        "q": "\"Here's my idea — isn't it great? What do you think?\"",
        "quality": "bad",
        "feedback": "Pitching, not learning. Compliments are worthless data. In discovery you talk "
                    "about their life, never your idea.",
    },
    {
        "q": "\"What have you already tried to fix this, and why didn't it stick?\"",
        "quality": "good",
        "feedback": "Strong. Past attempts reveal genuine motivation, real alternatives, and the "
                    "true bar your solution must clear.",
    },
]

# --------------------------------------------------------------------------- #
#  SESSION STATE HELPERS
# --------------------------------------------------------------------------- #
def init_state():
    ss = st.session_state
    ss.setdefault("stage", "welcome")
    ss.setdefault("name", "")
    ss.setdefault("scenario_idx", None)
    ss.setdefault("scores", {})          # round_key -> points
    ss.setdefault("interview_set", None) # the 4 questions shown this game


def reset_game(keep_name=True):
    name = st.session_state.get("name", "")
    for k in list(st.session_state.keys()):
        if k in ("stage", "scenario_idx", "scores", "interview_set", "venture_choice") \
                or k.startswith(("r1_", "r2_", "r3_", "r4_", "r5_", "ord_")):
            st.session_state.pop(k, None)
    init_state()
    st.session_state["name"] = name if keep_name else ""


def _order(key, n):
    """Stable, per-session shuffled ordering of range(n) so the correct answer
    isn't always in the same slot. Cached in session_state; cleared on reset."""
    if key not in st.session_state:
        order = list(range(n))
        random.shuffle(order)
        st.session_state[key] = order
    return st.session_state[key]


MAX_SCORE = 100  # 5 rounds x 20 points each


def total_score():
    return sum(st.session_state["scores"].values())


def rank_for(score):
    if score >= 90:
        return "🏆 Lean-Startup Master", "You validate with evidence and resist the urge to build too soon."
    if score >= 75:
        return "🥇 Validation Pro", "Strong instincts — a couple of decisions to sharpen and you're there."
    if score >= 55:
        return "🥈 Rising Founder", "Solid grasp of the fundamentals; watch for solution-first thinking."
    if score >= 35:
        return "🥉 Aspiring Founder", "Good start — revisit riskiest-assumption thinking and the Mom Test."
    return "🌱 Idea Explorer", "Every founder starts here. Replay and focus on testing behaviour, not opinions."


# --------------------------------------------------------------------------- #
#  SIDEBAR
# --------------------------------------------------------------------------- #
def render_sidebar():
    with st.sidebar:
        st.markdown("### 🚀 Venture Quest")
        st.caption("Build & Validate — a lean-startup game")

        stage = st.session_state["stage"]
        order = ["welcome", "round1", "round2", "round3", "round4", "round5", "debrief"]
        labels = {
            "welcome": "Start",
            "round1": "1 · Frame the opportunity",
            "round2": "2 · Riskiest assumption",
            "round3": "3 · Customer interview",
            "round4": "4 · Design an experiment",
            "round5": "5 · Read the evidence",
            "debrief": "🏁 Debrief",
        }
        current = "round1" if stage.startswith("round1") else stage
        st.markdown("#### Progress")
        for key in order:
            done = order.index(key) < order.index(current) if current in order else False
            mark = "✅" if done else ("▶️" if key == current else "◻️")
            st.markdown(f"{mark} {labels[key]}")

        if st.session_state["scores"]:
            st.markdown("---")
            st.metric("Score so far", f"{total_score()} / 100")

        st.markdown("---")
        with st.expander("📚 Concept glossary"):
            st.markdown(
                "- **Job-to-be-done** — the progress a customer is trying to make; frame problems "
                "around this, not your product.\n"
                "- **Desirability / Feasibility / Viability** — do they *want* it? can we *build* it? "
                "can we *sustain* a business? Test the riskiest one first.\n"
                "- **Riskiest-assumption test** — attack the belief that, if false, kills everything.\n"
                "- **The Mom Test** — talk about their *life & past behaviour*, not your idea; never pitch.\n"
                "- **MVP** — the smallest test that produces real evidence (concierge, Wizard-of-Oz, "
                "smoke test, pre-sale), not a small product.\n"
                "- **Pivot / Persevere / Kill** — decide from behavioural evidence against a "
                "pre-set threshold."
            )
        st.markdown("---")
        if st.button("🔄 Restart game"):
            reset_game()
            st.rerun()


# --------------------------------------------------------------------------- #
#  STAGES
# --------------------------------------------------------------------------- #
def stage_welcome():
    st.markdown(
        '<div class="vq-hero"><h1>🚀 Venture Quest: Build &amp; Validate</h1>'
        '<p>Take one startup idea from a hunch to a tested opportunity. '
        'Five rounds, real founder decisions, instant feedback.</p></div>',
        unsafe_allow_html=True,
    )
    st.write(
        "You'll pick a customer, hunt the riskiest assumption, run a customer "
        "interview, design an experiment, and make the pivot-or-persevere call — "
        "scored out of 100 with coaching after every choice."
    )

    st.session_state["name"] = st.text_input(
        "Your name (or team name)", value=st.session_state.get("name", ""),
        placeholder="e.g. Team Nightowls",
    )

    st.markdown("#### Choose your venture")
    choice = st.radio(
        "Pick one to work on:",
        options=list(range(len(SCENARIOS))),
        format_func=lambda i: f"{SCENARIOS[i]['title']} — {SCENARIOS[i]['tagline']}",
        index=None,
        key="venture_choice",
    )

    name_ok = bool(st.session_state["name"].strip())
    ready = name_ok and choice is not None

    if st.button("▶️ Start the quest", type="primary", disabled=not ready):
        st.session_state["scenario_idx"] = choice
        # Freeze a 4-question interview set (2 good, 2 weak) for this playthrough
        goods = [q for q in INTERVIEW_QUESTIONS if q["quality"] == "good"]
        bads = [q for q in INTERVIEW_QUESTIONS if q["quality"] == "bad"]
        chosen = random.sample(goods, 2) + random.sample(bads, 2)
        random.shuffle(chosen)
        st.session_state["interview_set"] = chosen
        st.session_state["stage"] = "round1"
        st.rerun()

    if not name_ok:
        st.info("Enter a name to begin.")
    elif choice is None:
        st.info("Pick a venture to begin.")


def _sc():
    return SCENARIOS[st.session_state["scenario_idx"]]


def stage_round1():
    sc = _sc()
    st.markdown(f"### Round 1 · Frame the opportunity — *{sc['title']}*")
    st.markdown(f'<div class="vq-card">{sc["founder_hook"]}</div>', unsafe_allow_html=True)

    with st.expander("💡 Why this round matters"):
        st.write(
            "Great ventures start from a **specific customer** and a **real job-to-be-done**, "
            "not from a solution looking for a market. A sharp, narrow beachhead makes every "
            "later test cheaper and more honest."
        )

    locked = st.session_state.get("r1_locked", False)
    seg = st.radio(
        "**A. Who is your sharpest first customer (beachhead)?**",
        options=_order("ord_r1_seg", len(sc["segments"])),
        format_func=lambda i: sc["segments"][i]["label"],
        index=None,
        key="r1_seg",
        disabled=locked,
    )
    prob = st.radio(
        "**B. How should you frame the problem?**",
        options=_order("ord_r1_prob", len(sc["problems"])),
        format_func=lambda i: sc["problems"][i]["label"],
        index=None,
        key="r1_prob",
        disabled=locked,
    )

    if not locked:
        ready = seg is not None and prob is not None
        if not ready:
            st.caption("⛳ Choose one option in **A** and one in **B** to unlock the next step.")
        if st.button("Lock in answers", type="primary", disabled=not ready):
            st.session_state["r1_locked"] = True
            # each sub-choice worth up to 10 -> round out of 20
            pts = round(sc["segments"][seg]["score"] / 2) + round(sc["problems"][prob]["score"] / 2)
            st.session_state["scores"]["round1"] = min(pts, 20)
            st.rerun()
    else:
        s_fb = sc["segments"][seg]
        p_fb = sc["problems"][prob]
        st.markdown(
            f'<div class="vq-card {"vq-good" if s_fb["score"]>=15 else "vq-warn" if s_fb["score"]>=8 else "vq-bad"}">'
            f'<b>Customer:</b> {s_fb["feedback"]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="vq-card {"vq-good" if p_fb["score"]>=15 else "vq-warn" if p_fb["score"]>=8 else "vq-bad"}">'
            f'<b>Problem framing:</b> {p_fb["feedback"]}</div>', unsafe_allow_html=True)
        st.success(f"Round 1 score: {st.session_state['scores']['round1']} / 20")
        if st.button("Next round ▶️", type="primary"):
            st.session_state["stage"] = "round2"
            st.rerun()


def stage_round2():
    sc = _sc()
    st.markdown(f"### Round 2 · Find the riskiest assumption — *{sc['title']}*")
    st.markdown(
        f'<div class="vq-card">Every idea rests on assumptions. Some are cheap to be wrong '
        f'about; one is fatal. Your job: find the belief that would <b>kill the venture</b> '
        f'if it turned out false — and test <i>that</i> first.</div>',
        unsafe_allow_html=True,
    )
    with st.expander("💡 Desirability, Feasibility, Viability"):
        st.markdown(
            "Tag each assumption: "
            '<span class="vq-pill vq-pill-d">Desirability</span> do they want it? · '
            '<span class="vq-pill vq-pill-f">Feasibility</span> can we build it? · '
            '<span class="vq-pill vq-pill-v">Viability</span> can it sustain a business? '
            "Early on, **desirability** (market risk) is usually the riskiest and cheapest to test.",
            unsafe_allow_html=True,
        )

    locked = st.session_state.get("r2_locked", False)
    a_order = _order("ord_r2", len(sc["assumptions"]))
    pill = {"D": '<span class="vq-pill vq-pill-d">Desirability</span>',
            "F": '<span class="vq-pill vq-pill-f">Feasibility</span>',
            "V": '<span class="vq-pill vq-pill-v">Viability</span>'}
    st.markdown("**Which assumption should you test first?**")
    for i in a_order:
        a = sc["assumptions"][i]
        st.markdown(f'{pill[a["type"]]} &nbsp; {a["text"]}', unsafe_allow_html=True)
    pick = st.radio(
        "Your pick:",
        options=a_order,
        format_func=lambda i: sc["assumptions"][i]["text"][:70] + "…",
        index=None,
        key="r2_pick",
        label_visibility="collapsed",
        disabled=locked,
    )

    if not locked:
        ready = pick is not None
        if not ready:
            st.caption("⛳ Select the assumption you'd test first to continue.")
        if st.button("Lock in", type="primary", disabled=not ready):
            st.session_state["r2_locked"] = True
            st.session_state["scores"]["round2"] = 20 if sc["assumptions"][pick]["riskiest"] else 8
            st.rerun()
    else:
        a = sc["assumptions"][pick]
        klass = "vq-good" if a["riskiest"] else "vq-bad"
        st.markdown(f'<div class="vq-card {klass}">{a["feedback"]}</div>', unsafe_allow_html=True)
        if not a["riskiest"]:
            right = next(x for x in sc["assumptions"] if x["riskiest"])
            st.markdown(
                f'<div class="vq-card vq-good"><b>Riskiest assumption:</b> {right["text"]}</div>',
                unsafe_allow_html=True)
        st.success(f"Round 2 score: {st.session_state['scores']['round2']} / 20")
        if st.button("Next round ▶️", type="primary"):
            st.session_state["stage"] = "round3"
            st.rerun()


def stage_round3():
    sc = _sc()
    qs = st.session_state["interview_set"]
    st.markdown(f"### Round 3 · Customer discovery interview — *{sc['title']}*")
    st.markdown(
        f'<div class="vq-card">You sit down with a {sc["context_noun"]} to learn whether the '
        f'problem is real. <b>Select the questions that will give you honest, useful evidence</b> '
        f'— and avoid the ones that flatter your idea.</div>',
        unsafe_allow_html=True,
    )
    with st.expander("💡 The Mom Test in one line"):
        st.write(
            "Ask about their **life and past behaviour**, not your idea. Good questions are about "
            "specific past events and real costs; bad questions ask for opinions, predictions, or "
            "compliments — even your mum can't lie about facts, but she'll happily lie about your idea."
        )

    locked = st.session_state.get("r3_locked", False)
    st.markdown("**Tick every question you'd actually ask:**")
    picks = []
    for i, q in enumerate(qs):
        if st.checkbox(q["q"], key=f"r3_{i}", disabled=locked):
            picks.append(i)

    if not locked:
        ready = len(picks) >= 1
        if not ready:
            st.caption("⛳ Tick at least one question to run the interview.")
        if st.button("Run the interview", type="primary", disabled=not ready):
            st.session_state["r3_locked"] = True
            score = 0
            for i, q in enumerate(qs):
                if q["quality"] == "good" and i in picks:
                    score += 10   # 2 good questions -> up to 20
                elif q["quality"] == "bad" and i in picks:
                    score -= 6    # penalty for pitching/leading questions
            st.session_state["scores"]["round3"] = max(0, min(score, 20))
            st.session_state["r3_picks"] = picks
            st.rerun()
    else:
        picks = st.session_state.get("r3_picks", [])
        for i, q in enumerate(qs):
            chosen = i in picks
            good = q["quality"] == "good"
            if good:
                klass = "vq-good" if chosen else "vq-warn"
                head = "✅ Good question — asked" if chosen else "⚠️ Good question — you skipped it"
            else:
                klass = "vq-bad" if chosen else "vq-good"
                head = "❌ Weak question — you asked it" if chosen else "✅ Weak question — correctly avoided"
            st.markdown(
                f'<div class="vq-card {klass}"><b>{head}</b><br>{q["q"]}<br>'
                f'<i>{q["feedback"]}</i></div>', unsafe_allow_html=True)
        st.success(f"Round 3 score: {st.session_state['scores']['round3']} / 20")
        if st.button("Next round ▶️", type="primary"):
            st.session_state["stage"] = "round4"
            st.rerun()


def stage_round4():
    sc = _sc()
    st.markdown(f"### Round 4 · Design an experiment — *{sc['title']}*")
    st.markdown(
        f'<div class="vq-card">Your interviews suggest the problem is real. Now design the '
        f'<b>cheapest test that produces real behavioural evidence</b> for the riskiest '
        f'assumption — and commit to a success metric before you run it.</div>',
        unsafe_allow_html=True,
    )
    with st.expander("💡 An MVP is a test, not a small product"):
        st.write(
            "Concierge, Wizard-of-Oz, smoke-test landing pages and pre-sales all let you observe "
            "**behaviour** without building the real thing. Also set an **actionable, falsifiable "
            "threshold** in advance (e.g. 'at least 4 of 10 pre-pay') so you can't rationalise the "
            "result afterwards."
        )

    locked = st.session_state.get("r4_locked", False)
    metric_labels = [
        "A concrete behaviour with a pre-set threshold (e.g. ≥40% re-order or pre-pay)",
        "Lots of likes / positive comments on a post",
        "We'll know it's working when it feels right",
    ]
    mvp = st.radio(
        "**A. Which experiment best tests the riskiest assumption?**",
        options=_order("ord_r4_mvp", len(sc["mvp_options"])),
        format_func=lambda i: sc["mvp_options"][i]["label"],
        index=None,
        key="r4_mvp",
        disabled=locked,
    )
    metric = st.radio(
        "**B. What's the best success metric to set beforehand?**",
        options=_order("ord_r4_metric", 3),
        format_func=lambda i: metric_labels[i],
        index=None,
        key="r4_metric",
        disabled=locked,
    )

    if not locked:
        ready = mvp is not None and metric is not None
        if not ready:
            st.caption("⛳ Pick an experiment in **A** and a success metric in **B** to continue.")
        if st.button("Lock in experiment", type="primary", disabled=not ready):
            st.session_state["r4_locked"] = True
            metric_score = {0: 8, 1: 3, 2: 1}[metric]
            # round out of 20: experiment up to 12, metric up to 8
            mvp_pts = {20: 12, 8: 5, 5: 2}.get(sc["mvp_options"][mvp]["score"], 5)
            st.session_state["scores"]["round4"] = min(mvp_pts + metric_score, 20)
            st.session_state["r4_metric_score"] = metric_score
            st.rerun()
    else:
        m = sc["mvp_options"][mvp]
        klass = "vq-good" if m["score"] >= 15 else "vq-warn" if m["score"] >= 8 else "vq-bad"
        st.markdown(f'<div class="vq-card {klass}"><b>Experiment:</b> {m["feedback"]}</div>',
                    unsafe_allow_html=True)
        ms = st.session_state.get("r4_metric_score", 0)
        metric_fb = {
            8: ("vq-good", "A pre-set, behavioural threshold makes the result honest and hard to spin."),
            3: ("vq-bad", "Likes and comments are vanity metrics — they don't predict paying behaviour."),
            1: ("vq-bad", "'Feels right' isn't falsifiable — you'll rationalise whatever happens."),
        }[ms]
        st.markdown(f'<div class="vq-card {metric_fb[0]}"><b>Success metric:</b> {metric_fb[1]}</div>',
                    unsafe_allow_html=True)
        st.success(f"Round 4 score: {st.session_state['scores']['round4']} / 20")
        if st.button("See what happens ▶️", type="primary"):
            st.session_state["stage"] = "round5"
            st.rerun()


def stage_round5():
    sc = _sc()
    st.markdown(f"### Round 5 · Read the evidence & decide — *{sc['title']}*")
    st.markdown(f'<div class="vq-card vq-warn"><b>Results are in:</b> {sc["result_line"]}</div>',
                unsafe_allow_html=True)
    with st.expander("💡 Pivot, Persevere or Kill"):
        st.write(
            "**Persevere** when behavioural evidence beats your pre-set bar. **Pivot** when the data "
            "disconfirms your current path but points somewhere promising. **Kill** when there's no "
            "signal anywhere. Decide against the threshold you set — not against your mood."
        )

    locked = st.session_state.get("r5_locked", False)
    dec = st.radio(
        "**What do you do?**",
        options=_order("ord_r5", len(sc["decisions"])),
        format_func=lambda i: sc["decisions"][i]["label"],
        index=None,
        key="r5_dec",
        disabled=locked,
    )

    if not locked:
        ready = dec is not None
        if not ready:
            st.caption("⛳ Make your pivot / persevere / kill call to continue.")
        if st.button("Make the call", type="primary", disabled=not ready):
            st.session_state["r5_locked"] = True
            st.session_state["scores"]["round5"] = sc["decisions"][dec]["score"]
            st.rerun()
    else:
        d = sc["decisions"][dec]
        klass = "vq-good" if d["score"] >= 15 else "vq-warn" if d["score"] >= 8 else "vq-bad"
        st.markdown(f'<div class="vq-card {klass}">{d["feedback"]}</div>', unsafe_allow_html=True)
        st.success(f"Round 5 score: {st.session_state['scores']['round5']} / 20")
        if st.button("🏁 See your debrief", type="primary"):
            st.session_state["stage"] = "debrief"
            st.rerun()


def stage_debrief():
    sc = _sc()
    score = total_score()
    rank, blurb = rank_for(score)
    st.markdown(
        f'<div class="vq-hero"><h1>🏁 {st.session_state["name"]} — {score}/100</h1>'
        f'<p>{rank} · {blurb}</p></div>', unsafe_allow_html=True)

    st.markdown("#### Round-by-round")
    labels = {
        "round1": "1 · Frame the opportunity (/20)",
        "round2": "2 · Riskiest assumption (/20)",
        "round3": "3 · Customer interview (/20)",
        "round4": "4 · Design an experiment (/20)",
        "round5": "5 · Read the evidence (/20)",
    }
    for k in ["round1", "round2", "round3", "round4", "round5"]:
        v = st.session_state["scores"].get(k, 0)
        st.markdown(f"- **{labels[k]}** — {v}")

    st.markdown("#### The five habits you just practised")
    st.markdown(
        "1. **Start from a narrow customer & a real job-to-be-done**, not a solution.\n"
        "2. **Attack the riskiest assumption first** — usually desirability.\n"
        "3. **Interview for facts, not flattery** (the Mom Test).\n"
        "4. **Run the cheapest test that shows real behaviour**, with a threshold set in advance.\n"
        "5. **Decide from evidence** — pivot, persevere or kill against that threshold."
    )

    st.info(
        f"Venture: **{sc['title']}**. Replay with a different venture to compare how the same "
        f"validation logic plays out in a consumer app, a marketplace and a B2B tool."
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔁 Play a different venture", type="primary"):
            reset_game()
            st.rerun()
    with c2:
        if st.button("🔄 Restart from scratch"):
            reset_game(keep_name=False)
            st.rerun()

    st.markdown("---")
    st.caption(
        "Discussion prompts for class: Which round was hardest, and why? Where did you feel the "
        "pull to build too soon? What real assumption in your own project is the riskiest right now?"
    )


# --------------------------------------------------------------------------- #
#  ROUTER
# --------------------------------------------------------------------------- #
def main():
    init_state()
    render_sidebar()
    stage = st.session_state["stage"]
    router = {
        "welcome": stage_welcome,
        "round1": stage_round1,
        "round2": stage_round2,
        "round3": stage_round3,
        "round4": stage_round4,
        "round5": stage_round5,
        "debrief": stage_debrief,
    }
    router.get(stage, stage_welcome)()


if __name__ == "__main__":
    main()
