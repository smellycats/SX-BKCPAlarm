from main import BKCPAlarm


if __name__ == "__main__":
    fd = BKCPAlarm()
    fd.run()
    #fd.loop_get_data()
    #fd.get_bkcp()
