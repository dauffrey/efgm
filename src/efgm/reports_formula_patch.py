# Replace the formula block in src/efgm/reports.py with:

"```text",
"Q = (T × E × Fq)^(1/3)",
"F = Q / (1 + e)",
"```",

# Also update the interpretation text to note:
# Q is the geometric mean of positive quality factors. Entropy remains
# a denominator penalty. This prevents strong-but-imperfect quality factors
# from collapsing the score too aggressively.
