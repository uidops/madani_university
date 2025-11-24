# System of Linear Equations - Cramer's Method Solution

**Solution Summary:**

- **x =  1.000000**
- **y =  2.000000**
- **z =  3.000000**

---

## Input System
1. x + 2y + 3z = 14
2. 2x + y + 2z = 10
3. 3x + 2y + z = 10

## Coefficient Matrix and Constants
**Coefficient Matrix A:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|    1.000 |    2.000 |    3.000 |
|    2.000 |    1.000 |    2.000 |
|    3.000 |    2.000 |    1.000 |


**Constants Vector b:**

| b₁ | b₂ | b₃ |
| --- | --- | --- |
|  14.000 |  10.000 |  10.000 |

## Main Determinant
**det(A) =  8.000000**

## Cramer's Method - Variable Solutions
### For variable x: 
**Matrix A_x:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|   14.000 |    2.000 |    3.000 |
|   10.000 |    1.000 |    2.000 |
|   10.000 |    2.000 |    1.000 |


**det(A_x) =  8.000000**

**x = det(A_x) / det(A) =  8.000000 /  8.000000 =  1.000000**

### For variable y: 
**Matrix A_y:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|    1.000 |   14.000 |    3.000 |
|    2.000 |   10.000 |    2.000 |
|    3.000 |   10.000 |    1.000 |


**det(A_y) =  16.000000**

**y = det(A_y) / det(A) =  16.000000 /  8.000000 =  2.000000**

### For variable z: 
**Matrix A_z:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|    1.000 |    2.000 |   14.000 |
|    2.000 |    1.000 |   10.000 |
|    3.000 |    2.000 |   10.000 |


**det(A_z) =  24.000000**

**z = det(A_z) / det(A) =  24.000000 /  8.000000 =  3.000000**

## Solution Verification
**Equation 1:** x + 2y + 3z = 14
- Left side: (1.000 × 1.000000) + (2.000 × 2.000000) + (3.000 × 3.000000) =  14.000000
- Right side: 14.0
- Difference:  0.0000000000

**Equation 2:** 2x + y + 2z = 10
- Left side: (2.000 × 1.000000) + (1.000 × 2.000000) + (2.000 × 3.000000) =  10.000000
- Right side: 10.0
- Difference:  0.0000000000

**Equation 3:** 3x + 2y + z = 10
- Left side: (3.000 × 1.000000) + (2.000 × 2.000000) + (1.000 × 3.000000) =  10.000000
- Right side: 10.0
- Difference:  0.0000000000
