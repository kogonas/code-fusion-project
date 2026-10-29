
import json
import os

ADMIN_PASSWORD = "admin123"  # change this before sharing
REVIEW_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reviews.json")

FLAGS = {
    "wifi": "Wi-Fi",
    "outlets": "Outlets",
    "quiet": "Quiet",
    "groups": "Group-friendly",
    "food": "Food nearby",
    "reserve": "Reservable rooms",
    "offcampus": "Not owned by GSU",
}

LIB = "https://library.gsu.edu"
SC = "https://studentcenter.gsu.edu"
ROOMS = "https://rooms.library.gsu.edu/reserve/atlanta"
GSU = "https://www.gsu.edu"
MAPS = "https://www.google.com/maps/search/"

SPACES = [
    {"id": 1, "name": "Library South", "location": "100 Decatur St SE", "kind": "Library",
     "wifi": 1, "outlets": 1, "quiet": 1, "groups": 1, "food": 1, "reserve": 1, "offcampus": 0,
     "noise": "Quiet floors up top, louder lower floors", "seating": "Tables, carrels, group rooms",
     "hours": "Check library site (varies by term)",
     "eats": "Saxbys coffee shop in the library. Check posted food rules by floor.",
     "blurb": "One entrance of the University Library, with floors set aside for different study styles. Group rooms need a reservation.",
     "site": LIB},
    {"id": 2, "name": "Library North", "location": "Courtland St & Gilmer St", "kind": "Library",
     "wifi": 1, "outlets": 1, "quiet": 1, "groups": 1, "food": 1, "reserve": 1, "offcampus": 0,
     "noise": "Mixed, depends on floor", "seating": "Tables, soft seating, group rooms",
     "hours": "Check library site (varies by term)",
     "eats": "Saxbys coffee shop in the library. Check posted food rules by floor.",
     "blurb": "The second entrance to the same library. The Study Commons below the building adds extra seating, and Tech Spaces need an advance booking.",
     "site": LIB},
    {"id": 3, "name": "Library Study Rooms", "location": "Library North and South", "kind": "Reservable rooms",
     "wifi": 1, "outlets": 1, "quiet": 0, "groups": 1, "food": 0, "reserve": 1, "offcampus": 0,
     "noise": "Closed rooms, good for talking", "seating": "Small to large group rooms",
     "hours": "Book up to 21 days ahead, 3 hours per day",
     "eats": "Check room rules before bringing food.",
     "blurb": "40+ rooms. Reserve with your campus ID. Reservations take priority over walk-ins.",
     "site": ROOMS},
    {"id": 4, "name": "Aderhold Learning Center", "location": "Fairlie-Poplar District", "kind": "Classroom building",
     "wifi": 1, "outlets": 1, "quiet": 0, "groups": 1, "food": 0, "reserve": 0, "offcampus": 0,
     "noise": "Moderate between classes", "seating": "Hallway tables, computer lab",
     "hours": "Check GSU building hours",
     "eats": "Nothing confirmed inside. Downtown eateries are a short walk away.",
     "blurb": "Classroom building with a ground-floor computer lab and spots to sit between classes.",
     "site": GSU},
    {"id": 5, "name": "Student Center", "location": "55 Gilmer St SE", "kind": "Student life",
     "wifi": 1, "outlets": 1, "quiet": 0, "groups": 1, "food": 1, "reserve": 0, "offcampus": 0,
     "noise": "Lively", "seating": "Lounge seating and tables",
     "hours": "Check GSU Student Center",
     "eats": "Campus dining and a bookstore (Panther Dining). Check which spots are open.",
     "blurb": "A busy hub with food, lounges, and tables. Better for casual group work than deep focus.",
     "site": SC},
    {"id": 6, "name": "Starbucks and Saxbys on campus", "location": "Around the library area", "kind": "Cafe",
     "wifi": 1, "outlets": 0, "quiet": 0, "groups": 1, "food": 1, "reserve": 0, "offcampus": 0,
     "noise": "Busy, background chatter", "seating": "Cafe tables",
     "hours": "Check each shop",
     "eats": "Coffee, tea, and pastries.",
     "blurb": "Coffee shops students use for studying. They get crowded at peak hours.",
     "site": GSU},
    {"id": 7, "name": "Anatolia Cafe and Hookah Lounge", "location": "Off campus, downtown Atlanta", "kind": "Off-campus cafe",
     "wifi": 1, "outlets": 0, "quiet": 0, "groups": 1, "food": 1, "reserve": 0, "offcampus": 1,
     "noise": "Relaxed", "seating": "Lounge seating and tables",
     "hours": "Check before going",
     "eats": "Cafe drinks and food, plus hookah. Check the menu.",
     "blurb": "Recommended by GSU student writers as an alternative to the library.",
     "site": MAPS + "Anatolia+Cafe+Atlanta"},
    {"id": 8, "name": "Café Lucia", "location": "Downtown, near GSU", "kind": "Off-campus cafe",
     "wifi": 0, "outlets": 0, "quiet": 0, "groups": 1, "food": 1, "reserve": 0, "offcampus": 1,
     "noise": "Laid-back, jazz in the background", "seating": "Cafe tables",
     "hours": "Not verified",
     "eats": "Breakfast, coffee, and light meals.",
     "blurb": "A cozy cafe students recommend for morning study sessions. Amenities are not verified.",
     "site": MAPS + "Cafe+Lucia+Atlanta"},
    {"id": 9, "name": "Marlee’s Coffee & Tea House", "location": "Past Grady Hospital", "kind": "Off-campus cafe",
     "wifi": 0, "outlets": 0, "quiet": 0, "groups": 1, "food": 1, "reserve": 0, "offcampus": 1,
     "noise": "Not verified", "seating": "Cafe tables",
     "hours": "Not verified",
     "eats": "Coffee and tea.",
     "blurb": "A short walk from campus past Grady Hospital. Campus newspaper writers list it as a coffee stop. Amenities are not verified.",
     "site": MAPS + "Marlee%27s+Coffee+and+Tea+House+Atlanta"},
    {"id": 10, "name": "Atlanta-Fulton Central Library", "location": "1 Margaret Mitchell Sq NW", "kind": "Public library",
     "wifi": 1, "outlets": 0, "quiet": 1, "groups": 0, "food": 0, "reserve": 0, "offcampus": 1,
     "noise": "Quiet reading areas", "seating": "Tables and reading rooms",
     "hours": "Not verified",
     "eats": "No cafe confirmed. Eat before you go.",
     "blurb": "A free public library in downtown Atlanta that anyone can use. Wi-Fi and quiet are typical for public libraries but not verified here.",
     "site": MAPS + "Atlanta-Fulton+Central+Library"},
]

SAMPLE_REVIEWS = [
    {"space_id": 1, "author": "Maya T.", "rating": 5, "text": "Fifth floor is the quietest spot I’ve found on campus.", "flagged": False},
    {"space_id": 1, "author": "Devon R.", "rating": 4, "text": "Fills up fast near finals. Book a room early.", "flagged": False},
    {"space_id": 2, "author": "Priya S.", "rating": 5, "text": "Study Commons has plenty of seats when upstairs is packed.", "flagged": False},
    {"space_id": 2, "author": "Jordan K.", "rating": 4, "text": "Great for group work, a bit loud by the entrance.", "flagged": False},
    {"space_id": 3, "author": "Alex M.", "rating": 5, "text": "Best place for group projects. Reserve ahead.", "flagged": False},
    {"space_id": 4, "author": "Chris L.", "rating": 3, "text": "Fine for a quick session, can get crowded between classes.", "flagged": False},
    {"space_id": 5, "author": "Sam W.", "rating": 4, "text": "Great for meeting up and grabbing food between classes.", "flagged": False},
    {"space_id": 6, "author": "Nia B.", "rating": 4, "text": "Good coffee, but outlets are hard to find.", "flagged": False},
]


# ---------- review storage ----------
def load_reviews():
    if os.path.exists(REVIEW_FILE):
        with open(REVIEW_FILE, encoding="utf-8") as f:
            return json.load(f)
    return [dict(r) for r in SAMPLE_REVIEWS]


def save_reviews(reviews):
    with open(REVIEW_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)


# ---------- helpers ----------
def stars(n):
    n = round(n)
    return "★" * n + "☆" * (5 - n)


def space_reviews(reviews, space_id):
    return [r for r in reviews if r["space_id"] == space_id]


def average(reviews, space_id):
    rs = space_reviews(reviews, space_id)
    return sum(r["rating"] for r in rs) / len(rs) if rs else 0.0


def search(query="", active_flags=(), sort="rating", reviews=None):
    """Return spaces matching the search text AND every active flag."""
    reviews = reviews if reviews is not None else load_reviews()
    q = query.lower().strip()
    results = []
    for s in SPACES:
        text = " ".join([s["name"], s["location"], s["kind"], s["blurb"], s["noise"]]).lower()
        if q in text and all(s[f] for f in active_flags):
            results.append(s)
    if sort == "name":
        results.sort(key=lambda s: s["name"])
    elif sort == "reviews":
        results.sort(key=lambda s: -len(space_reviews(reviews, s["id"])))
    else:
        results.sort(key=lambda s: -average(reviews, s["id"]))
    return results


def tags(space):
    return ", ".join(label for key, label in FLAGS.items() if space[key])


# ---------- screens ----------
def show_list(spaces, reviews):
    print(f"\n{len(spaces)} of {len(SPACES)} spaces")
    print("-" * 60)
    for s in spaces:
        n = len(space_reviews(reviews, s["id"]))
        rating = f"{stars(average(reviews, s['id']))} {average(reviews, s['id']):.1f} ({n})" if n else "No reviews yet"
        print(f"[{s['id']:>2}] {s['name']}")
        print(f"     {s['kind']} · {s['location']}")
        print(f"     {rating}")
        print(f"     {tags(s)}")
    if not spaces:
        print("No spaces match. Clear a filter or change your search.")


def show_detail(space, reviews, is_admin):
    print("\n" + "=" * 60)
    print(space["name"])
    print(f"{space['kind']} · {space['location']}")
    print("=" * 60)
    print(space["blurb"])
    print(f"\nNoise:           {space['noise']}")
    print(f"Seating:         {space['seating']}")
    print(f"Hours/booking:   {space['hours']}")
    print(f"Food and drinks: {space['eats']}")
    print(f"Owner:           {'Not owned by GSU' if space['offcampus'] else 'GSU'}")
    print(f"Closing time:    Not verified. Check {space['site']}")
    if space["reserve"]:
        print(f"Need a room?     Reserve at {ROOMS} (up to 21 days ahead)")
    print(f"Features:        {tags(space)}")
    rs = space_reviews(reviews, space["id"])
    print(f"\nReviews ({len(rs)})")
    print("-" * 60)
    if not rs:
        print("No reviews yet. Be the first to add one.")
    for i, r in enumerate(rs, 1):
        flag = "  [FLAGGED]" if r["flagged"] else ""
        print(f"{i}. {stars(r['rating'])} {r['author']}{flag}")
        print(f"   {r['text']}")


def show_hours():
    print("\nWHEN DOES EVERYTHING CLOSE?")
    print("Closing times are not verified and change by semester, holiday, and exam week.")
    print("Check each link for today’s hours before you go.\n")
    for s in SPACES:
        print(f"{s['name']} ({'Not GSU' if s['offcampus'] else 'GSU'})")
        print(f"   Food and drinks: {s['eats']}")
        print(f"   Check hours:     {s['site']}")


def ask(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return "q"


def add_review(space, reviews):
    author = ask("Your name or initials: ")[:30]
    try:
        rating = int(ask("Rating (1-5): "))
    except ValueError:
        rating = 0
    text = ask("Your review: ")[:400]
    if not author or not text or not 1 <= rating <= 5:
        print("Add your name, a rating from 1 to 5, and a review.")
        return
    reviews.append({"space_id": space["id"], "author": author, "rating": rating, "text": text, "flagged": False})
    save_reviews(reviews)
    print("Review posted.")


def pick_review(space, reviews, action):
    rs = space_reviews(reviews, space["id"])
    if not rs:
        print("No reviews here.")
        return None
    try:
        idx = int(ask(f"Which review number to {action}? ")) - 1
        return rs[idx] if 0 <= idx < len(rs) else None
    except ValueError:
        return None


def space_menu(space, reviews, is_admin):
    while True:
        show_detail(space, reviews, is_admin)
        options = "[A]dd review  [R]eport review  "
        if is_admin:
            options += "[X] Remove review  "
        options += "[B]ack"
        choice = ask(f"\n{options}: ").lower()
        if choice == "a":
            add_review(space, reviews)
        elif choice == "r":
            r = pick_review(space, reviews, "report")
            if r:
                r["flagged"] = True
                save_reviews(reviews)
                print("Review reported. An admin will take a look.")
        elif choice == "x" and is_admin:
            r = pick_review(space, reviews, "remove")
            if r:
                reviews.remove(r)
                save_reviews(reviews)
                print("Review removed.")
        elif choice in ("b", "q", ""):
            return


def admin_panel(reviews):
    flagged = [r for r in reviews if r["flagged"]]
    print(f"\nREPORTED REVIEWS ({len(flagged)})")
    for i, r in enumerate(flagged, 1):
        name = next(s["name"] for s in SPACES if s["id"] == r["space_id"])
        print(f"{i}. {name} · {stars(r['rating'])} {r['author']}\n   {r['text']}")
    if flagged:
        pick = ask("Number to remove (Enter to skip): ")
        if pick.isdigit() and 1 <= int(pick) <= len(flagged):
            reviews.remove(flagged[int(pick) - 1])
            save_reviews(reviews)
            print("Review removed.")


def choose_filters():
    print("\nFilters:")
    keys = list(FLAGS)
    for i, k in enumerate(keys, 1):
        print(f"  {i}. {FLAGS[k]}")
    raw = ask("Numbers separated by commas (Enter for none): ")
    chosen = []
    for part in raw.split(","):
        if part.strip().isdigit() and 1 <= int(part) <= len(keys):
            chosen.append(keys[int(part) - 1])
    return chosen


def main():
    reviews = load_reviews()
    query, active, sort, is_admin = "", [], "rating", False
    print("GSU STUDY SPACES")
    while True:
        results = search(query, active, sort, reviews)
        show_list(results, reviews)
        print(f"\nSearch: '{query}'  Filters: {', '.join(FLAGS[f] for f in active) or 'none'}  Sort: {sort}")
        print("[#] open a space  [S]earch  [F]ilters  [O]rder  [H]ours/closing times  "
              f"[L]ogin as admin{' (logged in)' if is_admin else ''}  [M]oderate  [Q]uit")
        choice = ask("> ").lower()
        if choice.isdigit():
            match = next((s for s in SPACES if s["id"] == int(choice)), None)
            if match:
                space_menu(match, reviews, is_admin)
            else:
                print("No space with that number.")
        elif choice == "s":
            query = ask("Search by name, building, or feature: ")
        elif choice == "f":
            active = choose_filters()
        elif choice == "o":
            sort = {"1": "rating", "2": "name", "3": "reviews"}.get(
                ask("1 = Highest rated, 2 = Name, 3 = Most reviewed: "), sort)
        elif choice == "h":
            show_hours()
        elif choice == "l":
            if ask("Admin password: ") == ADMIN_PASSWORD:
                is_admin = True
                print("Logged in as admin.")
            else:
                print("Wrong password.")
        elif choice == "m":
            if is_admin:
                admin_panel(reviews)
            else:
                print("Log in as admin first.")
        elif choice == "q":
            print("Bye.")
            return


if __name__ == "__main__":
    main()
