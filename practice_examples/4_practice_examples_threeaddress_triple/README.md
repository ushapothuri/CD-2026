# Lab Practice 4 — Generating Three-Address Code in Triple Notation from AST 

This lab exercise demonstrates how an **Abstract Syntax Tree (AST)** can be traversed to generate **Three-Address Code (TAC)** and represent the generated code using **Triple Notation**.

The main objective is to understand how intermediate code can be represented more compactly using triples.

---

# 1. What is Three-Address Code?

**Three-Address Code (TAC)** is an intermediate representation used by compilers to represent computations as a sequence of simple instructions.

A TAC instruction generally contains:

* An operator
* Two operands
* A result

For example, consider:

```text
x = a + b * c
```

The expression is broken into simpler operations:

```text
t1 = b * c
t2 = a + t1
x = t2
```

Each instruction performs one simple operation.

The temporary variables `t1` and `t2` hold intermediate results.

---


# 2. Three-Address Code as Quadruples

One common representation of TAC is the **Quadruple**.

A quadruple contains four fields:

```text
(operator, argument1, argument2, result)
```

For:

```text
x = a + b * c
```

the TAC can be represented as:

| No. | Operator | Arg1 | Arg2 | Result |
| --- | -------- | ---- | ---- | ------ |
| 0   | `*`      | `b`  | `c`  | `t1`   |
| 1   | `+`      | `a`  | `t1` | `t2`   |
| 2   | `=`      | `t2` | —    | `x`    |

The corresponding quadruples are:

```text
( *, b,  c,  t1 )
( +, a,  t1, t2 )
( =, t2, —,  x  )
```

The result field explicitly stores the name of the temporary variable.

---

# 3. Why Triples?

Quadruples require a separate **result field** for every instruction.

For example:

```text
t1 = b * c
t2 = a + t1
```

requires the compiler to create and maintain temporary names such as:

```text
t1
t2
t3
...
```

For a large expression, many temporary names may be required.

**Triples avoid explicitly storing these temporary result names.**

Instead, the result of an operation is identified by the **position (index) of the triple itself**.

Thus, instead of:

```text
t1 = b * c
t2 = a + t1
```

we can refer to the result of the first operation simply as:

```text
(0)
```

because it is the result produced by triple number `0`.

---

# 4. Triple Representation

A triple generally contains three fields:

```text
(operator, argument1, argument2)
```

There is **no separate result field**.

The result is implicitly identified by the instruction number.

For:

```text
x = a + b * c
```

the triples are:

| No. | Operator | Arg1  | Arg2  |
| --- | -------- | ----- | ----- |
| 0   | `*`      | `b`   | `c`   |
| 1   | `+`      | `a`   | `(0)` |
| 2   | `=`      | `(1)` | `x`   |

Here:

```text
(0)
```

means **the result produced by triple 0**, and

```text
(1)
```

means **the result produced by triple 1**.

Therefore, the triples can be written as:

```text
0: ( *, b,    c   )
1: ( +, a,    (0) )
2: ( =, (1),  x   )
```

Notice that there is no `t1` or `t2`.

---

# 5. Quadruple vs Triple

The difference becomes clearer by comparing the two representations.

### Quadruples

```text
0: ( *, b,  c,  t1 )
1: ( +, a,  t1, t2 )
2: ( =, t2, —,  x  )
```

### Triples

```text
0: ( *, b,    c   )
1: ( +, a,    (0) )
2: ( =, (1),  x   )
```

The quadruple explicitly stores the result:

```text
result = t1
result = t2
```

The triple uses the instruction number itself as the identity of the result:

```text
result of instruction 0 → (0)
result of instruction 1 → (1)
```

Thus, triples avoid the need for explicit temporary variable names.

---


# 6. How the AST is Traversed

The program in this practice example walks through the AST and generates triples.

For an operator node:

1. Traverse the left child.
2. Traverse the right child.
3. Generate a new triple for the operator.
4. Use the index of the generated triple as the result reference.
5. Return this index to the parent node.

For example:

```text
        +
       / \
      a   *
         / \
        b   c
```

The traversal first processes:

```text
b * c
```

and creates:

```text
0: ( *, b, c )
```

The index `0` represents the result of this operation.

The parent `+` node then uses `(0)`:

```text
1: ( +, a, (0) )
```

Thus, the AST is naturally converted into triples through postorder traversal.

---

# 7. Why Are Triples Useful?

Triples have an important advantage: **they eliminate the need for explicit temporary names**.

Compare:

```text
t1 = a + b
t2 = c - d
t3 = t1 * t2
```

with:

```text
0: ( +, a,    b   )
1: ( -, c,    d   )
2: ( *, (0),  (1) )
```

The second representation does not require `t1`, `t2`, or `t3`.

This can reduce the amount of storage needed for intermediate results.

However, triples have an important consideration: **references depend on instruction positions**. If instructions are moved during optimization, references such as `(0)` and `(1)` may need to be updated.

---

# 8. Indirect Triples

A related representation is called **Indirect Triples**.

Instead of referring directly to triple positions, an additional table of pointers/references is maintained.

Conceptually:

```text
Pointer Table

0 → Triple 0
1 → Triple 1
2 → Triple 2
```

The pointer table can be rearranged during optimization without changing the actual triples.

This makes code movement and reordering easier than with ordinary triples.

For this practice exercise, the focus is on **ordinary triples**.

---

# 9. Comparison

| Feature               | Quadruples       | Triples                      |
| --------------------- | ---------------- | ---------------------------- |
| Fields                | 4                | 3                            |
| Operator              | Yes              | Yes                          |
| Operand 1             | Yes              | Yes                          |
| Operand 2             | Yes              | Yes                          |
| Separate result field | Yes              | No                           |
| Temporary variables   | Usually required | Not explicitly required      |
| Result identification | Temporary name   | Instruction index            |
| Storage               | More             | Less                         |
| Instruction movement  | Easier           | References may need updating |

---

# 10. Compilation Flow

This practice exercise can be viewed as the next step after AST construction:

```text
        Source Program
              │
              ▼
           Parsing
              │
              ▼
             AST
              │
              │ Postorder Traversal
              ▼
      Three-Address Code
              │
       ┌──────┴──────┐
       ▼             ▼
  Quadruples       Triples
       │             │
  Result = t1    Result = index
       │             │
       └──────┬──────┘
              ▼
       Intermediate Code
```

---

# 11. Practice Exercises

For each expression below:

1. Construct the AST.
2. Traverse the AST in postorder.
3. Generate Three-Address Code.
4. Represent the TAC using quadruples.
5. Convert the quadruples into triples.

### Exercise 1

```text
x = a + b * c
```

### Exercise 2

```text
y = (a + b) * (c - d)
```

### Exercise 3

```text
z = (a - b) / (c + d * e)
```

### Exercise 4

```text
result = (a + b) * (c - d) + e
```

For each exercise, pay particular attention to how a temporary variable in the quadruple representation is replaced by an **instruction index reference** in the triple representation.

---

