"""Shared console pretty-printer for JEV answers, used by every example script.
Not part of the jevzilla package -- copy this alongside an example if you share
a single file, or keep the whole examples/ folder together."""


def bar(pct: float, width: int = 20) -> str:
    filled = round(pct * width)
    return "█" * filled + "░" * (width - filled)


def print_verdict(title: str, state_summary: str, answers: dict) -> None:
    line = "─" * 60
    print(f"\n{line}\n {title}\n{line}")
    print(f" {state_summary}\n{line}")
    for key, a in answers.items():
        label = key.replace("_", " ").title()
        if a["type"] == "score":
            top = a["legend"][str(round(a["score"]))]
            print(f" {label:<22}: {top}  (confidence {a['confidence']:.0%})")
            for idx, name in a["legend"].items():
                print(f"   {name:<18} {bar(a['probabilities'][idx])} {a['probabilities'][idx]:.0%}")
        elif a["type"] == "noul":
            verdict = "YES" if a["noul"] >= 0.5 else "NO"
            print(f" {label:<22}: {verdict}  ({a['noul']:.0%})")
        elif a["type"] == "choice":
            print(f" {label:<22}: {a['choice']}  (confidence {a['confidence']:.0%})")
    print(line + "\n")
