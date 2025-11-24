# System of Linear Equations - Cramer's Method Solution

**Solution Summary:**

- **x =  1.500000**
- **y =  1.500000**
- **z =  1.500000**

---

## Input System
1. 2x + y + z = 6
2. x + 2y + z = 6
3. x + y + 2z = 6

## Coefficient Matrix and Constants
**Coefficient Matrix A:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|    2.000 |    1.000 |    1.000 |
|    1.000 |    2.000 |    1.000 |
|    1.000 |    1.000 |    2.000 |


**Constants Vector b:**

| b₁ | b₂ | b₃ |
| --- | --- | --- |
|  6.000 |  6.000 |  6.000 |

## Main Determinant
**det(A) =  4.000000**

## Cramer's Method - Variable Solutions
### For variable x: 
**Matrix A_x:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|    6.000 |    1.000 |    1.000 |
|    6.000 |    2.000 |    1.000 |
|    6.000 |    1.000 |    2.000 |


**det(A_x) =  6.000000**

**x = det(A_x) / det(A) =  6.000000 /  4.000000 =  1.500000**

### For variable y: 
**Matrix A_y:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|    2.000 |    6.000 |    1.000 |
|    1.000 |    6.000 |    1.000 |
|    1.000 |    6.000 |    2.000 |


**det(A_y) =  6.000000**

**y = det(A_y) / det(A) =  6.000000 /  4.000000 =  1.500000**

### For variable z: 
**Matrix A_z:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|    2.000 |    1.000 |    6.000 |
|    1.000 |    2.000 |    6.000 |
|    1.000 |    1.000 |    6.000 |


**det(A_z) =  6.000000**

**z = det(A_z) / det(A) =  6.000000 /  4.000000 =  1.500000**

## Solution Verification
**Equation 1:** 2x + y + z = 6
- Left side: (2.000 × 1.500000) + (1.000 × 1.500000) + (1.000 × 1.500000) =  6.000000
- Right side: 6.0
- Difference:  0.0000000000

**Equation 2:** x + 2y + z = 6
- Left side: (1.000 × 1.500000) + (2.000 × 1.500000) + (1.000 × 1.500000) =  6.000000
- Right side: 6.0
- Difference:  0.0000000000

**Equation 3:** x + y + 2z = 6
- Left side: (1.000 × 1.500000) + (1.000 × 1.500000) + (2.000 × 1.500000) =  6.000000
- Right side: 6.0
- Difference:  0.0000000000
