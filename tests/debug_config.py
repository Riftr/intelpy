def debug_config(configuration):
    print("** Debug Configuration Values **")
    print("Home system: " + configuration.value["home_system"])
    print("Eve Log Location: " + configuration.value["eve_log_location"])
    print("All watched channels:")
    for channel in configuration.value["watched_channels"]:
        print("- " + channel)

    print("Alert systems:")
    print(configuration.value["alert_systems"])
    print("Alert jumps: " + str(configuration.value["alert_jumps"]))

    print("Watch active? " + str(configuration.value["log_watch_active"]))
    print("Config loc: " + configuration.value["config_loc"])
    print("Alarm sound: " + configuration.value["alarm_sound"])
    print("Display alerts? " + str(configuration.value["display_alerts"]))
    print("Display clear? " + str(configuration.value["display_clear"]))
    print("Display all? " + str(configuration.value["display_all"]))

    print("** END Debug Configuration Values **")