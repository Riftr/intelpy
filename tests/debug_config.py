def debug_config(configuration):
    print("** Debug Configuration Values **")
    print("Home system: " + configuration.value["home_system"])
    print("Eve Log Location: " + configuration.value["eve_log_location"])
    print("First watched channel: " + configuration.value["watched_channels"][0])
    print("All watched channels:")
    for channel in configuration.value["watched_channels"]:
        print("- " + channel)

    #if configuration.value["one_jump"] == False:
    #   print("1 jump: " + str(configuration.value["one_jump"]))

    print("alert values")
    print("In_system: " + str(configuration.value["in_system"]))
    print("one_jump: " + str(configuration.value["one_jump"]))
    print("two_jump: " + str(configuration.value["two_jump"]))
    print("three_jump: " + str(configuration.value["three_jump"]))
    print("** END Debug Configuration Values **")