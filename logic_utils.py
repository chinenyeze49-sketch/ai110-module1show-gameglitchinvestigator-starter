def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """
    Get the valid number range for a given difficulty level.

    This function returns the minimum and maximum bounds (inclusive) for the
    secret number based on the selected game difficulty. Difficulty directly
    impacts both the search space and the challenge of the guessing game.

    Args:
        difficulty: The difficulty level as a string.
            Valid values: "Easy", "Normal", "Hard".

    Returns:
        A tuple of (low, high) inclusive bounds for secret number generation.
        - Easy: 1-20 (smaller range, easier guessing)
        - Normal: 1-100 (standard range)
        - Hard: 1-50 (moderate range, harder than Normal)
        - Default (invalid input): 1-100

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Normal")
        (1, 100)
        >>> get_range_for_difficulty("Hard")
        (1, 50)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """
    Parse and validate user input into an integer guess.

    Converts raw string input from the user into a validated integer value.
    Handles None/empty input and non-numeric text with descriptive error
    messages. Supports decimal input by converting to int via truncation.

    Args:
        raw: The raw string input from the user. Can be an integer string,
            decimal string (e.g., "3.7"), or invalid input.

    Returns:
        A tuple of (ok, guess_int, error_message) where:
        - ok (bool): True if parsing succeeded, False if validation failed.
        - guess_int (int | None): The parsed integer, or None if parsing failed.
        - error_message (str | None): Descriptive error message, or None if success.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("3.7")
        (True, 3, None)
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
        >>> parse_guess("hello")
        (False, None, 'That is not a number.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """
    Compare player guess to secret number and provide feedback.

    Evaluates the player's guess against the secret number and returns
    an outcome classification and a formatted hint message with emoji.
    This is the core game logic for determining correctness and direction.

    Args:
        guess: The player's guessed integer value.
        secret: The target secret integer to match.

    Returns:
        A tuple of (outcome, message) where:
        - outcome (str): "Win", "Too High", or "Too Low" describing the result.
        - message (str): A formatted hint message with emoji:
            * "🎉 Correct!" for a winning guess
            * "📉 Go LOWER!" if guess is too high
            * "📈 Go HIGHER!" if guess is too low

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(60, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(40, 50)
        ('Too Low', '📈 Go HIGHER!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Calculate updated player score based on game outcome and attempt number.

    Applies score adjustments based on the guess outcome and attempt count.
    Higher rewards are given for winning with fewer attempts. Penalties vary
    by outcome type, and even attempts on "Too High" outcomes grant bonuses.

    Scoring Rules:
        - Win: 100 - 10*(attempt_number+1) points, minimum 10 points
        - Too High: +5 on even attempts, -5 on odd attempts
        - Too Low: -5 points (no attempt-based variation)
        - Other: No change to score

    Args:
        current_score: The player's current accumulated score.
        outcome: The result classification from check_guess().
            Expected values: "Win", "Too High", "Too Low".
        attempt_number: The current attempt number (1-indexed).

    Returns:
        The updated score after applying outcome-based adjustments.

    Examples:
        >>> update_score(0, "Win", 5)
        45
        >>> update_score(50, "Too High", 2)
        55
        >>> update_score(50, "Too High", 1)
        45
        >>> update_score(50, "Too Low", 1)
        45
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
