"""
Determines the association between four characters from the Rocinante
and four political systems using propositional logic.

Characters: James Holden, Alex Kamal, Joe Miller, Naomi Nagata
Systems:    Belters, OPA, MCRN, United Nations
"""

from logic import Variable, And, Or, Not, truth_table_rows

# ---------------------------------------------------------------------------
# 1. Define propositional variables
#    Each variable "X_Y" represents: Character X belongs to system Y.
# ---------------------------------------------------------------------------

CHARACTERS = ["Holden", "Kamal", "Miller", "Nagata"]
SYSTEMS    = ["Belters", "OPA", "MCRN", "UN"]

# Full names for display output
FULL_NAMES = {
    "Holden": "James Holden",
    "Kamal":  "Alex Kamal",
    "Miller": "Joe Miller",
    "Nagata": "Naomi Nagata",
}

# Build a dict mapping (character, system) -> Variable for easy lookup
prop = {}
for char in CHARACTERS:
    for sys in SYSTEMS:
        name = f"{char}_{sys}"
        prop[(char, sys)] = Variable(name)


# ---------------------------------------------------------------------------
# 2. Structural constraints (bijection)
#    - Each character belongs to exactly one political system.
#    - Each political system has exactly one character.
# ---------------------------------------------------------------------------

def exactly_one_prop(variables):
    """
    Build a proposition enforcing that exactly one of the given
    propositional variables is True.

    Encodes: (at least one is True)  AND  (no two are simultaneously True)
    """
    # At least one: big disjunction
    at_least_one = Or(*variables)

    # At most one: for every pair, they cannot both be True
    at_most_one_clauses = []
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            # ~(A & B)  is equivalent to  (~A | ~B)
            at_most_one_clauses.append(Or(Not(variables[i]), Not(variables[j])))

    return And(at_least_one, *at_most_one_clauses)


constraints = []

# Each character has exactly one system
for char in CHARACTERS:
    char_vars = [prop[(char, sys)] for sys in SYSTEMS]
    constraints.append(exactly_one_prop(char_vars))

# Each system has exactly one character
for sys in SYSTEMS:
    sys_vars = [prop[(char, sys)] for char in CHARACTERS]
    constraints.append(exactly_one_prop(sys_vars))


# ---------------------------------------------------------------------------
# 3. Knowledge-base facts
# ---------------------------------------------------------------------------

# Fact 1: "Through his parents, James Holden belongs to the United Nations."
#   Holden_UN = True
constraints.append(prop[("Holden", "UN")])

# Fact 2: "Joe Miller despises the Rocinante because it was constructed by
#          the MCRN, to which he is not associated."
#   Miller_MCRN = False  =>  ~Miller_MCRN
constraints.append(Not(prop[("Miller", "MCRN")]))

# Fact 3: "Naomi Nagata either belongs to the Belters or to the OPA."
#   Nagata_Belters v Nagata_OPA
constraints.append(Or(prop[("Nagata", "Belters")], prop[("Nagata", "OPA")]))


# ---------------------------------------------------------------------------
# 4. Combine all constraints into a single knowledge base
# ---------------------------------------------------------------------------

knowledge_base = And(*constraints)


# ---------------------------------------------------------------------------
# 5. Enumerate all satisfying assignments
# ---------------------------------------------------------------------------

all_vars = knowledge_base.variables()
rows     = truth_table_rows(all_vars)

solutions = []
for row in rows:
    if knowledge_base.evaluate(**row):
        # Extract the character -> system mapping from this satisfying row
        mapping = {}
        for char in CHARACTERS:
            for sys in SYSTEMS:
                if row[f"{char}_{sys}"]:
                    mapping[char] = sys
        solutions.append(mapping)


# ---------------------------------------------------------------------------
# 6. Display results
# ---------------------------------------------------------------------------

print("=" * 50)
print("  Hero Villain — Character / System Associations")
print("=" * 50)
print(f"\nTotal satisfying assignments found: {len(solutions)}\n")

for i, sol in enumerate(solutions, start=1):
    print(f"--- Solution {i} ---")
    print(f"  {'Character':<20} {'Political System'}")
    print(f"  {'-'*20} {'-'*16}")
    for char in CHARACTERS:
        print(f"  {FULL_NAMES[char]:<20} {sol[char]}")
    print()