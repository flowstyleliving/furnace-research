# CNVC Needs Inventory — reference copy

Sourced 2026-07-08. Direct fetch of cnvc.org returned 403; this copy is from the NYU mirror of the CNVC needs inventory, cross-checked against the sociocracyforall mirror. Part of [[empathy-geometry/README|Empathy Geometry]].

Two jobs:
1. **Needs vocabulary** for personas and event metadata ([[event-bank]], [[personas-e3]]) — named needs must come from this list.
2. **N-purity lexicon** for the need-vs-strategy checker in [[grammar-spec]] — need-slot terms must map here (morphological variants + a small versioned synonym map, to be built at implementation time).

## Inventory

**CONNECTION** — acceptance, affection, appreciation, belonging, cooperation, communication, closeness, community, companionship, compassion, consideration, consistency, empathy, inclusion, intimacy, love, mutuality, nurturing, respect/self-respect, safety, security, stability, support, to know and be known, to see and be seen, to understand and be understood, trust, warmth

**PHYSICAL WELL-BEING** — air, food, movement/exercise, rest/sleep, sexual expression, safety, shelter, touch, water

**HONESTY** — authenticity, integrity, presence

**PLAY** — joy, humor

**PEACE** — beauty, communion, ease, equality, harmony, inspiration, order

**AUTONOMY** — choice, freedom, independence, space, spontaneity

**MEANING** — awareness, celebration of life, challenge, clarity, competence, consciousness, contribution, creativity, discovery, efficacy, effectiveness, growth, hope, learning, mourning, participation, purpose, self-expression, stimulation, to matter, understanding

## Feelings inventory (F-purity lexicon)

Sourced 2026-07-08 from the NYU mirror of the CNVC feelings inventory. Used by F-purity in [[grammar-spec]]: a FEEL move's word must map here; faux-list words parse as JKL-FAUX instead.

**When needs are satisfied:**

AFFECTIONATE — compassionate, friendly, loving, open-hearted, sympathetic, tender, warm · ENGAGED — absorbed, alert, curious, engrossed, enchanted, entranced, fascinated, interested, intrigued, involved, spellbound, stimulated · HOPEFUL — expectant, encouraged, optimistic · CONFIDENT — empowered, open, proud, safe, secure · EXCITED — amazed, animated, ardent, aroused, astonished, dazzled, eager, energetic, enthusiastic, giddy, invigorated, lively, passionate, surprised, vibrant · GRATEFUL — appreciative, moved, thankful, touched · INSPIRED — amazed, awed, wonder · JOYFUL — amused, delighted, glad, happy, jubilant, pleased, tickled · EXHILARATED — blissful, ecstatic, elated, enthralled, exuberant, radiant, rapturous, thrilled · PEACEFUL — calm, clear-headed, comfortable, centered, content, equanimous, fulfilled, mellow, quiet, relaxed, relieved, satisfied, serene, still, tranquil, trusting · REFRESHED — enlivened, rejuvenated, renewed, rested, restored, revived

**When needs are not satisfied:**

AFRAID — apprehensive, dread, foreboding, frightened, mistrustful, panicked, petrified, scared, suspicious, terrified, wary, worried · ANNOYED — aggravated, dismayed, disgruntled, displeased, exasperated, frustrated, impatient, irritated, irked · ANGRY — enraged, furious, incensed, indignant, irate, livid, outraged, resentful · AVERSION — animosity, appalled, contempt, disgusted, dislike, hate, horrified, hostile, repulsed · CONFUSED — ambivalent, baffled, bewildered, dazed, hesitant, lost, mystified, perplexed, puzzled, torn · DISCONNECTED — alienated, aloof, apathetic, bored, cold, detached, distant, distracted, indifferent, numb, removed, uninterested, withdrawn · DISQUIET — agitated, alarmed, discombobulated, disconcerted, disturbed, perturbed, rattled, restless, shocked, startled, surprised, troubled, turbulent, turmoil, uncomfortable, uneasy, unnerved, unsettled, upset · EMBARRASSED — ashamed, chagrined, flustered, guilty, mortified, self-conscious · FATIGUE — beat, burnt out, depleted, exhausted, lethargic, listless, sleepy, tired, weary, worn out · PAIN — agony, anguished, bereaved, devastated, grief, heartbroken, hurt, lonely, miserable, regretful, remorseful · SAD — depressed, dejected, despair, despondent, disappointed, discouraged, disheartened, forlorn, gloomy, heavy hearted, hopeless, melancholy, unhappy, wretched · TENSE — anxious, cranky, distressed, distraught, edgy, fidgety, frazzled, irritable, jittery, nervous, overwhelmed, restless, stressed out · VULNERABLE — fragile, guarded, helpless, insecure, leery, reserved, sensitive, shaky · YEARNING — envious, jealous, longing, nostalgic, pining, wistful

Checker note: *mistrustful* (AFRAID) and *guarded, leery* (VULNERABLE) **are valid feelings** — expert-ruled 2026-07-13. **Exception:** *suspicious*, though listed under AFRAID in the NYU mirror, is expert-ruled **not** a feeling (an evaluation of the other's trustworthiness) → treated as faux/evaluation (felt versions: mistrustful, wary, uneasy). General rule: inventory membership decides, minus this one override; a faux-feeling is an other-action charge — *or* an inward self-judgment (inadequate, worthless) — absent from the inventory. See [[grammar-spec]] F-purity.

## Faux-feelings — RED-LINED 2026-07-13

The finalized list lives in [[grammar-spec]] F-purity (highest-leverage lexicon in the checker stack): *charges* absent from the CNVC inventory; they parse as JKL-FAUX, not FEEL. Operating rule — the CNVC feelings inventory above is the **whitelist** (any word there is a valid FEEL, minus the `suspicious` override); the faux list is a curated **blacklist**.

Faux covers **two flavors**, both of which fail F-purity:
1. **outward other-action charges** — "I feel *ignored / steamrolled / manipulated*" (an accusation about what the other did, wearing a feeling's clothes);
2. **inward self-evaluations** — "I feel *inadequate / worthless / stupid*" (a verdict about the self, wearing a feeling's clothes).

**Expert ruling 2026-07-13:** *"i feel inadequate is absolutely a jackal move."* This **supersedes** an earlier draft line here that scoped self-evaluations *out* of the charge-detector to protect vulnerable self-disclosure. It does not: a self-verdict is jackal aimed inward. The giraffe form names the felt state and the unmet need instead ("I feel **discouraged**, I need to know my work **matters**"). See [[grammar-spec]] F-purity for the finalized lists.

## Sources

- NYU mirror (needs): https://wp.nyu.edu/coaching/tools/needs-inventory/
- NYU mirror (feelings): https://wp.nyu.edu/coaching/tools/feelings-inventory/
- Center for Nonviolent Communication: https://www.cnvc.org/
- Sociocracy For All NVC feelings and needs list: https://www.sociocracyforall.org/nvc-feelings-and-needs-list/
