def get_args(update):
    args = update.message.message.split(" ")
    del args[0]
    return args
