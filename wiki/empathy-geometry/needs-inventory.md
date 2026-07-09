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

Checker note: *mistrustful, suspicious* (AFRAID) and *guarded, leery* (VULNERABLE) sit near the faux boundary — they can encode the other's action. Expert to rule on borderline words during the faux red-line.

## Faux-feelings — DRAFT pending expert red-line

The draft list lives in [[grammar-spec]] (highest-leverage lexicon in the checker stack): words that encode the other's action rather than one's own state; they parse as JKL-FAUX, not FEEL.

## Sources

- NYU mirror (needs): https://wp.nyu.edu/coaching/tools/needs-inventory/
- NYU mirror (feelings): https://wp.nyu.edu/coaching/tools/feelings-inventory/
- Center for Nonviolent Communication: https://www.cnvc.org/
- Sociocracy For All NVC feelings and needs list: https://www.sociocracyforall.org/nvc-feelings-and-needs-list/
