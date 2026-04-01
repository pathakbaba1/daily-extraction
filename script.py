import os
import re
import datetime
import subprocess

# Operational Parameters
QUESTIONS_REGULAR = [
    "1. Did I actively practice behavioral questions out loud for 30 mins after waking up?",
    "2. Did I leave for the library around 12 PM?",
    "3. Did I keep my phone strictly put away in the library (Block 1)?",
    "4. Did I leave for the library again at 8 PM?",
    "5. Did I keep my phone strictly put away in the library (Block 2)?",
    "6. CONTRACT: Will I go home, take a shower, and go straight to bed?"
]

QUESTIONS_CDS = [
    "1. Am I in the library right now?",
    "2. CONTRACT: Will I go home, take a shower, and go straight to bed?"
]

QUESTIONS_SATURDAY = [
    "1. Did I actively practice behavioral questions out loud for 30 mins after waking up?",
    "2. Did I leave for the library around 12 PM?",
    "3. Did I keep my phone strictly put away in the library (Block 1)?",
    "4. Did I leave for the library again at 8 PM?",
    "5. Did I keep my phone strictly put away in the library (Block 2)?",
    "6. Will I give leetcode contest now?",
    "7. CONTRACT: Will I go home, take a shower, and go straight to bed?"
]

LOG_FILE = "extraction_telemetry.csv"
REQUIRED_PHRASE = "yes i am proud of it"


def print_boot_sequence():
    """Initializes the terminal with the psychological baseline."""
    print("=" * 65)
    print(" SYSTEM BOOT: OPERATION EXTRACTION ".center(65, "="))
    print("=" * 65)
    print("Good evening. Your Master's degree and your future role in Big")
    print("Tech are not granted; they are engineered. Every green commit")
    print("is a brick in that foundation. You are the man who does not numb")
    print("himself. You are the man who executes the mission.")
    print("-" * 65)
    print("INSTRUCTION ALGORITHM:")
    print("To confirm a successful protocol, you must physically sign it.")
    print(f"The ONLY accepted input for a verified execution is:")
    print(f"-> yes i am proud of it")
    print("=" * 65 + "\n")


def get_questions_for_today():
    """Select the right question set based on the day of the week."""
    day = datetime.datetime.now().strftime("%A")  # e.g. 'Tuesday'
    if day in ("Tuesday", "Thursday"):
        return QUESTIONS_CDS, day
    elif day == "Saturday":
        return QUESTIONS_SATURDAY, day
    else:
        return QUESTIONS_REGULAR, day


def execute_daily_log():
    # Change to the script's directory so git commands and log file work correctly
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print_boot_sequence()

    questions, day_name = get_questions_for_today()
    total = len(questions)
    print(f"Today is {day_name}. Running {total}-point protocol.\n")
    score = 0

    for q in questions:
        answer = input(f"{q}\n> ").strip().lower()

        # Scrubbing punctuation and normalizing standalone 'im' to 'i am'
        clean_answer = answer.replace("'", "").replace(",", "").replace(".", "")
        clean_answer = re.sub(r"\bim\b", "i am", clean_answer)

        if clean_answer == REQUIRED_PHRASE:
            score += 1
            print("  [Verified]\n")
        else:
            print("  [Failed]\n")

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    log_entry = f"{date_str}, {day_name}, Score: {score}/{total}\n"

    # Internal redundancy: Always maintain local telemetry
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    # The GitHub Constraint
    if score == total:
        print("=" * 65)
        print(f"Flawless execution. All {total} contracts signed.")
        print("Committing to remote repository...")
        try:
            subprocess.run(["git", "add", LOG_FILE], check=True)
            subprocess.run(
                ["git", "commit", "-m", f"Day Won: {date_str} - Proud."], check=True
            )
            subprocess.run(["git", "push"], check=True)
            print(
                "\nPush successful. The board is green. Walk away from the machine."
            )
        except subprocess.CalledProcessError:
            print("\nGit command failed. Check repository initialization.")
    else:
        print("=" * 65)
        print(f"System degraded: {score}/{total}. Local log updated.")
        print("No GitHub commit pushed. Do not miss twice.")


if __name__ == "__main__":
    execute_daily_log()
