# System of Linear Equations - Cramer's Method Solution

**Solution Summary:**

- **x =  11.040000**
- **y =  16.400000**
- **z =  23.720000**

---

## Input System
1. 2x + 3y + z = 95
2. x + 2y + 3z = 115
3. 4x + y + 2z = 108

## Coefficient Matrix and Constants
**Coefficient Matrix A:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|    2.000 |    3.000 |    1.000 |
|    1.000 |    2.000 |    3.000 |
|    4.000 |    1.000 |    2.000 |


**Constants Vector b:**

| b₁ | b₂ | b₃ |
| --- | --- | --- |
|  95.000 |  115.000 |  108.000 |

## Main Determinant
**det(A) =  25.000000**

## Cramer's Method - Variable Solutions
### For variable x: 
**Matrix A_x:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|   95.000 |    3.000 |    1.000 |
|  115.000 |    2.000 |    3.000 |
|  108.000 |    1.000 |    2.000 |


**det(A_x) =  276.000000**

**x = det(A_x) / det(A) =  276.000000 /  25.000000 =  11.040000**

### For variable y: 
**Matrix A_y:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|    2.000 |   95.000 |    1.000 |
|    1.000 |  115.000 |    3.000 |
|    4.000 |  108.000 |    2.000 |


**det(A_y) =  410.000000**

**y = det(A_y) / det(A) =  410.000000 /  25.000000 =  16.400000**

### For variable z: 
**Matrix A_z:**

| Col 1 | Col 2 | Col 3 |
| --- | --- | --- |
|    2.000 |    3.000 |   95.000 |
|    1.000 |    2.000 |  115.000 |
|    4.000 |    1.000 |  108.000 |


**det(A_z) =  593.000000**

**z = det(A_z) / det(A) =  593.000000 /  25.000000 =  23.720000**

## Solution Verification
**Equation 1:** 2x + 3y + z = 95
- Left side: (2.000 × 11.040000) + (3.000 × 16.400000) + (1.000 × 23.720000) =  95.000000
- Right side: 95.0
- Difference:  0.0000000000

**Equation 2:** x + 2y + 3z = 115
- Left side: (1.000 × 11.040000) + (2.000 × 16.400000) + (3.000 × 23.720000) =  115.000000
- Right side: 115.0
- Difference:  0.0000000000

**Equation 3:** 4x + y + 2z = 108
- Left side: (4.000 × 11.040000) + (1.000 × 16.400000) + (2.000 × 23.720000) =  108.000000
- Right side: 108.0
- Difference:  0.0000000000
