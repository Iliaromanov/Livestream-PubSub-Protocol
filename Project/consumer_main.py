from Consumer import Consumer
from util import Commands

def main():
    cons = Consumer()
    print(f"Consumer - [{cons.cons_id}] - setup complete.")
    print("cmd:")
    print("- sub [pid] Optional[sid] - subscribe to producer pid, stream sid")
    print("- unsub [pid] Optional[sid] - unsubscribe from producer pid, stream sid")
    print("- exit - end program")

    while True:
        cmd = input(f"Consumer - {cons.cons_id} - waiting on input ...\n> ").split()

        if cmd[0] == Commands.SUB:
            if len(cmd) == 3:
                # sub to specific stream
                cons.subscribe_stream(cmd[1], cmd[2])
            elif len(cmd) == 2:
                cons.subscribe_producer(cmd[1])
            else:
                print("Invalid Command")
                continue 
        elif cmd[0] == Commands.UNSUB:
            if len(cmd) == 3:
                cons.unsubscribe_stream(cmd[1], cmd[2])
            elif len(cmd) == 2:
                cons.unsubscribe_producer(cmd[1])
            else:
                print("Invalid Command")
                continue
        elif cmd[0] == Commands.EXIT:
            exit()
        else:
            print("Invalid Command")



if __name__ == "__main__":
    main()