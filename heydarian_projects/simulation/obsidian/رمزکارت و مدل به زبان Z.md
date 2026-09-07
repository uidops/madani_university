## تمرین ۵: رمزکارت و مدل به زبان Z

#### اضافه کردن غلط بودن رمز کارت به مدل زیر و نوشتن مدل به زبان Z


```mermaid
	stateDiagram-v2
    [*] --> Reading_Card

    Reading_Card --> Ejecting_Card : Card Not Readable
    Reading_Card --> Reading_PIN : Card Read Successfully

    Reading_PIN --> Ejecting_Card : Cancel Pressed
    Reading_PIN --> Choosing_Transaction : PIN Read Successfully

    Choosing_Transaction --> Ejecting_Card : Cancel Pressed
    Choosing_Transaction --> Performing_Transaction : Transaction Chosen

    Performing_Transaction --> Ejecting_Card : Finished
    Performing_Transaction --> Choosing_Transaction : Another Transaction

    Ejecting_Card --> [*]
```


#### پاسخ:


به مدل بخش چک کردن رمز کارت اضافه می‌کنیم:


```mermaid
stateDiagram-v2
    [*] --> Reading_Card

    Reading_Card --> Ejecting_Card : Card Not Readable
    Reading_Card --> Reading_PIN : Card Read Successfully

    Reading_PIN --> Ejecting_Card : Cancel Pressed
    Reading_PIN --> Reading_PIN : Invalid PIN (Attempts < 3)
    Reading_PIN --> Ejecting_Card : Invalid PIN (Attempts = 3)
    Reading_PIN --> Choosing_Transaction : PIN Read Successfully

    Choosing_Transaction --> Ejecting_Card : Cancel Pressed
    Choosing_Transaction --> Performing_Transaction : Transaction Chosen

    Performing_Transaction --> Ejecting_Card : Finished
    Performing_Transaction --> Choosing_Transaction : Another Transaction

    Ejecting_Card --> [*]
```


تحلیل با زبان Z:

$$States = \{ReadingCard, ReadingPIN, ChoosingTransaction, PerformingTransaction, EjectingCard\}$$

$$DefaultState = \{ReadingCard\}$$

$$MaxAttempts = 3$$

وقتی در حالت ReadingCard هستیم:
$$\text{NextState} = \{ s \in States \mid (s = ReadingPIN \land IsCardValid) \lor (s = EjectingCard \land \neg IsCardValid) \}$$

وقتی در حالت ReadingPin هستیم:

اگر IsPinCorrect = true بود:
$$\text{NextState} = \{ s \in States \mid s = ChoosingTransaction \land NextAttempts=MaxAttempts \}$$

اگر IsPinCorrect = false بود:
$$\text{NextState} = \{ s \in States \land NextAttempts = NextAttempts + 1 \mid (s = ReadingPIN \land \text{NextAttempts} < \text{MaxAttempts}) \lor (s = EjectingCard \land \text{NextAttempts} = \text{MaxAttempts}) \}$$

وقتی در حالت ChoosingTransaction هستیم:

$$\text{NextState} = \{ s \in States \mid (s = PerformingTransaction \land IsTransactionChosen) \lor (s = EjectingCard \land IsCanceled) \}$$

وقتی در حالت PerformingTransaction هستیم:
$$NextState = \{ s\in States \mid (s = ChoosingTransaction \land IsAnotherTransaction) \lor (s = EjectingCard \land IsFinished)  \}$$


تمرین بعدی: [[هابیل و خباز]]

