from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.ticket import Ticket, TicketStatus


# One-click ticket creation stub

def create_ticket(
    db: Session, *, finding_id: int | None, external_system: str, summary: str, description: str | None
) -> Ticket:
    ticket = Ticket(
        finding_id=finding_id,
        external_system=external_system,
        external_id=None,
        status=TicketStatus.open,
        summary=summary,
        description=description,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
