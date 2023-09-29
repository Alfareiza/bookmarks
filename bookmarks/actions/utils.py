from bookmarks.actions.models import Action


# Pag 210.
def create_action(user, verb, target=None):
    """
    Permite crear acciones que incluyan opcionalmente un objeto target
    """
    action = Action(user=user, verb=verb, target=target)
    action.save()
