# Track A: Scheduled Orders
## Acceptance Criteria

1. **Valid lead time**  
   WHEN a customer schedules an order for a time at least 45 minutes and no more than 7 days from the current time,\
    &nbsp;  THE SYSTEM SHALL accept the scheduled order.

3. **Lead time too short**  
   WHEN a customer schedules an order for a time less than 45 minutes from the current time,\
    &nbsp;  THE SYSTEM SHALL reject it with error `SCHEDULE_TOO_SOON`.

5. **Lead time too long**  
   WHEN a customer schedules an order for a time more than 7 days from the current time,\
    &nbsp;  THE SYSTEM SHALL reject it with error `SCHEDULE_TOO_FAR`.

7. **Restaurant open hours**  
   WHEN a customer schedules an order,\
    &nbsp;  THE SYSTEM SHALL accept it only if the restaurant is open at the requested delivery time.

9. **Restaurant closed**  
   IF the restaurant is closed at the requested delivery time,\
    &nbsp;  THEN THE SYSTEM SHALL reject the scheduled order with error `RESTAURANT_CLOSED`.

11. **Automatic release**  
   WHEN a scheduled order is exactly 30 minutes from its requested delivery time,\
    &nbsp;  THE SYSTEM SHALL move the order from SCHEDULED to PLACED.

13. **Release exactly once**  
   WHEN a scheduled order becomes eligible for automatic release,\
    &nbsp;  THE SYSTEM SHALL release it exactly once, even if the release process is evaluated more than once.

15. **Cancellation before release**  
   WHEN a customer cancels a scheduled order before it is released,\
    &nbsp;  THE SYSTEM SHALL mark the order `CANCELLED` and SHALL never release it to the restaurant kitchen queue.

17. **Cancellation after release**  
   WHEN a customer attempts to cancel a scheduled order after it has been released,\
    &nbsp;  THE SYSTEM SHALL reject the cancellation and SHALL leave the order in its released state.

## Out of Scope
- Rescheduling an existing scheduled order.
- Partial cancellation of individual items in a scheduled order.
- Restaurant-side editing of scheduled order contents.
- Delivery driver assignment, routing, and real-time delivery tracking.
- Changes to restaurant hours after an order has been accepted.
- Payment authorization, refunds, and promotional pricing.
- Group orders
