
### تمرین ۴:‌ کنترل سلامت کارت در سیستم ATM


#### کنترل سالم بودن کارت در این سیستم تعبیه و تعریف نشده است. لذا مشاهده می‌شود که همه جزئیات در این مدل ذکر نشده است. این بخش از جزئیات را به مدل‌سازی اضافه کنید.


```mermaid
stateDiagram-v2
    [*] --> Off
    
    Off --> SelfTest: turn on / startup
    SelfTest --> Idle: success
    SelfTest --> OutOfService: failure
    
    Idle --> Off: turn off / shutDown
    Idle --> ServicingCustomer: cardInserted
    Idle --> Maintenance: service
    
    ServicingCustomer --> Idle: cancel
    ServicingCustomer --> OutOfService: failure
    
    Maintenance --> OutOfService: failure
    
    OutOfService --> Maintenance: service
    OutOfService --> Off: turn off / shutDown
    
    classDef off fill:#E0E0E0,stroke:#424242,color:#000
    classDef ready fill:#B3E5FC,stroke:#01579B,color:#000
    classDef active fill:#FFE0B2,stroke:#E65100,color:#000
    classDef service fill:#FFF9C4,stroke:#F57F17,color:#000
    classDef failure fill:#FFB6B6,stroke:#C62828,color:#000
    
    class Off off
    class Idle ready
    class SelfTest,ServicingCustomer active
    class Maintenance service
    class OutOfService failure
```


#### پاسخ:

```mermaid
stateDiagram-v2
    [*] --> Off
    
    Off --> SelfTest: turn on / startup
    SelfTest --> Idle: success
    SelfTest --> OutOfService: failure
    
    Idle --> Off: turn off / shutDown
    Idle --> ValidatingCard: cardInserted
    Idle --> Maintenance: service
    
    ValidatingCard --> ServicingCustomer: cardValid
    ValidatingCard --> EjectingCard: cardInvalid
    ValidatingCard --> RetainingCard: cardBlocked
    
    EjectingCard --> Idle: cardEjected
    RetainingCard --> Idle: cardRetained
    
    ServicingCustomer --> Idle: cancel
    ServicingCustomer --> OutOfService: failure
    
    Maintenance --> OutOfService: failure
    
    OutOfService --> Maintenance: service
    OutOfService --> Off: turn off / shutDown
    
    classDef off fill:#E0E0E0,stroke:#424242,color:#000
    classDef ready fill:#B3E5FC,stroke:#01579B,color:#000
    classDef active fill:#FFE0B2,stroke:#E65100,color:#000
    classDef validation fill:#D1C4E9,stroke:#4527A0,color:#000
    classDef service fill:#FFF9C4,stroke:#F57F17,color:#000
    classDef failure fill:#FFB6B6,stroke:#C62828,color:#000
    classDef card fill:#F8BBD0,stroke:#AD1457,color:#000
    
    class Off off
    class Idle ready
    class SelfTest,ServicingCustomer active
    class ValidatingCard validation
    class Maintenance service
    class OutOfService failure
    class EjectingCard,RetainingCard card
```


تمرین بعدی:‌ [[رمزکارت و مدل به زبان Z]]
