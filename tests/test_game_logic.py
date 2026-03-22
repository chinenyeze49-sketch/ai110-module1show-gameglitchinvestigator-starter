from logic_utils import check_guess, parse_guess

# ============================================================================
# Basic check_guess tests
# ============================================================================

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"


# ============================================================================
# Edge case: Negative numbers
# ============================================================================

def test_check_guess_negative_guess():
    """Negative guess compared to positive secret."""
    result = check_guess(-5, 50)
    assert result == ("Too Low", "📈 Go HIGHER!")

def test_check_guess_negative_secret():
    """Negative secret compared to positive guess."""
    result = check_guess(5, -50)
    assert result == ("Too High", "📉 Go LOWER!")

def test_check_guess_both_negative():
    """Both guess and secret are negative."""
    result = check_guess(-30, -50)
    assert result == ("Too High", "📉 Go LOWER!")

def test_check_guess_negative_equal():
    """Negative guess equals negative secret."""
    result = check_guess(-42, -42)
    assert result == ("Win", "🎉 Correct!")

def test_parse_guess_negative():
    """Parsing a negative number."""
    ok, guess, err = parse_guess("-5")
    assert ok is True
    assert guess == -5
    assert err is None

def test_parse_guess_negative_decimal():
    """Parsing a negative decimal (e.g., -3.7)."""
    ok, guess, err = parse_guess("-3.7")
    assert ok is True
    assert guess == -3  # Should truncate to int
    assert err is None


# ============================================================================
# Edge case: Decimal numbers
# ============================================================================

def test_parse_guess_decimal_truncates():
    """Decimal numbers should be converted to int by truncation."""
    ok, guess, err = parse_guess("3.7")
    assert ok is True
    assert guess == 3
    assert err is None

def test_parse_guess_decimal_rounds_down():
    """Decimal 9.99 should truncate to 9."""
    ok, guess, err = parse_guess("9.99")
    assert ok is True
    assert guess == 9
    assert err is None

def test_parse_guess_decimal_zero_point():
    """Decimal like 0.5 should truncate to 0."""
    ok, guess, err = parse_guess("0.5")
    assert ok is True
    assert guess == 0
    assert err is None

def test_parse_guess_decimal_negative():
    """Negative decimal should truncate correctly."""
    ok, guess, err = parse_guess("-2.8")
    assert ok is True
    assert guess == -2
    assert err is None

def test_check_guess_with_decimal_converted():
    """Check guess with a decimal that was parsed."""
    ok, guess, err = parse_guess("50.9")
    assert ok is True
    result = check_guess(guess, 50)
    assert result == ("Win", "🎉 Correct!")  # 50.9 truncates to 50


# ============================================================================
# Edge case: Extremely large numbers
# ============================================================================

def test_parse_guess_extremely_large():
    """Parsing very large numbers."""
    ok, guess, err = parse_guess("99999")
    assert ok is True
    assert guess == 99999
    assert err is None

def test_parse_guess_extremely_large_decimal():
    """Parsing very large decimal numbers."""
    ok, guess, err = parse_guess("99999.99")
    assert ok is True
    assert guess == 99999
    assert err is None

def test_check_guess_extremely_large_guess():
    """Guess is extremely large compared to secret."""
    result = check_guess(999999, 50)
    assert result == ("Too High", "📉 Go LOWER!")

def test_check_guess_extremely_large_secret():
    """Secret is extremely large compared to guess."""
    result = check_guess(50, 999999)
    assert result == ("Too Low", "📈 Go HIGHER!")

def test_check_guess_both_extremely_large():
    """Both guess and secret are extremely large."""
    result = check_guess(999999, 999999)
    assert result == ("Win", "🎉 Correct!")


# ============================================================================
# Edge case: Empty and None input
# ============================================================================

def test_parse_guess_empty_string():
    """Empty string input should return error."""
    ok, guess, err = parse_guess("")
    assert ok is False
    assert guess is None
    assert err == "Enter a guess."

def test_parse_guess_none_input():
    """None input should return error."""
    ok, guess, err = parse_guess(None)
    assert ok is False
    assert guess is None
    assert err == "Enter a guess."

def test_parse_guess_whitespace_only():
    """Whitespace-only input should return error."""
    ok, guess, err = parse_guess("   ")
    assert ok is False
    assert guess is None
    assert err == "That is not a number."


# ============================================================================
# Edge case: Text input instead of numbers
# ============================================================================

def test_parse_guess_alphabetic():
    """Pure alphabetic text should return error."""
    ok, guess, err = parse_guess("hello")
    assert ok is False
    assert guess is None
    assert err == "That is not a number."

def test_parse_guess_mixed_alphanumeric():
    """Mixed text and numbers should return error."""
    ok, guess, err = parse_guess("12abc")
    assert ok is False
    assert guess is None
    assert err == "That is not a number."

def test_parse_guess_special_characters():
    """Special characters should return error."""
    ok, guess, err = parse_guess("!@#$%")
    assert ok is False
    assert guess is None
    assert err == "That is not a number."

def test_parse_guess_text_with_decimal():
    """Text with a decimal point should return error."""
    ok, guess, err = parse_guess("12.34.56")
    assert ok is False
    assert guess is None
    assert err == "That is not a number."

def test_parse_guess_scientific_notation():
    """Scientific notation should return error."""
    ok, guess, err = parse_guess("1e5")
    assert ok is False
    assert guess is None
    assert err == "That is not a number."
