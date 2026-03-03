from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Contact, LinkPrecedence
from app.schemas import ContactResponseDetail, IdentifyRequest, IdentifyResponse


def identify_contact(db: Session, payload: IdentifyRequest) -> IdentifyResponse:
    email = payload.email
    phoneNumber = payload.phoneNumber

    if not email and not phoneNumber:
        raise ValueError("Atleast email or phoneNumber must be given")

    matches = db.query(Contact).filter(
        or_(Contact.email == email, Contact.phoneNumber == phoneNumber)
    ).all()

    if not matches:
        new_contact = Contact(
            email=email,
            phoneNumber=phoneNumber,
            linkPrecedence=LinkPrecedence.Primary
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        return IdentifyResponse(
            contact=ContactResponseDetail(
                primaryContactId=new_contact.id,
                emails=[email] if email else [],
                phoneNumbers=[phoneNumber] if phoneNumber else [],
                secondaryContactIds=[]
            )
        )

    primaryIds = set()
    for contact in matches:
        primaryIds.add(contact.linkedId if contact.linkedId else contact.id)

    cluster = db.query(Contact).filter(
        or_(
            Contact.id.in_(primaryIds),
            Contact.linkedId.in_(primaryIds)
        )
    ).order_by(Contact.createdAt.asc()).all()

    primary_contact = cluster[0]

    for contact in cluster[1:]:
        if contact.id in primaryIds and contact.id != primary_contact.id:
            contact.linkPrecedence = LinkPrecedence.Secondary
            contact.linkedId = primary_contact.id

    db.commit()

    existing_emails = set(c.email for c in cluster if c.email)
    existing_phoneNumbers = set(c.phoneNumber for c in cluster if c.phoneNumber)

    new_data_present = False
    if email and email not in existing_emails:
        new_data_present = True
    if phoneNumber and phoneNumber not in existing_phoneNumbers:
        new_data_present = True

    if new_data_present:
        new_secondary = Contact(
            email=email,
            phoneNumber=phoneNumber,
            linkedId=primary_contact.id,
            linkPrecedence=LinkPrecedence.Secondary
        )
        db.add(new_secondary)
        db.commit()
        db.refresh(new_secondary)
        cluster.append(new_secondary)

    emails_list = [primary_contact.email] if primary_contact.email else []
    phones_list = [primary_contact.phoneNumber] if primary_contact.phoneNumber else []
    secondary_ids = []

    for contact in cluster[1:]:
        if contact.email and contact.email not in emails_list:
            emails_list.append(contact.email)
        if contact.phoneNumber and contact.phoneNumber not in phones_list:
            phones_list.append(contact.phoneNumber)
        if contact.id != primary_contact.id:
            secondary_ids.append(contact.id)

    return IdentifyResponse(
        contact=ContactResponseDetail(
            primaryContactId=primary_contact.id,
            emails=emails_list,
            phoneNumbers=phones_list,
            secondaryContactIds=secondary_ids
        )
    )
