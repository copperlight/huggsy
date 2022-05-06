import random

DICE = {
    1: [
        "+-------+",
        "|       |",
        "|   o   |",
        "|       |",
        "+-------+"
    ],
    2: [
        "+-------+",
        "|     o |",
        "|       |",
        "| o     |",
        "+-------+"
    ],
    3: [
        "+-------+",
        "|     o |",
        "|   o   |",
        "| o     |",
        "+-------+"
    ],
    4: [
        "+-------+",
        "| o   o |",
        "|       |",
        "| o   o |",
        "+-------+"
    ],
    5: [
        "+-------+",
        "| o   o |",
        "|   o   |",
        "| o   o |",
        "+-------+"
    ],
    6: [
        "+-------+",
        "| o   o |",
        "| o   o |",
        "| o   o |",
        "+-------+"
    ]
}


def roll_dice() -> str:
    first_die = DICE[random.randint(0,  7)]
    second_die = DICE[random.randint(0,  7)]

    result = ["```"]
    for idx, line in enumerate(first_die):
        result.append(line + " " + second_die[idx])
    result.append("```")

    return "\n".join(result)
