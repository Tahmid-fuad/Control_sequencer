import re

# --- Opcode nibbles (4-bit opcodes) ---
OP_NIB = {
    "LDA": 0x1, "LDB": 0x2, "OUT": 0x3, "SUB": 0x4,
    "HLT": 0x5,  # single-op
    "LDI": 0x6,  # loads 10-bit literal from next line
    "STA": 0x7, "CMP": 0x8, "JMP": 0x9,
    "JNZ": 0xA, "JNC": 0xB, "SFT": 0xC, "RTE": 0xD,
}

PACKED_OPS = {"LDA", "LDB", "OUT", "SUB", "STA", "CMP",
              "JMP", "JNZ", "JNC", "SFT", "RTE"}
SINGLE_OPS = {"HLT"}
IMMEDIATE_OPS = {"LDI"}

# -------------------------------------------------------------
# Numeric parser with suffix enforcement
# -------------------------------------------------------------

def parse_with_suffix(token: str, bit_limit: int, label: str) -> int:
    """Parse number with suffix b/d/h, validate within bit_limit."""
    tok = token.strip().lower()

    # Validate suffix
    if not re.fullmatch(r"[0-9a-f]+[bdh]", tok):
        raise ValueError(
            f"Invalid {label} '{token}': must end with b, d, or h "
            f"(binary/decimal/hex). Example: 1011b, 11d, 0ah"
        )

    val_str, suffix = tok[:-1], tok[-1]

    try:
        if suffix == "b":
            val = int(val_str, 2)
        elif suffix == "d":
            val = int(val_str, 10)
        elif suffix == "h":
            val = int(val_str, 16)
    except ValueError:
        raise ValueError(f"Bad numeric format in '{token}'")

    # Range check
    if not (0 <= val < (1 << bit_limit)):
        raise ValueError(
            f"{label} '{token}' out of range for {bit_limit}-bit value (0..{(1<<bit_limit)-1})"
        )

    return val

# -------------------------------------------------------------
# Core encoding helpers
# -------------------------------------------------------------

def encode_word(op_nib: int, operand6: int) -> str:
    """Encode opcode nibble + 6-bit operand into 3-hex-digit (10-bit) word."""
    if not (0 <= op_nib <= 0xF):
        raise ValueError(f"Opcode nibble out of range: {op_nib}")
    if not (0 <= operand6 <= 0x3F):
        raise ValueError(f"Operand out of range (0..63): {operand6}")
    val10 = (op_nib << 6) | operand6
    return f"{val10:03x}"

# -------------------------------------------------------------

input_file = "input.txt"
output_file = "output"

with open(input_file, "r", encoding="utf-8") as f:
    raw_lines = f.readlines()

bytes_out = []
i = 0

def get_next_nonempty_line():
    """Get next non-empty token, injecting 000 for all blank lines."""
    global i
    while i < len(raw_lines):
        nxt = raw_lines[i].strip()
        i += 1
        if nxt == "":
            bytes_out.append("000")
            continue
        return nxt
    raise ValueError("Missing literal after LDI")

# -------------------------------------------------------------
# Assembler loop
# -------------------------------------------------------------

while i < len(raw_lines):
    line = raw_lines[i].strip()
    i += 1

    # Blank line → insert 000
    if not line:
        bytes_out.append("000")
        continue

    parts = line.split()
    up0 = parts[0].upper()

    # --- Literal 10-bit data word ---
    if len(parts) == 1 and up0 not in OP_NIB:
        try:
            val10 = parse_with_suffix(parts[0], 10, "literal value")
            bytes_out.append(f"{val10:03x}")
            continue
        except ValueError as e:
            raise ValueError(f"Line {i}: {e}")

    # --- Packed ops ---
    if up0 in PACKED_OPS:
        if len(parts) < 2:
            raise ValueError(f"Missing operand for {up0}")

        operand_token = parts[1].strip().lower()

        # Special rule for SFT / RTE → still 6-bit operand with suffix
        operand_val = parse_with_suffix(operand_token, 6, f"{up0} operand")

        bytes_out.append(encode_word(OP_NIB[up0], operand_val))
        continue

    # --- Single ops ---
    if up0 in SINGLE_OPS:
        bytes_out.append(encode_word(OP_NIB[up0], 0))
        continue

    # --- LDI (next line is a 10-bit literal) ---
    if up0 in IMMEDIATE_OPS:
        bytes_out.append(encode_word(OP_NIB[up0], 0))  # operand unused
        literal_line = get_next_nonempty_line()
        lit_val = parse_with_suffix(literal_line, 10, "LDI literal")
        bytes_out.append(f"{lit_val:03x}")
        continue

    raise ValueError(f"Unrecognized opcode or token: '{line}'")

# -------------------------------------------------------------
# Output file
# -------------------------------------------------------------
out_lines = ["v3.0 hex words addressed", f"0: {' '.join(bytes_out)}"]
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
