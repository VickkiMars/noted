import notify2

notify2.init("Noted")

def sent(content):
    n = notify2.Notification("Notification", content)
    n.set_timeout(10000)
    n.show()