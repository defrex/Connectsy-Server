

registered = dict()

def register(event, contacts):
    current = registered.get(event.id, dict())
    for contact in contacts:
        current[contact.number] = contact.name
    registered[event.id] = current
