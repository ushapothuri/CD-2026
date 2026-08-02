# Lab Practice 5 - Generating MIPS Assembly from Three-Address Code

This lab exercise demonstrates how to convert **Three-Address Code (TAC) in Triple Representation into MIPS assembly instructions**.

The triples are used as the input to a simple **code generator** that produces MIPS assembly statements.

---
# 1. Basic MIPS Instructions Used

The code generator uses a small subset of MIPS instructions.

### Load a value

```asm
lw $t0, <memoryaddress>
```

Loads a value from memory into a register.

### Load an immediate value

```asm
li $t0, 10
```

Loads a constant directly into a register.

### Addition

```asm
add $t2, $t0, $t1
```

Equivalent to:

```text
t2 = t0 + t1
```

### Subtraction

```asm
sub $t2, $t0, $t1
```

Equivalent to:

```text
t2 = t0 - t1
```

### Multiplication

```asm
mul $t2, $t0, $t1
```

Equivalent to:

```text
t2 = t0 * t1
```

### Division

```asm
div $t2, $t0, $t1
```

### Store a value

```asm
sw $t2, <memoryaddress>
```

Stores a register value into memory.

---


# 2. Simple Register Allocation

The code generator uses the temporary registers:

```text
$t0  $t1  $t2  ...  $t9
```

Initially, all ten registers are considered available.

When a value is needed:

```text
allocate a free register
        ↓
load the value
        ↓
perform the operation
```

When a register is no longer needed, it is made available again.

This is a **simple register allocation strategy** intended for learning purposes.

It is not a complete register allocator used in production compilers.

---

# 3. Register Allocation Example

Consider:

```text
(0) * b, c
```

The generator may allocate:

```text
b → $t0
c → $t1
```

and generate:

```asm
lw $t0, ...
lw $t1, ...
mul $t2, $t0, $t1
```

The result of triple `(0)` is now available in:

```text
$t2
```

The generator records this association:

```text
Triple 0 → $t2
```

Therefore, when a later triple refers to:

```text
(0)
```

the generator knows that the value is currently in `$t2`.

---

# 4. Triple References and Registers

This is an important connection between the previous lab and this lab.

Suppose the triples are:

```text
(0) * b, c
(1) + a, (0)
(2) x = (1)
```

After generating triple `(0)`:

```text
(0) → $t2
```

When generating triple `(1)`, the reference:

```text
(0)
```

is resolved to:

```text
$t2
```

Therefore, the generator can produce something conceptually like:

```asm
lw  $t0, ...
lw  $t1, ...
mul $t2, $t0, $t1

lw  $t0, ...
add $t3, $t0, $t2

sw  $t3, ...
```

The exact registers can vary depending on the allocation sequence.

---

# 5. Loading Variables and Constants

The generator distinguishes between **literals** and **variables**.

For a constant:

```text
5
```

it generates:

```asm
li $t0, 5
```

For a variable:

```text
a
```

it generates a load instruction:

```asm
lw $t0, <address-of-a>
```

Thus:

```text
5
```

and

```text
a
```

are handled differently.

---

# 6. Memory Addressing and Frame Pointer

At this stage, the code generator uses a placeholder representation:

```text
disp($fp)ofx
```

for the location of a variable such as `x`.

This should be understood as a **teaching placeholder**, not as actual MIPS assembly syntax.

The intended future representation is a frame-pointer-relative address such as:

```asm
lw $t0, 4($fp)
```

or:

```asm
sw $t1, 8($fp)
```

where the offset is determined by the compiler's **activation record / stack-frame layout**.

For example, a future symbol-table mapping could be:

```text
Variable       Offset
----------------------
a              4($fp)
b              8($fp)
c              12($fp)
x              16($fp)
```

Then:

```text
load a
```

could generate:

```asm
lw $t0, 4($fp)
```

and:

```text
store x
```

could generate:

```asm
sw $t1, 16($fp)
```

This part is deliberately left for a later extension of the lab.

---

# 7. Complete Translation Example

Consider:

```text
x = (a + b) * (c - d)
```

## AST

```text
             =
           /   \
          x     *
               / \
              +   -
             / \ / \
            a  b c  d
```

## Three-Address Code

```text
t1 = a + b
t2 = c - d
t3 = t1 * t2
x = t3
```

## Triple Representation

```text
(0) + a, b
(1) - c, d
(2) * (0), (1)
(3) x = (2)
```

## MIPS Code Generation

The triple:

```text
(0) + a, b
```

can be translated conceptually as:

```asm
lw  $t0, <address-of-a>
lw  $t1, <address-of-b>
add $t2, $t0, $t1
```

The result of triple `(0)` is now in:

```text
$t2
```

For:

```text
(1) - c, d
```

the generator may produce:

```asm
lw  $t0, <address-of-c>
lw  $t1, <address-of-d>
sub $t3, $t0, $t1
```

Now:

```text
(0) → $t2
(1) → $t3
```

For:

```text
(2) * (0), (1)
```

the references are replaced by their currently allocated registers:

```asm
mul $t4, $t2, $t3
```

Finally:

```text
(3) x = (2)
```

stores the result:

```asm
sw $t4, <address-of-x>
```

Thus, conceptually:

```asm
lw  $t0, <address-of-a>
lw  $t1, <address-of-b>
add $t2, $t0, $t1

lw  $t0, <address-of-c>
lw  $t1, <address-of-d>
sub $t3, $t0, $t1

mul $t4, $t2, $t3

sw  $t4, <address-of-x>
```

The actual offsets will be introduced when the frame-pointer-based memory layout is implemented.

---


# 8. Register Mapping

The generator maintains a mapping between triple indices and registers.

For example:

```text
Triple Index       Register
----------------------------
(0)                $t2
(1)                $t3
(2)                $t4
```

When a later triple contains:

```text
(1)
```

the generator looks up the mapping and obtains:

```text
$t3
```

This is how the triple representation is connected to register allocation.

---

# 9. Register Reuse

Registers containing temporary operands that are no longer needed can be released and reused.

For example:

```text
load a → $t0
load b → $t1
add    → $t2
```

After the addition has been generated, `$t0` and `$t1` may no longer be needed for that operation.

They can therefore become available for subsequent instructions.

This simple approach helps demonstrate the basic idea of **register allocation and register reuse** without introducing the complex Algorithms.

---


# 10. Home Work Extension: Frame-Pointer-Based Variables

The current implementation uses a placeholder such as:

```text
disp($fp)ofvariable
```

to represent the memory location of a variable.

The next extension can introduce a symbol table such as:

```text
symbol_table = {
    "a": 4,
    "b": 8,
    "c": 12,
    "d": 16,
    "x": 20
}
```

where the values represent offsets from `$fp`.

The code generator can then produce actual instructions:

```asm
lw $t0, 4($fp)
lw $t1, 8($fp)
```

and:

```asm
sw $t2, 20($fp)
```

This provides a natural transition from simple code generation to **activation records and run-time memory organization**.

---


# 11. Key Takeaway

The important idea in this exercise is:

> **The code generator walks through the intermediate representation and translates each three-address instruction into one or more target-machine instructions.**

For example:

```text
(0) + a, b
```

becomes conceptually:

```asm
lw  $t0, <address-of-a>
lw  $t1, <address-of-b>
add $t2, $t0, $t1
```

The result of triple `(0)` is associated with `$t2`.

A later instruction:

```text
(1) * (0), c
```

can therefore use `$t2` directly as one of its operands.

Thus, the complete flow is:

```text
AST
 ↓
TAC
 ↓
Triples
 ↓
Triple → Register Mapping
 ↓
MIPS Instructions
```

This exercise provides the foundation for extending the compiler with **proper stack-frame management, register allocation, instruction selection, and eventually complete target-code generation**.
