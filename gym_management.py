# ============================================================
#  BIT Gym Membership Management System
#  PRG1406 — Advanced Programming (Python and C)
#  Group Assignment 1 — May 2026
# ============================================================


# ─────────────────────────────────────────────────────────────
#  PART 2 & 3 & 4 — Classes with Inheritance, Magic Methods,
#                    and Decorators
# ─────────────────────────────────────────────────────────────

class Member:
    """
    PARENT CLASS — represents a standard gym member.
    Demonstrates: __str__, __eq__, __len__ (Part 3)
    and @staticmethod, @classmethod (Part 4).
    """

    total_members = 0  # class variable — shared across all instances

    def __init__(self, name: str, age: int, weight: float,
                 height: float, is_active: bool):
        self.name = name
        self.age = age
        self.weight = weight      # kg
        self.height = height      # metres
        self.is_active = is_active
        Member.total_members += 1

    # ── PART 3: Magic Methods ────────────────────────────────

    def __str__(self) -> str:
        """Controls what print(member) displays."""
        status = "Active" if self.is_active else "Inactive"
        bmi = Member.calculate_bmi(self.weight, self.height)
        return (f"[Member] {self.name} | Age: {self.age} | "
                f"BMI: {bmi:.2f} | Status: {status}")

    def __eq__(self, other) -> bool:
        """Two members are equal if they share the same name (case-insensitive)."""
        if isinstance(other, Member):
            return self.name.lower() == other.name.lower()
        return False

    def __len__(self) -> int:
        """Returns the member's age as the 'record length'."""
        return self.age

    # ── PART 4: Decorators ───────────────────────────────────

    @staticmethod
    def calculate_bmi(weight: float, height: float) -> float:
        """
        @staticmethod — belongs to the class, not an instance.
        No 'self' or 'cls' needed. Called as Member.calculate_bmi(w, h).
        """
        return weight / (height ** 2)

    @classmethod
    def get_total_members(cls) -> int:
        """
        @classmethod — receives the class itself as first argument.
        Used to access class-level data (total_members counter).
        """
        return cls.total_members

    # ── Display ──────────────────────────────────────────────

    def display_info(self) -> None:
        bmi = Member.calculate_bmi(self.weight, self.height)
        status = "Active" if self.is_active else "Inactive"
        print(f"\n{'─'*46}")
        print(f"  Name    : {self.name}")
        print(f"  Age     : {self.age} years")
        print(f"  Weight  : {self.weight:.1f} kg")
        print(f"  Height  : {self.height:.2f} m")
        print(f"  BMI     : {bmi:.2f}")
        print(f"  Status  : {status}")
        print(f"{'─'*46}")


class PremiumMember(Member):
    """
    CHILD CLASS — PremiumMember IS A Member with added perks.
    Demonstrates: super().__init__(), new attributes/methods (Part 2),
    and @property decorator (Part 4).
    """

    def __init__(self, name: str, age: int, weight: float,
                 height: float, is_active: bool,
                 trainer_name: str, monthly_fee: float,
                 sessions_per_week: int):
        # ── Call the parent constructor (Part 2) ──
        super().__init__(name, age, weight, height, is_active)

        # ── New attributes specific to PremiumMember ──
        self.trainer_name = trainer_name
        self.monthly_fee = monthly_fee            # float
        self.sessions_per_week = sessions_per_week  # int

    # ── PART 4: @property Decorator ─────────────────────────

    @property
    def yearly_cost(self) -> float:
        """
        @property — accessed like an attribute, not a method.
        Computes yearly_cost dynamically from monthly_fee.
        Usage: premium.yearly_cost   (no parentheses needed)
        """
        return self.monthly_fee * 12

    # ── PART 3: Override Magic Methods ──────────────────────

    def __str__(self) -> str:
        base = super().__str__().replace("[Member]", "[Premium]")
        return (f"{base}\n          Trainer: {self.trainer_name} | "
                f"Fee: ${self.monthly_fee:.2f}/mo | "
                f"Sessions: {self.sessions_per_week}x/week")

    def __len__(self) -> int:
        """For a PremiumMember, 'length' = weekly sessions."""
        return self.sessions_per_week

    # ── Display ──────────────────────────────────────────────

    def display_premium_info(self) -> None:
        self.display_info()

        # ── PART 1: Arithmetic expressions ──────────────────
        yearly           = self.yearly_cost                            # expression 1
        weekly_calories  = 450 * self.sessions_per_week                # expression 2
        cost_per_session = self.monthly_fee / (self.sessions_per_week * 4) if self.sessions_per_week > 0 else 0  # expression 3

        print(f"  Trainer         : {self.trainer_name}")
        print(f"  Monthly Fee     : ${self.monthly_fee:.2f}")
        print(f"  Yearly Cost     : ${yearly:.2f}")
        print(f"  Cost/Session    : ${cost_per_session:.2f}")
        print(f"  Sessions/Week   : {self.sessions_per_week}")
        print(f"  Est. Weekly Cal : {weekly_calories} kcal burned")
        print(f"{'─'*46}\n")


# ─────────────────────────────────────────────────────────────
#  PART 1 — Input helpers with validation (while + try/except)
# ─────────────────────────────────────────────────────────────

def get_int(prompt: str, min_val: int = 1) -> int:
    """Validated integer input — re-prompts on bad input, never crashes."""
    while True:
        try:
            value = int(input(prompt))
            if value < min_val:
                print(f"  Value must be at least {min_val}.")
                continue
            return value
        except ValueError:
            print("  Please enter a whole number (e.g. 25).")


def get_float(prompt: str, min_val: float = 0.01) -> float:
    """Validated float input — re-prompts on bad input, never crashes."""
    while True:
        try:
            value = float(input(prompt))
            if value < min_val:
                print(f"  Value must be greater than {min_val}.")
                continue
            return value
        except ValueError:
            print("  Please enter a valid decimal number (e.g. 70.5).")


def get_str(prompt: str) -> str:
    """Validated string input — re-prompts if the user leaves it empty."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty.")


# ─────────────────────────────────────────────────────────────
#  Main Program
# ─────────────────────────────────────────────────────────────

def main():
    print("\n" + "=" * 52)
    print("   BIT GYM MEMBERSHIP MANAGEMENT SYSTEM")
    print("   PRG1406 -- Group Assignment 1")
    print("=" * 52)

    # ── Register a Regular Member ────────────────────────────
    print("\n  REGISTER REGULAR MEMBER")
    name1      = get_str("  Full name           : ")
    age1       = get_int("  Age (years)         : ")
    weight1    = get_float("  Weight (kg)         : ")
    height1    = get_float("  Height (m, e.g 1.75): ", min_val=0.5)
    # PART 1: correct boolean — NOT bool(input(...))
    is_active1: bool = input("  Active member? (yes/no): ").strip().lower() == "yes"

    member1 = Member(name1, age1, weight1, height1, is_active1)

    # ── Register a Premium Member ────────────────────────────
    print("\n  REGISTER PREMIUM MEMBER")
    name2      = get_str("  Full name           : ")
    age2       = get_int("  Age (years)         : ")
    weight2    = get_float("  Weight (kg)         : ")
    height2    = get_float("  Height (m, e.g 1.80): ", min_val=0.5)
    is_active2: bool = input("  Active member? (yes/no): ").strip().lower() == "yes"
    trainer    = get_str("  Trainer's name      : ")
    fee        = get_float("  Monthly fee ($)     : ")
    sessions   = get_int("  Sessions per week   : ")

    premium1 = PremiumMember(name2, age2, weight2, height2,
                             is_active2, trainer, fee, sessions)

    # ── Arithmetic expressions (Part 1) ─────────────────────
    bmi1            = Member.calculate_bmi(weight1, height1)
    bmi2            = Member.calculate_bmi(weight2, height2)
    total_yearly    = premium1.yearly_cost
    weekly_calories = 450 * sessions

    # ── Summary Screen (Part 1 — f-strings everywhere) ──────
    print("\n\n" + "=" * 52)
    print("         MEMBERSHIP SUMMARY REPORT")
    print("=" * 52)

    print(f"\n  Total members registered : {Member.get_total_members()}")

    print(f"\n  REGULAR MEMBER — {name1.upper()}")
    member1.display_info()
    print(f"  BMI {bmi1:.2f} is classified as: ", end="")
    if   bmi1 < 18.5: print("Underweight")
    elif bmi1 < 25.0: print("Normal weight")
    elif bmi1 < 30.0: print("Overweight")
    else:             print("Obese")

    print(f"\n  PREMIUM MEMBER — {name2.upper()}")
    premium1.display_premium_info()

    # ── Magic Methods Demo ───────────────────────────────────
    print("  MAGIC METHODS DEMO (Part 3)")
    print(f"  print(member1)       -> {member1}")
    print(f"  print(premium1)      -> {premium1}")
    print(f"  len(member1)         -> {len(member1)}  (age in years)")
    print(f"  len(premium1)        -> {len(premium1)}  (sessions per week)")
    print(f"  member1 == premium1  -> {member1 == premium1}")

    # ── Decorators Demo ──────────────────────────────────────
    print(f"\n  DECORATORS DEMO (Part 4)")
    print(f"  @staticmethod  Member.calculate_bmi({weight2}, {height2}) = {Member.calculate_bmi(weight2, height2):.2f}")
    print(f"  @classmethod   Member.get_total_members()                 = {Member.get_total_members()}")
    print(f"  @property      premium1.yearly_cost                       = ${premium1.yearly_cost:.2f}")

    # ── Final Summary ────────────────────────────────────────
    print(f"\n  {'='*48}")
    print(f"  {name1} is a regular member with a BMI of {bmi1:.2f}.")
    print(f"  {name2} is a premium member. Annual investment: ${total_yearly:.2f}.")
    print(f"  {name2} burns approximately {weekly_calories} kcal per week.")
    print(f"  {'='*48}")
    print("  Program completed successfully. No errors.\n")


if __name__ == "__main__":
    main()
