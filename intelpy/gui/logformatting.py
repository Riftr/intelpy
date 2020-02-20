# Format strings for the log screen
def format_alert(string):
    return ("<font color=\"red\"><h2>" + string + "</h2></font>")  # Todo: strange bug here when it's the first thing


def format_info(string):
    return ("<font color=\"gray\">" + string + "</font>")


def format_important(string):
    return ("<b>" + string + "</b>")


def format_recent_alert(string):
    return ("<b>" + string + "</b>")


def format_recent_alert_timer(string):
    return ("<font color=\"red\"><b>" + string + "</b></font>")
