

## تمرین ۲: تحلیل دوکلید با یک لامپ با زبان Z



### نقشه سیستم یک لامپ و دو کلید را از منظر برق‌کشی ساختمان مشخص کنید (یعنی طراحی سیستم را مشخص کنید) و این سیستم را در یک مدل‌سازی تحلیلی مبتنی بر ریاضی — زبان Z (نظریه مجموعه‌ها) توصیف کنید.


#### مدل‌سازی ریاضی با زبان Z


$$
\text{States} = \{on, off\}
$$

$$
\text{DefaultState} = \{off\}
$$

$$
\text{Keys} = \{Key_1, Key_2\}
$$

#### تعریف عملکرد کلیدها

چون هر دو کلید عملکرد یکسانی دارند، برای هر دو یک فرمول واحد بر پایه تفاضل مجموعه‌ها تعریف می‌شود:

$$
Key_1 = \text{NextState} = \text{States} - \text{CurrentState}
$$

$$
Key_2 = \text{NextState} = \text{States} - \text{CurrentState}
$$

---

#### اجرای سناریو

##### حالت اولیه

$$
\text{CurrentState} = \text{DefaultState} = \{off\}
$$

##### زدن کلید اول برای بار اول

$$
\text{NextState} = \text{States} - \text{CurrentState} = \{on, off\} - \{off\} = \{on\}
$$

$$
\text{CurrentState} = \{on\}
$$

> [!example] نتیجه
> لامپ از حالت خاموش به حالت روشن می‌رود.

##### زدن کلید دوم

$$
\text{NextState} = \text{States} - \text{CurrentState} = \{on, off\} - \{on\} = \{off\}
$$

$$
\text{CurrentState} = \{off\}
$$

> [!example] نتیجه
> لامپ مجدداً به حالت خاموش برمی‌گردد.

---

#### اجرای همزمان دو کلید

در حالتی که هر دو کلید همزمان زده شوند، چون هر دو یک کار را انجام می‌دهند، اشتراک‌شان همان یک عمل است و لامپ فقط یک‌بار تغییر حالت می‌دهد:

$$
\text{NextState} = (\text{States} - \text{CurrentState}) \cap (\text{States} - \text{CurrentState}) = \text{States} - \text{CurrentState}
$$

##### با حالت اولیه

$$
\text{CurrentState} = \{off\}
$$

$$
\text{NextState} = \{on, off\} - \{off\} = \{on\}
$$

$$
\text{CurrentState} = \{on\}
$$

> [!note] نتیجه نهایی
> بنابراین در اجرای همزمان، لامپ روشن می‌شود و اثر دو کلید روی هم انباشته نمی‌شود.


تمرین بعدی: [[تحلیل ارور شبکه با زبان Z]]